# Minimum Information about Xenobiotics-Microbiome Biotransformation -- MIX-MB(B)
## Biotransformation Process Standards

This document identifies Minimum Information (MI) required to report the biotransformation process between microorganisms and xenobiotic compounds. MIX-MB(B) bridges MIX-MB(X) (xenobiotics) and MIX-MB(M) (microbes) by defining standards for the experimental assays, measurements, and outcomes.

**Author:** Mahnoor Zulfiqar
**Version:** 0.1.0
**Release Date:** February 5, 2026 (Draft)
**Status:** Draft Standard  
**Part of:** MIX-MB Standard v0.1  
**Replaces:** N/A  
**Compatible with:** 
- MIX-MB(X) v0.1.0
- MIX-MB(M) v0.1.0

**Breaking Changes:** N/A  
**Alignment:** ChEMBL, BioAssay Ontology (BAO), STRENDA, MIAME, FAIR principles

---

## Table of Contents

- [1. Overview](#1-overview)
  - [1.1 How is this document organised?](#11-how-is-this-document-organised)
  - [1.2 Which sections are important for contributors?](#12-which-sections-are-important-for-contributors)
  - [1.3 Which sections are important for data submitters?](#13-which-sections-are-important-for-data-submitters)
  - [1.4 Identifiers and Cross-Referencing](#14-identifiers-and-cross-referencing)
- [2. Bioschemas](#2-bioschemas)
  - [2.1 Study Profile](#21-study-profile)
  - [2.2 LabProtocol Profile](#22-labprotocol-profile)
  - [2.3 Dataset Profile](#23-dataset-profile)
- [3. Ontologies](#3-ontologies)
  - [3.1 BioAssay Ontology (BAO)](#31-bioassay-ontology-bao)
  - [3.2 Gene Ontology (GO) — Biological Process](#32-gene-ontology-go---biological-process)
  - [3.3 Chemical Methods Ontology (CHMO)](#33-chemical-methods-ontology-chmo)
  - [3.4 Reaction Types Ontology](#34-reaction-types-ontology)
- [4. Assay Design and Experimental Setup](#4-assay-design-and-experimental-setup)
  - [4.1 Assay Type Classification](#41-assay-type-classification)
  - [4.2 Required Assay Information](#42-required-assay-information)
  - [4.3 Substrate Preparation](#43-substrate-preparation)
  - [4.4 Cell/Enzyme Preparation](#44-cellenzyme-preparation)
  - [4.5 Reaction Setup](#45-reaction-setup)
  - [4.6 Sampling and Quenching](#46-sampling-and-quenching)
- [5. Analytical Methods and Detection](#5-analytical-methods-and-detection)
  - [5.1 LC-MS/MS Method](#51-lc-msms-method)
  - [5.2 Data Processing](#52-data-processing)
  - [5.3 Quality Control](#53-quality-control)
- [6. Activity Measurements and Outcomes](#6-activity-measurements-and-outcomes)
  - [6.1 Activity Types](#61-activity-types)
  - [6.2 Quantitative Measurements](#62-quantitative-measurements)
  - [6.3 Dose-Response Data](#63-dose-response-data)
  - [6.4 Time-Course Data](#64-time-course-data)
- [7. Product Characterization](#7-product-characterization)
  - [7.1 Metabolite Identification](#71-metabolite-identification)
  - [7.2 Structural Characterization](#72-structural-characterization)
  - [7.3 Transformation Pathway](#73-transformation-pathway)
- [8. Data Formats — ACTIVITY.tsv](#8-data-formats---activitytsv)
  - [8.1 MIX-MB(B) Activity Template (Template.xlsx — Activity Sheet)](#81-mix-mbb-activity-template-templatexlsx--activity-sheet)
  - [8.2 ChEMBL ACTIVITY.tsv Mapping](#82-chembl-activitytsv-mapping)
  - [8.3 Controlled Vocabularies for Activity Fields](#83-controlled-vocabularies-for-activity-fields)
  - [8.4 Example Template Rows](#84-example-template-rows)
- [9. Controls and Validation](#9-controls-and-validation)
  - [9.1 Required Controls](#91-required-controls)
  - [9.2 Quality Assurance](#92-quality-assurance)
- [10. Statistical Analysis](#10-statistical-analysis)
  - [10.1 Required Statistical Information](#101-required-statistical-information)
  - [10.2 Data Visualization Requirements](#102-data-visualization-requirements)
- [11. Data Quality Tiers](#11-data-quality-tiers)
- [12. Example Complete Record](#12-example-complete-record)
- [13. Integration with Other Standards](#13-integration-with-other-standards)
- [15. Version History](#15-version-history)
- [16. References](#16-references)
- [17. Contact and Contributions](#17-contact-and-contributions)

---


## 1. Overview

MIX-MB(B) establishes minimum information standards for documenting biotransformation experiments where microorganisms metabolize xenobiotic compounds. This standard ensures:

- **Reproducibility:** Complete experimental protocols and conditions
- **Comparability:** Standardized measurements and reporting
- **Traceability:** Links between substrates, organisms, and products
- **Quality:** Validation and quality control measures

This standard covers in vitro biotransformation assays (whole cells, lysates, purified enzymes), ex vivo studies, in situ community-level measurements, time-course experiments, dose-response studies, and product identification. It bridges MIX-MB(X) (xenobiotics) and MIX-MB(M) (microbes):

```
MIX-MB(X)              MIX-MB(B)              MIX-MB(M)
[Xenobiotics] -----> [Biotransformation] <----- [Microbes]
   Substrate              Process               Organism
   Product               Assay                  Enzyme
   Structure             Activity               Strain
```

### 1.1 How is this document organised?

- **Section 1** — Introduction to MIX-MB(B): scope, relationship to MIX-MB(X) and MIX-MB(M), and how to use this document.
- **Section 2** — Bioschemas profiles: structured metadata for the experimental study, assay protocol, and activity datasets.
- **Section 3** — Ontologies: BAO for assay classification, GO for biological processes and molecular functions, CHMO for analytical techniques, and reaction type classification.
- **Section 4** — Assay design and experimental setup: how to classify assay types, document substrate and cell/enzyme preparation, reaction conditions, and sampling strategy.
- **Section 5** — Analytical methods and detection: which LC-MS/MS acquisition parameters and data processing steps to report.
- **Section 6** — Activity measurements and outcomes: how to record substrate depletion, product formation, transformation rates, dose-response, and time-course data.
- **Section 7** — Product characterization: MSI metabolite identification confidence levels, structural elucidation, and transformation pathway documentation.
- **Section 8** — Data formats: how to populate ChEMBL `ACTIVITY.tsv` and `ASSAY.tsv` submission files.
- **Section 9** — Controls and validation: required experimental controls and analytical quality assurance criteria.
- **Section 10** — Statistical analysis: minimum statistical reporting requirements.
- **Section 11** — Data quality tiers: Gold / Silver / Bronze compliance levels.
- **Section 12** — Example complete record: a fully annotated MIX-MB(B)-compliant biotransformation study.
- **Section 13** — Integration with MIX-MB(X) and MIX-MB(M): complete data package structure and cross-referencing strategy.
- **Section 14** — Software tools and resources: data acquisition, processing, and deposition tools.

### 1.2 Which sections are important for contributors?

If you want to propose changes to the standard, focus on **Sections 2 and 3** (the Bioschemas metadata fields and ontologies), then follow the contribution process in [Versioning.md](Versioning.md) and [CONTRIBUTING.md](../CONTRIBUTING.md). Changes require a 7-day community review and 2 independent endorsements.

### 1.3 Which sections are important for data submitters?

If you are preparing data for submission, you need:
- **Section 4** — how to classify your assay type and document the experimental setup
- **Section 6** — how to quantify and record biotransformation activity results
- **Section 8** — how to populate `ACTIVITY.tsv` and `ASSAY.tsv` for ChEMBL submission
- **Section 9** — minimum controls required for a valid submission
- **[Template.xlsx](Templates/Template.xlsx)** — colour-coded submission template (green = mandatory, blue = recommended, yellow = optional), specifically the **Activity** and **Assay** sheets.

### 1.4 Identifiers and Cross-Referencing

**This is the first practical step: establish the three-way identifier link (RIDX → CIDX → AIDX) before recording any activity.**

#### The Three-Way Identifier System

Every biotransformation event in MIX-MB is anchored by three identifiers that must be consistent across all submission files:

| Identifier | Entity | Appears in | Format example |
|-----------|--------|-----------|----------------|
| **RIDX** | Reference (study / publication) | All files | `Zimmermann_GutBiotransformationAtlas` |
| **CIDX** | Compound (substrate or product) | `COMPOUND_RECORD.tsv`, `ACTIVITY.tsv` | `CIDX0001` |
| **AIDX** | Assay (organism × condition) | `ASSAY.tsv`, `ASSAY_PARAM.tsv`, `ACTIVITY.tsv` | `Zimmermann_Actinomyces_graevenitzii_biotransformation` |

Every row in `ACTIVITY.tsv` must carry all three identifiers. They are the join keys that link compounds to assays to publications — if any one is missing or inconsistent, the record cannot be deposited or queried.

#### Reference Index (RIDX)

The RIDX is assigned once per study and used unchanged across every file in the submission.

**Minting rules:**
- Format: `[FirstAuthorLastName]_[DescriptiveLabel]`, e.g. `Zimmermann_GutBiotransformationAtlas`
- Must be unique across all submissions to the target database
- Use only ASCII letters, digits, underscores, and hyphens — no spaces or special characters
- Set the RIDX at the outset of data preparation; do not change it after any file references it

#### Activity Record Cross-Referencing

Individual rows in `ACTIVITY.tsv` do not require their own unique identifier, but every row must carry a consistent `CIDX × AIDX × RIDX` triplet. Each such triplet represents one compound–assay interaction.

**Rules:**
- The same `CIDX × AIDX` pair may appear on multiple rows if multiple activity types are reported (e.g. both `Substrate` and `Product` for the same compound in the same assay)
- Do not reuse the same `CIDX × AIDX × ACTION_TYPE` combination for separate measurements — add a distinguishing note in `ACTIVITY_COMMENT` instead
- Every CIDX referenced in `ACTIVITY.tsv` must exist in `COMPOUND_RECORD.tsv`; every AIDX must exist in `ASSAY.tsv` — orphan references will fail ChEMBL validation

#### Minting Scheme for Unconfirmed Biotransformation Events

| Situation | `ACTION_TYPE` | CIDX to use | Notes |
|-----------|--------------|------------|-------|
| Substrate consumed (confirmed) | `Substrate` | Known `CIDX[nnnn]` | Quantitative `VALUE` recommended |
| Product identified (MSI Level 1–2) | `Product` | Known `CIDX[nnnn]` | InChIKey required in `COMPOUND_RECORD.tsv` |
| Product putatively characterised (MSI Level 3) | `Product` | `PUTATIVE_[RIDX]_[n]` | Add structural class and MSI level in `ACTIVITY_COMMENT` |
| Product detected, unknown structure (MSI Level 4–5) | `Product` | `UNKNOWN_[RIDX]_[n]` | Add m/z, adduct type, and MSI level in `ACTIVITY_COMMENT` |
| No biotransformation detected | `No Activity` | Substrate CIDX | Set `TEXT_VALUE` to `"No biotransformation detected"` |

For time-course or dose-response experiments, group multiple measurements under the same `CIDX × AIDX` pair and distinguish individual rows using `ACTIVITY_COMMENT` (e.g. timepoint or concentration) rather than minting new identifiers.

#### sameAs Cross-Referencing for Biotransformation Records

`ACTIVITY.tsv` rows themselves are not linked externally via `sameAs`. Cross-database interoperability is achieved through the compound and assay entities that the activity references:
- **Compound identity:** via InChIKey and `sameAs` URLs in the compound record — see [MIX-MB(X) Section 1.4](MIXMB_Xenobiotics.md)
- **Organism identity:** via NCBI TaxID and `sameAs` URLs in the assay record — see [MIX-MB(M) Section 1.4](MIXMB_Microbes.md)

If the same biotransformation event is reported in a separate publication or database, cross-reference it using `ACTIVITY_COMMENT` with a DOI or database accession rather than a `sameAs` property.

---

## 2. Bioschemas

MIX-MB(B) uses Bioschemas profiles to provide structured, FAIR-compliant annotation of the experimental study, laboratory protocol, and results dataset. These profiles cross-link with the organism metadata in MIX-MB(M) (Taxon, Sample profiles) and the chemical metadata in MIX-MB(X) (MolecularEntity profile). Bioschemas fulfils the Findability and Interoperability aspects of FAIR.

The following profiles are used:

| Profile | Source | Version | Use in MIX-MB(B) |
|---------|--------|---------|------------------|
| [Study](https://bioschemas.org/profiles/Study/0.3-DRAFT) | Bioschemas | 0.3-DRAFT | Overall experiment design and metadata |
| [LabProtocol](https://bioschemas.org/profiles/LabProtocol/0.7-DRAFT) | Bioschemas | 0.7-DRAFT | Biotransformation assay protocol |
| [Dataset](https://bioschemas.org/profiles/Dataset/1.0-RELEASE) | Bioschemas | 1.0-RELEASE | Activity and measurement results |

**_NOTE:_** Study and LabProtocol profiles map to `ASSAY.tsv` and `ASSAY_PARAM.tsv` for ChEMBL submission. Dataset covers activity data in `ACTIVITY.tsv` and supports deposition in MetaboLights or GNPS.

---

### 2.1 Study Profile

Use [Bioschemas Study 0.3-DRAFT](https://bioschemas.org/profiles/Study/0.3-DRAFT) to describe the overall biotransformation experiment, linking the xenobiotic substrate, microbial organism, and assay conditions into a single structured record.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"Study"` |
| `@id` | IRI | ONE | Globally unique IRI identifying this study |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/Study/0.3-DRAFT"` |
| `identifier` | PropertyValue, Text, URL | ONE | Study identifier (e.g., RIDX, MetaboLights accession, DOI) |
| `name` | Text | ONE | Study title |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `description` | Text | ONE | Free-text description of the biotransformation study |
| `author` | Organization, Person | MANY | Principal investigator(s) and contributing authors |
| `datePublished` | Date | ONE | Publication or submission date |
| `url` | URL | ONE | Link to the study in a public repository (e.g., MetaboLights) |
| `studyDomain` | Text | MANY | Research domains: `"microbiology"`, `"xenobiotic biotransformation"` |

**Optional Properties (MIX-MB(B) relevant):**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `citation` | CreativeWork, URL | MANY | Related publications |
| `keywords` | DefinedTerm, Text | MANY | Descriptive keywords (e.g., gut microbiome, drug metabolism) |
| `measurementTechnique` | DefinedTerm, Text, URL | MANY | Analytical technique (e.g., LC-MS/MS, CHMO:0000470) |
| `variableMeasured` | PropertyValue, Text | MANY | Primary outcome variable (e.g., substrate depletion %) |
| `isPartOf` | CreativeWork, URL | MANY | Larger project or dataset collection this study belongs to |

**Example:**
```json
{
  "@context": "https://schema.org/",
  "@type": "Study",
  "@id": "https://www.ebi.ac.uk/metabolights/MTBLS1234",
  "http://purl.org/dc/terms/conformsTo": {
    "@id": "https://bioschemas.org/profiles/Study/0.3-DRAFT",
    "@type": "CreativeWork"
  },
  "identifier": "MTBLS1234",
  "name": "Microbial biotransformation of NSAIDs by human gut bacteria under anaerobic conditions",
  "description": "Whole-cell biotransformation screen of 12 NSAIDs against 25 human gut bacterial strains, measuring substrate depletion and product formation by LC-MS/MS over 24 hours",
  "author": [
    { "@type": "Person", "name": "Mahnoor Zulfiqar", "affiliation": "EMBL Heidelberg" }
  ],
  "datePublished": "2026-03-05",
  "url": "https://www.ebi.ac.uk/metabolights/MTBLS1234",
  "studyDomain": ["microbiology", "xenobiotic biotransformation"],
  "measurementTechnique": {
    "@type": "DefinedTerm",
    "name": "liquid chromatography-mass spectrometry",
    "termCode": "CHMO:0000470"
  },
  "variableMeasured": "substrate depletion percentage",
  "keywords": ["gut microbiome", "drug biotransformation", "NSAID metabolism", "LC-MS/MS"]
}
```

**_NOTE:_** `identifier` from this profile maps to the `RIDX` field across all ChEMBL submission files (`REFERENCE.tsv`, `ASSAY.tsv`, `ACTIVITY.tsv`).

---

### 2.2 LabProtocol Profile

Use [Bioschemas LabProtocol 0.7-DRAFT](https://bioschemas.org/profiles/LabProtocol/0.7-DRAFT) to document the biotransformation assay protocol — covering inoculation, substrate exposure, incubation conditions, sampling, and analytical extraction.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"LabProtocol"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., protocols.io DOI) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/LabProtocol/0.7-DRAFT"` |
| `purpose` | Text | ONE | Purpose of the protocol (e.g., `"Anaerobic whole-cell biotransformation assay"`) |
| `url` | URL | ONE | Link to the protocol (protocols.io, supplementary material, etc.) |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `name` | Text | ONE | Protocol name |
| `identifier` | PropertyValue, Text, URL | ONE | Protocol identifier (e.g., protocols.io accession) |
| `description` | Text | ONE | Short description of the method |
| `instrument` | Text, URL | MANY | Equipment used (e.g., anaerobic chamber, LC-MS system) |
| `reagent` | BioChemEntity, ChemicalSubstance, MolecularEntity | MANY | Substrates, solvents, and reagents used |
| `bioSampleUsed` | BioSample, Sample, URL | MANY | Microbial cultures (links to MIX-MB(M) Sample records) |
| `labEquipment` | DefinedTerm, Text, URL | MANY | Specific equipment |

**Optional Properties (MIX-MB(B) relevant):**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `duration` | Text, URL | ONE | Total protocol duration (e.g., `"24 hours"`) |
| `step` | HowToSection, HowToStep, URL | MANY | Sequential protocol steps |
| `computationalTool` | SoftwareApplication | MANY | Software used in the analysis pipeline |
| `citation` | CreativeWork, URL | MANY | Literature supporting this protocol |
| `isPartOf` | LabProtocol, URL | MANY | Parent protocol this is a sub-protocol of |

**Example:**
```json
{
  "@context": "https://schema.org/",
  "@type": "LabProtocol",
  "@id": "https://dx.doi.org/10.17504/protocols.io.xyz123",
  "http://purl.org/dc/terms/conformsTo": {
    "@id": "https://bioschemas.org/profiles/LabProtocol/0.7-DRAFT",
    "@type": "CreativeWork"
  },
  "name": "Anaerobic whole-cell biotransformation assay with gut bacteria",
  "purpose": "Quantify xenobiotic biotransformation by gut bacterial strains under physiological anaerobic conditions",
  "identifier": "protocols.io:xyz123",
  "url": "https://dx.doi.org/10.17504/protocols.io.xyz123",
  "description": "Stationary-phase cultures are washed, resuspended at OD₆₀₀ 1.0, and incubated with xenobiotic at 37°C under strict anaerobic conditions for 24 hours. Substrate depletion and product formation are quantified by LC-MS/MS.",
  "instrument": [
    "Anaerobic chamber (Coy Laboratory Products)",
    "Agilent 1290 UHPLC",
    "Thermo Q Exactive Plus Orbitrap MS"
  ],
  "reagent": [
    { "@type": "ChemicalSubstance", "name": "Ibuprofen", "identifier": "CHEMBL1201246" },
    { "@type": "ChemicalSubstance", "name": "DMSO (vehicle)", "identifier": "CHEBI:28262" },
    { "@type": "ChemicalSubstance", "name": "BHI medium supplemented with hemin and vitamin K1" }
  ],
  "bioSampleUsed": {
    "@type": "Sample",
    "identifier": "biosample:SAMN02604091",
    "name": "Escherichia coli K-12 MG1655 anaerobic culture"
  },
  "duration": "24 hours",
  "step": [
    { "@type": "HowToStep", "name": "Culture preparation", "text": "Grow bacteria to stationary phase in BHI medium under anaerobic conditions" },
    { "@type": "HowToStep", "name": "Cell harvesting", "text": "Centrifuge at 5000 × g, 10 min, 4°C; wash twice with sterile PBS" },
    { "@type": "HowToStep", "name": "Substrate addition", "text": "Add xenobiotic to final concentration of 100 µM (0.1% DMSO)" },
    { "@type": "HowToStep", "name": "Incubation", "text": "Incubate at 37°C in anaerobic chamber for 24 h with sampling at 0, 3, 6, 12, 24 h" },
    { "@type": "HowToStep", "name": "Sample quenching", "text": "Add equal volume ice-cold acetonitrile with 0.1% formic acid; centrifuge at 15,000 × g" },
    { "@type": "HowToStep", "name": "LC-MS/MS analysis", "text": "Analyse supernatant by reversed-phase LC-MS/MS in negative ion mode" }
  ]
}
```

**_NOTE:_** This profile maps to `ASSAY.tsv` (`ASSAY_DESCRIPTION`, `ASSAY_TYPE`) and `ASSAY_PARAM.tsv` (incubation conditions, atmosphere, duration) for ChEMBL submission.

---

### 2.3 Dataset Profile

Use [Bioschemas Dataset 1.0-RELEASE](https://bioschemas.org/profiles/Dataset/1.0-RELEASE) to describe the biotransformation activity data — making results findable and citable as a distinct, structured dataset linked to the study and compounds.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"Dataset"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., MetaboLights URL, DOI) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/Dataset/1.0-RELEASE"` |
| `name` | Text | ONE | Dataset name |
| `description` | Text | ONE | Description of the activity dataset contents |
| `identifier` | PropertyValue, Text, URL | ONE | Dataset identifier (e.g., MetaboLights accession, DOI) |
| `keywords` | DefinedTerm, Text | MANY | Keywords for discovery |
| `license` | CreativeWork, URL | ONE | Dataset license (e.g., CC BY 4.0) |
| `url` | URL | ONE | URL where the dataset can be accessed |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `creator` | Organization, Person | MANY | Dataset authors |
| `citation` | CreativeWork, URL | MANY | Publication associated with the dataset |
| `measurementTechnique` | DefinedTerm, Text, URL | MANY | Analytical method (e.g., LC-MS/MS) |
| `variableMeasured` | PropertyValue, Text | MANY | Variables in the dataset (substrate depletion, product concentration) |
| `version` | Text | ONE | Dataset version |
| `distribution` | DataDownload | MANY | Download links for the data files |
| `encodingFormat` | Text, URL | MANY | File format(s) (e.g., `"text/tab-separated-values"`) |

**Optional Properties (MIX-MB(B) relevant):**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `isBasedOn` | CreativeWork, URL | MANY | Raw data files or preceding datasets this is derived from |
| `isPartOf` | CreativeWork, URL | MANY | Larger study or repository collection |
| `hasPart` | CreativeWork, URL | MANY | Component datasets (e.g., raw mzML, processed TSVs) |
| `temporalCoverage` | Text | ONE | Date range of experiments |
| `sameAs` | URL | MANY | Same dataset in another repository |

**Example:**
```json
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "@id": "https://www.ebi.ac.uk/metabolights/MTBLS1234",
  "http://purl.org/dc/terms/conformsTo": {
    "@id": "https://bioschemas.org/profiles/Dataset/1.0-RELEASE",
    "@type": "CreativeWork"
  },
  "name": "Biotransformation activity data — NSAIDs × gut bacteria screen",
  "description": "ChEMBL-formatted activity data (ACTIVITY.tsv, ASSAY.tsv) for the biotransformation of 12 NSAIDs by 25 human gut bacterial strains, quantified by LC-MS/MS substrate depletion and product formation.",
  "identifier": "MTBLS1234",
  "keywords": ["biotransformation", "gut microbiome", "NSAID", "LC-MS/MS", "substrate depletion"],
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "url": "https://www.ebi.ac.uk/metabolights/MTBLS1234",
  "creator": [
    { "@type": "Person", "name": "Mahnoor Zulfiqar", "affiliation": "EMBL Heidelberg" }
  ],
  "citation": {
    "@type": "CreativeWork",
    "identifier": "https://doi.org/10.xxxx/example",
    "name": "Systematic screen of gut microbial drug biotransformation"
  },
  "measurementTechnique": {
    "@type": "DefinedTerm",
    "name": "liquid chromatography-mass spectrometry",
    "termCode": "CHMO:0000470"
  },
  "variableMeasured": [
    { "@type": "PropertyValue", "name": "substrate_depletion", "unitText": "%" },
    { "@type": "PropertyValue", "name": "product_concentration", "unitText": "µM" }
  ],
  "distribution": [
    {
      "@type": "DataDownload",
      "name": "ACTIVITY.tsv",
      "encodingFormat": "text/tab-separated-values",
      "contentUrl": "https://www.ebi.ac.uk/metabolights/MTBLS1234/files/ACTIVITY.tsv"
    },
    {
      "@type": "DataDownload",
      "name": "mzML raw files",
      "encodingFormat": "application/mzML+xml",
      "contentUrl": "https://www.ebi.ac.uk/metabolights/MTBLS1234/files/"
    }
  ]
}
```

**_NOTE:_** This profile maps to `ACTIVITY.tsv` and supports data deposition in MetaboLights, GNPS, or other public repositories alongside the ChEMBL submission files.

---

## 3. Ontologies

### 3.1 BioAssay Ontology (BAO)

**Required Assay Classifications:**
- **BAO:0000697** - metabolism assay
- **BAO:0002989** - biotransformation assay
- **BAO:0000522** - cell-based assay
- **BAO:0000698** - cell-free assay
- **BAO:0002856** - enzymatic assay

**Assay Format:**
- **BAO:0000219** - single concentration response
- **BAO:0000357** - dose-response assay
- **BAO:0000208** - time-course assay

**Detection Method:**
- **BAO:0000196** - mass spectrometry
- **BAO:0000315** - chromatography
- **BAO:0000217** - spectrophotometry

### 3.2 Gene Ontology (GO) - Biological Process

**Biotransformation Processes:**
- **GO:0006805** - xenobiotic metabolic process
- **GO:0006082** - organic acid metabolic process
- **GO:0042737** - drug catabolic process
- **GO:0018894** - dibenzo-p-dioxin metabolic process
- **GO:0006725** - cellular aromatic compound metabolic process

**Molecular Functions:**
- **GO:0016491** - oxidoreductase activity
- **GO:0016740** - transferase activity
- **GO:0016787** - hydrolase activity
- **GO:0016829** - lyase activity
- **GO:0016853** - isomerase activity
- **GO:0016874** - ligase activity

### 3.3 Chemical Methods Ontology (CHMO)

**Analytical Techniques:**
- **CHMO:0000470** - liquid chromatography-mass spectrometry
- **CHMO:0000497** - gas chromatography-mass spectrometry
- **CHMO:0000591** - nuclear magnetic resonance spectroscopy
- **CHMO:0000228** - high performance liquid chromatography
- **CHMO:0000830** - ultra performance liquid chromatography

### 3.4 Reaction Types Ontology

**Common Biotransformation Reactions:**

| Reaction Type | Description | EC Class |
|--------------|-------------|----------|
| Hydroxylation | Addition of -OH group | EC 1.14.x.x |
| Reduction | Addition of H or removal of O | EC 1.x.x.x |
| Oxidation | Removal of H or addition of O | EC 1.x.x.x |
| Hydrolysis | Cleavage by water addition | EC 3.x.x.x |
| Decarboxylation | Loss of CO₂ | EC 4.1.1.x |
| Deamination | Loss of NH₂ | EC 3.5.x.x |
| N-reduction | Reduction of nitrogen groups | EC 1.7.x.x |
| Azo reduction | Cleavage of N=N bonds | EC 1.7.1.17 |
| Demethylation | Loss of CH₃ group | EC 1.14.x.x |
| Dehalogenation | Loss of halogen | EC 3.8.x.x |
| Conjugation | Addition of larger moiety | EC 2.x.x.x |
| Acetylation | Addition of acetyl group | EC 2.3.1.x |
| Glucuronidation | Addition of glucuronic acid | EC 2.4.1.17 |
| Sulfation | Addition of sulfate | EC 2.8.2.x |

---

## 4. Assay Design and Experimental Setup

### 4.1 Assay Type Classification

**Level 1: Biological System**
- `whole cell assay` - Intact living cells
- `cell lysate assay` - Disrupted cells with enzymes
- `purified enzyme assay` - Isolated single enzyme
- `tissue/organ assay` - Ex vivo tissue preparation
- `community assay` - Mixed microbial population
- `in vivo assay` - Whole organism (e.g., animal model)

**Level 2: Experimental Format**
- `endpoint assay` - Single timepoint measurement
- `time-course assay` - Multiple timepoints
- `dose-response assay` - Multiple substrate concentrations
- `screening assay` - High-throughput format
- `mechanistic assay` - Detailed pathway elucidation

### 4.2 Required Assay Information

#### 4.2.1 Assay Identifier (AIDX)

Format: `A{number}_{OrganismAbbrev}_{Strain}_{Condition}`

**Examples:**
```
A001_Ecoli_K12_aerobic
A002_Btheta_VPI5482_anaerobic
A003_Csporogenes_ATCC15579_anaerobic
```

#### 4.2.2 Assay Description

**Required Components:**
1. **Biological system:** Whole cells, lysate, enzyme
2. **Substrate:** Xenobiotic compound name
3. **Organism:** Scientific name and strain
4. **Key conditions:** Aerobic/anaerobic, temperature
5. **Measurement:** What is being quantified

**Example:**
```
"Biotransformation of ibuprofen by Escherichia coli K-12 MG1655 
whole cells under anaerobic conditions at 37°C, measuring substrate 
depletion and metabolite formation by LC-MS/MS over 24 hours"
```

### 4.3 Substrate Preparation

**Required Information:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| Stock concentration | Yes | Concentration of stock solution |
| Stock solvent | Yes | Solvent used (DMSO, ethanol, water) |
| Solvent percentage | Yes | Final % in assay (keep <1% organic) |
| Storage conditions | Yes | Temperature, light protection |
| Working concentration | Yes | Final concentration in assay |
| Preparation method | Yes | Dissolution, sonication, etc. |

**Example:**
```yaml
substrate_preparation:
  compound: "Ibuprofen"
  stock_solution:
    concentration: "100 mM"
    solvent: "DMSO"
    preparation: "dissolved with vortexing"
    storage: "-20°C, protected from light"
  working_solution:
    final_concentration: "100 µM"
    dilution_factor: "1:1000"
    solvent_percentage: "0.1% DMSO"
    preparation: "diluted in sterile medium"
```

### 4.4 Cell/Enzyme Preparation

**For Whole Cell Assays:**
```yaml
cell_preparation:
  culture_source: "overnight culture in BHI"
  harvest_method: "centrifugation 5000 × g, 10 min, 4°C"
  washing:
    buffer: "sterile PBS, pH 7.4"
    wash_cycles: 2
  resuspension:
    buffer: "fresh BHI medium"
    cell_density: "OD₆₀₀ = 1.0 (normalized)"
    cell_count: "~1 × 10⁹ CFU/mL"
  viability_check: ">95% viable (live/dead staining)"
```

**For Cell Lysate Assays:**
```yaml
lysate_preparation:
  cell_harvest: "as above"
  lysis_method: "sonication (3 × 30 s, on ice)"
  lysis_buffer: "50 mM Tris-HCl, pH 7.5, 10 mM MgCl₂"
  centrifugation: "15000 × g, 20 min, 4°C"
  lysate_fraction: "supernatant (cytoplasmic fraction)"
  protein_concentration: "5 mg/mL (Bradford assay)"
  storage: "aliquots at -80°C, single use"
```

**For Purified Enzyme Assays:**
```yaml
enzyme_preparation:
  enzyme_source: "recombinant, expressed in E. coli"
  purification_method: "His-tag affinity chromatography"
  purity: ">95% (SDS-PAGE)"
  specific_activity: "12.5 U/mg"
  concentration: "0.5 mg/mL"
  storage_buffer: "50 mM Tris-HCl, pH 7.5, 20% glycerol"
  storage: "-80°C, avoid freeze-thaw"
```

### 4.5 Reaction Setup

**Standard Reaction Components:**

```yaml
reaction_mixture:
  total_volume: "1.0 mL"
  
  components:
    - name: "Cell suspension or lysate"
      volume: "900 µL"
      final_concentration: "OD₆₀₀ 1.0 or 5 mg/mL protein"
    
    - name: "Substrate (from stock)"
      volume: "1 µL"
      final_concentration: "100 µM"
    
    - name: "Cofactors (if needed)"
      components:
        - "NADH: 1 mM"
        - "NADPH: 1 mM"
        - "FAD: 50 µM"
    
    - name: "Solvent control"
      volume: "1 µL DMSO"
      purpose: "vehicle control"

  incubation:
    temperature: "37°C"
    atmosphere: "anaerobic (chamber or sealed tubes)"
    shaking: "100 rpm (or static)"
    duration: "0, 1, 3, 6, 12, 24 hours"
    
  controls:
    - "Negative control: heat-killed cells + substrate"
    - "Substrate control: substrate + medium only"
    - "Cell control: cells + solvent only"
```

### 4.6 Sampling and Quenching

**Required Information:**

```yaml
sampling_procedure:
  timepoints: [0, 1, 3, 6, 12, 24]  # hours
  sample_volume: "100 µL per timepoint"
  
  quenching_method:
    method: "acidification"
    reagent: "add 100 µL ice-cold acetonitrile with 0.1% formic acid"
    temperature: "on ice immediately"
    
  sample_processing:
    centrifugation: "15000 × g, 10 min, 4°C"
    supernatant_collection: "150 µL"
    storage: "-80°C until analysis"
    stability: "stable for 6 months"
    
  internal_standard:
    compound: "13C6-ibuprofen"
    concentration: "10 µM final"
    addition_timing: "at quenching step"
```

---

## 5. Analytical Methods and Detection

### 5.1 LC-MS/MS Method

**Required Method Parameters:**

```yaml
lcms_method:
  instrument:
    lc_system: "Agilent 1290 Infinity II UHPLC"
    ms_system: "Thermo Q Exactive Plus Orbitrap"
    
  chromatography:
    column: "Waters Acquity UPLC BEH C18"
    dimensions: "2.1 × 100 mm, 1.7 µm"
    column_temperature: "40°C"
    injection_volume: "5 µL"
    flow_rate: "0.3 mL/min"
    
    mobile_phase:
      A: "water + 0.1% formic acid"
      B: "acetonitrile + 0.1% formic acid"
    
    gradient:
      - time: "0 min", B: "5%"
      - time: "1 min", B: "5%"
      - time: "8 min", B: "95%"
      - time: "10 min", B: "95%"
      - time: "10.1 min", B: "5%"
      - time: "12 min", B: "5%"
  
  mass_spectrometry:
    ionization: "ESI negative mode"
    scan_type: "Full MS + dd-MS²"
    resolution: "70,000 FWHM (MS1), 17,500 (MS2)"
    mass_range: "50-1000 m/z"
    agc_target: "3e6"
    max_it: "100 ms"
    
    ms2_parameters:
      collision_energy: "stepped NCE 20, 40, 60"
      isolation_window: "1.0 m/z"
      
  data_acquisition:
    software: "Xcalibur 4.1"
    data_format: "mzML (centroid)"
```

### 5.2 Data Processing

**Required Information:**

```yaml
data_processing:
  peak_detection:
    software: "MZmine 2.53"
    mass_tolerance: "5 ppm"
    rt_tolerance: "0.1 min"
    min_peak_height: "1e4"
    
  peak_integration:
    method: "automated with manual review"
    baseline_correction: "local minimum"
    smoothing: "Savitzky-Golay (5 points)"
    
  compound_identification:
    level: "MSI Level 2"
    criteria:
      - "Accurate mass match (<5 ppm)"
      - "MS² spectral match (similarity >0.7)"
      - "Retention time match (±0.2 min)"
    reference_databases:
      - "MassBank"
      - "HMDB"
      - "GNPS"
      
  quantification:
    method: "external standard curve"
    calibration_range: "0.1-100 µM"
    calibration_points: 8
    curve_fit: "linear, 1/x weighting"
    r_squared: ">0.995"
    loq: "0.5 µM"
    lod: "0.1 µM"
```

### 5.3 Quality Control

**Required QC Measures:**

```yaml
quality_control:
  system_suitability:
    - "Column pressure: within specifications"
    - "Peak shape: tailing factor <1.5"
    - "Retention time stability: ±0.1 min"
    - "Mass accuracy: <5 ppm"
    
  blanks:
    - type: "Extraction blank"
      frequency: "every batch"
      acceptance: "no interfering peaks"
    - type: "Injection blank"
      frequency: "between samples"
      acceptance: "carryover <1%"
      
  standards:
    - type: "Calibration standard"
      frequency: "each batch"
      acceptance: "within 85-115% of expected"
    - type: "Quality control standard"
      frequency: "every 10 samples"
      acceptance: "within 80-120%, CV <20%"
      
  internal_standard:
    recovery: "70-130%"
    cv: "<20%"
```

---

## 6. Activity Measurements and Outcomes

### 6.1 Activity Types

**Primary Activities:**

| Activity Type | Description | Units | ChEMBL Type |
|--------------|-------------|-------|-------------|
| Substrate depletion | % of substrate remaining | % or µM | Inhibition |
| Product formation | Amount of product formed | µM | Product |
| Transformation rate | Rate of conversion | µM/hr | Rate |
| Half-life | Time to 50% conversion | hours | T50 |
| Biotransformation index | Ratio product/substrate | unitless | Ratio |

**Qualitative Activities:**
- `Substrate` - Compound consumed
- `Product` - Compound formed
- `No activity` - No transformation detected
- `Partial transformation` - Incomplete conversion
- `Complete transformation` - >95% conversion

### 6.2 Quantitative Measurements

**Required for Each Activity:**

```yaml
activity_measurement:
  cidx: "C001"
  aidx: "A001_Ecoli_K12"
  ridx: "REF_001"
  
  # Primary measurement
  type: "Biotransformation"
  action_type: "SUBSTRATE"
  
  substrate_depletion:
    initial_concentration: 100  # µM
    final_concentration: 15     # µM
    depletion_percentage: 85    # %
    relation: "="
    value: 85
    units: "%"
    sd_plus: 5.2
    sd_minus: 5.2
    
  # Transformation rate
  transformation_rate:
    value: 3.5
    units: "µM/hour"
    relation: "="
    calculation: "linear regression (0-24h)"
    r_squared: 0.98
    
  # Product formation
  product_formation:
    cidx: "P001"
    concentration: 72  # µM
    recovery: 85       # % of depleted substrate
    
  # Statistical parameters
  replicates:
    biological: 3
    technical: 2
  statistical_test: "one-way ANOVA"
  p_value: 0.003
  significance: "p < 0.01"
```

### 6.3 Dose-Response Data

**For Multiple Concentrations:**

```yaml
dose_response:
  substrate_concentrations: [1, 5, 10, 25, 50, 100, 200, 500]  # µM
  
  results:
    - concentration: 1
      activity: 10
      cv: 12
    - concentration: 5
      activity: 35
      cv: 8
    - concentration: 10
      activity: 55
      cv: 6
    # ... additional points
    
  curve_fitting:
    model: "Michaelis-Menten"
    km: 25.3  # µM
    vmax: 450  # nmol/min/mg protein
    hill_coefficient: 1.0
    r_squared: 0.96
```

### 6.4 Time-Course Data

**For Kinetic Studies:**

```yaml
time_course:
  timepoints: [0, 1, 3, 6, 12, 24, 48]  # hours
  
  substrate_profile:
    - time: 0
      concentration: 100.0
      sd: 0.0
    - time: 1
      concentration: 95.2
      sd: 3.1
    - time: 3
      concentration: 85.7
      sd: 4.5
    - time: 6
      concentration: 68.3
      sd: 5.2
    - time: 12
      concentration: 42.1
      sd: 6.8
    - time: 24
      concentration: 15.4
      sd: 4.2
    - time: 48
      concentration: 2.1
      sd: 0.8
      
  product_profile:
    - time: 0
      concentration: 0.0
    - time: 1
      concentration: 3.8
    # ... matching timepoints
    
  kinetics:
    rate_constant: 0.073  # h⁻¹
    half_life: 9.5        # hours
    model: "first-order decay"
```

---

## 7. Product Characterization

### 7.1 Metabolite Identification

**MSI Confidence Levels:**

**Level 1 - Identified Compounds:**
```yaml
metabolite:
  metabolite_id: "M001"
  identification_level: "Level 1"
  compound_name: "Hydroxy-ibuprofen"
  evidence:
    - "Authentic standard comparison"
    - "Retention time match (±0.05 min)"
    - "Accurate mass match (Δ <2 ppm)"
    - "MS² spectral match (similarity >0.95)"
  confidence: "Confirmed"
```

**Level 2 - Putatively Annotated:**
```yaml
metabolite:
  metabolite_id: "M002"
  identification_level: "Level 2"
  putative_name: "Carboxy-ibuprofen"
  evidence:
    - "Accurate mass (Δ <5 ppm)"
    - "MS² library match (similarity 0.85)"
    - "Expected biotransformation product"
  confidence: "Probable"
```

**Level 3 - Putatively Characterized:**
```yaml
metabolite:
  metabolite_id: "M003"
  identification_level: "Level 3"
  chemical_class: "Hydroxylated aromatic compound"
  evidence:
    - "Accurate mass indicates +16 Da (hydroxylation)"
    - "MS² fragmentation consistent with aromatic hydroxylation"
  confidence: "Tentative"
```

**Level 4 - Unknown:**
```yaml
metabolite:
  metabolite_id: "M004"
  identification_level: "Level 4"
  description: "Unknown biotransformation product"
  observed_mass: 237.1234
  retention_time: 5.67
```

### 7.2 Structural Characterization

**Required for New Metabolites:**

```yaml
structure_elucidation:
  metabolite_id: "M001"
  
  mass_spectrometry:
    exact_mass: 222.1256
    molecular_formula: "C13H18O3"
    formula_error: "1.2 ppm"
    double_bond_equivalents: 5
    
    ms2_fragments:
      - mz: 177.0916
        formula: "C11H13O2"
        assignment: "[M-COOH]-"
      - mz: 161.0966
        formula: "C11H13O"
        assignment: "[M-COOH-O]-"
        
  nmr_spectroscopy:
    acquired: true
    1h_nmr: "500 MHz, CD3OD"
    13c_nmr: "125 MHz, CD3OD"
    2d_experiments: ["COSY", "HSQC", "HMBC"]
    
  proposed_structure:
    smiles: "CC(C)Cc1ccc(cc1)C(C)(O)C(=O)O"
    inchi_key: "NEWMETABOLITE-UHFFFAOYSA-N"
    transformation_site: "tertiary carbon hydroxylation"
```

### 7.3 Transformation Pathway

**Pathway Documentation:**

```yaml
transformation_pathway:
  pathway_id: "PATH_001"
  substrate:
    cidx: "C001"
    name: "Ibuprofen"
    smiles: "CC(C)Cc1ccc(cc1)C(C)C(=O)O"
    
  steps:
    - step: 1
      reaction_type: "hydroxylation"
      enzyme: "cytochrome P450-like"
      product:
        metabolite_id: "M001"
        name: "Hydroxy-ibuprofen"
        smiles: "CC(C)Cc1ccc(cc1)C(C)(O)C(=O)O"
        
    - step: 2
      reaction_type: "oxidation"
      enzyme: "alcohol dehydrogenase"
      product:
        metabolite_id: "M002"
        name: "Carboxy-ibuprofen"
        smiles: "CC(C)Cc1ccc(cc1)C(=O)C(=O)O"
        
  branching_pathways:
    - branch: "A"
      steps: [1, 2]
      major: true
      percentage: 75
    - branch: "B"
      steps: [3]
      major: false
      percentage: 25
```

---

## 8. Data Formats - ACTIVITY.tsv

The MIX-MB(B) activity data lives in two formats: the **Template.xlsx Activity sheet** (the primary submitter input) and **ChEMBL ACTIVITY.tsv** (the pipeline output). The template is a superset of the ChEMBL format, adding metabolite detection, annotation, kinetic, and reaction-type columns as MIX-MB extensions.

---

### 8.1 MIX-MB(B) Activity Template (Template.xlsx — Activity Sheet)

This is the **primary submission format**. Submitters fill this sheet; the BioXend pipeline converts it to ChEMBL-ready files.

| # | Column | Required | Type | Description |
|---|--------|----------|------|-------------|
| 1 | `Chemical_identifier` | Yes* | String | CIDX — auto-filled by pipeline. If filling manually, use the same identifier as in `COMPOUND_RECORD.tsv`. |
| 2 | `Common_Name` | Yes | String | Common name of the xenobiotic (drug, pesticide, etc.) — must match the compound entry. |
| 3 | `SMILES` | Yes | String | Canonical SMILES of the parent compound — must match `COMPOUND_RECORD.tsv`. |
| 4 | `ASSAY_identifier` | Yes | String | AIDX — must match a valid record in `ASSAY.tsv`. Use the vocabulary defined in the Assay sheet. |
| 5 | `TEXT_VALUE` | Cond. | String | Qualitative activity result from controlled vocabulary (see 8.3). Leave empty when reporting a `VALUE`. |
| 6 | `VALUE` | Cond. | Numeric | Numerical measurement (e.g., % depletion, µM product). Leave empty when using `TEXT_VALUE`. |
| 7 | `RELATION` | Cond. | String | Relationship operator for `VALUE`: `=`, `<`, `>`, `~`, `<=`, `>=`. Required when `VALUE` is provided. |
| 8 | `UPPER_VALUE` | No | Numeric | Upper bound of a range; `VALUE` is then the lower bound. |
| 9 | `UNITS` | Cond. | String | Unit of `VALUE` (e.g., `%`, `µM`, `µM/hour`, `h`). Required when `VALUE` is provided. |
| 10 | `ACTIVITY_COMMENT` | **Yes** | Text | Free-text: thresholds, p-values, conditions, interpretation. **If left empty, BioXend will not annotate an activity value for this row.** |
| 11 | `Metabolite_mz` | No | Numeric | Observed m/z of the detected biotransformation product (parent ion). |
| 12 | `Metabolite_retention_time` | No | Text | Retention time of the metabolite with unit (e.g., `2.17 min`). |
| 13 | `Metabolite_annotation` | No | String | Top annotation: SMILES, compound name, or ChemONT chemical class. Check a chemical database to determine the appropriate annotation level. |
| 14 | `Metabolite_annotation_level` | No | Integer | MSI identification confidence: `1` (confirmed with authentic standard) to `5` (unknown). See Section 7 for full level definitions. |
| 15 | `Kinetic_parameters` | No | Text | Kinetic data — biotransformation assays only (e.g., Km, Vmax, rate constant k, half-life t½). |
| 16 | `Reaction_type` | No | String | Type of biotransformation reaction (controlled vocabulary in 8.3; EC numbers in Section 3.4). |
| 17 | `Activity_type` | Yes | String | Always `Biotransformation` for all entries in this standard. |
| 18 | `ACTION_TYPE` | Cond. | String | Effect classification (see 8.3). **Leave empty if no confirmed activity — do not guess.** |

> \* `Chemical_identifier` is auto-filled by the BioXend pipeline; only supply manually when submitting without it.

---

### 8.2 ChEMBL ACTIVITY.tsv Mapping

The BioXend pipeline maps template columns to ChEMBL `ACTIVITY.tsv`. Columns 11–16 (metabolite, annotation, kinetics, reaction type) are MIX-MB extensions concatenated into `ACTIVITY_COMMENT`.

| ChEMBL Column | Required | Template column | Notes |
|---------------|----------|-----------------|-------|
| `CIDX` | Yes | 1 `Chemical_identifier` | Auto-generated or manually provided |
| `AIDX` | Yes | 4 `ASSAY_identifier` | Must match a row in `ASSAY.tsv` |
| `RIDX` | Yes | Study-level | Same across all activity rows in one study |
| `TEXT_VALUE` | Cond. | 5 `TEXT_VALUE` | Controlled vocabulary (see 8.3) |
| `RELATION` | Cond. | 7 `RELATION` | Required with `VALUE` |
| `VALUE` | Cond. | 6 `VALUE` | Numerical measurement |
| `UPPER_VALUE` | No | 8 `UPPER_VALUE` | For range measurements |
| `UNITS` | Cond. | 9 `UNITS` | Required with `VALUE` |
| `ACTIVITY_COMMENT` | **Yes** | 10 + cols 11–16 | Pipeline concatenates ACTIVITY_COMMENT with metabolite and kinetic fields |
| `TYPE` | Yes | 17 `Activity_type` | Always `Biotransformation` |
| `ACTION_TYPE` | Cond. | 18 `ACTION_TYPE` | Null if no confirmed activity |

---

### 8.3 Controlled Vocabularies for Activity Fields

**`TEXT_VALUE` — use one of these exact strings:**

| TEXT_VALUE | Meaning |
|------------|---------|
| `Compound metabolized` | Parent compound consumed/depleted |
| `Compound NOT metabolized` | No measurable transformation detected |
| `Product detected` | Biotransformation product observed |
| `Partial transformation` | Incomplete conversion (< 95%) |
| `Complete transformation` | Full conversion (≥ 95%) |

**`ACTION_TYPE` — effect classification:**

| ACTION_TYPE | Use when |
|-------------|----------|
| `SUBSTRATE` | The compound is consumed as a substrate |
| `PRODUCT` | The compound is a detected biotransformation product |
| `No Activity` | No transformation detected; leave `VALUE` empty |
| `INHIBITION` | The compound inhibits a microbial enzyme or process |
| `STIMULATION` | The compound stimulates a microbial process |

**`Reaction_type` — controlled vocabulary (see Section 3.4 for EC numbers):**

`hydroxylation` | `reduction` | `oxidation` | `hydrolysis` | `decarboxylation` | `deamination` | `N-reduction` | `azo_reduction` | `demethylation` | `dehalogenation` | `conjugation` | `acetylation` | `glucuronidation` | `sulfation`

---

### 8.4 Example Template Rows

**No biotransformation detected:**

| Col | Value |
|-----|-------|
| Chemical_identifier | HMM0089 |
| Common_Name | Diazepam |
| SMILES | C15H13ClN2O |
| ASSAY_identifier | assay1 |
| TEXT_VALUE | Compound NOT metabolized |
| ACTIVITY_COMMENT | No biotransformation of Diazepam after 24h anaerobic incubation; background <2% |
| Activity_type | Biotransformation |
| ACTION_TYPE | No Activity |

**Compound metabolised with putative metabolite (MSI Level 4):**

| Col | Value |
|-----|-------|
| Chemical_identifier | HMM0085 |
| Common_Name | Diazepam |
| ASSAY_identifier | assay3 |
| TEXT_VALUE | Compound metabolized |
| ACTIVITY_COMMENT | Diazepam biotransformed to desmethyldiazepam; 85% conversion after 24h; n=3 |
| Metabolite_mz | 372.151 |
| Metabolite_retention_time | 2.573 min |
| Metabolite_annotation | Desmethyldiazepam |
| Metabolite_annotation_level | 4 |
| Reaction_type | hydrolysis |
| Activity_type | Biotransformation |
| ACTION_TYPE | SUBSTRATE |

**Quantitative depletion with kinetics and confirmed product (MSI Level 2):**

| Col | Value |
|-----|-------|
| Chemical_identifier | HMM0001 |
| Common_Name | Ibuprofen |
| SMILES | CC(C)Cc1ccc(cc1)C(C)C(=O)O |
| ASSAY_identifier | assay2 |
| TEXT_VALUE | Compound metabolized |
| VALUE | 85 |
| RELATION | = |
| UNITS | % |
| ACTIVITY_COMMENT | 85% substrate depletion after 24h; SD ±5.2%; p<0.01 one-way ANOVA n=3; 37°C anaerobic |
| Metabolite_mz | 222.126 |
| Metabolite_retention_time | 4.85 min |
| Metabolite_annotation | CC(C)Cc1ccc(cc1)C(C)(O)C(=O)O |
| Metabolite_annotation_level | 2 |
| Kinetic_parameters | t½=9.5h; k=0.073 h⁻¹ |
| Reaction_type | hydroxylation |
| Activity_type | Biotransformation |
| ACTION_TYPE | SUBSTRATE |

---

## 9. Controls and Validation

### 9.1 Required Controls

**Essential Controls:**

```yaml
experimental_controls:
  
  negative_controls:
    - type: "Heat-killed cells"
      preparation: "95°C for 20 min"
      purpose: "Confirm biological activity"
      expected: "No transformation"
      
    - type: "Medium only"
      composition: "Substrate + medium without cells"
      purpose: "Chemical stability"
      expected: "Substrate stable"
      
    - type: "Cells only"
      composition: "Cells + solvent without substrate"
      purpose: "Cell viability and background"
      expected: "No interfering peaks"
      
  positive_controls:
    - type: "Known substrate"
      compound: "Reference compound with known transformation"
      purpose: "System functionality"
      expected: "Expected transformation"
      
  internal_controls:
    - type: "Internal standard"
      compound: "Isotope-labeled substrate"
      purpose: "Extraction efficiency and quantification"
      expected: "Consistent recovery"
```

### 9.2 Quality Assurance

**Acceptance Criteria:**

```yaml
quality_assurance:
  
  assay_validity:
    - criterion: "Negative control"
      requirement: "<5% background transformation"
      measured: "2.1%"
      status: "PASS"
      
    - criterion: "Positive control"
      requirement: ">80% expected transformation"
      measured: "92%"
      status: "PASS"
      
    - criterion: "Internal standard recovery"
      requirement: "70-130%"
      measured: "105%"
      status: "PASS"
      
  reproducibility:
    - parameter: "Biological replicates (n=3)"
      cv: "8.5%"
      requirement: "<20%"
      status: "PASS"
      
    - parameter: "Technical replicates (n=2)"
      cv: "4.2%"
      requirement: "<15%"
      status: "PASS"
      
  analytical_performance:
    - parameter: "Mass accuracy"
      value: "2.3 ppm"
      requirement: "<5 ppm"
      status: "PASS"
      
    - parameter: "Retention time stability"
      value: "±0.08 min"
      requirement: "±0.2 min"
      status: "PASS"
```

---

## 10. Statistical Analysis

### 10.1 Required Statistical Information

```yaml
statistical_analysis:
  
  experimental_design:
    type: "Completely randomized design"
    independent_variable: "Substrate concentration"
    dependent_variable: "Biotransformation percentage"
    replicates:
      biological: 3
      technical: 2
      
  descriptive_statistics:
    mean: 85.3
    median: 86.1
    standard_deviation: 5.2
    standard_error: 3.0
    confidence_interval_95: "[79.4, 91.2]"
    
  hypothesis_testing:
    null_hypothesis: "No biotransformation occurs"
    alternative_hypothesis: "Biotransformation occurs"
    test: "one-sample t-test vs. 0% transformation"
    test_statistic: 28.4
    degrees_of_freedom: 2
    p_value: 0.0012
    significance_level: 0.05
    conclusion: "Reject null hypothesis (p < 0.05)"
    
  comparative_analysis:
    comparison: "Treatment vs. control"
    test: "two-sample t-test"
    p_value: 0.003
    effect_size_cohen_d: 2.45
    interpretation: "Large effect, highly significant"
```

### 10.2 Data Visualization Requirements

**Recommended Plots:**
- Time-course plot (concentration vs. time)
- Dose-response curve (activity vs. concentration)
- Bar chart with error bars (comparing conditions)
- Heatmap (multiple substrates × organisms)
- Pathway diagram (substrate → intermediates → products)

---

## 11. Data Quality Tiers

### Tier 1: Gold Standard (Publication-Ready)

- All Level A and B information complete
- Quantitative activity data with statistical analysis (n ≥ 3 biological replicates)
- Metabolite products identified at MSI Level 1 or 2
- Raw LC-MS data deposited in a public repository (MetaboLights, GNPS)
- Transformation pathway documented with proposed mechanism
- All required controls passed (negative, positive, internal standard)
- Mass accuracy ≤ 5 ppm; internal standard recovery 70–130%

### Tier 2: Silver Standard (Research-Grade)

- All Level A information complete
- Quantitative or semi-quantitative activity data (n ≥ 2 biological replicates)
- Metabolite products identified at MSI Level 2 or 3
- Negative and internal standard controls included
- Basic analytical quality control documented

### Tier 3: Bronze Standard (Preliminary)

- All Level A essential information (CIDX, AIDX, RIDX, TEXT_VALUE, ACTION_TYPE)
- Qualitative activity (substrate consumed / product detected / no activity)
- Single measurement acceptable for initial screening
- Suitable for large-scale screening studies where quantification is impractical

---

## 12. Example Complete Record

```yaml
# MIX-MB(B) Compliant Biotransformation Record

# Assay Identification
assay_id: "A001_Ecoli_K12_Ibuprofen"
assay_date: "2023-09-15"
assay_type: "whole cell biotransformation"
assay_format: "time-course with dose-response"

# Links to Other Standards
substrate_reference: "C001"  # from MIX-MB(X)
organism_reference: "ORG_001"  # from MIX-MB(M)
publication_reference: "REF_001"

# Assay Description
description: >
  Biotransformation of ibuprofen by Escherichia coli K-12 MG1655
  under anaerobic conditions. Whole cells were incubated with 
  substrate at 37°C for 24 hours. Substrate depletion and metabolite
  formation were quantified by LC-MS/MS.

# Experimental Setup
substrate:
  cidx: "C001"
  name: "Ibuprofen"
  chembl_id: "CHEMBL1201246"
  stock_concentration: "100 mM in DMSO"
  working_concentrations: [10, 25, 50, 100, 200]  # µM
  final_concentration_tested: 100  # µM
  solvent_percentage: 0.1  # % DMSO

organism:
  organism_id: "ORG_001"
  scientific_name: "Escherichia coli"
  ncbi_taxid: 511145
  strain: "K-12 substr. MG1655"

cell_preparation:
  culture_medium: "LB broth"
  growth_phase: "stationary phase"
  harvest_od600: 2.0
  washing: "2× PBS"
  resuspension_medium: "M9 minimal medium"
  final_od600: 1.0
  cell_concentration: "~8 × 10⁸ CFU/mL"

reaction_conditions:
  volume: "1.0 mL"
  temperature: "37°C"
  atmosphere: "anaerobic (chamber, <0.1% O₂)"
  shaking: "100 rpm"
  duration: "24 hours"
  sampling_times: [0, 3, 6, 12, 24]  # hours

controls:
  negative:
    - "Heat-killed cells (95°C, 20 min) + substrate"
    - "Medium only + substrate"
  positive:
    - "Known substrate transformation (aspirin)"
  internal_standard:
    - "13C6-ibuprofen, 10 µM"

# Analytical Method
analytical_method:
  platform: "LC-MS/MS"
  instrument: "Agilent 1290 UHPLC - Thermo Q Exactive Plus"
  
  chromatography:
    column: "Waters BEH C18, 2.1×100mm, 1.7µm"
    mobile_phase_A: "H₂O + 0.1% FA"
    mobile_phase_B: "ACN + 0.1% FA"
    flow_rate: "0.3 mL/min"
    gradient: "5-95% B in 8 min"
    
  mass_spectrometry:
    ionization: "ESI negative"
    resolution: "70,000"
    mass_range: "50-1000 m/z"
    fragmentation: "HCD, NCE 40"

# Results
activity_data:
  substrate_activity:
    cidx: "C001"
    aidx: "A001_Ecoli_K12_Ibuprofen"
    ridx: "REF_001"
    type: "Biotransformation"
    action_type: "SUBSTRATE"
    
    initial_concentration: 100  # µM
    final_concentration: 12    # µM
    depletion: 88              # %
    depletion_sd: 4.5          # %
    
    transformation_rate: 3.67  # µM/hour
    rate_sd: 0.31
    
    biological_replicates: 3
    technical_replicates: 2
    
    statistical_test: "one-way ANOVA"
    p_value: 0.0008
    significance: "p < 0.001"
    
  product_activity:
    cidx: "P001"
    metabolite_id: "M001"
    name: "Hydroxy-ibuprofen"
    identification_level: "Level 2"
    
    concentration: 78  # µM
    recovery: 88.6     # % of depleted substrate
    
    exact_mass: 222.1256
    retention_time: 4.85  # min
    ms2_match_score: 0.87

# Transformation Pathway
pathway:
  reaction_type: "reductive hydroxylation"
  enzyme_class: "EC 1.14.x.x (oxidoreductase)"
  cofactor_requirement: "NADPH-dependent"
  
  proposed_mechanism: >
    Cytochrome P450-like enzyme catalyzes hydroxylation at the
    tertiary carbon of the isobutyl side chain.

# Quality Control
qc_results:
  negative_control: "PASS - <2% background"
  positive_control: "PASS - 95% expected transformation"
  internal_standard_recovery: "102% (PASS: 70-130%)"
  biological_replicate_cv: "5.1% (PASS: <20%)"
  technical_replicate_cv: "2.8% (PASS: <15%)"
  mass_accuracy: "1.8 ppm (PASS: <5 ppm)"

# Data Quality
quality_tier: "Gold Standard"
data_completeness: "100% Level A, 95% Level B"
validation_status: "PASS"
raw_data_available: true
raw_data_repository: "MetaboLights"
raw_data_accession: "MTBLS1234"

# Contact
principal_investigator: "Dr. Jane Smith"
laboratory: "Microbial Metabolism Lab, University XYZ"
date_performed: "2023-09-15"
date_analyzed: "2023-09-20"
```

---

## 13. Integration with Other Standards

### 13.1 Complete Data Package

A complete biotransformation study submission includes:

```
Study Package
├── MIX-MB(X) - Xenobiotics
│   ├── COMPOUND_RECORD.tsv
│   ├── COMPOUND_CTAB.sdf
│   └── Chemical structures
│
├── MIX-MB(M) - Microbes  
│   ├── Organism metadata
│   ├── Growth conditions
│   └── Culture information
│
├── MIX-MB(B) - Biotransformation (THIS STANDARD)
│   ├── ASSAY.tsv
│   ├── ASSAY_PARAM.tsv
│   ├── ACTIVITY.tsv
│   └── Experimental details
│
├── REFERENCE.tsv
│   └── Publication metadata
│
└── Raw Data
    ├── LC-MS data (mzML)
    ├── NMR data (nmrML)
    └── Analysis scripts
```

### 13.2 Cross-Referencing

**Linking Strategy:**
```yaml
cross_references:
  substrate:
    cidx: "C001"
    from_standard: "MIX-MB(X)"
    file: "COMPOUND_RECORD.tsv"
    
  organism:
    organism_id: "ORG_001"
    ncbi_taxid: 511145
    from_standard: "MIX-MB(M)"
    
  assay:
    aidx: "A001"
    links_to: ["C001", "ORG_001"]
    from_standard: "MIX-MB(B)"
    file: "ASSAY.tsv"
    
  activity:
    links_assay: "A001"
    links_compound: "C001"
    from_standard: "MIX-MB(B)"
    file: "ACTIVITY.tsv"
```


---

## 15. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-05 | Initial draft: Core biotransformation standards |

---

## 16. References

1. ChEMBL Bioactivity Database: https://www.ebi.ac.uk/chembl/
2. BioAssay Ontology (BAO): http://www.bioassayontology.org/
3. MSI Metabolomics Standards: https://metabolomicssociety.org/
4. STRENDA Guidelines: http://www.beilstein-strenda-db.org/
5. Gene Ontology: http://geneontology.org/
6. Chemical Methods Ontology: https://terminology.nfdi4chem.de/ts/ontologies/chmo
7. MetaboLights: https://www.ebi.ac.uk/metabolights/
8. GNPS: https://gnps.ucsd.edu/
9. mzML Standard: http://www.psidev.info/mzml
10. FAIR Principles: https://www.go-fair.org/fair-principles/

---

## 17. Contact and Contributions

For questions, suggestions, or contributions to this standard, please contact:
- **Maintainer:** Mahnoor Zulfiqar
- **Institution:** NFDI4Microbiota
- **Email:** [Contact information](mailto:zmahnoor14@gmail.com)
- **Repository:** [[GitHub repository URL](https://github.com/zmahnoor14/BioXend)]

This standard bridges MIX-MB(X) and MIX-MB(M) to provide comprehensive documentation of microbial xenobiotic biotransformation processes. It is a living document that will be updated based on community feedback and evolving best practices.

---

