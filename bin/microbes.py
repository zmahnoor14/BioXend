#!/usr/bin/env python3
"""
microbes.py — Module 3 (BioXend / MIX-MB)

Reads the Microbes sheet and Experiment sheet from a MIX-MB
Template_open.ods and produces:
  - ASSAY.tsv     ChEMBL deposition format

Each row in the Microbes sheet = one assay entry.
ASSAY_DESCRIPTION is auto-built using the following rules:
  - If "metagenome" appears in Bacteria_scientific_name → community template
  - Otherwise → single-bacteria template
Experimental context (instrument, time course, oxygen) is joined from the
Experiment sheet via the 'identifier' column ('all' or comma-separated
assay_identifiers).

Column mappings  (template column → ChEMBL field):
  assay_identifier             → AIDX 
  Bacteria_scientific_name     → ASSAY_ORGANISM
  Strain                       → ASSAY_STRAIN
  NCBI Tax ID                  → ASSAY_TAX_ID
  Sample_isolation_source      → ASSAY_SOURCE
  Tissue                       → ASSAY_TISSUE
  Cell type                    → ASSAY_CELL_TYPE
  SUBCELLULAR_FRACTION         → ASSAY_SUBCELLULAR_FRACTION
  Protein name (or Gene name)  → TARGET_NAME
  UniProt ID                   → TARGET_ACCESSION
  TARGET_TYPE, TARGET_ORGANISM, TARGET_TAX_ID, ASSAY_GROUP, ASSAY_TYPE
                               → same name in both sheets

Template colour coding:
  Green  = Mandatory   → AIDX, RIDX, ASSAY_DESCRIPTION, ASSAY_TYPE,
                         ASSAY_ORGANISM, ASSAY_TAX_ID
  Blue   = Recommended → ASSAY_STRAIN, ENAorSRA accessions,
                         UniProt ID (when Protein name given)
  Yellow = Optional    → ASSAY_SOURCE, ASSAY_TISSUE, ASSAY_CELL_TYPE,
                         ASSAY_SUBCELLULAR_FRACTION, TARGET_* columns,
                         ASSAY_GROUP

Usage:
    python bin/microbes.py \\
        --input   Standards/Templates/Template_open.ods \\
        --ridx    GutMeta \\
        --xenobiotic_class drug \\   # singular form: 'drug' not 'drugs'
        --outdir  results/
"""

import argparse
import re
import sys
from pathlib import Path

