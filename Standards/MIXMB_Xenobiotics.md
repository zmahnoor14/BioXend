# Minimum Information about Xenobiotics-Microbiome Biotransformation -- MIX-MB(X)

## Xenobiotics Component Standard (X)

This document identifies the Minimum Information (MI) required to report xenobiotics involved in microbial biotransformation studies, ensuring comprehensive documentation of chemical substrates and their transformation products.

**Author:** Mahnoor Zulfiqar
**Version:** 0.1.0  
**Release Date:** March 16, 2026 (Draft)  
**Status:** Draft Standard  
**Part of:** MIX-MB Standard v0.1  
**Replaces:** N/A  
**Compatible with:** 
- MIX-MB(M) v0.1.0
- MIX-MB(B) v0.1.0

**Alignment:** BioSchemas, ChEMBL, ChEBI, ChemONT, MSI Standards, FAIR principles

---

## Table of Contents

- [1. Overview](#1-overview)
  - [1.1 How is this document organised?](#11-how-is-this-document-organised)
  - [1.2 Which sections are important for contributors?](#12-which-sections-are-important-for-contributors)
  - [1.3 Which sections are important for data submitters?](#13-which-sections-are-important-for-data-submitters)
  - [1.4 Identifiers and Cross-Referencing](#14-identifiers-and-cross-referencing)
- [2. Bioschemas](#2-bioschemas)
  - [2.1 Xenobiotics — ChemicalSubstance Profile with Concentration](#21-xenobiotics----chemicalsubstance-profile-with-concentration)
  - [2.2 Products and Metabolites with MSI Levels](#22-products-and-metabolites-with-msi-levels)
  - [2.3 Concentration Documentation](#23-concentration-documentation)
- [3. Ontologies](#3-ontologies)
  - [3.1 ChEBI (Chemical Entities of Biological Interest)](#31-chebi-chemical-entities-of-biological-interest)
  - [3.2 ChemOnt (Chemical Ontology)](#32-chemont-chemical-ontology)
  - [3.3 Unit Ontology (UO)](#33-unit-ontology-uo)
  - [3.4 Gene Ontology (GO) — Biotransformation Processes](#34-gene-ontology-go---biotransformation-processes)
  - [3.5 MIX-MB Controlled Vocabularies](#35-mix-mb-controlled-vocabularies)
- [4. Data Validation Rules](#4-data-validation-rules)
- [5. Data Quality Tiers](#5-data-quality-tiers)
- [6. How to use the Template](#6-how-to-use-the-template)
- [7. Version History](#7-version-history)
- [8. References](#8-references)
- [9. Contact and Contributions](#9-contact-and-contributions)

---

## 1. Overview

MIX-MB(X) establishes minimum information standards for reporting microbial biotransformation of xenobiotics, ensuring data is:
- **Findable:** Properly annotated with identifiers and metadata
- **Accessible:** Standardized formats for submission to public repositories
- **Interoperable:** Uses community ontologies and controlled vocabularies
- **Reusable:** Provenance and methodology information

### 1.1 How is this document organised?
- **Section 1** — Introduction to MIX-MB(X) for Xenobiotics and how to use it.
- **Section 2** — Bioschemas profiles: what metadata fields to use for substrates and metabolites, with JSON examples.
- **Section 3** — Ontologies: which controlled vocabularies and identifiers to use (ChEBI, ChemOnt, GO, Unit Ontology).
- **Section 4** — Validation rules
- **Section 5** — Data quality tiers
- **Section 6** — How to use template
- 

### 1.2 Which sections are important for contributors?

If you want to propose changes to the standard, focus on **Sections 2 and 3** (the metadata fields and ontologies), then follow the contribution process in [Versioning.md](Versioning.md) and [CONTRIBUTING.md](../CONTRIBUTING.md). Changes require a 7-day community review and 2 independent endorsements.

### 1.3 Which sections are important for data submitters?

If you are preparing data for submission, you need:
- **Section 2.1** — required fields for xenobiotic substrates
- **Section 2.3** — how to report concentrations
- **Section 4.1** — what analytical information to include
- **Section 5** — validation checklist before you submit
- **[Template.xlsx](Templates/Template.xlsx)** — colour-coded submission template (green = mandatory, blue = recommended, yellow = optional) specifically the Compounds sheet.

### 1.4 Identifiers and Cross-Referencing

**This is the first practical step: name your compounds properly before filling in any other field.**

#### Compound Index (CIDX)

Each compound in a MIX-MB submission must be assigned a **CIDX** — a study-local identifier that ties together `COMPOUND_RECORD.tsv`, `COMPOUND_CTAB.sdf`, and `ACTIVITY.tsv`.

**Minting rules:**
- Format: `CIDX` followed by a zero-padded integer, e.g. `CIDX0001`, `CIDX0002`
- Assign sequentially within a study; CIDXs do not need to be globally unique
- Assign one CIDX per distinct chemical structure (identical canonical SMILES = same CIDX)
- For biotransformation products that are detected but not fully characterised, use the `UNKNOWN_` or `PUTATIVE_` prefix scheme (see below)

#### External Identifier Priority Order

When referencing a compound in an external database, use the following priority order:

| Priority | Identifier | Field | Example |
|----------|-----------|-------|---------|
| 1 | **InChIKey** | `inChIKey` | `HEFNNWSXXWATRW-UHFFFAOYSA-N` |
| 2 | **ChEMBL ID** | `identifier` | `CHEMBL1201246` |
| 3 | **PubChem CID** | `identifier` | `CID:4583` |
| 4 | **ChEBI ID** | `identifier` | `CHEBI:3686` |
| 5 | **CAS Number** | `additionalProperty` → `cas_number` | `42399-41-7` |

The **InChIKey** is the canonical structure identifier in MIX-MB and is **mandatory** for all known compounds. It identifies the chemical structure independently of naming conventions or database-specific numbering.

#### Minting Scheme for Unknown Compounds

For biotransformation products that cannot be fully identified at the time of submission, use the following naming convention:

| Situation | CIDX format | MSI Level | Example |
|-----------|------------|-----------|---------|
| Confirmed structure | `CIDX[nnnn]` | Level 1–2 | `CIDX0003` |
| Putatively characterised (structural class known) | `PUTATIVE_[RIDX]_[n]` | Level 3 | `PUTATIVE_GutMeta_P1` |
| Unknown (mass only, no formula or structure) | `UNKNOWN_[RIDX]_[n]` | Level 4–5 | `UNKNOWN_GutMeta_M3` |

- `[RIDX]` is the reference index for the study (e.g. `GutMeta`)
- `[n]` is a sequential integer within the study
- Once an unknown compound is formally identified, replace its `UNKNOWN_` CIDX with a standard CIDX and update all linked `ACTIVITY.tsv` rows accordingly

#### sameAs Linking Policy

Use the `sameAs` property to assert equivalence between a compound in your submission and the same compound in an external database. This is **required** for Gold-tier submissions and **strongly recommended** for Silver.

| Database | URL pattern | Example |
|----------|-----------|---------|
| ChEMBL | `https://www.ebi.ac.uk/chembl/compound_report_card/{ID}/` | `https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1201246/` |
| PubChem | `https://pubchem.ncbi.nlm.nih.gov/compound/{CID}` | `https://pubchem.ncbi.nlm.nih.gov/compound/4583` |
| ChEBI | `https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:{n}` | `https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:3686` |
| Wikidata | `https://www.wikidata.org/wiki/{QID}` | `https://www.wikidata.org/wiki/Q412690` |

**Rules:**
- Include at least one `sameAs` URL for every known compound
- For unknowns (`UNKNOWN_` / `PUTATIVE_` CIDXs), omit `sameAs` — do not add speculative links
- When a compound exists in multiple databases, list all confirmed `sameAs` URLs
- If a database entry is merged or deprecated, update `sameAs` to the canonical replacement URL

---

## 2. Bioschemas
MIX-MB(X) integrates already established standards such as BioSchema profile [Bioschemas ChemicalSubstance](https://bioschemas.org/types/ChemicalSubstance/) and [Bioschemas MolecularEntity](https://bioschemas.org/profiles/MolecularEntity/). BioSchemas fulfils Findability aspect of FAIR. 

**_NOTE:_** ChemicalSubstance is not inclusive of all fields present in the Bioschemas ChemicalSubstance Profile, some are specific to this use case.

### 2.1 Xenobiotics -- ChemicalSubstance Profile with Concentration

The parent compound or xenobiotic used within the research follows [Bioschemas ChemicalSubstance](https://bioschemas.org/types/ChemicalSubstance/) with concentration and sample information captured as properties:

**Required Properties:**
- `@context`: https://schema.org/
- `@type`: ChemicalSubstance
- `@id`: Globally unique IRI identifying the compound (e.g., canonical database URL such as `https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1201246/`)
- `dct:conformsTo`: https://bioschemas.org/profiles/ChemicalSubstance/0.4-RELEASE
- `identifier`: Compound identifier as Text, PropertyValue, or URL (e.g., ChEMBL ID, PubChem CID, InChI Key)
- `name`: Chemical name of the compound (Text)
- `url`: URL of the compound's entry in a reference database (e.g., ChEMBL, PubChem, ChEBI)
- `inChIKey`: Standard InChI Key
- `identifier`: Compound identifier (ChEMBL ID, PubChem CID, InChI Key)
- `smiles`: Canonical SMILES string *(MIX-MB extension)*
- `chemicalComposition`: Chemical formula (e.g: Molecular formula in this context)
- `molecularWeight`: Molecular weight with unit [Units should be included in the form ‘ ‘, for example ‘12 amu’.]

**Recommended Properties:**
- `alternateName`: An alias for the item (Text, MANY) — e.g., trade names, synonyms, preferred compound name
- `iupacName`: IUPAC systematic name *(from MolecularEntity profile, not ChemicalSubstance)*
- `monoisotopicMolecularWeight`: Exact monoisotopic mass *(from MolecularEntity profile, not ChemicalSubstance)*
- `chemicalRole`: A role played by the molecular entity within a chemical context (DefinedTerm, MANY) — use ChEBI terms e.g., xenobiotic, drug, metabolite
- `associatedDisease`: A disease associated with this BioChemEntity (MedicalCondition or URL, MANY)
- `bioChemInteraction`: A BioChemEntity this compound interacts with (BioChemEntity, MANY) — e.g., drug targets, enzymes, receptors
- `bioChemSimilarity`: A similar BioChemEntity, e.g., obtained by fingerprint similarity algorithms (BioChemEntity, MANY)
- `biologicalRole`: A role played by the BioChemEntity within a biological context (DefinedTerm, MANY) — use ChEBI terms e.g., enzyme inhibitor, antimicrobial agent
- `description`: A free-text description of the item (Text, ONE)
- `disambiguatingDescription`: A short description used to disambiguate from other similar items (Text, ONE)
- `image`: A structural image of the compound (ImageObject or URL, MANY) — e.g., 2D/3D depiction
- `potentialUse`: Intended use of the BioChemEntity by humans (DefinedTerm, MANY) — e.g., pharmaceutical, pesticide, food additive
- `sameAs`: URL of a reference web page that unambiguously indicates the item's identity in another database (URL, MANY)

**Sample Properties (using `additionalProperty`) not available in the ChemicalSubstance Profile:**
- `cas_number`: CAS Registry Number of the compound
- `vendor`: Supplier/vendor who provided the compound (e.g., Sigma-Aldrich, TCI)
- `purity`: Purity percentage and measurement method (e.g., ≥98%, HPLC)
- `solubility`: Solubility information (solvent, concentration limit)
- `stock_concentration`: Stock solution concentration with unit and solvent
- `stock_solvent`: Solvent used to prepare the stock solution (e.g., DMSO, ethanol, water)
- `storage_conditions`: Storage conditions and stability notes (e.g., -20°C, protect from light)
- `local_synonym`: Local study-specific synonym or identifier used in the manuscript (e.g., compound 23)

**Analytical Detection Properties (using `additionalProperty`):**
- `mz`: Measured m/z value of the compound or eluted form
- `column_separation`: Separation technique used (e.g., LC, GC)
- `retention_time`: Retention time recorded during separation
- `retention_time_unit`: Unit for retention time (sec, min, hr)
- `eluted_compound`: Whether the eluted compound differs from the original (e.g., yes for salts where MS detects the active form)
- `eluted_compound_smiles`: SMILES of the eluted compound if different from the original

**_NOTE:_** This profile goes to the `COMPOUNDS_RECORD.tsv`, `COMPOUNDS_CTAB.sdf`, `ASSAY.tsv` and `ASSAY_PARAM.tsv` files for ChEMBL submission.

### 2.2 Products and Metabolites with MSI Levels

For biotransformation products characterised with mass spectrometry (MS), use the same **MolecularEntity profile** with **MSI identification confidence levels** to indicate the degree of characterization. This profile is optional and is only important in case if a xenobiotics product is measured and detected. 

**MSI Level Guidelines:**

Levels 1–5 follow the updated standard [Metabolomics Standards Initiative (MSI)](https://metabolomicssociety.org/resources/metabolomics-standards-initiative) scheme.

| Level | Description | Confidence | Required Information | Example |
|-------|-------------|------------|----------------------|---------|
| **Level 1** | Identified | Highest | Authenticated with authentic reference standard | HMDB ID, exact retention time match, MS² match to standard |
| **Level 2** | Putatively annotated | High | Library or database match with MS² similarity | MS² similarity >0.8, retention index agreement, spectral match to database |
| **Level 3** | Putatively characterized | Medium | Chemical class identified, partial structure known | Molecular formula confirmed, functional group identified, structure class known |
| **Level 4** | Unknown | Low | Minimal structural information | Exact mass only, no formula or structural information |
| **Level 5** | Unidentified | Unknown | Spectral data only, no structural hypothesis | Mass peak at m/z 254.1154, no formula or structure information |


**Required Properties (for all levels):**
- `@context`: https://schema.org/
- `@type`: MolecularEntity
- `@id`: Globally unique IRI identifying the product (e.g., canonical database URL, or a study-local URI for unknowns such as `#UNKNOWN_M3`)
- `dct:conformsTo`: https://bioschemas.org/profiles/MolecularEntity/0.7-DRAFT
- `molecularWeight`: Molecular weight with unit (QuantitativeValue or Text, ONE) — use UO unit codes (see Section 3.3); *Recommended in profile, Required for MIX-MB*
- `identifier`: Product identifier as DefinedTerm, PropertyValue, Text, or URL (use `UNKNOWN_` prefix for unknowns)
- `isPartOfBioChemEntity`: Reference to the parent xenobiotic (BioChemEntity, MANY)
- `chemicalRole`: Must include "metabolite" and/or "biotransformation product" (DefinedTerm, MANY) — use ChEBI terms
- `additionalProperty`: Must include MSI identification level (PropertyValue)

**Recommended Properties (if known):**
- `inChIKey`: Hashed InChI identifier (Text, ONE) — *Recommended in profile*
- `iupacName`: IUPAC systematic name (Text, ONE) — *Recommended in profile*
- `molecularFormula`: Molecular formula (Text, ONE) — *Recommended in profile*
- `molecularWeight`: Molecular weight with unit (QuantitativeValue or Text, ONE) — *Recommended in profile, Required for MIX-MB*
- `sameAs`: Reference URLs unambiguously indicating the product’s identity in other databases (URL, MANY) — *Recommended in profile*
- `alternateName`: Product name or systematic designation (Text, MANY)
- `associatedDisease`: A disease associated with this entity (MedicalCondition, PropertyValue, or URL, MANY)
- `bioChemInteraction`: A BioChemEntity this product interacts with (BioChemEntity, MANY)
- `bioChemSimilarity`: A similar molecular entity, e.g., obtained by fingerprint similarity algorithms (BioChemEntity, MANY)
- `biologicalRole`: A role played by the entity in a biological context (DefinedTerm, MANY) — use ChEBI terms
- `chemicalRole`: A role played by the molecular entity within a chemical context (DefinedTerm, MANY) — *Optional in profile, Required for MIX-MB*
- `description`: A free-text description of the product (Text, ONE)
- `disambiguatingDescription`: A short description to distinguish from similar items (Text, ONE)
- `hasBioChemEntityPart`: A BioChemEntity that (in some sense) has this entity as a part (BioChemEntity, MANY)
- `hasMolecularFunction`: Molecular function performed by this entity (DefinedTerm, PropertyValue, Text, or URL, MANY) — use GO terms
- `hasRepresentation`: A common representation of this entity such as a chemical structure or structural classification (DefinedTerm, PropertyValue, Text, or URL, MANY) — e.g., SMILES, InChI, or ChemOnt/ClassyFire class (see Section 3.2)
- `image`: A structural image of the compound (ImageObject or URL, MANY)
- `isEncodedByBioChemEntity`: A gene or BioChemEntity encoding this entity (Gene, MANY)
- `isInvolvedInBiologicalProcess`: Biological process this entity is involved in (DefinedTerm, PropertyValue, Text, or URL, MANY) — use GO terms (see Section 3.4)
- `isLocatedInSubcellularLocation`: Subcellular location where this entity is located (DefinedTerm, PropertyValue, Text, or URL, MANY)
- `isPartOfBioChemEntity`: The parent BioChemEntity this entity is a part of (BioChemEntity, MANY) — *Optional in profile, Required for MIX-MB*
- `monoisotopicMolecularWeight`: Exact monoisotopic mass (QuantitativeValue or Text, ONE)
- `potentialUse`: Intended use of the entity by humans (DefinedTerm, MANY)
- `subjectOf`: A CreativeWork or Event about this entity (CreativeWork or Event, MANY) — e.g., publication, dataset
- `taxonomicRange`: Taxonomic grouping of the organism that expresses or relates to this entity (DefinedTerm, Taxon, Text, or URL, MANY)

**Analytical Detection Properties (using `additionalProperty`):**

*Required for all MSI levels:*
- `MSI_level`: MSI identification confidence level assigned to this product (Level 1–5; see MSI Level Guidelines above)
- `mz`: Measured m/z value of the detected ion
- `adduct_type`: Ion adduct form detected (e.g., [M+H]+, [M-H]-, [M+Na]+, [M+NH4]+)
- `ionization_mode`: Ionization mode used (e.g., ESI positive, ESI negative, APCI)
- `mass_accuracy_ppm`: Mass measurement accuracy relative to theoretical mass (parts per million)
- `retention_time`: Retention time recorded during chromatographic separation
- `retention_time_unit`: Unit for retention time (sec, min, hr)
- `signal_to_noise`: Signal-to-noise ratio of the detected peak
- `detection_frequency`: Number of replicates in which the compound was detected (e.g., 3/3)
- `transformation_type`: Type of biotransformation from the parent compound (use controlled vocabulary from Section 3.5)
- `mass_difference_from_parent`: Exact mass difference from the parent xenobiotic (e.g., +15.9949 Da for hydroxylation)

*Level 1 (Identified) — additional required:*
- `reference_standard`: Authentic reference standard used for confirmation (supplier, catalog number)
- `retention_time_match`: Retention time difference compared to the authentic reference standard (with unit)
- `ms2_similarity_score`: MS/MS spectral similarity score vs the reference standard spectrum (0–1)

*Level 2 (Putatively annotated) — additional required:*
- `ms2_similarity_score`: MS/MS spectral similarity score vs matched library spectrum (e.g., cosine similarity ≥ 0.7)
- `spectral_library`: Spectral library used for matching (e.g., GNPS, MassBank, HMDB, mzCloud)
- `library_match_id`: Identifier of the matched library spectrum (e.g., GNPS accession, MassBank ID)
- `retention_index_match`: Agreement between experimental and literature retention index (if applicable)

*Level 3 (Putatively characterized) — additional required:*
- `structural_hypothesis`: Proposed structural class or transformation type (e.g., double hydroxylation at aliphatic chain)
- `fragment_pattern`: Key fragment ions supporting the structural assignment (e.g., m/z 177, 159, 137)
- `chemont_class`: ClassyFire/ChemOnt structural classification of the putative compound (use in `hasRepresentation`; maps to template `Metabolite_annotation` column) — e.g., "Phenylpropanoic acids", "Dihydroxylated phenylpropionic acid"; see Section 3.2

*Level 4/5 (Unknown/Unidentified) — additional required:*
- `ms2_available`: Whether an MS/MS spectrum was acquired for this signal (yes/no)
- `possible_molecular_formula`: Proposed molecular formula derived from accurate mass measurement (± ppm tolerance)
- `detection_consistency`: Number of replicates with a confirmed signal (e.g., 2 out of 3)

**_NOTE:_** This profile goes to the `ASSAY.tsv` and `ACTIVITY.tsv` files for ChEMBL submission.

### 2.3 Concentration Documentation

Concentration is documented using `additionalProperty` (PropertyValue) for both substrates (Section 2.1) and biotransformation products (Section 2.2). All five properties below apply to both, though `initial_concentration` and `stock_concentration` are most relevant to substrates, while `final_concentration` and `concentration_change` are most relevant to products.

| Property | Description | Recommended Units | Example |
|---|---|---|---|
| `stock_concentration` | Concentration of the compound in the prepared stock solution, before dilution into the assay medium | mmol/L, mg/mL, µg/µL | 100 mmol/L in DMSO |
| `initial_concentration` | Starting concentration of the compound in the assay at time zero (t=0), after dilution from stock | µM, µg/mL, mmol/L | 50 µM |
| `final_concentration` | Measured concentration of the compound (substrate remaining or product formed) at the experimental endpoint or a defined timepoint | µM, µg/mL, nmol/L | 2.5 µM at 24 h |
| `concentration_change` | Absolute or relative change in concentration compared to the initial value — use to report substrate degradation or product formation | µM, %, fold-change | 95% degradation; +45.2 µM product |
| `detection_limit` | Lower limit of quantitation (LLOQ) for the analytical method used; signals below this value should not be reported as quantified | nmol/L, µg/mL, ppm | 10 nM |

---

## 3. Ontologies

### 3.1 ChEBI (Chemical Entities of Biological Interest)

**Required ChEBI Classifications:**
- **Chemical Role** (`chemicalRole`): Intrinsic chemical role of the compound (e.g., CHEBI:50906 'xenobiotic', CHEBI:25212 'metabolite') — for biotransformation products (§2.2), must include CHEBI:25212 'metabolite'
- **Biological Role** (`biologicalRole`): How the compound functions in a biological context (e.g., CHEBI:38439 'calcium channel blocker', CHEBI:33281 'antimicrobial agent', CHEBI:35222 'inhibitor')
- **Application** (`potentialUse`): Intended therapeutic or practical use (e.g., CHEBI:35610 'drug', CHEBI:49295 'pharmaceutical', CHEBI:35842 'analgesic')

**Example Annotations:**
```
Diltiazem (substrate):
  Chemical Role:   CHEBI:3686 (diltiazem), CHEBI:50906 (xenobiotic)
  Biological Role: CHEBI:38439 (calcium channel blocker)
  Application:     CHEBI:35474 (antihypertensive agent), CHEBI:35498 (antiarrhythmic drug)

N-desmethyldiltiazem (biotransformation product):
  Chemical Role:   CHEBI:25212 (metabolite)
  Biological Role: CHEBI:38439 (calcium channel blocker)
```

### 3.2 ChemOnt (Chemical Ontology)

Use [ClassyFire Chemical Ontology](http://classyfire.wishartlab.com/) for structural classification:

**Required Levels:**
1. **Kingdom:** Highest level (e.g., Organic compounds, Inorganic compounds)
2. **Superclass:** Major structural category (e.g., Organoheterocyclic compounds)
3. **Class:** Structural class (e.g., Benzene and substituted derivatives)
4. **Subclass:** Detailed structural features (optional)

**Example:**
```
Diltiazem:
  Kingdom: Organic compounds
  Superclass: Organoheterocyclic compounds
  Class: Benzothiazepines
  Subclass: 1,5-Benzothiazepines
  Direct Parent: 1,5-Benzothiazepines
```

### 3.3 Unit Ontology (UO)

Use [Unit Ontology](https://bioportal.bioontology.org/ontologies/UO) for standardized unit codes in quantitative measurements. UO ensures interoperability of measurement data across databases and computational tools.

**Required Unit Codes:**
- **Mass:** `GM` (gram), `DA` (dalton), `MGM` (milligram), `UGM` (microgram)
- **Volume:** `ML` (milliliter), `UL` (microliter), `NL` (nanoliter)
- **Concentration:** `MMO` (millimolar), `UMO` (micromolar), `NMO` (nanomolar), `PMO` (picomolar)
- **Time:** `MIN` (minute), `HOUR` (hour), `DAY` (day), `SEC` (second)
- **Temperature:** `CEL` (degree Celsius), `DEK` (kelvin)
- **pH:** Dimensionless (no unit code)
- **Percentage:** `%` (percent)

**Example - Concentration and Quantitation Units:**
```yaml
concentrations:
  stock_concentration:
    value: 100
    unitCode: MMO
    description: "millimolar (mmol/L)"
  
  metabolite_concentration:
    value: 45.2
    unitCode: UMO
    description: "micromolar (µM)"
  
  exact_mass:
    value: 222.1256
    unitCode: DA
    description: "dalton (unified atomic mass unit)"
  
  molecular_weight:
    value: 206.28
    unitCode: GM
    description: "gram per mole (g/mol)"
  
  retention_time:
    value: 4.32
    unitCode: MIN
    description: "minute"
  
  substrate_degradation:
    value: 95
    unitCode: "%"
    description: "percent"
```


### 3.4 Gene Ontology (GO) - Biotransformation Processes

Use [Gene Ontology](http://geneontology.org/) to classify biotransformation processes and enzymatic reactions. GO provides standardized terms for biological processes that enable semantic linking with genomic and proteomic data.

**Phase I - Oxidation/Reduction/Hydrolysis Terms:**
Phase I refers to the xenobiotics modification via common enzymatics reactions such as oxidation, reduction and hydrolysis
- GO:0018126 (hydroxylation)
- GO:0055114 (oxidation-reduction)
- GO:0004435 (phosphodiesterase activity)
- GO:0008941 (glucuronidase activity - Phase II)

**Phase II - Conjugation Terms:**
Phase II refers to the further modification of the xenobiotics metabolite from phase I, via conjugation of methyl, glycosul, alkyl or sulfide groups. 
- GO:0016757 (transferase activity, transferring glycosyl groups)
- GO:0008194 (UDP-glycosyltransferase activity)
- GO:0016620 (transferase activity, transferring alkyl or aryl groups)
- GO:0008146 (sulfotransferase activity)

**Common Biotransformation GO Terms Reference:**

| Transformation | GO Term | GO ID |
|---|---|---|
| Hydroxylation | Hydroxylation | GO:0018126 |
| Glucuronidation | UDP-glucuronosyltransferase activity | GO:0008194 |
| Sulfation | Sulfotransferase activity | GO:0008146 |
| Acetylation | Acetyltransferase activity | GO:0016408 |
| Oxidation | Oxidation-reduction process | GO:0055114 |
| Reduction | Oxidation-reduction process | GO:0055114 |
| Hydrolysis | Hydrolase activity | GO:0016787 |
| Deamination | Protein deamination | GO:0018133 |
| Conjugation | Transferase activity | GO:0016757 |
| Methylation | Methyltransferase activity | GO:0008168 |

### 3.5 MIX-MB Controlled Vocabularies

These terms must be used exactly as written to ensure consistency across submissions.

**Transformation types** (use in `additionalProperty` → `transformation_type`, and in template `Reaction_type` column):

These terms map directly to GO terms (see Section 3.4). Use the MIX-MB term as the `value` and the GO URI as `valueReference` when expressing in JSON-LD.

| MIX-MB Term | Description | GO ID | GO URI |
|---|---|---|---|
| `hydroxylation` | Addition of -OH group | GO:0018126 | http://purl.obolibrary.org/obo/GO_0018126 |
| `oxidation` | Oxidation reaction | GO:0055114 | http://purl.obolibrary.org/obo/GO_0055114 |
| `reduction` | Reduction reaction | GO:0055114 | http://purl.obolibrary.org/obo/GO_0055114 |
| `hydrolysis` | Hydrolytic cleavage | GO:0016787 | http://purl.obolibrary.org/obo/GO_0016787 |
| `decarboxylation` | Loss of CO₂ | GO:0017001 | http://purl.obolibrary.org/obo/GO_0017001 |
| `deamination` | Loss of amino group | GO:0018133 | http://purl.obolibrary.org/obo/GO_0018133 |
| `conjugation` | Addition of a larger molecular group | GO:0016757 | http://purl.obolibrary.org/obo/GO_0016757 |
| `demethylation` | Loss of methyl group | GO:0032259 | http://purl.obolibrary.org/obo/GO_0032259 |
| `acetylation` | Addition of acetyl group | GO:0016408 | http://purl.obolibrary.org/obo/GO_0016408 |
| `glucuronidation` | Addition of glucuronic acid | GO:0008194 | http://purl.obolibrary.org/obo/GO_0008194 |
| `sulfation` | Addition of sulfate group | GO:0008146 | http://purl.obolibrary.org/obo/GO_0008146 |

**Activity ACTION_TYPE** (use in ACTIVITY.tsv):

| Term | Meaning |
|------|---------|
| `Biotransformation` | General transformation event |
| `Substrate` | Compound consumed in the reaction |
| `Product` | Compound produced by the reaction |
| `No Activity` | No biotransformation detected |

<to be updated>

---


## 4. Data Validation Rules

Before submitting data, verify that all compound records pass the following checks. The pipeline (`generate_compound_files.py`) performs these checks automatically; they also apply to manually prepared submissions.

### 4.1 Structural Identifiers

| Rule | Check |
|------|-------|
| SMILES is present | Every compound must have a non-empty canonical SMILES string |
| SMILES is valid | SMILES must parse without errors (use RDKit or OpenBabel to verify) |
| InChIKey is present | Mandatory for all known compounds (MSI Level 1–2) |
| InChIKey format | Must match the pattern `[A-Z]{14}-[A-Z]{10}-[A-Z]` (27 characters) |
| SMILES–InChIKey consistency | InChIKey must be derivable from the provided SMILES (no manual mismatches) |

### 4.2 Compound Index (CIDX)

| Rule | Check |
|------|-------|
| CIDX is present | Every row in `COMPOUND_RECORD.tsv` must have a CIDX |
| CIDX format | Must follow `CIDX` + zero-padded integer, e.g. `CIDX0001` |
| CIDX uniqueness | Each CIDX must be unique within the study |
| Unknown prefix | Uncharacterised compounds must use `UNKNOWN_[RIDX]_[n]` or `PUTATIVE_[RIDX]_[n]` — never a bare CIDX |

### 4.3 Required Fields

The following fields must be non-empty in `COMPOUND_RECORD.tsv` for every compound:

- `CIDX`, `RIDX`, `COMPOUND_NAME`

The following fields must be non-empty in `COMPOUND_CTAB.sdf` for every compound:

- Canonical SMILES, InChI, InChIKey, CIDX (as SDF property tag)

### 4.4 Concentration and Units

| Rule | Check |
|------|-------|
| Unit codes are standardised | All concentration values must use UO unit codes (see Section 3.3): `MMO`, `UMO`, `NMO`, etc. |
| Numeric values are positive | Concentration, molecular weight, and retention time values must be > 0 |
| Detection limit is provided | If quantitative data are reported, `detection_limit` should be included |

### 4.5 MSI Level Consistency

| MSI Level | Required fields |
|-----------|----------------|
| Level 1 | InChIKey, `reference_standard`, `ms2_similarity_score`, `retention_time_match` |
| Level 2 | InChIKey, `ms2_similarity_score`, `spectral_library`, `library_match_id` |
| Level 3 | `structural_hypothesis`, `fragment_pattern`, `chemont_class` |
| Level 4/5 | `mz`, `ms2_available`, `detection_consistency` |

---

## 5. Data Quality Tiers

MIX-MB(X) defines three compliance tiers for xenobiotic compound data. Higher tiers enable broader reuse, database cross-linking, and publication in FAIR-compliant repositories.

### Tier 1 — Gold (Publication-Ready)

Meets all mandatory and recommended fields. Suitable for ChEMBL submission and FAIR data publications.

- InChIKey present and verified against SMILES
- At least one external database ID (ChEMBL, PubChem, or ChEBI)
- `sameAs` links provided for all known compounds
- Full Bioschemas ChemicalSubstance JSON-LD record (Section 2.1)
- Purity, vendor, and stock concentration documented
- Concentration data complete: initial, final, and detection limit
- For detected products: MSI Level 1 or 2 with full analytical evidence

### Tier 2 — Silver (Research-Grade)

Meets all mandatory fields with partial recommended fields. Suitable for internal data sharing and preprint deposition.

- InChIKey present
- At least one external database ID
- `COMPOUND_NAME`, `SMILES`, `CIDX`, `RIDX` all present
- Initial substrate concentration documented
- For detected products: MSI Level 2 or 3 acceptable

### Tier 3 — Bronze (Preliminary / Screening)

Meets only mandatory fields. Suitable for large-scale screening data where full characterisation is not yet possible.

- Valid SMILES and `COMPOUND_NAME` present
- `CIDX` and `RIDX` assigned
- Qualitative activity reported (substrate consumed / product detected / no activity)
- Single measurement acceptable; full replication not required at this tier

---


## 6. How to use the Template

The MIX-MB submission template is provided as [Templates/Template.xlsx](Templates/Template.xlsx). The **Compounds** sheet covers the MIX-MB(X) standard.

### Colour coding

| Colour | Meaning |
|--------|---------|
| Green | Mandatory — must be filled for a valid submission |
| Blue | Recommended — strongly encouraged; required for Tier 1 (Gold) |
| Yellow | Optional — fill if available |

### Step-by-step

1. **Open** `Template.xlsx` and go to the **Compounds** sheet.
2. **Add one row per compound.** If the same compound appears in multiple assays, it still gets only one row here — the link to assays is made in the Activity sheet.
3. **Fill in the CIDX** — assign sequentially (`CIDX0001`, `CIDX0002`, …). Use `UNKNOWN_` or `PUTATIVE_` prefixes for uncharacterised compounds (see Section 1.4).
4. **Fill in the SMILES.** Use canonical SMILES. If you have a structure drawn in ChemDraw or Marvin, export as canonical SMILES.
5. **Generate the InChIKey** from the SMILES using any of the following:
   - Python/RDKit: `Chem.MolToInchi(mol)` → `inchi.InchiToInchiKey(inchi)`
   - Online: [https://www.cheminfo.org/Chemistry/Cheminformatics/FormatConverter/index.html](https://www.cheminfo.org/Chemistry/Cheminformatics/FormatConverter/index.html)
6. **Look up external database IDs** using the InChIKey:
   - ChEMBL: search by InChIKey at [ebi.ac.uk/chembl](https://www.ebi.ac.uk/chembl/)
   - PubChem: search at [pubchem.ncbi.nlm.nih.gov](https://pubchem.ncbi.nlm.nih.gov/)
7. **Fill in concentration fields** (stock, initial, units) using UO unit codes (Section 3.3).
8. **For biotransformation products,** go to the **Metabolites** sub-section and assign an MSI level before filling in the analytical detection fields.
9. **Validate** your completed sheet against the rules in Section 4 before running the pipeline or submitting.



## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-05 | Draft |

---

## 8. References
1. ChEMBL Database Guidelines: https://www.ebi.ac.uk/chembl/
2. Metabolomics Standards Initiative: https://metabolomicssociety.org/resources/metabolomics-standards-initiative
3. Bioschemas Specifications: https://bioschemas.org/
4. ChEBI Ontology: https://www.ebi.ac.uk/chebi/
5. ClassyFire Chemical Taxonomy: http://classyfire.wishartlab.com/
6. Gene Ontology: http://geneontology.org/
7. FAIR Principles: https://www.go-fair.org/fair-principles/
8. Unit Ontology: https://bioportal.bioontology.org/ontologies/UO

---


## 9. Contact and Contributions

For questions, suggestions, or contributions to this standard, please contact:
- **Maintainer:** Mahnoor Zulfiqar
- **Institution:** NFDI4Microbiota
- **Email:** [Contact information](mailto:zmahnoor14@gmail.com)
- **Repository:** [[GitHub repository URL](https://github.com/zmahnoor14/BioXend)]

This standard is a living document and will be updated based on community feedback and evolving best practices.