#!/usr/bin/env python3
"""
experiment.py — Module: ASSAY_PARAM generator (BioXend / MIX-MB)

Reads the Experiment sheet from a MIX-MB Template_open_MB.ods and
produces ASSAY_PARAM.tsv in ChEMBL deposition format.

The AIDX list is derived from the first column ('identifier') of the
Experiment sheet.  Comma-separated values are expanded; rows whose
identifier is 'all' or 'most' apply to all discovered AIDXs.
An optional --assay ASSAY.tsv argument can override the AIDX list
(backward-compatible with earlier pipeline versions).

Each row in ASSAY_PARAM.tsv is one parameter entry for one assay.
Parameters are only emitted when the source field is non-empty
(except DOSE, which is emitted only when --dose is supplied).

Experiment sheet column → ASSAY_PARAM TYPE mapping:
  Pre-culture preparation and conditions  → PRE-CULTURE PREPARATION  (TEXT_VALUE)
  Sample preparation                      → SAMPLE PREPARATION        (TEXT_VALUE)
  Incubation temperature in celsius       → TEMPERATURE               (VALUE, UNITS=celsius, RELATION==)
  Time-course info (+ Time_unit)          → TIMEPOINT                 (TEXT_VALUE: "values unit")
  Oxygen conditions                       → CONDITION                 (TEXT_VALUE)
  Media composition                       → MEDIA                     (TEXT_VALUE)
  Shaking speed                           → SHAKING SPEED             (TEXT_VALUE)
  Negative controls                       → CONTROL                   (TEXT_VALUE)
  Antibiotic pre-treatment                → ANTIBIOTICS               (TEXT_VALUE)
  Sample storage                          → STORAGE                   (TEXT_VALUE)
  Biomass/inoculum density at the start   → BIOMASS                   (TEXT_VALUE — emitted only when non-empty)
  Biomass/inoculum density at the end     → BIOMASS                   (COMMENTS — appended to start row, or separate)
  --dose / --dose_units CLI args          → DOSE                      (VALUE, UNITS, RELATION==)

Usage:
    python bin/experiment.py \\
        --input   Standards/Templates/Template_open_MB.ods \\
        --outdir  results/ \\
        [--dose 5] [--dose_units uM] [--dose_comments "tested drug concentration"] \\
        [--strict]
"""

import argparse
import sys
from pathlib import Path

import odf  # noqa: F401 — required by pandas odf engine
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# ChEMBL ASSAY_PARAM.tsv columns (in deposition order)
ASSAY_PARAM_COLS = ["AIDX", "TYPE", "RELATION", "VALUE", "UNITS", "TEXT_VALUE", "COMMENTS"]

MANDATORY_PARAM_FIELDS = ["AIDX", "TYPE"]

# Controlled vocabulary for TYPE — must match the values emitted by _COL_MAP / special handlers
VALID_PARAM_TYPES = {
    "PRE-CULTURE PREPARATION",
    "SAMPLE PREPARATION",
    "TEMPERATURE",
    "TIMEPOINT",
    "CONDITION",
    "MEDIA",
    "SHAKING SPEED",
    "CONTROL",
    "ANTIBIOTICS",
    "STORAGE",
    "BIOMASS",
    "DOSE",
}

# Row offsets in the ODS template (0-based, header=None read)
_ROW_COLNAMES   = 1
_ROW_DATA_START = 4

# Experiment sheet column → (TYPE, mode)
# mode: "text"  → emit TEXT_VALUE; VALUE/UNITS/RELATION left empty
#       "numeric" → emit VALUE + UNITS + RELATION="="; TEXT_VALUE left empty
_COL_MAP = [
    ("Pre-culture preparation and conditions",          "PRE-CULTURE PREPARATION", "text"),
    ("Sample preparation",                              "SAMPLE PREPARATION",       "text"),
    ("Incubation temperature in celsius",               "TEMPERATURE",              "numeric_celsius"),
    # TIMEPOINT handled specially (combines timepoints + unit)
    ("Oxygen conditions",                               "CONDITION",                "text"),
    ("Media composition",                               "MEDIA",                    "text"),
    ("Shaking speed",                                   "SHAKING SPEED",            "text"),
    ("Negative controls",                               "CONTROL",                  "text"),
    ("Antibiotic pre-treatment",                        "ANTIBIOTICS",              "text"),
    ("Sample storage",                                  "STORAGE",                  "text"),
]

# Biomass columns — combined into a single BIOMASS row
_COL_BIOMASS_START = "Biomass/inoculum density at the start"
_COL_BIOMASS_END   = "Biomass/inoculum density at the end"
_COL_TIMEPOINTS    = "Time-course information (i.e., number of timepoints)"
_COL_TIME_UNIT     = "Time_unit"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(v) -> str:
    """Normalise a cell value: NaN floats and 'nan'-like strings become ''."""
    if not isinstance(v, str):
        try:
            return "" if pd.isna(v) else str(v)
        except (TypeError, ValueError):
            return str(v)
    v = v.strip()
    return "" if v in ("nan", "None", "NaN") else v


