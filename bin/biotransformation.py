#!/usr/bin/env python3
"""
biotransformation.py — Module 5 (BioXend / MIX-MB)

Reads the Biotransformation sheet from a MIX-MB Template_open.ods and
produces:
  - ACTIVITY.tsv     ChEMBL deposition format

Each row in the Biotransformation sheet = one activity entry.
Columns 11–16 (metabolite detection, annotation, kinetics, reaction type)
are MIX-MB extensions concatenated into ACTIVITY_COMMENT alongside
column 10.

Column mappings (template column → ChEMBL ACTIVITY.tsv field):
  Chemical_identifier / Common_Name  → CIDX  (via --compounds COMPOUND_RECORD.tsv)
  [--ridx CLI arg]                   → RIDX  (ChEMBL reference column)
  ASSAY_Identifier                   → AIDX  (via --assays ASSAY_MAPPING.tsv)
  Activity type                      → TYPE
  TEXT_VALUE                         → TEXT_VALUE
  RELATION                           → RELATION
  VALUE                              → VALUE
  UPPER_VALUE                        → UPPER_VALUE
  UNITS                              → UNITS
  ACTIVITY_COMMENT + extension cols  → ACTIVITY_COMMENT (concatenated)
  ACTION_TYPE                        → ACTION_TYPE

Extension columns appended to ACTIVITY_COMMENT (if filled):
  Reaction type           → "The reaction is <val>"
  Metabolite m/z          → "The Metabolite m/z is <val>"
  Metabolite retention time → "with retention time <val>."  (joined with m/z line)
  Metabolite annotation   → "The annotated metabolite is <val> with annotation level of <level>"
  Metabolite annotation level → (combined with annotation line above)

Ignored template columns (not mapped):
  Common_Name, SMILES           — used only to look up CIDX from Chemicals sheet
  Kinetic_parameter_type        — not deposited to ChEMBL
  Kinetic_parameter_value       — not deposited to ChEMBL
  Classify_activity             — ML classification only

Template colour coding:
  Green  = Mandatory   → CIDX, AIDX, RIDX, ACTIVITY_COMMENT, TYPE
  Blue   = Recommended → TEXT_VALUE or VALUE (at least one required)
  Yellow = Optional    → UPPER_VALUE, ACTION_TYPE, metabolite/kinetic cols

Usage:
    # Recommended — run chemicals and microbes steps first:
    python bin/biotransformation.py \\
        --input     Standards/Templates/Template_open.ods \\
        --ridx      GutMeta \\
        --compounds results/COMPOUND_RECORD.tsv \\
        --assays    results/ASSAY_MAPPING.tsv \\
        --outdir    results/

    # Without mapping files (requires Chemical_identifier and AIDX to be
    # pre-filled in the template, or falls back to raw user values):
    python bin/biotransformation.py \\
        --input   Standards/Templates/Template_open.ods \\
        --ridx    GutMeta \\
        --outdir  results/
"""

import argparse
import sys
from pathlib import Path

import odf  # noqa: F401 — required by pandas odf engine
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# ChEMBL ACTIVITY.tsv columns (in deposition order)
CHEMBL_COLS = [
    "CIDX",
    "RIDX",
    "AIDX",
    "TYPE",
    "TEXT_VALUE",
    "RELATION",
    "VALUE",
    "UPPER_VALUE",
    "UNITS",
    "ACTIVITY_COMMENT",
    "ACTION_TYPE",
]

MANDATORY_FIELDS = ["CIDX", "RIDX", "AIDX", "ACTIVITY_COMMENT", "TYPE"]

VALID_TEXT_VALUES = {
    "Compound metabolized",
    "Compound NOT metabolized",
    "Product detected",
    "Partial transformation",
    "Complete transformation",
}

VALID_ACTION_TYPES = {"SUBSTRATE", "PRODUCT", "No Activity", "INHIBITION", "STIMULATION"}

VALID_RELATIONS = {"=", "<", ">", "~", "<=", ">="}

VALID_UNITS = {"%"}

# Template sheet row offsets (0-based, read with header=None)
#   row 0 — section group headers  (skip)
#   row 1 — column names           (use as header)
#   row 2 — data types             (skip)
#   row 3 — field descriptions     (skip)
#   row 4+ — data rows
_ROW_COLNAMES   = 1
_ROW_DATA_START = 4

