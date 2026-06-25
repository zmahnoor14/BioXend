#!/usr/bin/env python3
"""
fill_template.py — Module 7 (BioXend / MIX-MB)

Produces a copy of Template_open.ods with auto-resolved metadata fields
pre-filled in the Chemicals and Microbes sheets. All cell styles (colors,
fonts, borders) are preserved from the original template.

Fields filled / appended:

  Chemicals sheet (matched by Common_Name):
    CIDX (new column prepended as col 0) — auto-generated CIDX from COMPOUND_MAPPING.tsv
    InChI                — RDKit-derived from SMILES
    InChIKey             — RDKit-derived from SMILES
    Molecular_formula    — RDKit-derived from SMILES
    Molecular_weight     — RDKit average molecular weight
    Monoisotopic_mass    — RDKit exact molecular weight
    Note: Chemical_identifier (user-provided) is preserved as-is.

  Microbes sheet (matched by assay_identifier):
    AIDX (new column prepended as col 0) — pipeline-generated AIDX from ASSAY_MAPPING.tsv
    ASSAY_TAX_ID         — resolved via StrainInfo (if user left it blank)
    ASSAY_ORGANISM       — NCBI canonical name (overwritten when corrected)
    ASSAY_STRAIN         — from ASSAY.tsv (only filled if blank)
    TARGET_NAME          — resolved via UniProt
    TARGET_ORGANISM      — resolved via UniProt / NCBI canonical
    TARGET_TAX_ID        — resolved via UniProt
    Note: assay_identifier (user-provided) is preserved as-is.

Usage:
    python bin/fill_template.py \\
        --input            exampledata/Template_filled.ods \\
        --compound_mapping results/COMPOUND_MAPPING.tsv \\
        --assay_tsv        results/ASSAY.tsv \\
        --assay_mapping    results/ASSAY_MAPPING.tsv \\
        --name_changes     results/ORGANISM_NAME_CHANGES.tsv \\
        --outdir           results/
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import MolToInchi, InchiToInchiKey
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from odf.namespaces import OFFICENS, TABLENS

# Template row offsets (0-based)
_ROW_COLNAMES   = 1
_ROW_DATA_START = 4


# ── ODS cell helpers ──────────────────────────────────────────────────────────

def _sheet_rows(sheet: Table) -> list:
    """Return only direct child table:table-row elements (not nested)."""
    return [n for n in sheet.childNodes
            if hasattr(n, "qname") and n.qname == (TABLENS, "table-row")]


def _row_cells(row: TableRow) -> list:
    """Expand table:number-columns-repeated to return a flat list of cells.

    Repeated cells share the same element object — this is fine for reading.
    For writing we only target cells in named columns, which are never
    part of a repeated trailing-empty block in a well-formed template.
    """
    cells = []
    for node in row.childNodes:
        if not hasattr(node, "qname"):
            continue
        if node.qname not in ((TABLENS, "table-cell"),
                               (TABLENS, "covered-table-cell")):
            continue
        repeat = int(node.getAttrNS(TABLENS, "number-columns-repeated") or 1)
        for _ in range(repeat):
            cells.append(node)
    return cells


def _get_text(cell) -> str:
    """Extract string value from an ODS table cell."""
    parts = []
    for p in cell.getElementsByType(P):
        for node in p.childNodes:
            if hasattr(node, "data"):
                parts.append(node.data)
    return "".join(parts).strip()


def _set_text(cell, value: str) -> None:
    """Set the string value of an ODS cell, preserving the cell style."""
    # Remove existing text:p children
    for p in list(cell.getElementsByType(P)):
        cell.removeChild(p)
    # Declare value type as string
    cell.setAttrNS(OFFICENS, "value-type", "string")
    # Remove any numeric value attribute that might conflict
    for key in list(cell.attributes.keys()):
        if key[0] == OFFICENS and "value" in key[1]:
            del cell.attributes[key]
    # Write new text content
    p = P()
    p.addText(str(value))
    cell.addElement(p)


def _write_cell_at(row: TableRow, col_index: int, value: str) -> None:
    """Write value to the logical column col_index in row.

    Handles number-columns-repeated by splitting the repeated block so that
    only the target column receives the value. Uses only attribute changes and
    insertBefore/addElement — never removeChild — to avoid the odfpy document
    cache ValueError that removeChild raises on template-loaded cells.

    Split strategy (no removeChild needed):
      offset == 0: write to node, set its repeat to 1, insert suffix after it.
      offset  > 0: shrink node to prefix, insert target after it, insert suffix.
    """
    pos = 0
    for node in list(row.childNodes):
        if not hasattr(node, "qname"):
            continue
        if node.qname not in ((TABLENS, "table-cell"), (TABLENS, "covered-table-cell")):
            continue

        repeat = int(node.getAttrNS(TABLENS, "number-columns-repeated") or 1)
        if pos + repeat <= col_index:
            pos += repeat
            continue

        # node covers col_index (pos <= col_index < pos + repeat)
        offset = col_index - pos
        style  = node.getAttrNS(TABLENS, "style-name")

        def _new_empty(count: int = 1) -> TableCell:
            c = TableCell()
            if style:
                c.setAttrNS(TABLENS, "style-name", style)
            if count != 1:
                c.setAttrNS(TABLENS, "number-columns-repeated", str(count))
            return c

        def _insert_after(anchor, new_node) -> None:
            """Insert new_node immediately after anchor in row."""
            found = False
            for child in list(row.childNodes):
                if found:
                    row.insertBefore(new_node, child)
                    return
                if child is anchor:
                    found = True
            row.addElement(new_node)

        if offset == 0:
            # node starts at col_index: write directly, split off suffix.
            _set_text(node, value)
            suffix = repeat - 1
            if suffix >= 1:
                node.setAttrNS(TABLENS, "number-columns-repeated", "1")
                _insert_after(node, _new_empty(suffix))
        else:
            # prefix | target | suffix  — shrink node to prefix, insert rest.
            node.setAttrNS(TABLENS, "number-columns-repeated", str(offset))
            target = _new_empty()
            _set_text(target, value)
            _insert_after(node, target)
            suffix = repeat - offset - 1
            if suffix >= 1:
                _insert_after(target, _new_empty(suffix))

        return


def _col_index(sheet: Table) -> dict[str, int]:
    """Return {column_name: column_index} from the header row (row 1)."""
    rows = _sheet_rows(sheet)
    if len(rows) <= _ROW_COLNAMES:
        return {}
    cells = _row_cells(rows[_ROW_COLNAMES])
    return {_get_text(c): i for i, c in enumerate(cells) if _get_text(c)}


def _fill_sheet(
    sheet: Table,
    key_col: str,
    updates: dict[str, dict[str, str]],
    force_cols: set[str] | None = None,
) -> int:
    """Fill cells in *sheet* where the key column matches a key in *updates*.

    Blank cells are always filled.  Cells in *force_cols* are overwritten even
    when the user already provided a value (used for canonical name corrections).

    Returns the number of cells written.
    """
    force_cols = force_cols or set()
    col_idx = _col_index(sheet)
    if key_col not in col_idx:
        print(f"[WARN] Key column '{key_col}' not found in sheet — skipping.",
              file=sys.stderr)
        return 0

    ki = col_idx[key_col]
    rows = _sheet_rows(sheet)
    filled = 0

    for row in rows[_ROW_DATA_START:]:
        cells = _row_cells(row)
        if ki >= len(cells):
            continue
        key_val = _get_text(cells[ki])
        if not key_val or key_val not in updates:
            continue

        for col_name, new_value in updates[key_val].items():
            if not new_value:
                continue
            if col_name not in col_idx:
                continue
            ci = col_idx[col_name]
            if ci >= len(cells):
                continue
            existing = _get_text(cells[ci])
            if existing and col_name not in force_cols:
                continue  # preserve user-provided value
            # Use _write_cell_at (not _set_text on cells[ci]) to correctly
            # handle repeated-cell blocks — cells[ci] may share an object with
            # adjacent empty columns, causing the value to bleed across them.
            _write_cell_at(row, ci, str(new_value))
            filled += 1

    return filled


def _prepend_column(
    sheet: Table,
    col_name: str,
    key_to_value: "dict[str, str]",
    key_col: str,
    dtype: str = "",
    description: str = "",
) -> int:
    """Insert a new column as the FIRST column (position 0) in *sheet*.

    Unlike _fill_sheet, which writes into pre-existing columns, this function
    inserts a brand-new column that does not yet exist in the template.

    *key_to_value* maps the value found in *key_col* (e.g. Common_Name or
    assay_identifier) to the string to write in the new column.
    Rows 0–3 receive the section header, column name, dtype, and description.
    Data rows (4+) are matched by *key_col*; unmatched rows get an empty cell.

    Key values are pre-read BEFORE any row modifications so that inserting
    a new first column does not shift the key column index mid-loop.

    Returns the number of data cells written with a non-empty value.
    """
    col_idx = _col_index(sheet)
    ki = col_idx.get(key_col, -1)
    if ki < 0:
        print(f"[WARN] Key column '{key_col}' not found — cannot prepend '{col_name}'.",
              file=sys.stderr)
        return 0

    rows = _sheet_rows(sheet)

    # Pre-read key values from all data rows BEFORE modifying anything.
    row_keys: "list[str]" = []
    for row in rows[_ROW_DATA_START:]:
        cells = _row_cells(row)
        row_keys.append(_get_text(cells[ki]) if ki < len(cells) else "")

    written = 0
    for i, row in enumerate(rows):
        if i == 0:
            value = ""
        elif i == _ROW_COLNAMES:
            value = col_name
        elif i == 2:
            value = dtype
        elif i == 3:
            value = description
        else:
            data_idx = i - _ROW_DATA_START
            key = row_keys[data_idx] if 0 <= data_idx < len(row_keys) else ""
            value = key_to_value.get(key, "") if key else ""

        new_cell = TableCell()
        if value:
            new_cell.setAttrNS(OFFICENS, "value-type", "string")
            p = P()
            p.addText(value)
            new_cell.addElement(p)

        # Insert before the first existing cell child so it becomes column 0.
        first_cell = next(
            (n for n in row.childNodes
             if hasattr(n, "qname")
             and n.qname in ((TABLENS, "table-cell"), (TABLENS, "covered-table-cell"))),
            None,
        )
        if first_cell is not None:
            row.insertBefore(new_cell, first_cell)
        else:
            row.addElement(new_cell)

        if value and i >= _ROW_DATA_START:
            written += 1

    return written


# ── Molecular property computation ────────────────────────────────────────────

def _mol_props(smiles: str) -> dict[str, str]:
    """Compute molecular properties from a SMILES string via RDKit.

    Formula, average MW, and monoisotopic mass are computed independently from
    InChI so that salt/mixture SMILES (containing '.' separators) still yield
    mass values even when MolToInchi fails on disconnected structures.
    """
    result = {
        "InChI": "", "InChIKey": "",
        "Molecular_formula": "",
        "Molecular_weight": "", "Monoisotopic_mass": "",
    }
    if not smiles:
        return result
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"[WARN] RDKit could not parse SMILES '{smiles[:50]}'", file=sys.stderr)
        return result

    # Formula and masses work reliably for disconnected (salt/mixture) SMILES.
    try:
        result["Molecular_formula"] = CalcMolFormula(mol)
        result["Molecular_weight"]  = f"{Descriptors.MolWt(mol):.4f}"
        result["Monoisotopic_mass"] = f"{Descriptors.ExactMolWt(mol):.4f}"
    except Exception as exc:
        print(f"[WARN] RDKit mass/formula error for SMILES '{smiles[:50]}': {exc}",
              file=sys.stderr)

    # InChI can fail on multi-component SMILES — compute separately so a
    # failure here does not discard the mass values computed above.
    try:
        inchi = MolToInchi(mol) or ""
        if inchi:
            result["InChI"]    = inchi
            result["InChIKey"] = InchiToInchiKey(inchi) or ""
    except Exception as exc:
        print(f"[WARN] RDKit InChI error for SMILES '{smiles[:50]}': {exc}",
              file=sys.stderr)

    return result


# ── Update-dict builders ──────────────────────────────────────────────────────

def _read_sheet_df(ods_path: Path, sheet_name: str) -> pd.DataFrame:
    raw = pd.read_excel(ods_path, sheet_name=sheet_name, header=None, engine="odf")
    cols = [str(c).strip() for c in raw.iloc[_ROW_COLNAMES].tolist()]
    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = cols
    return df.reset_index(drop=True).dropna(how="all").fillna("")


def build_chemicals_updates(
    ods_path: Path,
    compound_mapping_path: Path,
) -> "tuple[dict[str, dict[str, str]], dict[str, str]]":
    """Return (updates, cidx_by_name) for the Chemicals sheet.

    updates      — {Common_Name: {col_name: value}} for existing columns
                   (InChI, InChIKey, Molecular_formula, Molecular_weight,
                   Monoisotopic_mass). Chemical_identifier is NOT touched.
    cidx_by_name — {Common_Name: CIDX} used to append the new CIDX column.
    """
    cidx_map: "dict[str, str]" = {}
    if compound_mapping_path.exists():
        cm = pd.read_csv(compound_mapping_path, sep="\t", dtype=str).fillna("")
        for _, row in cm.iterrows():
            name = str(row.get("Common_Name", "")).strip()
            cidx = str(row.get("CIDX", "")).strip()
            if name and cidx:
                cidx_map[name] = cidx

    df = _read_sheet_df(ods_path, "Chemicals")
    updates: "dict[str, dict[str, str]]" = {}

    for _, row in df.iterrows():
        name   = str(row.get("Common_Name", "")).strip()
        smiles = str(row.get("SMILES", "")).strip()
        if not name:
            continue

        # Prefer Eluted_compound_SMILES when the user flagged that the eluted
        # compound differs from the stock (e.g. free base vs. salt form).
        eluted        = str(row.get("Eluted_compound", "")).strip().lower()
        eluted_smiles = str(row.get("Eluted_compound_SMILES", "")).strip()
        if eluted in ("true", "1", "yes") and eluted_smiles:
            smiles = eluted_smiles

        entry = _mol_props(smiles)
        if any(entry.values()):
            updates[name] = entry

    return updates, cidx_map


def build_microbes_updates(
    assay_tsv_path: Path,
    assay_mapping_path: Path,
    name_changes_path: "Path | None",
) -> "tuple[dict[str, dict[str, str]], set[str], dict[str, str]]":
    """Return (updates, force_cols, aidx_by_key) for the Microbes sheet.

    updates       — {assay_identifier: {col_name: value}} for existing columns
                    (ASSAY_TAX_ID, ASSAY_ORGANISM, ASSAY_STRAIN, TARGET_NAME,
                    TARGET_ORGANISM, TARGET_TAX_ID). assay_identifier is NOT touched.
    force_cols    — columns overwritten even when not blank (NCBI canonical corrections)
    aidx_by_key   — {assay_identifier: AIDX} used to append the new AIDX column.
    """
    if not assay_tsv_path.exists() or not assay_mapping_path.exists():
        return {}, set(), {}

    assay_df   = pd.read_csv(assay_tsv_path,   sep="\t", dtype=str).fillna("")
    mapping_df = pd.read_csv(assay_mapping_path, sep="\t", dtype=str).fillna("")

    key_to_aidx: "dict[str, str]" = {
        row["assay_identifier"]: row["AIDX"]
        for _, row in mapping_df.iterrows()
        if row.get("assay_identifier") and row.get("AIDX")
    }
    aidx_to_row: "dict[str, pd.Series]" = {
        row["AIDX"]: row
        for _, row in assay_df.iterrows()
        if row.get("AIDX")
    }

    # Columns whose resolved value always wins (NCBI canonical name corrections)
    force_cols: "set[str]" = set()

    if name_changes_path and name_changes_path.exists():
        nc = pd.read_csv(name_changes_path, sep="\t", dtype=str).fillna("")
        for _, row in nc.iterrows():
            field = row.get("field", "").strip()
            if field:
                force_cols.add(field)

    fill_cols = [
        "ASSAY_TAX_ID", "ASSAY_ORGANISM", "ASSAY_STRAIN",
        "TARGET_NAME", "TARGET_ORGANISM", "TARGET_TAX_ID",
    ]

    updates: "dict[str, dict[str, str]]" = {}
    for user_key, aidx in key_to_aidx.items():
        if aidx not in aidx_to_row:
            continue
        assay_row = aidx_to_row[aidx]
        updates[user_key] = {
            col: assay_row.get(col, "")
            for col in fill_cols
            if assay_row.get(col, "")
        }

    return updates, force_cols, key_to_aidx


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Fill auto-resolved metadata back into a copy of Template_open.ods. "
            "Only blank cells are filled; user-provided values are preserved "
            "(except organism names corrected by NCBI Taxonomy)."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input",            required=True,
                        help="Path to Template_open.ods")
    parser.add_argument("--compound_mapping", required=True,
                        help="Path to COMPOUND_MAPPING.tsv from chemicals.py")
    parser.add_argument("--assay_tsv",        required=True,
                        help="Path to ASSAY.tsv from microbes.py")
    parser.add_argument("--assay_mapping",    required=True,
                        help="Path to ASSAY_MAPPING.tsv from microbes.py")
    parser.add_argument("--name_changes",     default=None,
                        help="Path to ORGANISM_NAME_CHANGES.tsv (optional)")
    parser.add_argument("--outdir",           default=".",
                        help="Output directory")
    args = parser.parse_args()

    ods_path = Path(args.input)
    outdir   = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not ods_path.exists():
        sys.exit(f"ERROR: template not found: {ods_path}")

    # ── Build update dicts ──────────────────────────────────────────────────
    print("Computing fill-back values...")

    chem_updates, cidx_by_name = build_chemicals_updates(
        ods_path, Path(args.compound_mapping)
    )
    microbe_updates, force_cols, aidx_by_key = build_microbes_updates(
        Path(args.assay_tsv),
        Path(args.assay_mapping),
        Path(args.name_changes) if args.name_changes else None,
    )

    # ── Load ODS (preserves all cell styles) ───────────────────────────────
    print("Loading template (preserving formatting)...")
    doc = load(str(ods_path))

    sheets = {
        s.getAttribute("name"): s
        for s in doc.spreadsheet.getElementsByType(Table)
    }

    # ── Fill Chemicals (existing columns) ──────────────────────────────────
    if "Chemicals" in sheets and chem_updates:
        n = _fill_sheet(sheets["Chemicals"], "Common_Name", chem_updates)
        print(f"  Chemicals: {n} cell(s) filled in existing columns.")
    else:
        print("  Chemicals: nothing to fill in existing columns.")

    # ── Prepend CIDX as column 0 in Chemicals ──────────────────────────────
    if "Chemicals" in sheets and cidx_by_name:
        n = _prepend_column(
            sheets["Chemicals"], "CIDX", cidx_by_name, "Common_Name",
            dtype="string",
            description="Auto-generated ChEMBL compound index (BioXend)",
        )
        print(f"  Chemicals: CIDX prepended as column 0 ({n} value(s) written).")
    else:
        print("  Chemicals: no CIDX values to prepend.")

    # ── Fill Microbes (existing columns) ───────────────────────────────────
    if "Microbes" in sheets and microbe_updates:
        n = _fill_sheet(
            sheets["Microbes"], "assay_identifier",
            microbe_updates, force_cols=force_cols,
        )
        if force_cols:
            print(f"  Microbes: {n} cell(s) filled "
                  f"(incl. canonical-name corrections for: "
                  f"{', '.join(sorted(force_cols))}).")
        else:
            print(f"  Microbes: {n} cell(s) filled in existing columns.")
    else:
        print("  Microbes: nothing to fill in existing columns.")

    # ── Prepend AIDX as column 0 in Microbes ───────────────────────────────
    if "Microbes" in sheets and aidx_by_key:
        n = _prepend_column(
            sheets["Microbes"], "AIDX", aidx_by_key, "assay_identifier",
            dtype="string",
            description="Auto-generated ChEMBL assay index (BioXend)",
        )
        print(f"  Microbes: AIDX prepended as column 0 ({n} value(s) written).")
    else:
        print("  Microbes: no AIDX values to prepend.")

    # ── Save ────────────────────────────────────────────────────────────────
    out_path = outdir / "Template_BioXend_completed.ods"
    doc.save(str(out_path))
    size_kb = out_path.stat().st_size // 1024
    print(f"Written: {out_path} ({size_kb} KB)")
    print("[SUCCESS] Completed template ready.")


if __name__ == "__main__":
    main()