def _read_sheet(ods_path: Path, sheet_name: str) -> pd.DataFrame:
    """Generic ODS sheet reader using the standard template row layout."""
    raw = pd.read_excel(ods_path, sheet_name=sheet_name, header=None, engine="odf")
    col_names = [
        str(c).strip() if isinstance(c, str) else str(c)
        for c in raw.iloc[_ROW_COLNAMES].tolist()
    ]
    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    df = df.reset_index(drop=True).dropna(how="all")
    return df.map(_clean)


def _get_experiment_for_assay(exp_df: pd.DataFrame, aidx: str) -> pd.Series | None:
    """
    Return the first Experiment row that applies to *aidx*.

    A row matches when its 'identifier' field is 'all' (case-insensitive)
    or when aidx appears in the comma-separated list of identifiers.
    """
    for _, row in exp_df.iterrows():
        raw_id = str(row.get("identifier") or "").strip()
        if not raw_id:
            continue
        if raw_id.lower() in ("all", "most"):
            return row
        ids = [x.strip() for x in raw_id.split(",")]
        if aidx in ids:
            return row
    return None


def _make_row(aidx: str, type_: str, relation: str = "", value: str = "",
              units: str = "", text_value: str = "", comments: str = "") -> dict:
    return {
        "AIDX":       aidx,
        "TYPE":       type_,
        "RELATION":   relation,
        "VALUE":      value,
        "UNITS":      units,
        "TEXT_VALUE": text_value,
        "COMMENTS":   comments,
    }