# Template column names for MIX-MB extension fields appended to ACTIVITY_COMMENT.
# Kinetic_parameter_type, Kinetic_parameter_value, and Classify_activity are
# intentionally excluded — they are not deposited to ChEMBL.
_COL_REACTION_TYPE  = "Reaction type"
_COL_METABOLITE_MZ  = "Metabolite m/z"
_COL_METABOLITE_RT  = "Metabolite retention time"
_COL_METABOLITE_ANN = "Metabolite annotation"
_COL_METABOLITE_LVL = "Metabolite annotation level"


# ---------------------------------------------------------------------------
# Reading helpers
# ---------------------------------------------------------------------------

def _clean(v):
    """Normalise a cell value: NaN floats and 'nan'-like strings become ''."""
    if not isinstance(v, str):
        try:
            return "" if pd.isna(v) else str(v)
        except (TypeError, ValueError):
            return str(v)
    v = v.strip()
    return "" if v in ("nan", "None", "NaN") else v


def _read_sheet(ods_path: Path, sheet_name: str) -> pd.DataFrame:
    """
    Generic ODS sheet reader using the standard template row layout.
    Strips leading/trailing whitespace from column names.
    """
    raw = pd.read_excel(ods_path, sheet_name=sheet_name, header=None, engine="odf")
    col_names = [
        str(c).strip() if isinstance(c, str) else str(c)
        for c in raw.iloc[_ROW_COLNAMES].tolist()
    ]
    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    df = df.reset_index(drop=True)
    df = df.dropna(how="all")
    return df.map(_clean)


def read_biotransformation_sheet(ods_path: Path) -> pd.DataFrame:
    """Parse the Biotransformation sheet from Template_open.ods."""
    return _read_sheet(ods_path, "Biotransformation")


# ---------------------------------------------------------------------------
# CIDX resolution
# ---------------------------------------------------------------------------

def _build_cidx_map(
    ods_path: Path,
    compounds_tsv: "Path | None" = None,
) -> "dict[str, str]":
    """
    Build a {common_name_lower: cidx} lookup map from two sources.

    Source 1 — Chemicals sheet in the same template:
        Common_Name → Chemical_identifier
    Source 2 — COMPOUND_RECORD.tsv from the workflow (if provided):
        COMPOUND_NAME → CIDX  (overrides source 1; workflow CIDXs are authoritative
        when Chemical_identifier was auto-generated rather than pre-filled)
    """
    cidx_map: "dict[str, str]" = {}

    # Source 1: Chemicals sheet
    try:
        chem_df = _read_sheet(ods_path, "Chemicals")
        for _, row in chem_df.iterrows():
            name = str(row.get("Common_Name") or "").strip()
            cidx = str(row.get("Chemical_identifier") or "").strip()
            if name and cidx:
                cidx_map[name.lower()] = cidx
    except Exception as exc:
        print(
            f"[WARN] Could not read Chemicals sheet for CIDX lookup: {exc}",
            file=sys.stderr,
        )

    # Source 2: COMPOUND_RECORD.tsv (overrides Chemicals sheet)
    if compounds_tsv is not None and Path(compounds_tsv).exists():
        try:
            rec_df = pd.read_csv(compounds_tsv, sep="\t", dtype=str).fillna("")
            for _, row in rec_df.iterrows():
                name = str(row.get("COMPOUND_NAME") or "").strip()
                cidx = str(row.get("CIDX") or "").strip()
                if name and cidx:
                    cidx_map[name.lower()] = cidx
        except Exception as exc:
            print(
                f"[WARN] Could not read COMPOUND_RECORD.tsv for CIDX lookup: {exc}",
                file=sys.stderr,
            )

    if not cidx_map:
        print(
            "[WARN] CIDX map is empty — Chemical_identifier column may be blank in "
            "the Chemicals sheet. Supply --compounds COMPOUND_RECORD.tsv so that "
            "workflow-generated CIDXs can be used for lookup.",
            file=sys.stderr,
        )
    else:
        print(f"[INFO] CIDX map loaded: {len(cidx_map)} compound(s).", file=sys.stderr)

    return cidx_map


