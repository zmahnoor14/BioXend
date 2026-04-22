#!/usr/bin/env python3
"""
reference.py — Module 1 (BioXend / MIX-MB)

Reads the Reference sheet from a MIX-MB Template_open.ods and produces:
  - REFERENCE.tsv   
  - README.toml     

Usage:
    python reference.py --input Standards/Templates/Template_open.ods --outdir results/
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import tomli_w
import odf

# ---------------------------------------------------------------------------
# Column mappings
# ---------------------------------------------------------------------------

## README.toml

# README.toml section → template column mappings
_DEPOSITION_COLS  = ["Chembl_version", "Names", "Institutions", "Links"]
_DATASET_COLS     = ["Description", "Recent_changes", "Goal_of_submission"]
_SUMMARY_COLS     = ["Compounds", "Assays", "Endpoints", "Multiplexed"]

# Fields coerced to int, bool, or list
_INT_FIELDS  = {"Chembl_version", "Compounds", "Assays"}
_BOOL_FIELDS = {"Multiplexed"}
_LIST_FIELDS = {"Names", "Institutions", "Links", "Endpoints"}

## REFERENCE.tsv

# Columns emitted in REFERENCE.tsv (ChEMBL deposition order)
CHEMBL_COLS = [
    "RIDX", # Reference_identifier in the template
    "PUBMED_ID",  
    "DATA_LICENCE",
    "CONTACT",
    "JOURNAL_NAME",
    "YEAR",
    "VOLUME",
    "ISSUE",
    "FIRST_PAGE",
    "LAST_PAGE",
    "REF_TYPE",
    "TITLE",
    "DOI",
    "PATENT_ID",
    "ABSTRACT",
    "AUTHORS"
]



# Mandatory fields checked during validation
MANDATORY_FIELDS = ["RIDX", "DATA_LICENCE", "CONTACT", "YEAR", "REF_TYPE", "TITLE", "DOI", "ABSTRACT", "AUTHORS"]
CONDITIONAL_MANDATORY_FIELDS = ["PUBMED_ID"]  # Mandatory (if the REF_TYPE is "Publication")
# Template sheet row indices (0-based)
_ROW_COLNAMES = 1
_ROW_DATA_START = 4


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------

def read_reference_sheet(ods_path: Path) -> pd.DataFrame:
    """
    Parse the Reference sheet from Template_open.ods.

    Returns a clean DataFrame with one row per reference entry.
    """
    raw = pd.read_excel(ods_path, sheet_name="Reference", header=None, engine="odf")

    col_names = raw.iloc[_ROW_COLNAMES].tolist()

    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    df = df.reset_index(drop=True)
    df = df.dropna(how="all")

    # Normalise: strip whitespace from strings, replace NaN-like strings
    def _clean(v):
        if not isinstance(v, str):
            try:
                return "" if pd.isna(v) else v
            except (TypeError, ValueError):
                return v
        v = v.strip()
        return "" if v in ("nan", "None", "NaN") else v

    return df.map(_clean)


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def build_reference_tsv(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame ready to write as REFERENCE.tsv."""
    records = []
    for _, row in df.iterrows():
        rec: dict = {}

        # RIDX user-defined (e.g. GutMicrobiomeBiotransformation, Immunosuppressants_Microbes)
        rec["RIDX"] = str(row.get("Reference_identifier") or "").strip()

        for col in CHEMBL_COLS:
            if col == "RIDX":
                continue
            val = row.get(col, "")
            rec[col] = "" if (pd.isna(val) if not isinstance(val, str) else False) else str(val).strip()

        records.append(rec)

    return pd.DataFrame(records, columns=CHEMBL_COLS)


