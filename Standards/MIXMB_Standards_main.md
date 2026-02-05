# Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB)

**MIX-MB Standard Version:** 0.1  
**Release Date:** February 5, 2026 (Draft)  
**Status:** Draft Standard  
**DOI:** 10.5281/zenodo.XXXXXXX (to be assigned upon stable release)

---
The standards follow overall important information necessary for xenobiotics-microbiome biotransformations -- together with ChEMBL comptabible submission checklist.

## Component Standards

This standard comprises three interconnected sub-standards:

| Component | Version | Status | Last Updated | Document |
|-----------|---------|--------|--------------|----------|
| **MIX-MB(X)** - Xenobiotics | 0.1.0 | Draft | 2026-02-05 | [MIXMB_Xenobiotics.md](MIXMB_Xenobiotics.md) |
| **MIX-MB(M)** - Microbes | 0.1.0 | Draft | 2026-02-05 | [MIXMB_Microbes.md](MIXMB_Microbes.md) |
| **MIX-MB(B)** - Biotransformation | 0.1.0 | Draft | 2026-02-05 | [MIXMB_Biotransformation.md](MIXMB_Biotransformation.md) |

---

## Version Compatibility Matrix

| MIX-MB Version | MIX-MB(X) | MIX-MB(M) | MIX-MB(B) | Release Date | Status | Notes |
|----------------|-----------|-----------|-----------|--------------|--------|-------|
| 0.1 | 0.1.0 | 0.1.0 | 0.1.0 | 2026-02-05 | Draft | Initial draft for community review |
| 1.0 | 1.0.0 | 1.0.0 | 1.0.0 | TBD | Planned | First stable release |
| 1.1 | 1.0.0+ | 1.1.0+ | 1.0.0+ | Planned | Future | Updated microbe cultivation standards |
| 2.0 | 2.0.0 | 2.0.0 | 2.0.0 | Planned | Future | Major update: all components revised |

**Legend:**
- **Draft:** Pre-release, breaking changes expected
- **Planned:** Future release
- **+** symbol: Indicates forward compatibility (e.g., 1.0.0+ means 1.0.0 or higher)

---

## Version History

### Version 0.1 (2026-02-05) - Draft

**Status:** Draft Standard (Pre-release, breaking changes expected)

**Component Versions:**
- MIX-MB(X) v0.1.0
- MIX-MB(M) v0.1.0  
- MIX-MB(B) v0.1.0

**Draft Notes:**
- Initial draft of MIX-MB standards for community review
- Comprehensive coverage of xenobiotics, microbes, and biotransformation processes
- Alignment with ChEMBL, MSI, MIxS, and FAIR principles
- Complete Bioschemas integration
- Extensive ontology support (ChEBI, ChemOnt, BAO, GO, ENVO)
- Detailed data format specifications for ChEMBL submission

---

## REFERENCE.tsv
**Associated data to be filled within the template.**
For details please refer to the tutorial provided by ChEMBL on how to generate (REFERENCE.tsv file)[https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/reference.tsv]. 

## COMPOUND_RECORD.tsv
**Associated data to be provided as a CSV file.**
For details please refer to the tutorial provided by ChEMBL on how to generate (COMPOUND_RECORD.tsv file)[https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/compound_record.tsv].

To ensure your data is clear and traceable, we require a **CSV (Comma Separated Values) file** containing information about the chemical compounds used in your study. 

### Required and Optional Columns

Your CSV file must include the following columns:

| Column Name | Requirement | Description | Purpose |
| :--- | :--- | :--- | :--- |
| **SMILES** | **Required** | The **Simplified Molecular-Input Line-Entry System (SMILES)** string for the compound. This is the standardized, text-based way to represent the molecular structure. | Ensures **unambiguous** identification of the chemical structure. |
| **Names** | **Required** | The most **common or accepted name** of the chemical compound (e.g., *Acetaminophen*, *Propoxur*, *Propochlor*). | Provides a **standard, recognizable identifier** for the compound. |
| **Study\_ID** | **Optional** | A **unique identifier, synonym, or code** that you used to refer to this specific compound *within your own study or reference materials* (e.g., *prop\_1*, *Comp-A*, *Ref\_ID\_45*). | Crucial for **traceability**. If a user of your data wants to cross-reference a compound mentioned in your original paper (e.g., finding the structure for "prop\_1" in your study), they can easily do so. |

---

### Example CSV File Structure

Please provide a CSV file that looks like the following example.