# ---------------------------------------------------------------------------
# AIDX resolution
# ---------------------------------------------------------------------------

def _build_aidx_map(
    assay_mapping_tsv: "Path | None" = None,
) -> "dict[str, str]":
    """
    Build a {user_aidx: generated_aidx} lookup map from ASSAY_MAPPING.tsv.

    ASSAY_MAPPING.tsv is written by microbes.py alongside ASSAY.tsv.
    It maps the short user-provided identifier from the Microbes sheet AIDX
    column (e.g. 'assay1') to the pipeline-generated ChEMBL AIDX (e.g.
    'Zimmermann_gut_metagenome_community_Biotransformation').

    This is the exact analogue of _build_cidx_map for assays.
    """
    aidx_map: "dict[str, str]" = {}

    if assay_mapping_tsv is None or not Path(assay_mapping_tsv).exists():
        return aidx_map

    try:
        mapping_df = pd.read_csv(assay_mapping_tsv, sep="\t", dtype=str).fillna("")
        for _, row in mapping_df.iterrows():
            user_aidx = str(row.get("USER_AIDX") or "").strip()
            aidx      = str(row.get("AIDX") or "").strip()
            if user_aidx and aidx:
                aidx_map[user_aidx] = aidx
    except Exception as exc:
        print(
            f"[WARN] Could not read ASSAY_MAPPING.tsv for AIDX lookup: {exc}",
            file=sys.stderr,
        )

    if not aidx_map:
        print(
            "[WARN] AIDX map is empty — supply --assays ASSAY_MAPPING.tsv "
            "(generated by microbes.py) so that ASSAY_Identifier values are "
            "resolved to pipeline-generated AIDXs.",
            file=sys.stderr,
        )
    else:
        print(f"[INFO] AIDX map loaded: {len(aidx_map)} assay(s).", file=sys.stderr)

    return aidx_map


def _resolve_aidx(row: pd.Series, aidx_map: "dict[str, str]") -> str:
    """
    Return the ChEMBL AIDX for a Biotransformation sheet row.

    Priority:
      1. ASSAY_Identifier looked up in aidx_map (from ASSAY_MAPPING.tsv).
         This converts the user's short key to the pipeline-generated AIDX.
      2. ASSAY_Identifier used as-is when no mapping is available (fallback
         for cases where the user pre-filled a full ChEMBL AIDX directly).
    """
    user_aidx = str(row.get("ASSAY_Identifier") or "").strip()
    if not user_aidx:
        return ""

    if aidx_map:
        resolved = aidx_map.get(user_aidx, "")
        if resolved:
            return resolved
        print(
            f"[WARN] No AIDX mapping found for ASSAY_Identifier '{user_aidx}'. "
            "Using value as-is — verify it matches an AIDX in ASSAY.tsv.",
            file=sys.stderr,
        )

    return user_aidx


def _resolve_cidx(row: pd.Series, cidx_map: "dict[str, str]") -> str:
    """
    Return CIDX for a Biotransformation sheet row.

    Priority:
      1. Chemical_identifier column (pre-filled by the user in the template).
      2. Common_Name looked up in cidx_map (from Chemicals sheet /
         COMPOUND_RECORD.tsv).  Emits a warning when unresolved.
    """
    direct = str(row.get("Chemical_identifier") or "").strip()
    if direct:
        return direct

    common_name = str(row.get("Common_Name") or "").strip()
    if common_name:
        resolved = cidx_map.get(common_name.lower(), "")
        if not resolved:
            print(
                f"[WARN] No CIDX found for Common_Name '{common_name}'. "
                "Fill Chemical_identifier in the template, or supply --compounds.",
                file=sys.stderr,
            )
        return resolved

    return ""


# ---------------------------------------------------------------------------
# Comment builder
# ---------------------------------------------------------------------------

