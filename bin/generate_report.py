#!/usr/bin/env python3
"""
generate_report.py — Module 6 (BioXend / MIX-MB)

Reads all sheets from a MIX-MB Template_open.ods and produces:
  - report.html   Self-contained interactive HTML report

Usage:
    python bin/generate_report.py \\
        --input   exampledata/Template_filled.ods \\
        --outdir  results/
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

import os
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp")  # numba can't cache in read-only containers

import numpy as np
import odf
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

try:
    import umap
    _UMAP_AVAILABLE = True
except (ImportError, RuntimeError):
    _UMAP_AVAILABLE = False
    print("[WARN] umap-learn not available — UMAP will be omitted from report.", file=sys.stderr)


# ── Constants ──────────────────────────────────────────────────────────────────

_ROW_COLNAMES   = 1
_ROW_DATA_START = 4

_PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.35.2.min.js"

# ACTION_TYPE values that indicate a biotransformation occurred.
# An empty ACTION_TYPE means the compound was tested but showed no activity.
VALID_ACTION_TYPES = {
    "ACTIVATOR", "ALLOSTERIC ANTAGONIST", "ANTAGONIST",
    "ANTISENSE INHIBITOR", "BINDING AGENT", "BLOCKER",
    "CHELATING AGENT", "CROSS-LINKING AGENT", "DEGRADER",
    "DISRUPTING AGENT", "EXOGENOUS GENE", "EXOGENOUS PROTEIN",
    "GENE EDITING NEGATIVE MODULATOR", "HYDROLYTIC ENZYME", "INHIBITOR",
    "INVERSE AGONIST", "METHYLATING AGENT", "MODULATOR",
    "NEGATIVE ALLOSTERIC MODULATOR", "NEGATIVE MODULATOR", "OPENER",
    "POSITIVE MODULATOR", "OTHER", "OXIDATIVE ENZYME",
    "PARTIAL AGONIST", "POSITIVE ALLOSTERIC MODULATOR", "POSITIVE MODULATOR",
    "PROTEOLYTIC ENZYME", "REDUCING AGENT", "RELEASING AGENT",
    "RNAI INHIBITOR", "SEQUESTERING AGENT", "STABILISER", "SUBSTRATE",
    "VACCINE ANTIGEN",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _clean(v) -> str:
    if not isinstance(v, str):
        try:
            return "" if pd.isna(v) else str(v)
        except (TypeError, ValueError):
            return str(v)
    v = v.strip()
    return "" if v in ("nan", "None", "NaN") else v


def _read_sheet(ods_path: Path, sheet_name: str) -> pd.DataFrame:
    raw = pd.read_excel(ods_path, sheet_name=sheet_name, header=None, engine="odf")
    col_names = [str(c).strip() for c in raw.iloc[_ROW_COLNAMES].tolist()]
    df = raw.iloc[_ROW_DATA_START:].copy()
    df.columns = col_names
    return df.reset_index(drop=True).dropna(how="all").map(_clean)


def _get_col(row, *candidates) -> str:
    """Return first non-empty value from a list of candidate column names."""
    for c in candidates:
        v = _clean(row.get(c, ""))
        if v:
            return v
    return ""


def _is_active(row: pd.Series) -> bool:
    """Return True when ACTION_TYPE is a recognised biotransformation action.

    Empty ACTION_TYPE means the compound was tested but showed no activity.
    Classify_activity is intentionally not used — it is an optional field.
    """
    return _clean(row.get("ACTION_TYPE", "")).upper() in VALID_ACTION_TYPES



def _fetch_js(url: str, label: str) -> str | None:
    try:
        print(f"  Fetching {label} ... ", end="", flush=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            content = resp.read().decode("utf-8")
        print(f"OK ({len(content)//1024} KB)")
        return content
    except Exception as exc:
        print(f"FAILED ({exc})")
        return None


# ── Data builders ──────────────────────────────────────────────────────────────

def _assay_id(row: pd.Series) -> str:
    for col in row.index:
        if col.lower().strip() == "assay_identifier":
            v = _clean(row[col])
            if v:
                return v
    return ""


def _build_activity_matrix(bioT_df, chemicals_df, microbes_df):
    compounds = [_clean(r.get("Common_Name", "")) for _, r in chemicals_df.iterrows()]
    compounds = [c for c in compounds if c]

    assays = []
    assay_labels = []
    for _, r in microbes_df.iterrows():
        aid = _clean(r.get("assay_identifier", ""))
        if aid:
            org = _clean(r.get("ASSAY_ORGANISM", ""))
            strain = _clean(r.get("ASSAY_STRAIN", ""))
            label = org + (f" ({strain})" if strain else "")
            assays.append(aid)
            assay_labels.append(label or aid)

    # matrix[compound][assay] = None (untested) | 0 (not active) | 1 (active)
    matrix  = {c: {a: None for a in assays} for c in compounds}
    tooltip = {c: {a: ""   for a in assays} for c in compounds}

    for _, row in bioT_df.iterrows():
        cname = _clean(row.get("Common_Name", ""))
        aid   = _assay_id(row)
        if not cname or not aid:
            continue
        if cname not in matrix or aid not in matrix.get(cname, {}):
            continue

        text_val = _clean(row.get("TEXT_VALUE", ""))
        value    = _clean(row.get("VALUE", ""))
        units    = _clean(row.get("UNITS", ""))
        action   = _clean(row.get("ACTION_TYPE", ""))
        reaction = _clean(row.get("Reaction_type", ""))
        comment  = _clean(row.get("ACTIVITY_COMMENT", ""))

        # 1 = active (ACTION_TYPE present), 0 = tested / no activity (ACTION_TYPE empty)
        matrix[cname][aid] = 1 if _is_active(row) else 0

        parts = []
        if text_val:
            parts.append(text_val)
        if action:
            parts.append(f"Action: {action}")
        if reaction:
            parts.append(f"Reaction: {reaction}")
        if value:
            parts.append(f"Value: {value} {units}".strip())
        if comment:
            parts.append(comment[:100] + ("…" if len(comment) > 100 else ""))
        tooltip[cname][aid] = " | ".join(parts)

    return compounds, assays, assay_labels, matrix, tooltip


_morgan_gen = None

def _get_morgan_gen():
    global _morgan_gen
    if _morgan_gen is None:
        _morgan_gen = GetMorganGenerator(radius=2, fpSize=2048)
    return _morgan_gen


def _build_umap(chemicals_df, bioT_df):
    """Compute UMAP from Morgan fingerprints (Tanimoto distance). Returns list of point dicts."""
    if not _UMAP_AVAILABLE:
        return []

    gen  = _get_morgan_gen()
    rows = []
    fps  = []
    for _, r in chemicals_df.iterrows():
        name   = _clean(r.get("Common_Name", ""))
        smiles = _clean(r.get("SMILES", ""))
        if not name or not smiles:
            continue
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            continue
        fp = gen.GetFingerprint(mol)
        fps.append(fp)
        rows.append({"name": name, "smiles": smiles})

    if len(rows) < 4:
        return []

    # Pairwise Tanimoto distance matrix
    n = len(fps)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            sim = DataStructs.TanimotoSimilarity(fps[i], fps[j])
            dist[i, j] = dist[j, i] = 1.0 - sim

    n_neighbors = min(10, n - 1)
    coords = umap.UMAP(
        metric="precomputed",
        n_neighbors=n_neighbors,
        min_dist=0.3,
        random_state=42,
    ).fit_transform(dist)

    # Determine activity status per compound from bioT_df
    active_set   = set()
    inactive_set = set()
    for _, row in bioT_df.iterrows():
        cname = _clean(row.get("Common_Name", ""))
        if not cname:
            continue
        if _is_active(row):
            active_set.add(cname)
        else:
            inactive_set.add(cname)

    points = []
    for idx, r in enumerate(rows):
        name = r["name"]
        if name in active_set:
            status = "Metabolized"
        elif name in inactive_set:
            status = "Not metabolized"
        else:
            status = "Not tested"
        points.append({
            "name":   name,
            "smiles": r["smiles"],
            "x":      float(coords[idx, 0]),
            "y":      float(coords[idx, 1]),
            "status": status,
        })
    return points


def _build_qc(ref_df, chemicals_df, microbes_df, bioT_df):
    results = []

    ref_fields = ["DOI", "DATA_LICENCE", "CONTACT", "REF_TYPE", "YEAR",
                  "AUTHORS", "TITLE", "ABSTRACT"]
    if not ref_df.empty:
        row = ref_df.iloc[0]
        for f in ref_fields:
            val = _clean(row.get(f, ""))
            results.append({
                "sheet": "Reference", "field": f,
                "status": "ok" if val else "missing",
                "value": val[:60] if val else "—",
            })

    for _, row in chemicals_df.iterrows():
        name   = _clean(row.get("Common_Name", "?"))
        smiles = _clean(row.get("SMILES", ""))
        mol    = Chem.MolFromSmiles(smiles) if smiles else None
        status = "ok" if mol else ("invalid" if smiles else "missing")
        results.append({
            "sheet": "Chemicals", "field": f"{name} · SMILES",
            "status": status,
            "value": smiles[:40] if smiles else "—",
        })

    for _, row in microbes_df.iterrows():
        org   = _clean(row.get("ASSAY_ORGANISM", "?"))
        taxid = _clean(row.get("ASSAY_TAX_ID", ""))
        results.append({
            "sheet": "Microbes", "field": f"{org} · ASSAY_TAX_ID",
            "status": "ok" if taxid else "missing",
            "value": taxid if taxid else "—",
        })

    for _, row in bioT_df.iterrows():
        cname = _clean(row.get("Common_Name", ""))
        if not cname:
            continue
        aid      = _assay_id(row)
        text_val = _clean(row.get("TEXT_VALUE", ""))
        value    = _clean(row.get("VALUE", ""))
        results.append({
            "sheet": "Biotransformation",
            "field": f"{cname} × {aid}",
            "status": "ok" if (text_val or value) else "missing",
            "value": (text_val or value or "—")[:60],
        })

    return results


# ── HTML assembly ──────────────────────────────────────────────────────────────

def build_html(ref_df, chemicals_df, microbes_df, exp_df, bioT_df,
               plotly_js: str | None) -> str:

    ref = ref_df.iloc[0] if not ref_df.empty else pd.Series(dtype=str)
    title    = _clean(ref.get("TITLE",   "MIX-MB Biotransformation Report"))
    authors  = _clean(ref.get("AUTHORS", ""))
    year     = _clean(ref.get("YEAR",    ""))
    journal  = _clean(ref.get("JOURNAL_NAME", ""))
    doi      = _clean(ref.get("DOI",     ""))
    ridx     = _clean(ref.get("Reference_identifier", ""))
    abstract = _clean(ref.get("ABSTRACT", ""))
    doi_href = f"https://doi.org/{doi}" if doi else "#"

    compounds_list = [_clean(r.get("Common_Name", "")) for _, r in chemicals_df.iterrows()
                      if _clean(r.get("Common_Name", ""))]
    microbes_list  = [_clean(r.get("ASSAY_ORGANISM", "")) for _, r in microbes_df.iterrows()
                      if _clean(r.get("ASSAY_ORGANISM", ""))]

    active_count = sum(1 for _, r in bioT_df.iterrows() if _is_active(r))
    total_tested = sum(1 for _, r in bioT_df.iterrows()
                       if _clean(r.get("Common_Name", "")))
    pct = f"{100*active_count/total_tested:.0f}" if total_tested else "0"

    # ── UMAP
    print("  Computing structural UMAP...")
    umap_points = _build_umap(chemicals_df, bioT_df)

    if not _UMAP_AVAILABLE:
        umap_message = "UMAP unavailable — umap-learn is not installed in this environment."
    elif not umap_points:
        umap_message = "UMAP requires at least 4 compounds."
    else:
        umap_message = ""

    # ── Activity matrix
    compounds_hm, assays_hm, assay_labels_hm, matrix, tooltip_data = \
        _build_activity_matrix(bioT_df, chemicals_df, microbes_df)

    z_vals, text_vals = [], []
    for cname in compounds_hm:
        z_row, t_row = [], []
        for aid in assays_hm:
            v   = matrix.get(cname, {}).get(aid)
            tip = tooltip_data.get(cname, {}).get(aid, "")
            z_row.append(v)
            t_row.append(f"<b>{cname}</b><br><b>{aid}</b><br>{tip}" if tip
                         else f"<b>{cname}</b><br><b>{aid}</b><br>Not tested")
        z_vals.append(z_row)
        text_vals.append(t_row)

    # ── QC
    qc_data = _build_qc(ref_df, chemicals_df, microbes_df, bioT_df)

    # ── Experiment fields
    exp_fields = []
    if not exp_df.empty:
        exp_row = exp_df.iloc[0]
        field_map = [
            ("Instrument_for_measurement",                          "Instrument"),
            ("Incubation temperature in celsius",                   "Temperature (°C)"),
            ("DOSE",                                                "Dose"),
            ("DOSE_unit",                                           "Dose unit"),
            ("Oxygen conditions ",                                  "O₂ conditions"),
            ("Media composition ",                                  "Media"),
            ("Shaking speed",                                       "Shaking speed"),
            ("Time-course information (i.e., number of timepoints)","Timepoints"),
            ("Time_unit",                                           "Time unit"),
            ("Incubation duration (total time of assay)",           "Incubation duration"),
            ("Negative controls ",                                  "Negative controls"),
            ("Sample storage",                                      "Sample storage"),
            ("Pre-culture preparation and conditions",              "Pre-culture"),
            ("Sample preparation",                                  "Sample prep"),
        ]
        for col, label in field_map:
            val = _clean(exp_row.get(col, ""))
            if val:
                exp_fields.append({"label": label, "value": val})

    # ── Per-assay active compound counts
    microbe_activity: dict = {}
    for _, row in bioT_df.iterrows():
        aid = _assay_id(row)
        if aid and _is_active(row):
            microbe_activity[aid] = microbe_activity.get(aid, 0) + 1

    assay_to_org = {}
    for _, r in microbes_df.iterrows():
        aid    = _clean(r.get("assay_identifier", ""))
        org    = _clean(r.get("ASSAY_ORGANISM", ""))
        strain = _clean(r.get("ASSAY_STRAIN", ""))
        if aid:
            assay_to_org[aid] = org + (f" {strain}" if strain else "")

    # ── Biotransformation table rows
    bioT_rows = []
    for _, row in bioT_df.iterrows():
        cname = _clean(row.get("Common_Name", ""))
        if not cname:
            continue
        aid = _assay_id(row)
        bioT_rows.append({
            "compound":     cname,
            "assay":        aid,
            "organism":     assay_to_org.get(aid, aid),
            "text_value":   _clean(row.get("TEXT_VALUE", "")),
            "value":        _clean(row.get("VALUE", "")),
            "units":        _clean(row.get("UNITS", "")),
            "action_type":  _clean(row.get("ACTION_TYPE", "")),
            "reaction_type":_clean(row.get("Reaction_type", "")),
            "met_mz":       _clean(row.get("Metabolite_mz", "")),
            "met_rt":       _clean(row.get("Metabolite_rt", "")),
            "met_ann":      _clean(row.get("Metabolite_annotation", "")),
            "ann_level":    _clean(row.get("Metabolite_annotation_level", "")),
            "is_active":    _is_active(row),
            "comment":      _clean(row.get("ACTIVITY_COMMENT", "")),
        })

    # ── Microbe table rows
    microbe_table = []
    for _, row in microbes_df.iterrows():
        aid    = _clean(row.get("assay_identifier", ""))
        org    = _clean(row.get("ASSAY_ORGANISM", ""))
        strain = _clean(row.get("ASSAY_STRAIN", ""))
        taxid  = _clean(row.get("ASSAY_TAX_ID", ""))
        atype  = _clean(row.get("ASSAY_TYPE", ""))
        target = _clean(row.get("TARGET_NAME", ""))
        # Handle possible trailing space in column name
        target_acc = _get_col(row, "TARGET_ACCESSION ", "TARGET_ACCESSION")
        source     = _clean(row.get("ASSAY_SOURCE", ""))
        ena_proj   = _clean(row.get("ENAorSRA_project_Accession_number", ""))
        microbe_table.append({
            "aid":          aid,
            "organism":     org,
            "strain":       strain,
            "taxid":        taxid,
            "assay_type":   atype,
            "target":       target,
            "target_acc":   target_acc.strip(),
            "source":       source,
            "ena_proj":     ena_proj,
            "is_community": "metagenome" in org.lower(),
            "active_count": microbe_activity.get(aid, 0),
        })

    # ── Serialise
    report_data = {
        "title":             title,
        "compounds":         compounds_hm,
        "assays":            assays_hm,
        "assay_labels":      assay_labels_hm,
        "z_vals":            z_vals,
        "text_vals":         text_vals,
        "bioT_rows":         bioT_rows,
        "microbe_table":     microbe_table,
        "qc_data":           qc_data,
        "exp_fields":        exp_fields,
        "umap_points":       umap_points,
        "umap_message":      umap_message,
    }
    data_json = json.dumps(report_data, ensure_ascii=False).replace("</", "<\\/")

    # ── JS library blocks
    if plotly_js:
        plotly_block = f"<script>\n{plotly_js}\n</script>"
    else:
        plotly_block = f'<script src="{_PLOTLY_CDN}"></script>'

    # ── Microbe table HTML
    microbe_rows_html = _render_microbe_rows(microbe_table)

    # ── QC rows HTML
    qc_ok   = sum(1 for q in qc_data if q["status"] == "ok")
    qc_bad  = len(qc_data) - qc_ok
    qc_html = _render_qc_rows(qc_data)

    byline_parts = []
    if authors:
        byline_parts.append(authors)
    if journal:
        byline_parts.append(journal)
    if year:
        byline_parts.append(year)
    byline = " · ".join(byline_parts)
    doi_link = (f'<a href="{doi_href}" target="_blank" class="doi-link">DOI: {doi}</a>'
                if doi else "")

    abstract_block = (
        f'<details class="abstract-details">'
        f'<summary>Abstract</summary>'
        f'<p class="abstract-text">{abstract}</p>'
        f'</details>'
        if abstract else ""
    )

    ref_rows = ""
    if ridx:
        ref_rows += f"<tr><td>RIDX</td><td><code>{ridx}</code></td></tr>"
    if doi:
        ref_rows += f'<tr><td>DOI</td><td><a href="{doi_href}" target="_blank">{doi}</a></td></tr>'
    if journal:
        ref_rows += f"<tr><td>Journal</td><td>{journal}</td></tr>"
    if year:
        ref_rows += f"<tr><td>Year</td><td>{year}</td></tr>"
    if authors:
        ref_rows += f"<tr><td>Authors</td><td>{authors}</td></tr>"

    exp_items_html = "".join(
        f'<div class="exp-item">'
        f'<span class="exp-label">{f["label"]}</span>'
        f'<span class="exp-value">{f["value"]}</span>'
        f'</div>'
        for f in exp_fields
    )

    # Build full HTML
    html = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{title} — BioXend MIX-MB Report</title>\n"
        "<style>\n" + _CSS + "\n</style>\n"
        "</head>\n"
        "<body>\n"

        '<header class="site-header">\n'
        '  <div class="header-inner">\n'
        '    <div class="header-brand">\n'
        '      <span class="brand-logo">BioXend</span>\n'
        '      <span class="brand-sub">MIX-MB Interactive Report</span>\n'
        '    </div>\n'
        '    <div class="header-meta">\n'
        f'      <div class="header-title">{title}</div>\n'
        f'      <div class="header-byline">{byline} {doi_link}</div>\n'
        '    </div>\n'
        '  </div>\n'
        '  <div class="stats-bar">\n'
        f'    <div class="stat-pill"><span class="stat-n">{len(compounds_list)}</span><span class="stat-label">Compounds</span></div>\n'
        f'    <div class="stat-pill"><span class="stat-n">{len(microbes_list)}</span><span class="stat-label">Microbes / Assays</span></div>\n'
        f'    <div class="stat-pill"><span class="stat-n">{active_count}</span><span class="stat-label">Active Pairs</span></div>\n'
        f'    <div class="stat-pill"><span class="stat-n">{pct}%</span><span class="stat-label">Metabolized</span></div>\n'
        '  </div>\n'
        '</header>\n'

        '<nav class="tab-nav">\n'
        '  <button class="tab-btn active" data-tab="heatmap">Activity Heatmap</button>\n'
        '  <button class="tab-btn" data-tab="compounds">Compounds</button>\n'
        '  <button class="tab-btn" data-tab="microbes">Microbes</button>\n'
        '  <button class="tab-btn" data-tab="bioT">Biotransformation Details</button>\n'
        '  <button class="tab-btn" data-tab="qc">QC Summary</button>\n'
        '</nav>\n'

        '<main class="content">\n'

        # Heatmap tab
        '<section id="tab-heatmap" class="tab-panel active">\n'
        '  <div class="card full-width">\n'
        '    <h2 class="card-title">Compound × Microbe Activity Heatmap</h2>\n'
        '    <p class="card-desc">'
        '<span class="legend-swatch active-swatch"></span> Metabolized &nbsp;'
        '<span class="legend-swatch inactive-swatch"></span> Not metabolized &nbsp;'
        '<span class="legend-swatch untested-swatch"></span> Not tested &nbsp;'
        '· Hover cells for details.</p>\n'
        '    <div id="activity-heatmap"></div>\n'
        '  </div>\n'
        '</section>\n'

        # Compounds tab
        '<section id="tab-compounds" class="tab-panel">\n'
        '  <div class="card full-width">\n'
        '    <h2 class="card-title">Structural Chemical Space (UMAP)</h2>\n'
        '    <p class="card-desc">'
        'Morgan fingerprints (ECFP4, radius=2) · Tanimoto distance · '
        '<span class="legend-swatch active-swatch"></span> Metabolized in atleast one biological assay &nbsp;'
        '<span class="legend-swatch inactive-swatch"></span> Not metabolized &nbsp;'
        '<span class="legend-swatch untested-swatch"></span> Not tested</p>\n'
        '    <div id="umap-plot" style="height:480px;"></div>\n'
        '  </div>\n'
        '</section>\n'

        # Microbes tab
        '<section id="tab-microbes" class="tab-panel">\n'
        '  <div class="card full-width">\n'
        '    <h2 class="card-title">Microbial Assays</h2>\n'
        '    <div class="table-wrap">\n'
        '      <table class="data-table">\n'
        '        <thead><tr>'
        '<th>Assay ID</th><th>Organism</th><th>TaxID</th><th>Type</th>'
        '<th>Assay Type</th><th>Target</th><th>ENA Project</th><th>Active Cpds</th>'
        '</tr></thead>\n'
        f'        <tbody>{microbe_rows_html}</tbody>\n'
        '      </table>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n'

        # Biotransformation details tab
        '<section id="tab-bioT" class="tab-panel">\n'
        '  <div class="card full-width">\n'
        '    <h2 class="card-title">Biotransformation Activity Table</h2>\n'
        '    <div class="table-controls">\n'
        '      <input type="text" id="bioT-search" placeholder="Search compound, organism, reaction…"'
        '             oninput="filterBioT()" class="search-input">\n'
        '      <button onclick="exportBioT()" class="export-btn">Export CSV</button>\n'
        '    </div>\n'
        '    <div class="table-wrap">\n'
        '      <table class="data-table">\n'
        '        <thead><tr>'
        '<th onclick="sortBioT(0)">Compound ↕</th>'
        '<th onclick="sortBioT(1)">Organism ↕</th>'
        '<th>Result</th><th>Value</th><th>Action</th>'
        '<th onclick="sortBioT(5)">Reaction ↕</th>'
        '<th>Met. m/z</th><th>Met. RT</th><th>Ann. Level</th><th>Comment</th>'
        '</tr></thead>\n'
        '        <tbody id="bioT-tbody"></tbody>\n'
        '      </table>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n'

        # QC tab
        '<section id="tab-qc" class="tab-panel">\n'
        '  <div class="card full-width">\n'
        '    <h2 class="card-title">QC / Validation Summary</h2>\n'
        '    <div class="qc-summary">\n'
        f'      <span class="qc-pill ok-pill">✓ {qc_ok} OK</span>\n'
        f'      <span class="qc-pill bad-pill">✗ {qc_bad} Issues</span>\n'
        '    </div>\n'
        '    <div class="table-wrap">\n'
        '      <table class="data-table">\n'
        '        <thead><tr><th>Sheet</th><th>Field</th><th>Status</th><th>Value</th></tr></thead>\n'
        f'        <tbody>{qc_html}</tbody>\n'
        '      </table>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n'

        '</main>\n'

        + plotly_block + "\n"

        + f"<script>\nconst REPORT_DATA = {data_json};\n</script>\n"
        + "<script>\n" + _JS + "\n</script>\n"
        + "</body>\n</html>\n"
    )

    return html


# ── HTML fragment renderers ────────────────────────────────────────────────────


def _render_microbe_rows(microbe_table) -> str:
    html = ""
    for m in microbe_table:
        taxid_cell = (
            f'<a href="https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={m["taxid"]}"'
            f' target="_blank">{m["taxid"]}</a>'
            if m["taxid"] else "—"
        )
        target_cell = m["target"]
        if m["target_acc"]:
            target_cell = (
                f'<a href="https://www.uniprot.org/uniprot/{m["target_acc"]}"'
                f' target="_blank">{m["target"] or m["target_acc"]} ({m["target_acc"]})</a>'
            )
        ena_cell = (
            f'<a href="https://www.ebi.ac.uk/ena/browser/view/{m["ena_proj"]}"'
            f' target="_blank">{m["ena_proj"]}</a>'
            if m["ena_proj"] else "—"
        )
        kind = "🌍 Community" if m["is_community"] else "🧫 Pure culture"
        badge_cls = "active-badge" if m["active_count"] > 0 else "inactive-badge"
        html += (
            f'<tr>'
            f'<td><code>{m["aid"]}</code></td>'
            f'<td><i>{m["organism"]}</i>{" " + m["strain"] if m["strain"] else ""}</td>'
            f'<td>{taxid_cell}</td>'
            f'<td>{kind}</td>'
            f'<td>{m["assay_type"]}</td>'
            f'<td>{target_cell or "—"}</td>'
            f'<td>{ena_cell}</td>'
            f'<td><span class="activity-badge {badge_cls}">{m["active_count"]}</span></td>'
            f'</tr>\n'
        )
    return html


def _render_qc_rows(qc_data) -> str:
    html = ""
    for q in qc_data:
        row_cls  = "qc-ok-row"  if q["status"] == "ok" else "qc-bad-row"
        icon     = "✓"          if q["status"] == "ok" else "✗"
        icon_cls = "ok-icon"    if q["status"] == "ok" else "bad-icon"
        html += (
            f'<tr class="{row_cls}">'
            f'<td>{q["sheet"]}</td>'
            f'<td>{q["field"]}</td>'
            f'<td class="{icon_cls}">{icon}</td>'
            f'<td>{q["value"]}</td>'
            f'</tr>\n'
        )
    return html


# ── CSS ────────────────────────────────────────────────────────────────────────

_CSS = """
:root {
  --bg:#f6f8fa; --surface:#ffffff; --border:#e1e4e8;
  --text:#24292e; --muted:#586069; --accent:#0366d6;
  --green:#28a745; --red:#d73a49;
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);background:var(--bg);color:var(--text)}