import odf  # noqa: F401 — required by pandas odf engine
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# ChEMBL ASSAY.tsv columns (in deposition order)
CHEMBL_COLS = [
    "AIDX",                        # assay_identifier
    "RIDX",
    "ASSAY_DESCRIPTION",           # auto-built
    "ASSAY_TYPE",                  # same name
    "ASSAY_GROUP",                 # same name
    "ASSAY_ORGANISM",              # Bacteria_scientific_name
    "ASSAY_STRAIN",                # Strain
    "ASSAY_TAX_ID",                # NCBI Tax ID
    "ASSAY_SOURCE",                # Sample_isolation_source
    "ASSAY_TISSUE",                # Tissue
    "ASSAY_CELL_TYPE",             # Cell type
    "ASSAY_SUBCELLULAR_FRACTION",  # SUBCELLULAR_FRACTION
    "TARGET_TYPE",                 # same name
    "TARGET_NAME",                 # Protein name (fallback: Gene name)
    "TARGET_ACCESSION",            # UniProt ID
    "TARGET_ORGANISM",             # same name
    "TARGET_TAX_ID",               # same name
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

# Template sheet row offsets (0-based, read with header=None)
#   row 0 — section group headers  (skip)
#   row 1 — column names           (use as header)
#   row 2 — data types             (skip)
#   row 3 — field descriptions     (skip)
#   row 4+ — data rows
_ROW_COLNAMES   = 1
_ROW_DATA_START = 4


# ---------------------------------------------------------------------------
# Reading helpers
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


def _read_sheet(ods_path: Path, sheet_name: str) -> pd.DataFrame:
    """
    Generic ODS sheet reader using the standard template row layout.
    Strips leading/trailing whitespace from column names.
    """
    raw = pd.read_excel(ods_path, sheet_name=sheet_name, header=None, engine="odf")
    col_names = [
        str(c).strip() if isinstance(c, str) else c
        for c in raw.iloc[_ROW_COLNAMES].tolist()
    ]
    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    df = df.reset_index(drop=True)
    df = df.dropna(how="all")
    return df.map(_clean)


def read_microbes_sheet(ods_path: Path) -> pd.DataFrame:
    """Parse the Microbes sheet from Template_open.ods."""
    return _read_sheet(ods_path, "Microbes")


def read_experiment_sheet(ods_path: Path) -> pd.DataFrame:
    """
    Parse the Experiment sheet from Template_open.ods.

    Key columns used:
      identifier                                  — links rows to assay(s)
      Instrument_4_measurement
      Time-course information (i.e., number of timepoints)
      Time_unit
      Oxygen conditions
    """
    return _read_sheet(ods_path, "Experiment")


# ---------------------------------------------------------------------------
# Experiment-join helper
# ---------------------------------------------------------------------------

def _get_experiment_for_assay(exp_df: pd.DataFrame, aidx: str) -> pd.Series | None:
    """
    Return the first Experiment row that applies to *aidx*.

    A row matches when its 'identifier' field is 'all' (case-insensitive)
    or when aidx appears in the comma-separated list of identifiers.
    Returns None if no match is found.
    """
    for _, row in exp_df.iterrows():
        raw_id = str(row.get("identifier") or "").strip()
        if not raw_id:
            continue
        if raw_id.lower() == "all":
            return row
        ids = [x.strip() for x in raw_id.split(",")]
        if aidx in ids:
            return row
    return None


# ---------------------------------------------------------------------------
# Description helpers
# ---------------------------------------------------------------------------

def _parse_timecourse(raw: str):
    """
    Parse a comma-separated time-course string, e.g. '0,3,6,9,12,24'.

    Returns (n_timepoints, t_min, t_max) as strings, or ('', '', '') if
    the value is empty or cannot be parsed.
    """
    if not raw:
        return "", "", ""
    tokens = [t.strip() for t in raw.split(",") if t.strip()]
    if not tokens:
        return "", "", ""
    try:
        values = [float(t) for t in tokens]
        n   = str(len(values))
        lo  = str(int(min(values)) if min(values) == int(min(values)) else min(values))
        hi  = str(int(max(values)) if max(values) == int(max(values)) else max(values))
        return n, lo, hi
    except ValueError:
        # Non-numeric tokens — just report count
        return str(len(tokens)), tokens[0], tokens[-1]


def _build_description(
    microbe_row: pd.Series,
    exp_row: pd.Series | None,
    xenobiotic_class: str,
) -> str:
    """
    Build ASSAY_DESCRIPTION according to organism type:

    Single-bacteria template:
      The {xenobiotic_class} is tested on {organism} strain {strain} for
      biotransformation. The {xenobiotic_class} is measured with
      {instrument}, over {n} time points, between {t_min} to {t_max}
      {unit}, over oxygen condition: {oxygen}.

    Community template (triggered when 'metagenome' is in organism name):
      The {xenobiotic_class} is tested on {organism} community with study
      accession number {ENA_project} and sample accession number
      {ENA_sample} for biotransformation. The {xenobiotic_class} is
      measured with {instrument}, over {n} time points, between {t_min}
      to {t_max} {unit}, over oxygen condition: {oxygen}.

    Fields that are empty are omitted gracefully.
    """
    xeno     = xenobiotic_class.strip() if xenobiotic_class else "xenobiotic compound"
    organism = str(microbe_row.get("Bacteria_scientific_name") or "").strip()
    strain   = str(microbe_row.get("Strain") or "").strip()
    ena_proj = str(microbe_row.get("ENAorSRA_project_Accession_number") or "").strip()
    ena_samp = str(microbe_row.get("ENAorSRA_sample_Accession_number") or "").strip()

    # Experimental context (may be absent)
    if exp_row is not None:
        instrument   = str(exp_row.get("Instrument_4_measurement") or "").strip()
        timecourse   = str(exp_row.get(
            "Time-course information (i.e., number of timepoints)") or "").strip()
        time_unit    = str(exp_row.get("Time_unit") or "").strip()
        oxygen       = str(exp_row.get("Oxygen conditions") or "").strip()
    else:
        instrument = timecourse = time_unit = oxygen = ""

    n_tp, t_min, t_max = _parse_timecourse(timecourse)

    is_community = "metagenome" in organism.lower()

    # --- Sentence 1: who/what is tested ---
    if is_community:
        s1 = f"The {xeno} is tested on {organism} community"
        if ena_proj:
            s1 += f" with study accession number {ena_proj}"
        if ena_samp:
            s1 += f" and sample accession number {ena_samp}"
        s1 += " for biotransformation."
    else:
        s1 = f"The {xeno} is tested on {organism}"
        if strain:
            s1 += f" strain {strain}"
        s1 += " for biotransformation."

    # --- Sentence 2: measurement context ---
    parts2 = [f"The {xeno} is measured"]
    if instrument:
        parts2.append(f"with {instrument}")
    if n_tp:
        parts2.append(f"over {n_tp} time points")
        if t_min and t_max:
            unit_str = f" {time_unit}" if time_unit else ""
            parts2.append(f"between {t_min} to {t_max}{unit_str}")
    if oxygen:
        parts2.append(f"over oxygen condition: {oxygen}")

    s2 = ", ".join(parts2) + "." if len(parts2) > 1 else ""

    return f"{s1} {s2}".strip() if s2 else s1


# ---------------------------------------------------------------------------
# Identifier helpers
# ---------------------------------------------------------------------------

def _slugify(text: str) -> str:
    """Convert a string to a safe identifier segment (underscores, no spaces)."""
    text = text.strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "_", text)
    return text


