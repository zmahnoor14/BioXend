#!/usr/bin/env python3
"""
microbes.py — Module 3 (BioXend / MIX-MB)

Reads the Microbes sheet and Experiment sheet from a MIX-MB
Template_open.ods and produces:
  - ASSAY.tsv     ChEMBL deposition format

Each row in the Microbes sheet = one assay entry.
ASSAY_DESCRIPTION is auto-built using the following rules:
  - If "metagenome" appears in ASSAY_ORGANISM → community template
  - Otherwise → single-bacteria template
Experimental context (instrument, time course, oxygen) is joined from the
Experiment sheet via the 'identifier' column ('all' or comma-separated AIDXs).

Column mappings  (template column → ChEMBL field):
  AIDX                → AIDX (auto-generated if blank)
  ASSAY_ORGANISM      → ASSAY_ORGANISM
  ASSAY_STRAIN        → ASSAY_STRAIN
  ASSAY_TAX_ID        → ASSAY_TAX_ID
  ASSAY_SOURCE        → ASSAY_SOURCE
  ASSAY_TISSUE        → ASSAY_TISSUE
  ASSAY_CELL_TYPE     → ASSAY_CELL_TYPE
  ASSAY_SUBCELLULAR_FRACTION → ASSAY_SUBCELLULAR_FRACTION
  TARGET_NAME         → TARGET_NAME
  TARGET_ACCESSION    → TARGET_ACCESSION
  Gene_name           → used as fallback for TARGET_NAME

Auto-generated AIDX naming convention:
  [ASSAY_SOURCE_]ORGANISM[_STRAIN|_community]_Biotransformation[_ACCESSION|_TARGET_NAME]

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
    "RIDX",                       # from REFERENCE.tsv OR user provided (must match REFERENCE.tsv)
    "ASSAY_DESCRIPTION",           # auto-built
    "ASSAY_TYPE",                  
    "ASSAY_GROUP",                 
    "ASSAY_ORGANISM",              
    "ASSAY_STRAIN",                
    "ASSAY_TAX_ID",               # of no taxid present, then use StrainInfo to fetch the taxid from assay organism name
    "ASSAY_SOURCE",                
    "ASSAY_TISSUE",                
    "ASSAY_CELL_TYPE",             
    "ASSAY_SUBCELLULAR_FRACTION",  
    "TARGET_TYPE",                 
    "TARGET_NAME",                 
    "TARGET_ACCESSION",            
    "TARGET_TAX_ID",               # of no taxid present, then use StrainInfo to fetch the taxid from target organism name
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
VALID_TARGET_TYPES = {"3D CELL CULTURE", "ADMET", "CELL-LINE","CHIMERIC PROTEIN"
"LIPID","MACROMOLECULE", "METAL","MOLECULAR", "NO TARGET", "NON-MOLECULAR", "NUCLEIC-ACID",
"OLIGOSACCHARIDE", "ORGANISM","PHENOTYPE", "PROTEIN","PROTEIN COMPLEX","PROTEIN COMPLEX GROUP",
"PROTEIN FAMILY","PROTEIN NUCLEIC-ACID COMPLEX","PROTEIN-PROTEIN INTERACTION",
"SELECTIVITY GROUP","SINGLE PROTEIN","SMALL MOLECULE","SUBCELLULAR","TISSUE","UNCHECKED","UNDEFINED","UNKNOWN"}

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
    organism = str(microbe_row.get("ASSAY_ORGANISM") or "").strip()
    strain   = str(microbe_row.get("ASSAY_STRAIN") or "").strip()
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


def _make_aidx(
    organism: str,
    strain: str,
    assay_source: str,
    target_name: str,
    target_accession: str,
) -> str:
    """
    Build an AIDX using the ChEMBL naming convention:

      [ASSAY_SOURCE_]ORGANISM[_STRAIN | _community]_Biotransformation[_ACCESSION | _TARGET_NAME]

    Rules:
      - ASSAY_SOURCE is prepended if available.
      - If 'metagenome' is in the organism name, 'community' is appended
        instead of the strain.
      - 'Biotransformation' is always added.
      - If TARGET_NAME is filled: append TARGET_ACCESSION if available,
        otherwise append TARGET_NAME.

    Examples:
      Zimmermann_gut_metagenome_community_Biotransformation
      Zimmermann_Salmonella_typhimurium_LT2_Biotransformation
      Zimmermann_Salmonella_typhimurium_LT2_Biotransformation_P12345
    """
    parts = []
    if assay_source:
        parts.append(_slugify(assay_source))
    if organism:
        parts.append(_slugify(organism))
    is_community = "metagenome" in organism.lower()
    if is_community:
        parts.append("community")
    elif strain:
        parts.append(_slugify(strain))
    parts.append("Biotransformation")
    if target_name:
        if target_accession:
            parts.append(_slugify(target_accession))
        else:
            parts.append(_slugify(target_name))
    return "_".join(filter(None, parts))


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_assay_tsv(
    df: pd.DataFrame,
    ridx: str,
    exp_df: pd.DataFrame,
    xenobiotic_class: str,
) -> "tuple[pd.DataFrame, dict[str, str]]":
    """
    Build the ASSAY.tsv records from the Microbes sheet DataFrame.

    Returns (assay_df, aidx_map).

    aidx_map maps each user-provided AIDX key (from the template AIDX column,
    e.g. 'assay1') to the pipeline-generated ChEMBL AIDX (e.g.
    'Zimmermann_gut_metagenome_community_Biotransformation').  This map is
    written to ASSAY_MAPPING.tsv so that biotransformation.py can resolve
    Biotransformation-sheet ASSAY_Identifier values to the proper AIDX —
    exactly as COMPOUND_RECORD.tsv lets biotransformation.py resolve
    Common_Name to CIDX.

    The AIDX column in the template is the user's short cross-reference key.
    The pipeline ALWAYS derives the ChEMBL AIDX from organism / strain /
    source / target metadata using _make_aidx, regardless of the user key.
    """
    records = []
    aidx_map: "dict[str, str]" = {}   # user_key → generated AIDX
    aidx_counter: dict = {}

    for _, row in df.iterrows():
        organism = str(row.get("ASSAY_ORGANISM") or "").strip()
        strain   = str(row.get("ASSAY_STRAIN") or "").strip()

        # --- Optional Microbes fields (needed early for AIDX generation) ---
        assay_source    = str(row.get("ASSAY_SOURCE") or "").strip()
        assay_tissue    = str(row.get("ASSAY_TISSUE") or "").strip()
        assay_cell_type = str(row.get("ASSAY_CELL_TYPE") or "").strip()
        assay_subcell   = str(row.get("ASSAY_SUBCELLULAR_FRACTION") or "").strip()
        assay_group     = str(row.get("ASSAY_GROUP") or "").strip()

        # --- Target fields (needed early for AIDX generation) ---
        target_type      = str(row.get("TARGET_TYPE") or "").strip()
        target_name      = (
            str(row.get("TARGET_NAME") or "").strip()
            or str(row.get("Gene_name") or "").strip()
        )
        target_accession = str(row.get("TARGET_ACCESSION") or "").strip()
        target_organism  = str(row.get("TARGET_ORGANISM") or "").strip()

        raw_ttax = row.get("TARGET_TAX_ID")
        if raw_ttax == "" or raw_ttax is None:
            target_tax_id = ""
        else:
            try:
                target_tax_id = str(int(float(str(raw_ttax))))
            except (ValueError, TypeError):
                target_tax_id = str(raw_ttax).strip()

        # --- AIDX ---
        # user_key is what the user wrote in the template AIDX column (e.g.
        # 'assay1').  It is the cross-reference key used in the Biotransformation
        # sheet's ASSAY_Identifier column.  The pipeline ALWAYS generates the
        # proper ChEMBL AIDX from metadata — the user key is never used as-is.
        user_key = str(row.get("AIDX") or "").strip()
        if not user_key:
            # Fallback key so Biotransformation sheet rows can still reference
            # this assay even when the template AIDX column was left blank.
            user_key = f"assay{len(aidx_map) + 1}"

        base  = _make_aidx(organism, strain, assay_source, target_name, target_accession)
        count = aidx_counter.get(base, 0) + 1
        aidx_counter[base] = count
        aidx = base if count == 1 else f"{base}_{count}"

        aidx_map[user_key] = aidx

        # --- ASSAY_TYPE: normalise to single uppercase letter ---
        raw_type   = str(row.get("ASSAY_TYPE") or "").strip().upper()
        assay_type = raw_type[0] if raw_type else ""

        # --- ASSAY_TAX_ID: coerce float cells (e.g. 1348.0) to int string ---
        raw_tax = row.get("ASSAY_TAX_ID")
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

    return pd.DataFrame(records, columns=CHEMBL_COLS), aidx_map


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
    assay_df, aidx_map = build_assay_tsv(
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

    # --- Write ASSAY.tsv ---
    out_path = outdir / "ASSAY.tsv"
    assay_df.to_csv(out_path, sep="\t", index=False)
    print(f"Written: {out_path}")

    # --- Write ASSAY_MAPPING.tsv ---
    # Maps the user's short identifier (template AIDX column) to the
    # pipeline-generated ChEMBL AIDX.  Pass this file to biotransformation.py
    # via --assays so that ASSAY_Identifier values in the Biotransformation
    # sheet are correctly resolved — identical to how --compounds works for CIDX.
    mapping_path = outdir / "ASSAY_MAPPING.tsv"
    pd.DataFrame(
        list(aidx_map.items()), columns=["USER_AIDX", "AIDX"]
    ).to_csv(mapping_path, sep="\t", index=False)
    print(f"Written: {mapping_path}")

    print(f"[SUCCESS] {len(assay_df)} assay(s) written.")


if __name__ == "__main__":
    main()