def _extract_aidx_from_experiment(exp_df: pd.DataFrame) -> list[str]:
    """
    Extract all unique, specific AIDX values from the identifier column of
    the Experiment sheet.

    Rows whose identifier is 'all' or 'most' are skipped (they are catch-all
    rows that apply to every AIDX but do not define new ones).
    Comma-separated identifiers are expanded, so "AIDX001, AIDX002" yields
    two entries.

    Returns an ordered list with duplicates removed.
    """
    seen: set[str] = set()
    aidx_list: list[str] = []
    for _, row in exp_df.iterrows():
        raw_id = str(row.get("identifier") or "").strip()
        if not raw_id or raw_id.lower() in ("all", "most"):
            continue
        for aid in raw_id.split(","):
            aid = aid.strip()
            if aid and aid not in seen:
                seen.add(aid)
                aidx_list.append(aid)
    return aidx_list


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_assay_param(
    exp_df: pd.DataFrame,
    aidx_list: list[str],
    dose: str,
    dose_units: str,
    dose_comments: str,
) -> pd.DataFrame:
    """
    Build ASSAY_PARAM rows for every AIDX in *aidx_list*.

    For each AIDX, look up its Experiment row and emit one row per
    non-empty parameter.  DOSE is emitted when --dose is supplied.
    BIOMASS is emitted only when at least one biomass field is non-empty.
    """
    records = []

    for aidx in aidx_list:
        exp_row = _get_experiment_for_assay(exp_df, aidx)

        if exp_row is None:
            print(f"[WARN] No Experiment row found for AIDX '{aidx}' — skipping params.",
                  file=sys.stderr)
            continue

        # --- DOSE (from CLI, not from template sheet) ---
        if dose:
            records.append(_make_row(
                aidx, "DOSE",
                relation="=", value=dose, units=dose_units,
                comments=dose_comments,
            ))

        # --- Mapped text / numeric columns ---
        for col, type_, mode in _COL_MAP:
            val = _clean(exp_row.get(col, ""))
            if not val:
                continue

            if mode == "text":
                records.append(_make_row(aidx, type_, text_value=val))

            elif mode == "numeric_celsius":
                # Coerce e.g. "37.0" → "37"
                try:
                    num = str(int(float(val)))
                except (ValueError, TypeError):
                    num = val
                records.append(_make_row(
                    aidx, type_,
                    relation="=", value=num, units="celsius",
                ))

        # --- TIMEPOINT (combines timepoints string + time unit) ---
        timepoints = _clean(exp_row.get(_COL_TIMEPOINTS, ""))
        time_unit  = _clean(exp_row.get(_COL_TIME_UNIT, ""))
        if timepoints:
            tp_text = f"{timepoints} {time_unit}".strip() if time_unit else timepoints
            records.append(_make_row(aidx, "TIMEPOINT", text_value=tp_text))

        # --- BIOMASS (start + end combined; skip if both empty) ---
        biomass_start = _clean(exp_row.get(_COL_BIOMASS_START, ""))
        biomass_end   = _clean(exp_row.get(_COL_BIOMASS_END, ""))
        if biomass_start or biomass_end:
            text_val = biomass_start if biomass_start else ""
            comments = f"End: {biomass_end}" if biomass_end else ""
            if biomass_start and biomass_end:
                comments = f"End: {biomass_end}"
            records.append(_make_row(aidx, "BIOMASS", text_value=text_val, comments=comments))

    return pd.DataFrame(records, columns=ASSAY_PARAM_COLS)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(param_df: pd.DataFrame, expected_aidx: list[str]) -> list[str]:
    """
    Return a list of validation warning strings (empty list → all OK).

    Checks:
    - Mandatory fields (AIDX, TYPE) are non-empty.
    - TYPE belongs to the controlled vocabulary.
    - VALUE and RELATION are both set or both absent.
    - UNITS is required when VALUE is set for numeric TYPEs (TEMPERATURE, DOSE).
    - Each row has at least one of VALUE or TEXT_VALUE.
    - Every expected AIDX has at least one parameter row in the output.
    """
    errors: list[str] = []

    for i, row in param_df.iterrows():
        label = f"Row {i + 1} (AIDX={row.get('AIDX', '?')}, TYPE={row.get('TYPE', '?')})"

        for field in MANDATORY_PARAM_FIELDS:
            if not str(row.get(field) or "").strip():
                errors.append(f"{label}: mandatory field '{field}' is empty.")

        type_ = str(row.get("TYPE") or "").strip()
        if type_ and type_ not in VALID_PARAM_TYPES:
            errors.append(
                f"{label}: TYPE '{type_}' not in {sorted(VALID_PARAM_TYPES)}."
            )

        value    = str(row.get("VALUE")      or "").strip()
        units    = str(row.get("UNITS")      or "").strip()
        relation = str(row.get("RELATION")   or "").strip()
        text_val = str(row.get("TEXT_VALUE") or "").strip()

        # VALUE and RELATION should be paired
        if value and not relation:
            errors.append(f"{label}: RELATION is required when VALUE is set.")
        if relation and not value:
            errors.append(f"{label}: VALUE is required when RELATION is set.")

        # Numeric types require UNITS
        if value and not units and type_ in ("TEMPERATURE", "DOSE"):
            errors.append(
                f"{label}: UNITS is required when VALUE is set for TYPE '{type_}'."
            )

        # At least one of VALUE or TEXT_VALUE must carry content
        if not value and not text_val:
            errors.append(
                f"{label}: both VALUE and TEXT_VALUE are empty — "
                "at least one must be non-empty."
            )

    # Every expected AIDX should appear in the output
    seen_aidx = set(param_df["AIDX"].dropna().str.strip().tolist()) if not param_df.empty else set()
    for aidx in expected_aidx:
        if aidx not in seen_aidx:
            errors.append(
                f"AIDX '{aidx}': no parameter rows were generated "
                "(check the Experiment sheet identifier column)."
            )

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate ASSAY_PARAM.tsv from a MIX-MB Template_open_MB.ods. "
            "AIDXs are read from the first column ('identifier') of the "
            "Experiment sheet. Optionally supply --assay ASSAY.tsv to override "
            "the AIDX list (backward-compatible)."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to Template_open_MB.ods",
    )
    parser.add_argument(
        "--outdir", default=".",
        help="Output directory",
    )
    parser.add_argument(
        "--dose", default="",
        help="Drug/compound dose value (e.g. '5'). Omit to skip DOSE rows.",
    )
    parser.add_argument(
        "--dose_units", default="uM",
        help="Units for --dose (default: uM)",
    )
    parser.add_argument(
        "--dose_comments", default="",
        help="Optional COMMENTS text for the DOSE row",
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

    # --- Read Experiment sheet ---
    exp_df = _read_sheet(ods_path, "Experiment")
    if exp_df.empty:
        sys.exit("ERROR: no data rows found in the Experiment sheet.")

    # --- Resolve AIDX list ---
    if args.assay:
        assay_path = Path(args.assay)
        if not assay_path.exists():
            sys.exit(f"ERROR: ASSAY.tsv not found: {assay_path}")
        assay_df = pd.read_csv(assay_path, sep="\t", dtype=str).fillna("")
        if "AIDX" not in assay_df.columns:
            sys.exit(f"ERROR: 'AIDX' column not found in {assay_path}")
        aidx_list = [a for a in assay_df["AIDX"].dropna().str.strip().tolist() if a]
        if not aidx_list:
            sys.exit("ERROR: no AIDXs found in ASSAY.tsv.")
    else:
        aidx_list = _extract_aidx_from_experiment(exp_df)
        if not aidx_list:
            sys.exit(
                "ERROR: no specific AIDXs found in the Experiment sheet identifier "
                "column. Either add explicit AIDX values to the identifier column, "
                "or supply --assay ASSAY.tsv."
            )

    # --- Build ---
    param_df = build_assay_param(
        exp_df,
        aidx_list,
        dose=args.dose.strip(),
        dose_units=args.dose_units.strip(),
        dose_comments=args.dose_comments.strip(),
    )

    if param_df.empty:
        print("[WARN] No ASSAY_PARAM rows were generated — "
              "check that Experiment sheet fields are filled.", file=sys.stderr)

    # --- Validate ---
    errors = validate(param_df, aidx_list)
    if errors:
        for msg in errors:
            print(f"WARNING: {msg}", file=sys.stderr)
        if args.strict:
            sys.exit(1)

    # --- Write ---
    out_path = outdir / "ASSAY_PARAM.tsv"
    param_df.to_csv(out_path, sep="\t", index=False)
    print(f"Written: {out_path}")
    print(f"[SUCCESS] {len(param_df)} parameter row(s) written for {len(aidx_list)} assay(s).")


if __name__ == "__main__":
    main()