def build_readme_toml(df: pd.DataFrame) -> dict:
    """Return a nested dict matching the ChEMBL README.toml section layout."""

    def _coerce(col: str, val):
        raw = "" if (pd.isna(val) if not isinstance(val, str) else False) else str(val).strip()
        if col in _INT_FIELDS:
            try:
                return int(float(raw))
            except (ValueError, TypeError):
                return raw
        if col in _BOOL_FIELDS:
            return raw.lower() == "true"
        if col in _LIST_FIELDS:
            return [v.strip() for v in raw.replace("\n", ",").split(",") if v.strip()]
        return raw

    def _section(row, cols):
        return {col: _coerce(col, row.get(col, "")) for col in cols}

    rows = list(df.iterrows())

    def _build(row):
        deposition = _section(row, _DEPOSITION_COLS)
        deposition["Title"] = str(row.get("TITLE") or "").strip()

        return {
            "Deposition":   deposition,
            "Dataset":      _section(row, _DATASET_COLS),
            "Summary_stats": _section(row, _SUMMARY_COLS),
        }

    if len(rows) == 1:
        return _build(rows[0][1])

    # Multiple rows → array of tables per section
    result: dict = {"Deposition": [], "Dataset": [], "Summary_stats": []}
    for _, row in rows:
        built = _build(row)
        for section in result:
            result[section].append(built[section])
    return result


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of validation error strings (empty → all OK)."""
    errors: list[str] = []

    for i, row in df.iterrows():
        label = f"Row {i + 1}"

        if not str(row.get("Reference_identifier") or "").strip():
            errors.append(f"{label}: 'Reference_identifier' (RIDX) is empty.")

        has_doi = bool(str(row.get("DOI") or "").strip())
        has_pmid = bool(str(row.get("PUBMED_ID") or "").strip())
        if not has_doi and not has_pmid:
            errors.append(f"{label}: at least one of DOI or PUBMED_ID is required.")

        for field in MANDATORY_FIELDS:
            if not str(row.get(field) or "").strip():
                errors.append(f"{label}: mandatory field '{field}' is empty.")

        ref_type = str(row.get("REF_TYPE") or "").strip()
        if ref_type == "Publication":
            for field in CONDITIONAL_MANDATORY_FIELDS:
                if not str(row.get(field) or "").strip():
                    errors.append(f"{label}: conditional mandatory field '{field}' is empty.")

        ref_type = str(row.get("REF_TYPE") or "").strip()
        allowed = {"Publication", "Patent", "Dataset", "Book"}
        if ref_type and ref_type not in allowed:
            errors.append(f"{label}: REF_TYPE '{ref_type}' not in {allowed}.")

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate REFERENCE.tsv + README.toml from MIX-MB Template_open.ods",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to Template_open.ods"
    )
    parser.add_argument(
        "--outdir", default=".",
        help="Output directory"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit non-zero if any validation warnings are raised"
    )
    args = parser.parse_args()

    ods_path = Path(args.input)
    outdir = Path(args.outdir)

    if not ods_path.exists():
        sys.exit(f"ERROR: input file not found: {ods_path}")

    outdir.mkdir(parents=True, exist_ok=True)

    # --- Read ---
    df = read_reference_sheet(ods_path)
    if df.empty:
        sys.exit("ERROR: no data rows found in the Reference sheet.")

    # --- Validate ---
    errors = validate(df)
    if errors:
        for msg in errors:
            print(f"WARNING: {msg}", file=sys.stderr)
        if args.strict:
            sys.exit(1)

    # --- Write REFERENCE.tsv ---
    ref_df = build_reference_tsv(df)
    ref_path = outdir / "REFERENCE.tsv"
    ref_df.to_csv(ref_path, sep="\t", index=False)
    print(f"Written: {ref_path}")

    # --- Write RIDX.txt (first RIDX — consumed by downstream pipeline modules) ---
    ridx_value = str(ref_df["RIDX"].iloc[0]).strip() if not ref_df.empty else ""
    if not ridx_value:
        sys.exit("ERROR: Reference_identifier is empty in the Reference sheet.")
    ridx_path = outdir / "RIDX.txt"
    ridx_path.write_text(ridx_value + "\n")
    print(f"Written: {ridx_path}")

    # --- Write README.toml ---
    readme_path = outdir / "README.toml"
    with open(readme_path, "wb") as fh:
        tomli_w.dump(build_readme_toml(df), fh)
    print(f"Written: {readme_path}")


if __name__ == "__main__":
    main()