/* Header */
.site-header{background:linear-gradient(135deg,#1a1f36 0%,#2d3561 100%);color:#fff}
.header-inner{display:flex;align-items:center;gap:20px;padding:16px 32px}
.brand-logo{font-size:22px;font-weight:700;color:#7dd3fc}
.brand-sub{font-size:12px;color:#94a3b8;margin-left:6px}
.header-meta{flex:1}
.header-title{font-size:16px;font-weight:600;color:#e2e8f0}
.header-byline{font-size:12px;color:#94a3b8;margin-top:2px}
.doi-link{color:#7dd3fc;text-decoration:none}
.doi-link:hover{text-decoration:underline}
.stats-bar{display:flex;background:rgba(0,0,0,0.25);padding:10px 32px;gap:32px}
.stat-pill{display:flex;flex-direction:column;align-items:center}
.stat-n{font-size:24px;font-weight:700;color:#f0f9ff;line-height:1.1}
.stat-label{font-size:10px;color:#94a3b8;text-transform:uppercase;letter-spacing:.07em}

/* Tabs */
.tab-nav{display:flex;background:var(--surface);border-bottom:1px solid var(--border);
  padding:0 32px;overflow-x:auto;position:sticky;top:0;z-index:10}
.tab-btn{background:none;border:none;border-bottom:3px solid transparent;
  padding:12px 16px;font-size:13px;color:var(--muted);cursor:pointer;
  white-space:nowrap;transition:color .15s,border-color .15s}
.tab-btn:hover{color:var(--text)}
.tab-btn.active{color:var(--accent);border-bottom-color:var(--accent);font-weight:600}

/* Content */
.content{padding:24px 32px;max-width:1400px;margin:0 auto}
.tab-panel{display:none}
.tab-panel.active{display:block}

/* Cards */
.card{background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:20px;margin-bottom:20px}
.card.full-width{width:100%}
.card-title{font-size:15px;font-weight:600;margin-bottom:8px}
.card-desc{font-size:13px;color:var(--muted);margin-bottom:12px}
.panel-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:900px){.panel-grid{grid-template-columns:1fr}}

/* Info table */
.info-table td{padding:4px 8px;font-size:13px;vertical-align:top}
.info-table td:first-child{color:var(--muted);font-weight:500;width:80px}

/* Abstract */
.abstract-details{margin-top:12px}
.abstract-details summary{font-size:13px;color:var(--accent);cursor:pointer}
.abstract-text{font-size:13px;color:var(--muted);margin-top:8px;line-height:1.6}

/* Experiment */
.exp-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.exp-item{display:flex;flex-direction:column}
.exp-label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em}
.exp-value{font-size:13px;color:var(--text)}

/* Badges */
.activity-badge{display:inline-block;padding:2px 8px;border-radius:10px;
  font-size:11px;font-weight:600}
.active-badge{background:#dcfce7;color:#166534}
.inactive-badge{background:#fee2e2;color:#991b1b}

/* Legend */
.legend-swatch{display:inline-block;width:12px;height:12px;border-radius:2px;vertical-align:middle}
.active-swatch{background:#86efac}
.inactive-swatch{background:#fca5a5}
.untested-swatch{background:#e5e7eb}
/* Data tables */
.table-wrap{overflow-x:auto}
.data-table{width:100%;border-collapse:collapse;font-size:13px}
.data-table th{background:var(--bg);padding:8px 12px;text-align:left;
  border-bottom:2px solid var(--border);font-weight:600;cursor:pointer;white-space:nowrap}
.data-table td{padding:7px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.data-table tr:hover td{background:#f6f8fa}

/* QC */
.qc-summary{display:flex;gap:10px;margin-bottom:16px}
.qc-pill{display:inline-block;padding:4px 14px;border-radius:12px;font-size:13px;font-weight:600}
.ok-pill{background:#dcfce7;color:#166534}
.bad-pill{background:#fee2e2;color:#991b1b}
.qc-ok-row td{background:#f0fdf4}
.qc-bad-row td{background:#fef2f2}
.ok-icon{color:#16a34a;font-weight:700;text-align:center}
.bad-icon{color:#dc2626;font-weight:700;text-align:center}

/* Controls */
.table-controls{display:flex;gap:12px;margin-bottom:12px;align-items:center}
.search-input{padding:6px 12px;border:1px solid var(--border);border-radius:6px;
  font-size:13px;width:320px}
.export-btn{padding:6px 14px;background:var(--accent);color:#fff;border:none;
  border-radius:6px;font-size:13px;cursor:pointer}
.export-btn:hover{background:#0256bb}
code{background:#f3f4f6;padding:1px 5px;border-radius:3px;font-size:12px}
"""

# ── JavaScript ─────────────────────────────────────────────────────────────────
# Note: uses ${...} template literals which are fine here as a plain string (not an f-string)

_JS = r"""
// ── Tab switching ────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const name = this.dataset.tab;
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
    this.classList.add('active');
    if (name === 'heatmap')   renderHeatmap();
    if (name === 'compounds') renderUMAP();
  });
});

// ── Heatmap ───────────────────────────────────────────────────────────
let _heatmapDone = false;
function renderHeatmap() {
  if (_heatmapDone) return;
  _heatmapDone = true;
  const d = REPORT_DATA;
  if (!d.compounds.length || !d.assays.length) {
    document.getElementById('activity-heatmap').innerHTML =
      '<p style="padding:20px;color:#888">No activity data to display.</p>';
    return;
  }
  const rowH   = 36;
  const marginT = 20, marginB = 180, marginL = 230, marginR = 30;
  const height = marginT + marginB + d.compounds.length * rowH;
  const el = document.getElementById('activity-heatmap');
  el.style.height = height + 'px';

  // Replace null with -0.5 to render as grey "not tested"
  const z = d.z_vals.map(row => row.map(v => v === null ? -0.5 : v));
  Plotly.newPlot('activity-heatmap', [{
    type: 'heatmap',
    z: z,
    x: d.assay_labels,
    y: d.compounds,
    text: d.text_vals,
    hoverinfo: 'text',
    colorscale: [
      [0.0, '#e5e7eb'],
      [0.25, '#e5e7eb'],
      [0.35, '#fca5a5'],
      [0.65, '#fca5a5'],
      [0.75, '#86efac'],
      [1.0, '#86efac'],
    ],
    zmin: -0.5, zmax: 1,
    showscale: false,
    xgap: 3, ygap: 3,
  }], {
    margin: { t: marginT, b: marginB, l: marginL, r: marginR },
    xaxis: { tickangle: -40, tickfont: { size: 11 }, automargin: true },
    yaxis: { tickfont: { size: 11 }, automargin: true },
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
  }, { responsive: true });
}

// ── UMAP ─────────────────────────────────────────────────────────────
let _umapDone = false;
function renderUMAP() {
  if (_umapDone) return;
  _umapDone = true;
  const pts = REPORT_DATA.umap_points;
  if (!pts || pts.length === 0) {
    document.getElementById('umap-plot').innerHTML =
      `<p style="padding:40px 0;text-align:center;color:#888">${REPORT_DATA.umap_message}</p>`;
    return;
  }

  const colorMap = {
    'Metabolized':     '#86efac',
    'Not metabolized': '#fca5a5',
    'Not tested':      '#e5e7eb',
  };
  const borderMap = {
    'Metabolized':     '#16a34a',
    'Not metabolized': '#dc2626',
    'Not tested':      '#9ca3af',
  };

  const statuses = ['Metabolized', 'Not metabolized', 'Not tested'];
  const traces = statuses.map(s => {
    const sub = pts.filter(p => p.status === s);
    return {
      type: 'scatter',
      mode: 'markers+text',
      name: s,
      x: sub.map(p => p.x),
      y: sub.map(p => p.y),
      text: sub.map(p => p.name),
      textposition: 'top center',
      textfont: { size: 10, color: '#374151' },
      hovertemplate: '<b>%{text}</b><br>UMAP1: %{x:.2f}<br>UMAP2: %{y:.2f}<extra>' + s + '</extra>',
      marker: {
        size: 14,
        color: colorMap[s],
        line: { color: borderMap[s], width: 1.5 },
      },
    };
  });

  Plotly.newPlot('umap-plot', traces, {
    margin: { t: 20, b: 50, l: 60, r: 20 },
    xaxis: { title: 'UMAP 1', zeroline: false, gridcolor: '#f3f4f6' },
    yaxis: { title: 'UMAP 2', zeroline: false, gridcolor: '#f3f4f6' },
    legend: { orientation: 'h', y: -0.15 },
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
  }, { responsive: true });
}

// ── Biotransformation table ──────────────────────────────────────────
let _sortCol = -1, _sortAsc = true;

function renderBioTTable(rows) {
  const tbody = document.getElementById('bioT-tbody');
  tbody.innerHTML = '';
  rows.forEach(r => {
    const iActive = r.is_active === true;
    const cls     = iActive ? 'active-badge' : 'inactive-badge';
    const label   = r.text_value || (r.value ? r.value + ' ' + r.units : '—');
    const comment = r.comment.length > 70 ? r.comment.slice(0, 68) + '…' : r.comment;
    tbody.innerHTML +=
      `<tr>
        <td>${r.compound}</td>
        <td><i>${r.organism}</i></td>
        <td><span class="activity-badge ${cls}">${label}</span></td>
        <td>${r.value ? r.value + ' ' + r.units : ''}</td>
        <td>${r.action_type}</td>
        <td>${r.reaction_type}</td>
        <td>${r.met_mz}</td>
        <td>${r.met_rt}</td>
        <td>${r.ann_level}</td>
        <td title="${r.comment}">${comment}</td>
      </tr>`;
  });
}

function filterBioT() {
  const q = document.getElementById('bioT-search').value.toLowerCase();
  const rows = REPORT_DATA.bioT_rows.filter(r =>
    r.compound.toLowerCase().includes(q)     ||
    r.organism.toLowerCase().includes(q)     ||
    r.reaction_type.toLowerCase().includes(q)||
    r.action_type.toLowerCase().includes(q)  ||
    r.text_value.toLowerCase().includes(q)
  );
  renderBioTTable(rows);
}

function sortBioT(col) {
  const keys = ['compound','organism','text_value','value','action_type','reaction_type'];
  if (_sortCol === col) _sortAsc = !_sortAsc; else { _sortCol = col; _sortAsc = true; }
  const key = keys[col];
  const rows = [...REPORT_DATA.bioT_rows].sort((a, b) => {
    const av = (a[key] || '').toLowerCase(), bv = (b[key] || '').toLowerCase();
    return _sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
  });
  renderBioTTable(rows);
}

function exportBioT() {
  const cols = ['compound','organism','text_value','value','units','action_type',
                'reaction_type','met_mz','met_rt','ann_level','comment'];
  let csv = cols.join(',') + '\n';
  REPORT_DATA.bioT_rows.forEach(r => {
    csv += cols.map(c => '"' + (r[c] || '').replace(/"/g, '""') + '"').join(',') + '\n';
  });
  const a = document.createElement('a');
  a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
  a.download = 'biotransformation_data.csv';
  a.click();
}

// ── Init ─────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderHeatmap();
  renderBioTTable(REPORT_DATA.bioT_rows);
});
"""


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate interactive HTML report from MIX-MB Template_open.ods",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input",   required=True, help="Path to Template_open.ods")
    parser.add_argument("--outdir",  default=".",   help="Output directory")
    parser.add_argument(
        "--no-embed-js", action="store_true",
        help="Use CDN links instead of embedding JS (smaller file, needs internet to render)",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit non-zero if QC issues are found",
    )
    args = parser.parse_args()

    ods_path = Path(args.input)
    outdir   = Path(args.outdir)

    if not ods_path.exists():
        sys.exit(f"ERROR: input file not found: {ods_path}")

    outdir.mkdir(parents=True, exist_ok=True)

    print("Reading template sheets...")
    try:
        ref_df     = _read_sheet(ods_path, "Reference")
        chem_df    = _read_sheet(ods_path, "Chemicals")
        microbes_df= _read_sheet(ods_path, "Microbes")
        exp_df     = _read_sheet(ods_path, "Experiment")
        bioT_df    = _read_sheet(ods_path, "Biotransformation")
    except Exception as exc:
        sys.exit(f"ERROR reading ODS: {exc}")

    # Fetch JS libraries
    plotly_js = None
    if not args.no_embed_js:
        print("Fetching JS libraries for self-contained output...")
        plotly_js = _fetch_js(_PLOTLY_CDN, "Plotly.js")
        if not plotly_js:
            print("  [WARN] Plotly could not be fetched — falling back to CDN link.")

    print("Building report...")
    html = build_html(ref_df, chem_df, microbes_df, exp_df, bioT_df,
                      plotly_js)

    out_path = outdir / "report.html"
    out_path.write_text(html, encoding="utf-8")
    size_kb = out_path.stat().st_size // 1024
    print(f"Written: {out_path} ({size_kb} KB)")

    qc_data = _build_qc(ref_df, chem_df, microbes_df, bioT_df)
    issues  = [q for q in qc_data if q["status"] != "ok"]
    if issues:
        print(f"[WARN] {len(issues)} QC issue(s) found:")
        for q in issues:
            print(f"  {q['sheet']} · {q['field']}: {q['status']}")
        if args.strict:
            sys.exit(1)

    print(f"[SUCCESS] Report ready → {out_path}")


if __name__ == "__main__":
    main()
