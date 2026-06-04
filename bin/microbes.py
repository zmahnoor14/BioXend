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

Auto-generated AIDX naming convention:
  [ASSAY_SOURCE_]ORGANISM[_STRAIN|_community]_Biotransformation[_ACCESSION|_TARGET_NAME]

Usage:
    python bin/microbes.py \\
        --input   Standards/Templates/Template_open.ods \\
        --ridx    GutMeta \\
        --xenobiotic_class drug \\   # singular form: 'drug' not 'drugs', this will be used in ASSAY_DESCRIPTION sentences.
        --outdir  results/
"""

import argparse
import re
import sys
from pathlib import Path

import odf
import pandas as pd
import requests

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
    "ASSAY_TAX_ID",               
    "ASSAY_SOURCE",                
    "ASSAY_TISSUE",                
    "ASSAY_CELL_TYPE",             
    "ASSAY_SUBCELLULAR_FRACTION",  
    "TARGET_TYPE",
    "TARGET_NAME",
    "TARGET_ACCESSION",
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

# UniProt accession format (both canonical forms, uppercase only):
#   Old (SwissProt, 6 chars): [OPQ][0-9][A-Z0-9]{3}[0-9]          e.g. P0A6Y8
#   New (TrEMBL, 6 or 10 chars): [A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}  e.g. A2BC19, A0A023GPI8
_UNIPROT_ACCESSION_RE = re.compile(
    r"^([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$"
)
VALID_TARGET_TYPES = {
    "3D CELL CULTURE", "ADMET", "CELL-LINE", "CHIMERIC PROTEIN",
    "LIPID", "MACROMOLECULE", "METAL", "MOLECULAR", "NO TARGET", "NON-MOLECULAR", "NUCLEIC-ACID",
    "OLIGOSACCHARIDE", "ORGANISM", "PHENOTYPE", "PROTEIN", "PROTEIN COMPLEX", "PROTEIN COMPLEX GROUP",
    "PROTEIN FAMILY", "PROTEIN NUCLEIC-ACID COMPLEX", "PROTEIN-PROTEIN INTERACTION",
    "SELECTIVITY GROUP", "SINGLE PROTEIN", "SMALL MOLECULE", "SUBCELLULAR", "TISSUE",
    "UNCHECKED", "UNDEFINED", "UNKNOWN",
}

# Template sheet row offsets (0-based, read with header=None)
#   row 0 — section group headers  (skip)
#   row 1 — column names           (use as header)
#   row 2 — data types             (skip)
#   row 3 — field descriptions     (skip)
#   row 4+ — data rows
_ROW_COLNAMES   = 1
_ROW_DATA_START = 4


# ---------------------------------------------------------------------------
# UniProt lookup — protein name, organism, TaxID from accession
# ---------------------------------------------------------------------------

_UNIPROT_API = "https://rest.uniprot.org/uniprotkb"

_uniprot_cache: dict[str, dict] = {}


def _uniprot_lookup(accession: str) -> dict:
    """Fetch TARGET metadata from UniProt by accession number.

    Returns a dict with keys 'name', 'organism', 'taxid' (all strings).
    Empty strings are returned for any field that cannot be resolved.
    Results are cached per accession for the run lifetime.

    Fields resolved:
      proteinDescription.recommendedName.fullName.value → name
        (falls back to uniProtkbId, e.g. 'DNAK_ECOLI', when absent)
      organism.scientificName                           → organism
      organism.taxonId                                  → taxid
        (strain-level TaxID, e.g. 83333 for E. coli K12, not just 562)
    """
    empty: dict = {"name": "", "organism": "", "taxid": ""}
    if not accession:
        return empty
    if accession in _uniprot_cache:
        return _uniprot_cache[accession]

    result = dict(empty)
    try:
        resp = requests.get(
            f"{_UNIPROT_API}/{requests.utils.quote(accession)}.json",
            timeout=15,
        )
        if resp.status_code == 404:
            print(
                f"[WARN] UniProt accession '{accession}' not found.",
                file=sys.stderr,
            )
            _uniprot_cache[accession] = result
            return result
        resp.raise_for_status()
        data = resp.json()

        # Protein name: recommended name, else entry ID
        rec_name = (
            data.get("proteinDescription", {})
                .get("recommendedName", {})
                .get("fullName", {})
                .get("value", "")
        )
        result["name"] = rec_name or data.get("uniProtkbId", "")

        # Organism name and TaxID
        organism = data.get("organism", {})
        result["organism"] = organism.get("scientificName", "")
        taxid = organism.get("taxonId")
        result["taxid"] = str(taxid) if taxid else ""

        filled = [k for k, v in result.items() if v]
        print(
            f"[INFO] UniProt '{accession}': resolved {', '.join(filled)}.",
            file=sys.stderr,
        )

    except requests.exceptions.RequestException as exc:
        print(
            f"[WARN] UniProt lookup failed for '{accession}': {exc}",
            file=sys.stderr,
        )

    _uniprot_cache[accession] = result
    return result


# ---------------------------------------------------------------------------
# TaxID lookup — StrainInfo (DSMZ) and NCBI Taxonomy 
# ---------------------------------------------------------------------------

_STRAININFO_API   = "https://api.straininfo.dsmz.de"
_NCBI_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# Culture collection accession pattern: 2–5 uppercase letters + optional space + digits
# e.g. DSM 2840, ATCC 11775, NCTC 10537, LMG 2093
_ACCESSION_RE = re.compile(r'^[A-Z]{2,5}\s*\d+', re.ASCII)

_taxid_cache: dict[str, str] = {}


def _looks_like_accession(strain: str) -> bool:
    """Return True when strain resembles a culture collection accession number."""
    return bool(_ACCESSION_RE.match(strain.strip()))


def _straininfo_by_accession(accession: str) -> str:
    """Resolve NCBI TaxID from a culture collection accession number via StrainInfo.

    StrainInfo (https://straininfo.dsmz.de) links accession numbers from
    culture collections (DSM, ATCC, NCTC, LMG, …) to taxonomy.  This is
    its core use case: a strain number → species TaxID.

    Uses the v2 API (two calls):
      1. GET /v2/search/deposit/cc_no/{accession}  → list of siDP integers
      2. GET /v2/data/deposit/min/{siDP}            → deposit record with taxon.ncbi
    """
    try:
        search_resp = requests.get(
            f"{_STRAININFO_API}/v2/search/deposit/cc_no/"
            f"{requests.utils.quote(accession)}",
            timeout=15,
        )
        if search_resp.status_code == 404:
            return ""
        search_resp.raise_for_status()
        si_dp_ids = search_resp.json()
        if not si_dp_ids or not isinstance(si_dp_ids, list):
            return ""

        detail_resp = requests.get(
            f"{_STRAININFO_API}/v2/data/deposit/min/{si_dp_ids[0]}",
            timeout=15,
        )
        detail_resp.raise_for_status()
        records = detail_resp.json()
        record = records[0] if isinstance(records, list) and records else records
        taxid = str(
            (record.get("deposit") or {}).get("taxon", {}).get("ncbi") or ""
        ).strip()
        return taxid if taxid and taxid != "0" else ""

    except requests.exceptions.RequestException as exc:
        print(
            f"[WARN] StrainInfo accession lookup failed for '{accession}': {exc}",
            file=sys.stderr,
        )
    return ""


def _ncbi_taxid(organism: str) -> str:
    """Resolve NCBI TaxID from a species name via NCBI Taxonomy esearch.

    NCBI Taxonomy is the authoritative source for TaxIDs.  This is the
    primary lookup path for organism names.
    """
    try:
        resp = requests.get(
            _NCBI_ESEARCH_URL,
            params={
                "db": "taxonomy",
                "term": organism,
                "retmode": "json",
                "retmax": 1,
            },
            timeout=15,
        )
        resp.raise_for_status()
        ids = resp.json().get("esearchresult", {}).get("idlist", [])
        if ids:
            return str(ids[0])
    except requests.exceptions.RequestException as exc:
        print(
            f"[WARN] NCBI taxonomy lookup failed for '{organism}': {exc}",
            file=sys.stderr,
        )
    return ""


def lookup_taxid(organism: str, strain: str = "") -> str:
    """Return NCBI TaxID for *organism* / *strain*.

    Resolution order:
      1. If *strain* looks like a culture collection accession (e.g. DSM 2840,
         ATCC 11775) → StrainInfo deposit lookup.  This is StrainInfo's primary
         use case: mapping strain accession numbers to taxonomy.
      2. NCBI Taxonomy esearch by *organism* name.  NCBI is the authoritative
         source for TaxIDs and handles species names, metagenomes, and
         reclassified taxa.

    Results are cached per (organism, strain) pair for the run lifetime.
    Returns '' when both sources fail.
    """
    if not organism:
        return ""
    cache_key = f"{organism}\t{strain}"
    if cache_key in _taxid_cache:
        return _taxid_cache[cache_key]

    taxid  = ""
    source = ""

    if strain and _looks_like_accession(strain):
        taxid  = _straininfo_by_accession(strain)
        source = "StrainInfo"

    if not taxid:
        taxid  = _ncbi_taxid(organism)
        source = "NCBI"

    label = f"'{organism}'" + (f" strain '{strain}'" if strain else "")
    if taxid:
        print(f"[INFO] TaxID '{taxid}' resolved for {label} via {source}.",
              file=sys.stderr)
    else:
        print(f"[WARN] Could not resolve TaxID for {label}. "
              "Fill ASSAY_TAX_ID manually.", file=sys.stderr)

    _taxid_cache[cache_key] = taxid
    return taxid


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
      Instrument_for_measurement
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
      The {xenobiotic_class} is tested with {organism} strain {strain} for
      biotransformation. The {xenobiotic_class} is measured with
      {instrument}, over {n} time points, between {t_min} to {t_max}
      {unit}, over following condition: {oxygen}.

    Community template (triggered when 'metagenome' is in organism name):
      The {xenobiotic_class} is tested with {organism} community with study
      accession number {ENA_project} and sample accession number
      {ENA_sample} for biotransformation. The {xenobiotic_class} is
      measured with {instrument}, over {n} time points, between {t_min}
      to {t_max} {unit}, over following condition: {oxygen}.

    Fields that are empty are omitted gracefully.
    """
    xeno     = xenobiotic_class.strip() if xenobiotic_class else "xenobiotic compound"
    organism = str(microbe_row.get("ASSAY_ORGANISM") or "").strip()
    strain   = str(microbe_row.get("ASSAY_STRAIN") or "").strip()
    ena_proj = str(microbe_row.get("ENAorSRA_project_Accession_number") or "").strip()
    ena_samp = str(microbe_row.get("ENAorSRA_sample_Accession_number") or "").strip()

    # Experimental context (may be absent)
    if exp_row is not None:
        instrument   = str(exp_row.get("Instrument_for_measurement") or "").strip()
        timecourse   = str(exp_row.get(
            "Time-course information (i.e., number of timepoints)") or "").strip()
        time_unit    = str(exp_row.get("Time_unit") or "").strip()
        oxygen       = str(exp_row.get("Oxygen conditions") or "").strip()
    else:
        instrument = timecourse = time_unit = oxygen = ""

    n_tp, t_min, t_max = _parse_timecourse(timecourse)

    is_community = "metagenome" in organism.lower()

    # Sentence 1: 
    if is_community:
        s1 = f"The {xeno} is tested with {organism} community"
        if ena_proj:
            s1 += f" with study accession number {ena_proj}"
        if ena_samp:
            s1 += f" and sample accession number {ena_samp}"
        s1 += " for biotransformation."
    else:
        s1 = f"The {xeno} is tested with {organism}"
        if strain:
            s1 += f" strain {strain}"
        s1 += " for biotransformation."

    # Sentence 2:
    parts2 = [f"The {xeno} is measured"]
    if instrument:
        parts2.append(f"with {instrument}")
    if n_tp:
        parts2.append(f"over {n_tp} time points")
        if t_min and t_max:
            unit_str = f" {time_unit}" if time_unit else ""
            parts2.append(f"between {t_min} to {t_max}{unit_str}")
    if oxygen:
        parts2.append(f"over following condition: {oxygen}")

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
    taxid_lookup: bool = True,
) -> "tuple[pd.DataFrame, dict[str, str]]":
    """
    Build the ASSAY.tsv records from the Microbes sheet DataFrame.

    Returns (assay_df, aidx_map).

    aidx_map maps each user-provided AIDX key (from the template assay_identifier column,
    e.g. 'assay1') to the pipeline-generated ChEMBL AIDX (e.g.
    'Zimmermann_gut_metagenome_community_Biotransformation').  This map is
    written to ASSAY_MAPPING.tsv so that experiment.py and biotransformation.py can resolve
    Biotransformation-sheet ASSAY_Identifier values to the proper AIDX —
    exactly as COMPOUND_RECORD.tsv lets biotransformation.py resolve
    Common_Name to CIDX.

    The assay_identifier column in the template is the user's short cross-reference key.
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
        target_type      = str(row.get("TARGET_TYPE") or "").strip().upper()
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

        # UniProt: fill blank TARGET_NAME / TARGET_ORGANISM / TARGET_TAX_ID
        # from TARGET_ACCESSION.  Runs before the StrainInfo/NCBI fallback so
        # UniProt's strain-level TaxID takes priority when available.
        if target_accession and taxid_lookup:
            needs = not target_name or not target_organism or not target_tax_id
            if needs:
                uni = _uniprot_lookup(target_accession)
                if not target_name and uni["name"]:
                    target_name = uni["name"]
                if not target_organism and uni["organism"]:
                    target_organism = uni["organism"]
                if not target_tax_id and uni["taxid"]:
                    target_tax_id = uni["taxid"]

        # StrainInfo / NCBI fallback: only runs if TARGET_TAX_ID is still blank
        if not target_tax_id and taxid_lookup and target_organism:
            target_tax_id = lookup_taxid(target_organism)

        # AIDX
        user_key = str(row.get("assay_identifier") or "").strip()
        if not user_key:
            # Fallback key so Biotransformation sheet rows can still reference
            # this assay even when the template assay_identifier column was left blank.
            user_key = f"assay{len(aidx_map) + 1}"

        base  = _make_aidx(organism, strain, assay_source, target_name, target_accession)
        count = aidx_counter.get(base, 0) + 1
        aidx_counter[base] = count
        aidx = base if count == 1 else f"{base}_{count}"

        aidx_map[user_key] = aidx

        # ASSAY_TYPE
        raw_type   = str(row.get("ASSAY_TYPE") or "").strip().upper()
        assay_type = raw_type[0] if raw_type else ""

        # ASSAY_TAX_ID
        raw_tax = row.get("ASSAY_TAX_ID")
        if raw_tax == "" or raw_tax is None:
            assay_tax_id = ""
        else:
            try:
                assay_tax_id = str(int(float(str(raw_tax))))
            except (ValueError, TypeError):
                assay_tax_id = str(raw_tax).strip()

        if not assay_tax_id and taxid_lookup and organism:
            assay_tax_id = lookup_taxid(organism, strain)

        # --- Join Experiment row for this assay ---
        # Experiment sheet identifiers are user short keys (e.g. 'assay1'),
        # not the generated ChEMBL AIDXs, so look up by user_key.
        exp_row = _get_experiment_for_assay(exp_df, user_key)

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

        target_type = str(row.get("TARGET_TYPE") or "").strip().upper()
        if target_type and target_type not in VALID_TARGET_TYPES:
            errors.append(
                f"{label}: TARGET_TYPE '{target_type}' not in "
                f"{sorted(VALID_TARGET_TYPES)}."
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

        # TARGET_ACCESSION format check (when non-empty)
        target_acc = str(row.get("TARGET_ACCESSION") or "").strip()
        if target_acc and not _UNIPROT_ACCESSION_RE.match(target_acc):
            errors.append(
                f"{label}: TARGET_ACCESSION '{target_acc}' is not a valid UniProt "
                f"accession format (expected e.g. 'P0A6Y8' or 'A0A023GPI8')."
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
    parser.add_argument(
        "--no_taxid_lookup", action="store_true",
        help=(
            "Skip all remote metadata lookups (UniProt, StrainInfo, NCBI). "
            "Blank ASSAY_TAX_ID, TARGET_TAX_ID, TARGET_NAME, and "
            "TARGET_ORGANISM fields will remain empty."
        ),
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
        taxid_lookup=not args.no_taxid_lookup,
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
 
    mapping_path = outdir / "ASSAY_MAPPING.tsv"
    pd.DataFrame(
        list(aidx_map.items()), columns=["assay_identifier", "AIDX"]
    ).to_csv(mapping_path, sep="\t", index=False)
    print(f"Written: {mapping_path}")

    print(f"[SUCCESS] {len(assay_df)} assay(s) written.")


if __name__ == "__main__":
    main()