| SMILES | Names | Study_ID |
| :--- | :--- | :--- |
| $\text{CCC(C)Nc1ccc(Cl)c(OC)c1}$ | Propochlor | prop\_1 |
| $\text{CC(=O)Nc1ccc(O)cc1}$ | Acetaminophen | APAP |
| $\text{COc1ccc(NC(C)=O)cc1}$ | Phenacetin | Compound-B |

**CSV File Content (To be saved as a .csv file):**
```csv
SMILES,Names,Study_ID
CCC(C)Nc1ccc(Cl)c(OC)c1,Propochlor,prop_1
CC(=O)Nc1ccc(O)cc1,Acetaminophen,APAP
COc1ccc(NC(C)=O)cc1,Phenacetin,Compound-B
```
// Note: ChEMBL requires a chemical stucture for submission, hence empty SMILES would not be ideal.

## COMPOUND_CTAB.sdf
For details please refer to the tutorial provided by ChEMBL on how to generate (COMPOUND_CTAB.sdf file)[https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/compound_ctab.sdf]
The COMPOUND_CTAB.sdf is based on COMPOUND_RECORD

## ASSAY.tsv



## 7. Controlled Vocabularies not defined by any ontologies?

### 7.1 Transformation Types

Use standardized terms:
- `hydroxylation` - Addition of hydroxyl group
- `reduction` - Reduction reaction
- `oxidation` - Oxidation reaction
- `hydrolysis` - Hydrolytic cleavage
- `decarboxylation` - Loss of CO₂
- `deamination` - Loss of amino group
- `conjugation` - Addition of molecular moiety
- `demethylation` - Loss of methyl group
- `acetylation` - Addition of acetyl group
- `glucuronidation` - Addition of glucuronic acid
- `sulfation` - Addition of sulfate group

### 7.2 Assay Types

- `cell-based assay` - Whole cell biotransformation
- `lysate assay` - Cell-free lysate system
- `purified enzyme assay` - Isolated enzyme
- `community assay` - Mixed microbial community
- `in vivo assay` - Animal model
- `ex vivo assay` - Extracted sample

### 7.3 Activity Outcomes

- `Substrate` - Compound consumed by microorganism
- `Product` - Compound produced by transformation
- `No Activity` - No biotransformation detected
- `Inhibition` - Transformation inhibited
- `Stimulation` - Transformation enhanced

### 5.1 ChEMBL Submission Format

**Required Files:**

#### 5.1.1 REFERENCE.tsv
Publication metadata following ChEMBL specifications:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| RIDX | Yes | String | Reference identifier |
| DOI | Yes | String | Digital Object Identifier |
| TITLE | Yes | String | Publication title |
| AUTHORS | Yes | String | Author list |
| ABSTRACT | Yes | String | Publication abstract |
| YEAR | Yes | Integer | Publication year |
| JOURNAL_NAME | No | String | Journal name |
| VOLUME | No | String | Volume number |
| REF_TYPE | Yes | String | Publication, Patent, Dataset, Book |
| DATA_LICENCE | No | String | Data license (e.g., CC0, CC-BY) |

#### 5.1.2 COMPOUND_RECORD.tsv
Compound information:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| CIDX | Yes | String | Compound index |
| COMPOUND_NAME | Yes | String | Preferred compound name |
| RIDX | Yes | String | Reference identifier |
| COMPOUND_KEY | No | String | Unique compound key |
| SRC_ID | No | String | Source database ID |

#### 5.1.3 COMPOUND_CTAB.sdf
MOL/SDF file containing chemical structures in CTAB format.

**Requirements:**
- Canonical SMILES
- 2D or 3D coordinates
- InChI and InChI Key
- Associated CIDX for linkage

#### 5.1.4 ASSAY.tsv
Biotransformation assay description:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| AIDX | Yes | String | Assay identifier |
| DESCRIPTION | Yes | String | Assay description |
| ASSAY_TYPE | Yes | String | Biotransformation/Metabolism |
| ASSAY_ORGANISM | Yes | String | Microorganism name |
| ASSAY_TAX_ID | Yes | Integer | NCBI Taxonomy ID |
| ASSAY_STRAIN | No | String | Strain designation |
| ASSAY_CELL_TYPE | No | String | Cell type/compartment |
| RIDX | Yes | String | Reference identifier |