def _make_aidx(organism: str, strain: str, ridx: str, n: int) -> str:
    """
    Build a meaningful AIDX from organism, strain, and RIDX.

    Examples:
      GutMeta_Salmonella_typhimurium_LT2_biotransformation
      GutMeta_gut_metagenome_biotransformation
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


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_assay_tsv(
    df: pd.DataFrame,
    ridx: str,
    exp_df: pd.DataFrame,
    xenobiotic_class: str,
) -> pd.DataFrame:
    """
    Build the ASSAY.tsv records from the Microbes sheet DataFrame.

    One row per Microbes sheet entry. AIDX is used as-is from
    assay_identifier; if blank it is auto-generated from organism + RIDX.
    ASSAY_DESCRIPTION is built from Microbes + joined Experiment data.
    """
    records = []
    aidx_counter: dict = {}

    for _, row in df.iterrows():
        organism = str(row.get("Bacteria_scientific_name") or "").strip()
        strain   = str(row.get("Strain") or "").strip()

        # --- AIDX ---
        raw_aidx = str(row.get("assay_identifier") or "").strip()
        if raw_aidx:
            aidx = raw_aidx
        else:
            base  = _make_aidx(organism, strain, ridx, 1)
            count = aidx_counter.get(base, 0) + 1
            aidx_counter[base] = count
            aidx = base if count == 1 else f"{base}_{count}"

        # --- ASSAY_TYPE: normalise to single uppercase letter ---
        raw_type   = str(row.get("ASSAY_TYPE") or "").strip().upper()
        assay_type = raw_type[0] if raw_type else ""

        # --- ASSAY_TAX_ID: coerce float cells (e.g. 1348.0) to int string ---
        raw_tax = row.get("NCBI Tax ID")
        if raw_tax == "" or raw_tax is None:
            assay_tax_id = ""
        else:
            try:
                assay_tax_id = str(int(float(str(raw_tax))))
            except (ValueError, TypeError):
                assay_tax_id = str(raw_tax).strip()

        # --- Join Experiment row for this assay ---
        exp_row = _get_experiment_for_assay(exp_df, aidx)

        # --- ASSAY_DESCRIPTION ---
        description = _build_description(row, exp_row, xenobiotic_class)

        # --- Optional Microbes fields ---
        assay_source    = str(row.get("Sample_isolation_source") or "").strip()
        assay_tissue    = str(row.get("Tissue") or "").strip()
        assay_cell_type = str(row.get("Cell type") or "").strip()
        assay_subcell   = str(row.get("SUBCELLULAR_FRACTION") or "").strip()
        assay_group     = str(row.get("ASSAY_GROUP") or "").strip()

        # --- Target fields ---
        target_type      = str(row.get("TARGET_TYPE") or "").strip()
        target_name      = (
            str(row.get("Protein name") or "").strip()
            or str(row.get("Gene name") or "").strip()
        )
        target_accession = str(row.get("UniProt ID") or "").strip()
        target_organism  = str(row.get("TARGET_ORGANISM") or "").strip()

        raw_ttax = row.get("TARGET_TAX_ID")
        if raw_ttax == "" or raw_ttax is None:
            target_tax_id = ""
        else:
            try:
                target_tax_id = str(int(float(str(raw_ttax))))
            except (ValueError, TypeError):
                target_tax_id = str(raw_ttax).strip()

        records.append({
            "AIDX":                       aidx,
            "RIDX":                       ridx,
            "ASSAY_DESCRIPTION":          description,
            "ASSAY_TYPE":                 assay_type,
            "ASSAY_GROUP":                assay_group,
            "ASSAY_ORGANISM":             organism,
            "ASSAY_STRAIN":               strain,
            "ASSAY_TAX_ID":               assay_tax_id,
            "ASSAY_SOURCE":               assay_source,
            "ASSAY_TISSUE":               assay_tissue,
            "ASSAY_CELL_TYPE":            assay_cell_type,
            "ASSAY_SUBCELLULAR_FRACTION": assay_subcell,
            "TARGET_TYPE":                target_type,
            "TARGET_NAME":                target_name,
            "TARGET_ACCESSION":           target_accession,
            "TARGET_ORGANISM":            target_organism,
            "TARGET_TAX_ID":              target_tax_id,
        })

    return pd.DataFrame(records, columns=CHEMBL_COLS)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(assay_df: pd.DataFrame) -> list:
    """Return a list of validation warning strings (empty list → all OK)."""
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

        # TARGET_TAX_ID required when TARGET_ORGANISM is filled
        if str(row.get("TARGET_ORGANISM") or "").strip():
            if not str(row.get("TARGET_TAX_ID") or "").strip():
                errors.append(
                    f"{label}: TARGET_TAX_ID is required when "
                    f"TARGET_ORGANISM is filled."
                )

        # TARGET_ACCESSION recommended when TARGET_NAME is filled
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
            "(Microbes + Experiment sheets)"
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
        "--xenobiotic_class", default="xenobiotic compound",
        help=(
            "Singular form of the xenobiotic class used in ASSAY_DESCRIPTION "
            "(e.g. 'drug', 'pesticide', 'pollutant' — not 'drugs' or 'pesticides')"
        ),
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

    exp_df = read_experiment_sheet(ods_path)
    if exp_df.empty:
        print("[WARN] No data rows found in the Experiment sheet — "
              "ASSAY_DESCRIPTION will omit measurement context.", file=sys.stderr)

    # --- Build ---
    assay_df = build_assay_tsv(
        microbes_df,
        ridx=args.ridx,
        exp_df=exp_df,
        xenobiotic_class=args.xenobiotic_class,
    )

    # --- Validate ---
    errors = validate(assay_df)
    if errors:
        for msg in errors:
            print(f"WARNING: {msg}", file=sys.stderr)
        if args.strict:
            sys.exit(1)

    # --- Write ---
    out_path = outdir / "ASSAY.tsv"
    assay_df.to_csv(out_path, sep="\t", index=False)
    print(f"Written: {out_path}")
    print(f"[SUCCESS] {len(assay_df)} assay(s) written.")


if __name__ == "__main__":
    main()
