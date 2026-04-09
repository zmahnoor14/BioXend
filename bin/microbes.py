#!/usr/bin/env python3
"""
microbes.py — Module 3 (BioXend / MIX-MB)

Reads the Microbes sheet (and optionally the Chemicals sheet for compound
context) from a MIX-MB Template_open.ods and produces:
  - ASSAY.tsv     ChEMBL deposition format

Each row in the Microbes sheet = one assay entry.
ASSAY_DESCRIPTION is auto-built from organism, strain, sample source,
and compound names (pulled from the Chemicals sheet).

Template colour coding:
  Green  = Mandatory   → AIDX (auto-generated if blank), RIDX,
                         ASSAY_DESCRIPTION, ASSAY_TYPE,
                         ASSAY_ORGANISM, ASSAY_TAX_ID
  Blue   = Recommended → ASSAY_STRAIN, ENAorSRA accessions,
                         UniProt ID (if Protein name given)
  Yellow = Optional    → ASSAY_SOURCE, ASSAY_TISSUE, ASSAY_CELL_TYPE,
                         ASSAY_SUBCELLULAR_FRACTION, TARGET_* columns,
                         ASSAY_GROUP

Usage:
    python bin/microbes.py --input Standards/Templates/Template_open.ods \\
                           --ridx GutMeta --outdir results/
"""

import argparse
import re
import sys
from pathlib import Path
import odf
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# ChEMBL ASSAY.tsv columns (in deposition order)
CHEMBL_COLS = [
    "AIDX", # assay_identifier
    "RIDX",
    "ASSAY_DESCRIPTION", # not present in template
    "ASSAY_TYPE",
    "ASSAY_GROUP",
    "ASSAY_ORGANISM", #Bacteria_scientific_name
    "ASSAY_STRAIN", # Strain
    "ASSAY_TAX_ID", # NCBI Tax ID
    "ASSAY_SOURCE", # Sample_isolation_source
    "ASSAY_TISSUE", # Tissue
    "ASSAY_CELL_TYPE", # Cell type
    "ASSAY_SUBCELLULAR_FRACTION", # SUBCELLULAR_FRACTION
    "TARGET_TYPE",
    "TARGET_NAME", # Protein name or Gene name, whichever one is present
    "TARGET_ACCESSION", # UniProt ID (if Protein name given)
    "TARGET_ORGANISM",
    "TARGET_TAX_ID",
]

MANDATORY_FIELDS = [
    "AIDX",
    "RIDX",
    "ASSAY_DESCRIPTION",
    "ASSAY_TYPE",
    "ASSAY_ORGANISM",
    "ASSAY_TAX_ID",
]

VALID_ASSAY_TYPES = {"A", "F", "B", "U", "P", "T"}

# Template sheet row indices (0-based, read with header=None)
#   row 0 — section group headers  (skip)
#   row 1 — column names           (use as header)
#   row 2 — data types             (skip)
#   row 3 — field descriptions     (skip)
#   row 4+ — data rows
_ROW_COLNAMES   = 1
_ROW_DATA_START = 4


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------

def _clean(v):
    """Normalise a cell value: NaN floats and 'nan'-like strings become ''."""
    if not isinstance(v, str):
        try:
            return "" if pd.isna(v) else v
        except (TypeError, ValueError):
            return v
    v = v.strip()
    return "" if v in ("nan", "None", "NaN") else v


def read_microbes_sheet(ods_path: Path) -> pd.DataFrame:
    """
    Parse the Microbes sheet from Template_open.ods.

    Template layout:
      row 0 — section group headers  (skip)
      row 1 — column names           (use as header)
      row 2 — data types             (skip)
      row 3 — field descriptions     (skip)
      row 4+ — data rows
    """
    raw = pd.read_excel(ods_path, sheet_name="Microbes", header=None, engine="odf")
    col_names = raw.iloc[_ROW_COLNAMES].tolist()

    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    df = df.reset_index(drop=True)
    df = df.dropna(how="all")
    return df.map(_clean)


def read_compound_names(ods_path: Path) -> list:
    """
    Pull compound names from the Chemicals sheet for use in ASSAY_DESCRIPTION.
    Returns a list of Common_Name strings (empty strings excluded).
    """
    raw = pd.read_excel(ods_path, sheet_name="Chemicals", header=None, engine="odf")
    col_names = raw.iloc[_ROW_COLNAMES].tolist()

    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    df = df.reset_index(drop=True)
    df = df.dropna(how="all")
    df = df.map(_clean)

    names = [
        str(v).strip()
        for v in df.get("Common_Name", pd.Series(dtype=str)).tolist()
        if str(v).strip()
    ]
    return names


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _slugify(text: str) -> str:
    """Convert a string to a safe identifier segment (underscores, no spaces)."""
    text = text.strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "_", text)
    return text