def _build_activity_comment(row: pd.Series) -> str:
    """
    Build ACTIVITY_COMMENT from the free-text comment (col 10) plus any
    filled MIX-MB extension fields, using the prescribed sentence formats.

    Appended fragments (only when the source cell is non-empty):
      Reaction type           → "The reaction is <val>"
      Metabolite m/z + rt     → "The Metabolite m/z is <mz> with retention time <rt>."
                                 (or just one clause if only one is filled)
      Metabolite annotation   → "The annotated metabolite is <ann> with annotation
                                  level of <level>"  (level omitted if blank)
    """
    parts = []

    base = str(row.get("ACTIVITY_COMMENT") or "").strip()
    if base:
        parts.append(base)

    reaction = str(row.get(_COL_REACTION_TYPE) or "").strip()
    if reaction:
        parts.append(f"The reaction is {reaction}")

    mz = str(row.get(_COL_METABOLITE_MZ) or "").strip()
    rt = str(row.get(_COL_METABOLITE_RT) or "").strip()
    if mz and rt:
        parts.append(f"The Metabolite m/z is {mz} with retention time {rt}.")
    elif mz:
        parts.append(f"The Metabolite m/z is {mz}")
    elif rt:
        parts.append(f"with retention time {rt}.")

    annotation = str(row.get(_COL_METABOLITE_ANN) or "").strip()
    level      = str(row.get(_COL_METABOLITE_LVL) or "").strip()
    if annotation and level:
        parts.append(
            f"The annotated metabolite is {annotation} with annotation level of {level}"
        )
    elif annotation:
        parts.append(f"The annotated metabolite is {annotation}")

    return "; ".join(parts)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def _coerce_numeric(raw) -> str:
    """Coerce a numeric cell value (e.g. 85.0) to a clean string ('85')."""
    if raw == "" or raw is None:
        return ""
    try:
        fval = float(str(raw))
        return str(int(fval)) if fval == int(fval) else str(fval)
    except (ValueError, TypeError):
        return str(raw).strip()


