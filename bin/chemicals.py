#!/usr/bin/env python3
"""
chemicals.py — Module 2 (BioXend / MIX-MB)

Reads the Chemicals sheet from a MIX-MB Template_open.ods and produces:
  - COMPOUND_RECORD.tsv   ChEMBL deposition format
  - COMPOUND_CTAB.sdf     2D chemical structures (RDKit)

Template colour coding:
  Green  = Mandatory   → CIDX (auto-generated if blank), RIDX, COMPOUND_KEY,
                         COMPOUND_NAME, SMILES
  Blue   = Recommended → IUPAC_Name, InChI, InChIKey, CAS_number
  Yellow = Optional    → COMPOUND_SOURCE (Vendor / database_ID), Stock info,
                         MS columns

Usage:
    python bin/chemicals.py --input Standards/Templates/Template_open.ods \\
                        --ridx GutMeta --prefix CIDX --outdir results/
"""

import argparse
import sys
from pathlib import Path
import odf

import pandas as pd
import requests
from rdkit import Chem
from rdkit.Chem import AllChem

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# ChEMBL COMPOUND_RECORD.tsv columns (in deposition order)
CHEMBL_COLS = ["CIDX", "RIDX", "COMPOUND_KEY", "COMPOUND_NAME", "COMPOUND_SOURCE"]

MANDATORY_FIELDS = ["CIDX", "RIDX", "COMPOUND_KEY", "COMPOUND_NAME"]

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

def read_chemicals_sheet(ods_path: Path) -> pd.DataFrame:
    """
    Parse the Chemicals sheet from Template_open.ods.

    Returns a clean DataFrame with one row per compound entry.
    """
    raw = pd.read_excel(ods_path, sheet_name="Chemicals", header=None, engine="odf")

    col_names = raw.iloc[_ROW_COLNAMES].tolist()

    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    df = df.reset_index(drop=True)
    df = df.dropna(how="all")

    def _clean(v):
        if not isinstance(v, str):
            # NaN floats from empty cells must become "" so downstream
            # truthiness checks work correctly (float('nan') is truthy!)
            try:
                return "" if pd.isna(v) else v
            except (TypeError, ValueError):
                return v
        v = v.strip()
        return "" if v in ("nan", "None", "NaN") else v

    return df.map(_clean)


# ---------------------------------------------------------------------------
# ChEMBL lookup (optional enrichment / validation)
# ---------------------------------------------------------------------------

# def _query_chembl(smiles_list: list, batch_size: int = 100) -> dict:
    # """
    # Query ChEMBL API for molecules matching the given canonical SMILES.

    # Returns a dict keyed by canonical SMILES ->
    #     {"chembl_id": str, "pref_name": str}.
    # Compounds not found in ChEMBL are absent from the dict.
    # """
    # url_stem = "https://www.ebi.ac.uk"
    # fields = "molecule_chembl_id,pref_name,molecule_structures"
    # found: dict = {}

    # for i in range(0, len(smiles_list), batch_size):
    #     batch = smiles_list[i : i + batch_size]
    #     smiles_str = ",".join(batch)
    #     url = (
    #         f"{url_stem}/chembl/api/data/molecule?"
    #         f"molecule_structures__canonical_smiles__in={smiles_str}"
    #         f"&only={fields}&format=json&limit=1000"
    #     )
    #     print(
    #         f"[INFO] Querying ChEMBL batch "
    #         f"{i // batch_size + 1}/{(len(smiles_list) - 1) // batch_size + 1}"
    #     )
    #     try:
    #         resp = requests.get(url, timeout=30).json()
    #     except Exception as exc:
    #         print(f"[WARN] ChEMBL request failed: {exc}", file=sys.stderr)
    #         continue

    #     def _collect(resp_json: dict) -> None:
    #         for mol in resp_json.get("molecules", []):
    #             structs = mol.get("molecule_structures") or {}
    #             can = structs.get("canonical_smiles", "")
    #             if can:
    #                 found[can] = {
    #                     "chembl_id": mol.get("molecule_chembl_id", ""),
    #                     "pref_name":  mol.get("pref_name", ""),
    #                 }

    #     _collect(resp)
    #     while resp.get("page_meta", {}).get("next"):
    #         try:
    #             resp = requests.get(
    #                 url_stem + resp["page_meta"]["next"], timeout=30
    #             ).json()
    #             _collect(resp)
    #         except Exception as exc:
    #             print(f"[WARN] ChEMBL pagination failed: {exc}", file=sys.stderr)
    #             break

    # return found


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def _make_cidx(n: int, total: int, prefix: str) -> str:
    """
    Zero-padded CIDX scaled to dataset size:
      1–9 compounds   → PREFIX01  … PREFIX09
      10–99           → PREFIX001 … PREFIX099
      100–999         → PREFIX0001… PREFIX0999
      1000–9999       → PREFIX00001…PREFIX09999
    """
    width = len(str(total)) + 1
    return f"{prefix}{str(n).zfill(width)}"