#### 5.1.5 ASSAY_PARAM.tsv
Experimental parameters:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| AIDX | Yes | String | Assay identifier |
| TYPE | Yes | String | Parameter type |
| RELATION | No | String | =, <, >, ~, etc. |
| VALUE | Yes | Numeric | Parameter value |
| UNITS | No | String | Unit of measurement |
| TEXT_VALUE | No | String | Qualitative description |
| COMMENTS | No | String | Additional notes |

**Common Parameters:**
- Temperature (°C)
- Incubation time (hours)
- pH
- Cell density (OD600, CFU/mL)
- Substrate concentration (µM, mM)

#### 5.1.6 ACTIVITY.tsv
Biotransformation activity data:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| CIDX | Yes | String | Compound identifier |
| AIDX | Yes | String | Assay identifier |
| RIDX | Yes | String | Reference identifier |
| TEXT_VALUE | No | String | Qualitative result |
| RELATION | No | String | =, <, >, ~ |
| VALUE | No | Numeric | Quantitative value |
| UNITS | No | String | Unit of measurement |
| TYPE | Yes | String | Activity type |
| ACTION_TYPE | No | String | SUBSTRATE, PRODUCT, etc. |
| ACTIVITY_COMMENT | No | String | Notes on activity |

**Activity Types for Biotransformation:**
- `Biotransformation` - General transformation
- `Metabolism` - Metabolic conversion
- `Substrate` - Compound consumed
- `Product` - Compound produced
- `Inhibition` - Transformation inhibited
## 10. Example Complete Record

```yaml
# MIX-MB(X) Compliant Record

# Reference Information
reference:
  ridx: "HumanMicrobiome_DrugMetabolism_2019"
  doi: "10.1038/s41586-019-1291-3"
  title: "Mapping human microbiome drug metabolism by gut bacteria and their genes"
  authors: "Zimmermann M, Zimmermann-Kogadeeva M, Wegmann R, Goodman AL"
  year: 2019
  journal: "Nature"
  ref_type: "Publication"
  data_licence: "CC-BY-4.0"

# Compound Information
compound:
  cidx: "C001"
  compound_name: "Ibuprofen"
  chembl_id: "CHEMBL1201246"
  inchi_key: "HEFNNWSXXWATRW-UHFFFAOYSA-N"
  smiles: "CC(C)Cc1ccc(cc1)C(C)C(=O)O"
  molecular_formula: "C13H18O2"
  molecular_weight: 206.28
  chebi_id: "CHEBI:5855"
  chebi_role: ["xenobiotic", "non-steroidal anti-inflammatory drug"]
  classyfire:
    kingdom: "Organic compounds"
    superclass: "Benzenoids"
    class: "Benzene and substituted derivatives"

# Microorganism Information
organism:
  assay_organism: "Clostridium sporogenes"
  ncbi_taxid: 1509
  strain: "ATCC 15579"
  assay_tax_id: 1509

# Assay Information
assay:
  aidx: "A001_Csporogenes_ATCC15579"
  description: "Biotransformation of ibuprofen by Clostridium sporogenes"
  assay_type: "Biotransformation"
  assay_cell_type: "whole cell"
  
# Experimental Conditions
parameters:
  - type: "Temperature"
    value: 37
    units: "°C"
  - type: "Incubation time"
    value: 24
    units: "hours"
  - type: "pH"
    value: 7.0
    units: "pH"
  - type: "Substrate concentration"
    value: 100
    units: "µM"
  - type: "Cell density"
    value: 0.8
    units: "OD600"

# Growth Conditions
growth_conditions:
  medium: "BHI (Brain Heart Infusion)"
  atmosphere: "anaerobic"
  growth_phase: "stationary"

# Analytical Method
analytical_method:
  platform: "LC-MS/MS"
  instrument: "Thermo Q Exactive Plus Orbitrap"
  ionization: "ESI negative mode"
  column: "Waters Acquity UPLC BEH C18"
  
# Activity Data
activity:
  cidx: "C001"
  aidx: "A001_Csporogenes_ATCC15579"
  ridx: "HumanMicrobiome_DrugMetabolism_2019"
  type: "Biotransformation"
  action_type: "SUBSTRATE"
  text_value: "Compound metabolized"
  transformation_type: "reduction"
  biological_replicates: 3
  technical_replicates: 2

# Product Information
product:
  cidx: "P001"
  compound_name: "2-(4-isobutylphenyl)propionic acid (reduced)"
  identification_level: "Level 2"
  ms2_match: "HMDB library"
  confidence: "High"

# Data Quality
quality_tier: "Gold Standard"
validation_status: "Passed"
```

---