def build_activity_tsv(
    df: pd.DataFrame,
    ridx: str,
    cidx_map: "dict[str, str]",
    aidx_map: "dict[str, str]",
) -> pd.DataFrame:
    """
    Build the ACTIVITY.tsv records from the Biotransformation sheet DataFrame.

    One row per Biotransformation sheet entry.
    CIDX is resolved via Chemical_identifier (direct) or Common_Name lookup
    in cidx_map (built from the Chemicals sheet / COMPOUND_RECORD.tsv).
    AIDX is resolved via ASSAY_Identifier lookup in aidx_map (built from
    ASSAY_MAPPING.tsv produced by microbes.py) — the user's short key (e.g.
    'assay1') is mapped to the pipeline-generated ChEMBL AIDX.
    TYPE is always 'Biotransformation' per the MIX-MB standard.
    ACTIVITY_COMMENT concatenates the free-text comment with MIX-MB extension fields.
    """
    records = []

    for _, row in df.iterrows():
        activity_comment = _build_activity_comment(row)

        records.append({
            "CIDX":             _resolve_cidx(row, cidx_map),
            "RIDX":             ridx,
            "AIDX":             _resolve_aidx(row, aidx_map),
            "TYPE":             "Biotransformation",
            "TEXT_VALUE":       str(row.get("TEXT_VALUE") or "").strip(),
            "RELATION":         str(row.get("RELATION") or "").strip(),
            "VALUE":            _coerce_numeric(row.get("VALUE")),
            "UPPER_VALUE":      _coerce_numeric(row.get("UPPER_VALUE")),
            "UNITS":            str(row.get("UNITS") or "").strip(),
            "ACTIVITY_COMMENT": activity_comment,
            "ACTION_TYPE":      str(row.get("ACTION_TYPE") or "").strip(),
        })

    return pd.DataFrame(records, columns=CHEMBL_COLS)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(activity_df: pd.DataFrame) -> list:
    """Return a list of validation warning strings (empty list → all OK)."""
    errors = []

    for i, row in activity_df.iterrows():
        label = f"Row {i + 1} (CIDX={row.get('CIDX', '?')}, AIDX={row.get('AIDX', '?')})"

        for field in MANDATORY_FIELDS:
            val = str(row.get(field) or "").strip()
            if not val:
                errors.append(f"{label}: mandatory field '{field}' is empty.")

        text_val = str(row.get("TEXT_VALUE") or "").strip()
        value    = str(row.get("VALUE") or "").strip()
        relation = str(row.get("RELATION") or "").strip()
        units    = str(row.get("UNITS") or "").strip()
        action   = str(row.get("ACTION_TYPE") or "").strip()

        # At least one of TEXT_VALUE or VALUE must be present
        if not text_val and not value:
            errors.append(
                f"{label}: both TEXT_VALUE and VALUE are empty — "
                "at least one must be provided."
            )

        # TEXT_VALUE controlled vocabulary check
        if text_val and text_val not in VALID_TEXT_VALUES:
            errors.append(
                f"{label}: TEXT_VALUE '{text_val}' not in controlled vocabulary "
                f"{sorted(VALID_TEXT_VALUES)}."
            )

        # VALUE requires RELATION and UNITS
        if value:
            if not relation:
                errors.append(f"{label}: RELATION is required when VALUE is set.")
            if not units:
                errors.append(f"{label}: UNITS is required when VALUE is set.")

        if relation and relation not in VALID_RELATIONS:
            errors.append(
                f"{label}: RELATION '{relation}' not in {sorted(VALID_RELATIONS)}."
            )

        if units and units not in VALID_UNITS:
            errors.append(
                f"{label}: UNITS '{units}' not valid — must be '%'."
            )

        # ACTION_TYPE controlled vocabulary check
        if action and action not in VALID_ACTION_TYPES:
            errors.append(
                f"{label}: ACTION_TYPE '{action}' not in controlled vocabulary "
                f"{sorted(VALID_ACTION_TYPES)}."
            )

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate ACTIVITY.tsv from a MIX-MB Template_open.ods "
            "(Biotransformation sheet)"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to Template_open.ods",
    )
    parser.add_argument(
        "--ridx", required=True,
        help="RIDX (reference) identifier for this submission (must match REFERENCE.tsv)",
    )
    parser.add_argument(
        "--compounds", default=None,
        help=(
            "Path to COMPOUND_RECORD.tsv generated by the chemicals step. "
            "When supplied, workflow-generated CIDXs (COMPOUND_NAME → CIDX) "
            "override the Chemicals sheet lookup. Omit to rely on the "
            "Chemicals sheet alone."
        ),
    )
    parser.add_argument(
        "--assays", default=None,
        help=(
            "Path to ASSAY_MAPPING.tsv generated by the microbes step. "
            "Maps each user-provided ASSAY_Identifier (e.g. 'assay1') to the "
            "pipeline-generated ChEMBL AIDX. Omit only if ASSAY_Identifier "
            "values in the Biotransformation sheet are already full ChEMBL AIDXs."
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

    ods_path        = Path(args.input)
    outdir          = Path(args.outdir)
    compounds_tsv   = Path(args.compounds) if args.compounds else None
    assay_mapping   = Path(args.assays)    if args.assays    else None

    if not ods_path.exists():
        sys.exit(f"ERROR: input file not found: {ods_path}")
    if compounds_tsv is not None and not compounds_tsv.exists():
        sys.exit(f"ERROR: COMPOUND_RECORD.tsv not found: {compounds_tsv}")
    if assay_mapping is not None and not assay_mapping.exists():
        sys.exit(f"ERROR: ASSAY_MAPPING.tsv not found: {assay_mapping}")

    outdir.mkdir(parents=True, exist_ok=True)

    # --- Read ---
    df = read_biotransformation_sheet(ods_path)
    if df.empty:
        sys.exit("ERROR: no data rows found in the Biotransformation sheet.")

    # --- Build CIDX map (Chemicals sheet + optional COMPOUND_RECORD.tsv) ---
    cidx_map = _build_cidx_map(ods_path, compounds_tsv)

    # --- Build AIDX map (optional ASSAY_MAPPING.tsv from microbes step) ---
    aidx_map = _build_aidx_map(assay_mapping)

    # --- Build ---
    activity_df = build_activity_tsv(df, ridx=args.ridx, cidx_map=cidx_map, aidx_map=aidx_map)

    # --- Validate ---
    errors = validate(activity_df)
    if errors:
        for msg in errors:
            print(f"WARNING: {msg}", file=sys.stderr)
        if args.strict:
            sys.exit(1)

    # --- Write ---
    out_path = outdir / "ACTIVITY.tsv"
    activity_df.to_csv(out_path, sep="\t", index=False)
    print(f"Written: {out_path}")
    print(f"[SUCCESS] {len(activity_df)} activity row(s) written.")


if __name__ == "__main__":
    main()