def build_compound_records(
    df: pd.DataFrame,
    ridx: str,
    prefix: str,
    #skip_chembl: bool = False,
) -> pd.DataFrame:
    """
    Validate SMILES, assign CIDXs, and build the compound records table.

    The returned DataFrame carries private columns _smiles and _mol
    used by the SDF writer; these are dropped before TSV export.
    """
    # Optional ChEMBL lookup for enrichment / validation
    # chembl_map: dict = {}
    # if not skip_chembl:
    #     valid_smiles = [
    #         s for s in df.get("SMILES", pd.Series(dtype=str)).tolist()
    #         if isinstance(s, str) and s.strip()
    #     ]
    #     if valid_smiles:
    #         chembl_map = _query_chembl(valid_smiles)
    #         missing = [s for s in valid_smiles if s not in chembl_map]
    #         if missing:
    #             print(
    #                 f"[WARN] {len(missing)} SMILES not found in ChEMBL:",
    #                 file=sys.stderr,
    #             )
    #             for s in missing:
    #                 print(f"       {s}", file=sys.stderr)

    records = []
    auto_n = 1
    total = len(df)

    for i, row in df.iterrows():
        smiles = str(row.get("SMILES") or "").strip()

        # Validate SMILES with RDKit
        mol = Chem.MolFromSmiles(smiles) if smiles else None
        if mol is None:
            label = str(row.get("Common_Name") or f"row {i + 1}").strip()
            print(
                f"[WARN] Row {i + 1} ({label!r}): "
                f"invalid or missing SMILES — skipped.",
                file=sys.stderr,
            )
            continue

        # CIDX: use provided Chemical_identifier or auto-generate
        raw_cidx = str(row.get("Chemical_identifier") or "").strip()
        if raw_cidx:
            cidx = raw_cidx
        else:
            cidx = _make_cidx(auto_n, total, prefix)
            auto_n += 1  # only advance counter when auto-generating

        # COMPOUND_NAME (mandatory — green field)
        compound_name = str(row.get("Common_Name") or "").strip()

        # COMPOUND_KEY (mandatory — green field)
        # Local_Synonym used in the manuscript; fallback to Common_Name
        compound_key = str(row.get("Local_Synonym") or "").strip() or compound_name

        # COMPOUND_SOURCE (optional — yellow field)
        # Vendor preferred; fall back to database_ID
        vendor  = str(row.get("Vendor")      or "").strip()
        db_id   = str(row.get("database_ID") or "").strip()
        compound_source = vendor or db_id

        records.append(
            {
                "CIDX":            cidx,
                "RIDX":            ridx,
                "COMPOUND_KEY":    compound_key,
                "COMPOUND_NAME":   compound_name,
                "COMPOUND_SOURCE": compound_source,
                # private — used only by the SDF writer
                "_smiles":         smiles,
                "_mol":            mol,
            }
        )

    return pd.DataFrame(records)


def write_compound_ctab_sdf(record_df: pd.DataFrame, out_path: Path) -> None:
    """
    Write COMPOUND_CTAB.sdf.

    Each entry has:
      - Molecule name line (title): CIDX
      - 2D coordinates generated by RDKit
      - SDF property: CIDX
    """
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    writer = Chem.SDWriter(str(out_path))

    for _, row in record_df.iterrows():
        mol = row["_mol"]
        AllChem.Compute2DCoords(mol)
        mol.SetProp("_Name", str(row["CIDX"]))  # title line = CIDX
        mol.SetProp("CIDX",  str(row["CIDX"]))
        writer.write(mol)

    writer.close()


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(record_df: pd.DataFrame) -> list:
    """Return a list of validation error strings (empty list -> all OK)."""
    errors = []

    for i, row in record_df.iterrows():
        label = f"Row {i + 1} (CIDX={row.get('CIDX', '?')})"
        for field in MANDATORY_FIELDS:
            if not str(row.get(field) or "").strip():
                errors.append(f"{label}: mandatory field '{field}' is empty.")

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate COMPOUND_RECORD.tsv + COMPOUND_CTAB.sdf "
            "from a MIX-MB Template_open.ods"
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
        "--prefix", default="CIDX",
        help="Prefix for auto-generated CIDX values (e.g. HMDM -> HMDM0001)",
    )
    parser.add_argument(
        "--outdir", default=".",
        help="Output directory",
    )
    parser.add_argument(
        "--skip-chembl", action="store_true",
        help="Skip ChEMBL API lookup (faster, works offline)",
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
    df = read_chemicals_sheet(ods_path)
    if df.empty:
        sys.exit("ERROR: no data rows found in the Chemicals sheet.")

    # --- Build ---
    record_df = build_compound_records(
        df,
        ridx=args.ridx,
        prefix=args.prefix,
        #skip_chembl=args.skip_chembl,
    )

    if record_df.empty:
        sys.exit("ERROR: no valid compounds after SMILES validation.")

    # --- Validate ---
    errors = validate(record_df)
    if errors:
        for msg in errors:
            print(f"WARNING: {msg}", file=sys.stderr)
        if args.strict:
            sys.exit(1)

    # --- Write COMPOUND_RECORD.tsv ---
    record_path = outdir / "COMPOUND_RECORD.tsv"
    record_df[CHEMBL_COLS].to_csv(record_path, sep="\t", index=False)
    print(f"Written: {record_path}")

    # --- Write COMPOUND_CTAB.sdf ---
    sdf_path = outdir / "COMPOUND_CTAB.sdf"
    write_compound_ctab_sdf(record_df, sdf_path)
    print(f"Written: {sdf_path}")

    print(f"[SUCCESS] {len(record_df)} compound(s) processed.")


if __name__ == "__main__":
    main()