def _make_aidx(organism: str, strain: str, ridx: str, n: int) -> str:
    """
    Build a meaningful AIDX from organism and RIDX.

    Example: GutMeta_Salmonella_typhimurium_LT2_biotransformation
             GutMeta_gut_metagenome_1_biotransformation
    """
    parts = [ridx]
    if organism:
        parts.append(_slugify(organism))
    if strain:
        parts.append(_slugify(strain))
    if n > 1:
        parts.append(str(n))
    parts.append("biotransformation")
    return "_".join(filter(None, parts))


def _build_description(row: pd.Series, compound_names: list) -> str:
    """
    Auto-build ASSAY_DESCRIPTION from available fields.

    Pattern:
      Biotransformation assay measuring [compounds] by [organism] [strain]
      isolated from [source]. [additional context if available]
    """
    organism = str(row.get("Bacteria_scientific_name") or "").strip()
    strain   = str(row.get("Strain") or "").strip()
    source   = str(row.get("Sample_isolation_source") or "").strip()
    donor    = str(row.get("Human_donor_metadata") or "").strip()
    env      = str(row.get("Environmental_sample_metadata") or "").strip()
    internal = str(row.get("internal_sample_identifier") or "").strip()

    parts = ["Biotransformation assay"]

    if compound_names:
        compound_str = ", ".join(compound_names)
        parts.append(f"measuring biotransformation of {compound_str}")

    if organism:
        organism_str = organism
        if strain:
            organism_str += f" {strain}"
        parts.append(f"by {organism_str}")

    if source:
        parts.append(f"isolated from {source}")

    if donor:
        parts.append(f"(donor: {donor})")
    if env:
        parts.append(f"(environment: {env})")
    if internal:
        parts.append(f"[sample ID: {internal}]")

    return " ".join(parts) + "."


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_assay_tsv(
    df: pd.DataFrame,
    ridx: str,
    compound_names: list,
) -> pd.DataFrame:
    """
    Build the ASSAY.tsv records from the Microbes sheet DataFrame.

    One row per assay entry. AIDX is auto-generated if assay_identifier
    is blank. ASSAY_DESCRIPTION is auto-built from organism + compound context.
    """
    records = []
    aidx_counter: dict = {}  # tracks duplicates for auto-AIDX uniqueness

    for _, row in df.iterrows():
        organism = str(row.get("Bacteria_scientific_name") or "").strip()
        strain   = str(row.get("Strain") or "").strip()

        # AIDX: use provided assay_identifier or auto-generate
        raw_aidx = str(row.get("assay_identifier") or "").strip()
        if raw_aidx:
            aidx = raw_aidx
        else:
            base = _make_aidx(organism, strain, ridx, 1)
            count = aidx_counter.get(base, 0) + 1
            aidx_counter[base] = count
            aidx = base if count == 1 else f"{base}_{count}"

        # ASSAY_TYPE: normalise to single uppercase letter
        raw_type = str(row.get("ASSAY_TYPE") or "").strip().upper()
        assay_type = raw_type[0] if raw_type else ""

        # ASSAY_DESCRIPTION
        description = _build_description(row, compound_names)

        # ASSAY_ORGANISM
        assay_organism = organism

        # ASSAY_TAX_ID: accept integer or string; coerce to string
        raw_tax = row.get("NCBI Tax ID")
        if raw_tax == "" or raw_tax is None:
            assay_tax_id = ""
        else:
            try:
                assay_tax_id = str(int(float(str(raw_tax))))
            except (ValueError, TypeError):
                assay_tax_id = str(raw_tax).strip()

        # Optional fields
        assay_strain    = strain
        assay_source    = str(row.get("Sample_isolation_source") or "").strip()
        assay_tissue    = str(row.get("Tissue") or "").strip()
        assay_cell_type = str(row.get("Cell type") or "").strip()
        assay_subcell   = str(row.get("SUBCELLULAR_FRACTION") or "").strip()
        assay_group     = str(row.get("ASSAY_GROUP") or "").strip()

        # Target fields (optional)
        target_type = str(row.get("TARGET_TYPE") or "").strip()
        # TARGET_NAME: prefer Protein name; fall back to Gene name
        target_name = (
            str(row.get("Protein name") or "").strip()
            or str(row.get("Gene name") or "").strip()
        )
        target_accession = str(row.get("UniProt ID") or "").strip()
        target_organism  = str(row.get("TARGET_ORGANISM") or "").strip()
        raw_ttax         = row.get("TARGET_TAX_ID")
        if raw_ttax == "" or raw_ttax is None:
            target_tax_id = ""
        else:
            try:
                target_tax_id = str(int(float(str(raw_ttax))))
            except (ValueError, TypeError):
                target_tax_id = str(raw_ttax).strip()

        records.append(
            {
                "AIDX":                     aidx,
                "RIDX":                     ridx,
                "ASSAY_DESCRIPTION":        description,
                "ASSAY_TYPE":               assay_type,
                "ASSAY_GROUP":              assay_group,
                "ASSAY_ORGANISM":           assay_organism,
                "ASSAY_STRAIN":             assay_strain,
                "ASSAY_TAX_ID":             assay_tax_id,
                "ASSAY_SOURCE":             assay_source,
                "ASSAY_TISSUE":             assay_tissue,
                "ASSAY_CELL_TYPE":          assay_cell_type,
                "ASSAY_SUBCELLULAR_FRACTION": assay_subcell,
                "TARGET_TYPE":              target_type,
                "TARGET_NAME":              target_name,
                "TARGET_ACCESSION":         target_accession,
                "TARGET_ORGANISM":          target_organism,
                "TARGET_TAX_ID":            target_tax_id,
            }
        )

    return pd.DataFrame(records, columns=CHEMBL_COLS)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(assay_df: pd.DataFrame) -> list:
    """Return a list of validation error strings (empty list -> all OK)."""
    errors = []

    for i, row in assay_df.iterrows():
        label = f"Row {i + 1} (AIDX={row.get('AIDX', '?')})"

        for field in MANDATORY_FIELDS:
            if not str(row.get(field) or "").strip():
                errors.append(f"{label}: mandatory field '{field}' is empty.")

        assay_type = str(row.get("ASSAY_TYPE") or "").strip()
        if assay_type and assay_type not in VALID_ASSAY_TYPES:
            errors.append(
                f"{label}: ASSAY_TYPE '{assay_type}' not in "
                f"{sorted(VALID_ASSAY_TYPES)}."
            )

        # If TARGET_ORGANISM is filled, TARGET_TAX_ID becomes mandatory
        if str(row.get("TARGET_ORGANISM") or "").strip():
            if not str(row.get("TARGET_TAX_ID") or "").strip():
                errors.append(
                    f"{label}: TARGET_TAX_ID is required when "
                    f"TARGET_ORGANISM is filled."
                )

        # If Protein name is filled, UniProt ID is strongly recommended
        if str(row.get("TARGET_NAME") or "").strip():
            if not str(row.get("TARGET_ACCESSION") or "").strip():
                errors.append(
                    f"{label}: TARGET_ACCESSION (UniProt ID) is recommended "
                    f"when TARGET_NAME is provided."
                )

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate ASSAY.tsv from a MIX-MB Template_open.ods "
            "(Microbes + Chemicals sheets)"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to Template_open.ods",
    )
    parser.add_argument(
        "--ridx", required=True,
        help="RIDX identifier for this submission (must match REFERENCE.tsv)",
    )
    parser.add_argument(
        "--outdir", default=".",
        help="Output directory",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit non-zero if any validation warnings are raised",
    )
    args = parser.parse_args()

    ods_path = Path(args.input)
    outdir   = Path(args.outdir)

    if not ods_path.exists():
        sys.exit(f"ERROR: input file not found: {ods_path}")

    outdir.mkdir(parents=True, exist_ok=True)

    # --- Read ---
    microbes_df = read_microbes_sheet(ods_path)
    if microbes_df.empty:
        sys.exit("ERROR: no data rows found in the Microbes sheet.")

    compound_names = read_compound_names(ods_path)
    if not compound_names:
        print("[WARN] No compound names found in Chemicals sheet — "
              "ASSAY_DESCRIPTION will omit compound context.", file=sys.stderr)

    # --- Build ---
    assay_df = build_assay_tsv(microbes_df, ridx=args.ridx,
                                compound_names=compound_names)

    # --- Validate ---
    errors = validate(assay_df)
    if errors:
        for msg in errors:
            print(f"WARNING: {msg}", file=sys.stderr)
        if args.strict:
            sys.exit(1)

    # --- Write ASSAY.tsv ---
    out_path = outdir / "ASSAY.tsv"
    assay_df.to_csv(out_path, sep="\t", index=False)
    print(f"Written: {out_path}")
    print(f"[SUCCESS] {len(assay_df)} assay(s) written.")


if __name__ == "__main__":
    main()
