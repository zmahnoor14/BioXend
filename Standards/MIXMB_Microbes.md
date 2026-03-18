# Minimum Information about Xenobiotics-Microbiome Biotransformation -- MIX-MB(M)

## Microbial Component Standards (M)

This document identifies Minimum Information (MI) required to report microbial organisms involved in biotransformation of xenobiotics, ensuring comprehensive documentation of bacterial, and archaeal species/strains used in biotransformation studies and information on the assays.

**Author:** Mahnoor Zulfiqar

**Part of:** MIX-MB Standard_main      
**Compatible with:** 
- MIX-MB(X) 
- MIX-MB(B) 
**Alignment:** NCBI Taxonomy, MIxS, ChEMBL, FAIR principles

---

## Table of Contents

- [1. Overview](#1-overview)
  - [1.4 Identifiers and Cross-Referencing](#14-identifiers-and-cross-referencing)
- [2. Bioschemas](#2-bioschemas)
  - [2.1 Taxon Profile](#21-taxon-profile)
  - [2.2 TaxonName Profile](#22-taxonname-profile)
  - [2.3 Sample Profile](#23-sample-profile)
  - [2.4 Gene Profile](#24-gene-profile)
  - [2.5 Protein Profile](#25-protein-profile)
  - [2.6 ProteinAnnotation Profile](#26-proteinannotation-profile)
- [3. Ontologies and Standards](#3-ontologies-and-standards)
  - [3.1 NCBI Taxonomy](#31-ncbi-taxonomy)
  - [3.2 Additional Ontology Requirements](#32-additional-ontology-requirements)
  - [3.3 MIxS (Minimum Information about any Sequence)](#33-mixs-minimum-information-about-any-sequence)
  - [3.4 Environment Ontology (ENVO)](#34-environment-ontology-envo)
  - [3.5 Phenotype Ontology (PATO/OMP)](#35-phenotype-ontology-patoomp)
  - [3.6 Gene Ontology (GO) & Enzyme Commission (EC)](#36-gene-ontology-go--enzyme-commission-ec)
  - [3.7 Antibiotic Resistance Ontology (ARO)](#37-antibiotic-resistance-ontology-aro)
- [7. Controlled Vocabularies](#7-controlled-vocabularies)
  - [7.1 Oxygen Requirements](#71-oxygen-requirements)
  - [7.2 Cell Morphology](#72-cell-morphology)
  - [7.3 Sample Types](#73-sample-types)
  - [7.4 Growth Phases](#74-growth-phases)
- [4. Data Validation Rules](#4-data-validation-rules)
- [5. Data Quality Tiers](#5-data-quality-tiers)
- [8. Data Access and Repository Guidance](#8-data-access-and-repository-guidance)
- [9. Licence and Reuse](#9-licence-and-reuse)
- [10. Provenance](#10-provenance)
- [11. References](#11-references)
- [12. Contact and Contributions](#12-contact-and-contributions)

---

## 1. Overview

MIX-MB(M) establishes minimum information standards for reporting microbial organisms in xenobiotic biotransformation studies, ensuring data is:
- **Findable:** Properly annotated with taxonomic identifiers and strain information
- **Accessible:** Standardized formats compatible with public databases
- **Interoperable:** Uses community ontologies and controlled vocabularies
- **Reusable:** Complete provenance, cultivation, and experimental conditions



### 1.4 Identifiers and Cross-Referencing

**This is the first practical step: name your organisms properly before filling in any other field.**

#### Organism Identifiers

Each microbial organism in a MIX-MB submission must be identified with an **NCBI TaxID** — the primary organism identifier used across all MIX-MB files. This value populates `ASSAY_TAX_ID` in `ASSAY.tsv`.

**Identifier priority order:**

| Priority | Identifier | Field | Example |
|----------|-----------|-------|---------|
| 1 | **NCBI TaxID** | `identifier` / `ASSAY_TAX_ID` | `1351` |
| 2 | **LPSN scientific name** | `name` / `ASSAY_ORGANISM` | `Enterococcus faecalis` |
| 3 | **Culture collection ID** | `additionalProperty` → `culture_collection` | `ATCC 19433` |
| 4 | **Genome assembly accession** | `additionalProperty` → `genome_assembly` | `GCA_000007785.1` |

NCBI TaxID is **mandatory** for all organisms. If a strain does not yet have a registered TaxID (e.g. a novel isolate), report at the lowest available taxonomic rank and note the absence of a strain-level TaxID in `ACTIVITY_COMMENT`.

#### Assay Index (AIDX)

Each assay — representing one organism × condition combination × type — is assigned an **AIDX**, which links `ASSAY.tsv`, `ASSAY_PARAM.tsv`, and `ACTIVITY.tsv`.

**Minting rules:**
- Format: `[FirstAuthorLastName]_[Genus]_[species]_[ConditionOrNote]_[type]`, e.g. `Zimmermann_Actinomyces_graevenitzii_anaerobic_biotransformation`
- AIDXs must be unique within a study
- Use only ASCII letters, digits, underscores, and hyphens — no spaces
- add protein ID, if its an enzyme assay
- Each distinct organism–condition combination gets its own AIDX; do not reuse AIDXs across
 different strain batches or oxygen conditions

#### Minting Scheme for Uncharacterised or Novel Organisms

| Situation | AIDX format | `ASSAY_ORGANISM` value | `ASSAY_TAX_ID` |
|-----------|------------|----------------------|----------------|
| Known species, known strain | `[Author]_[Genus]_[species]_[Strain]` | Full binomial name | Registered species TaxID |
| Known species, undesignated strain | `[Author]_[Genus]_[species]_unknown_strain` | Full binomial name | Species-level TaxID |
| Novel isolate (unclassified) | `[Author]_unclassified_[IsolateID]` | `unclassified bacteria` | `2` (root Bacteria) or closest assigned TaxID |
| Mixed / community assay | `[Author]_mixed_community_[SourceDescription]` | `mixed microbial community` | `1` (root) or metagenome TaxID |

---

## 2. Bioschemas

MIX-MB(M) integrates established Bioschemas profiles for structured, FAIR-compliant annotation of microbial organisms, strains, and their biotransformation-relevant molecular components. Bioschemas fulfils the Findability and Interoperability aspects of FAIR.

The following profiles are used:

| Profile | Bioschemas Group | Version | Use in MIX-MB(M) |
|---------|-----------------|---------|------------------|
| [Taxon](https://bioschemas.org/profiles/Taxon/1.0-RELEASE) | Biodiversity | 1.0-RELEASE | Organism taxonomy identification |
| [TaxonName](https://bioschemas.org/profiles/TaxonName/1.0-RELEASE) | Biodiversity | 1.0-RELEASE | Structured scientific name representation |
| [Sample](https://bioschemas.org/profiles/Sample/0.2-RELEASE-2018_11_10) | Samples | 0.2-RELEASE | Microbial culture sample metadata |
| [Gene](https://bioschemas.org/profiles/Gene/1.0-RELEASE) | Genes | 1.0-RELEASE | Biotransformation-related genes |
| [Protein](https://bioschemas.org/profiles/Protein/0.11-RELEASE) | Proteins | 0.11-RELEASE | Biotransformation enzymes |
| [ProteinAnnotation](https://bioschemas.org/profiles/ProteinAnnotation/0.6-DRAFT) | Proteins | 0.6-DRAFT | Enzyme functional annotations |

**_NOTE:_** Taxon, TaxonName, and Sample profiles map to the `ASSAY.tsv` and `ASSAY_PARAM.tsv` ChEMBL submission files. Gene, Protein, and ProteinAnnotation profiles are for extended metadata (Section 6.2) and are optional but strongly recommended for Gold-standard submissions.

---

### 2.1 Taxon Profile

Use [Bioschemas Taxon 1.0-RELEASE](https://bioschemas.org/profiles/Taxon/1.0-RELEASE) to identify and classify the microbial organism involved in the biotransformation study.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"Taxon"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., NCBI Taxonomy URL) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/Taxon/1.0-RELEASE"` |
| `name` | Text | ONE | Currently valid scientific name for the taxon |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `taxonRank` | PropertyValue, Text, URL | MANY | Taxonomic rank, preferably as URI from a controlled vocabulary |
| `parentTaxon` | Taxon, Text, URL | ONE | Closest parent taxon |
| `sameAs` | URL | MANY | Reference URLs identifying the taxon (NCBI, Wikidata, etc.) |
| `scientificName` | TaxonName | ONE | Structured TaxonName object (see Section 2.2) |

**Optional Properties (MIX-MB(M) relevant):**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `identifier` | PropertyValue, Text, URL | ONE | Authority identifier (e.g., NCBI TaxID, GBIF) |
| `alternateName` | Text | MANY | Synonyms or former names |
| `alternateScientificName` | TaxonName | MANY | Synonym scientific names |
| `childTaxon` | Taxon, Text, URL | MANY | Known subspecies or strains |
| `dwc:vernacularName` | Text | MANY | Common name (e.g., "E. coli") |
| `url` | URL | ONE | Link to the taxon record in a reference database |
| `description` | Text | ONE | Free-text description of the taxon |

**_NOTE:_** `name` and `identifier` from this profile map directly to `ASSAY_ORGANISM` and `ASSAY_TAX_ID` in `ASSAY.tsv`.

---

### 2.2 TaxonName Profile

Use [Bioschemas TaxonName 1.0-RELEASE](https://bioschemas.org/profiles/TaxonName/1.0-RELEASE) as a structured representation of the organism's scientific name — used as the value of `scientificName` in Section 2.1.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"TaxonName"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., LPSN URL) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/TaxonName/1.0-RELEASE"` |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `name` | Text | ONE | Taxon name without authorship or date information |
| `taxonRank` | PropertyValue, Text, URL | MANY | Taxonomic rank, preferably as URI |
| `author` | Person, Organization | MANY | Authorship and date details per nomenclatural rules |
| `sameAs` | URL | MANY | URLs to additional name records (LPSN, Index Fungorum, etc.) |
| `url` | URL | ONE | Webpage for this taxon name record |

**Optional Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `identifier` | PropertyValue, Text, URL | ONE | Authority identifiers (GBIF, WoRMS, etc.) |
| `isBasedOn` | CreativeWork, Product, URL | MANY | Publication or resource underlying this name |
| `description` | Text | ONE | Description of the name or nomenclatural context |


---

### 2.3 Sample Profile

Use [Bioschemas Sample 0.2-RELEASE](https://bioschemas.org/profiles/Sample/0.2-RELEASE-2018_11_10) for individual microbial culture samples used in biotransformation assays. Each sample represents a specific strain in a specific cultivation condition.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"Sample"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., NCBI BioSample URL) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/Sample/0.2-RELEASE-2018_11_10"` |
| `identifier` | PropertyValue, Text, URL | MANY | Unique sample identifier (e.g., `biosample:SAMN12345`, AIDX) |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `url` | URL | ONE | URL of the sample record in a database or biobank |

**Optional Properties (MIX-MB(M) relevant — use `additionalProperty`):**

| `additionalProperty` name | Value | Description |
|--------------------------|-------|-------------|
| `strain` | Text | Strain designation (e.g., K-12 substr. MG1655, ATCC 25922) |
| `culture_collection` | Text | Culture collection identifier (e.g., ATCC, DSMZ, CGSC) |
| `oxygen_requirement` | CV term | Oxygen condition (see Section 7.1 for controlled vocabulary) |
| `growth_medium` | Text | Medium name (e.g., BHI, M9 minimal medium, LB broth) |
| `incubation_temperature` | Text | Growth temperature with unit (e.g., "37°C") |
| `sample_type` | CV term | Sample type (see Section 7.3 for controlled vocabulary) |
| `harvest_phase` | CV term | Growth phase at harvest (see Section 7.4 for controlled vocabulary) |
| `biosafety_level` | Text | BSL classification (e.g., "BSL-1", "BSL-2") |



**_NOTE:_** This profile maps to `ASSAY.tsv` (strain, cell type, assay organism fields) and `ASSAY_PARAM.tsv` (growth conditions) for ChEMBL submission.

---

### 2.4 Gene Profile

Use [Bioschemas Gene 1.0-RELEASE](https://bioschemas.org/profiles/Gene/1.0-RELEASE) to annotate biotransformation-relevant genes in the microbial genome (e.g., genes encoding nitroreductases, azoreductases, dehalogenases, or other xenobiotic-metabolising enzymes).

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"Gene"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., NCBI Gene URL) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/Gene/1.0-RELEASE"` |
| `identifier` | PropertyValue, Text, URL | ONE | Gene identifier (e.g., NCBI Gene ID, locus tag) |
| `name` | Text | ONE | Gene symbol or name (e.g., "nfsA", "porA") |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `description` | Text | ONE | Gene function description |
| `encodesBioChemEntity` | BioChemEntity | MANY | Protein(s) or RNA encoded by this gene |
| `isPartOfBioChemEntity` | BioChemEntity | MANY | Chromosome or genome this gene belongs to |
| `url` | URL | ONE | Link to the gene record in NCBI Gene or equivalent |

**Optional Properties (MIX-MB(M) relevant):**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `hasMolecularFunction` | DefinedTerm, PropertyValue, URL | MANY | GO molecular function term |
| `isInvolvedInBiologicalProcess` | DefinedTerm, PropertyValue, URL | MANY | GO biological process term |
| `taxonomicRange` | DefinedTerm, Taxon, Text, URL | MANY | Organism(s) expressing this gene |
| `hasBioPolymerSequence` | Text | ONE | Nucleotide sequence (FASTA) |
| `alternateName` | Text | MANY | Alternative gene names or synonyms |
| `sameAs` | URL | MANY | Same gene in other databases (UniProt gene page, Ensembl, etc.) |



---

### 2.5 Protein Profile

Use [Bioschemas Protein 0.11-RELEASE](https://bioschemas.org/profiles/Protein/0.11-RELEASE) to describe enzymes responsible for xenobiotic biotransformation encoded by the microorganism.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"Protein"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., UniProt URL) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/Protein/0.11-RELEASE"` |
| `identifier` | PropertyValue, Text, URL | ONE | Protein identifier (e.g., UniProt accession, PDB ID) |
| `name` | Text | ONE | Protein name |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `description` | Text | ONE | Protein function; start with "Function: [...]" |
| `isEncodedByBioChemEntity` | Gene | MANY | Gene(s) encoding this protein |
| `taxonomicRange` | DefinedTerm, Taxon, Text, URL | MANY | Organism(s) expressing this protein |
| `url` | URL | ONE | Link to the protein record (UniProt, etc.) |

**Optional Properties (MIX-MB(M) relevant):**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `hasMolecularFunction` | DefinedTerm, PropertyValue, URL | MANY | GO molecular function term |
| `isInvolvedInBiologicalProcess` | DefinedTerm, PropertyValue, URL | MANY | GO biological process term |
| `isLocatedInSubcellularLocation` | DefinedTerm, PropertyValue, URL | MANY | Subcellular localisation |
| `bioChemInteraction` | BioChemEntity | MANY | Interacting molecules (substrates, cofactors) |
| `hasBioPolymerSequence` | Text | ONE | Amino acid sequence (FASTA) |
| `alternateName` | Text | MANY | Protein synonyms |
| `sameAs` | URL | MANY | Same protein in other databases (PDB, STRING, etc.) |


---

### 2.6 ProteinAnnotation Profile

Use [Bioschemas ProteinAnnotation 0.6-DRAFT](https://bioschemas.org/profiles/ProteinAnnotation/0.6-DRAFT) to annotate specific functional features of biotransformation enzymes — such as active sites, binding sites, EC number assignments, or domain annotations.

**Minimum Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `@context` | URL | ONE | `"https://schema.org/"` |
| `@type` | Text | ONE | `"ProteinAnnotation"` |
| `@id` | IRI | ONE | Globally unique IRI (e.g., UniProt feature URL) |
| `dct:conformsTo` | IRI | ONE | `"https://bioschemas.org/profiles/ProteinAnnotation/0.6-DRAFT"` |
| `identifier` | PropertyValue, Text, URL | ONE | Annotation identifier |

**Recommended Properties:**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `name` | Text | ONE | Name of the annotation (e.g., "Active site", "FMN binding") |
| `additionalType` | URL | MANY | Nature of annotation (e.g., domain, active site, variant) |
| `description` | Text | ONE | Description of the annotated feature |
| `creationMethod` | PropertyValue | ONE | Method used to generate the annotation (experimental / predicted) |
| `url` | URL | ONE | Link to annotation in database |

**Optional Properties (MIX-MB(M) relevant):**

| Property | Expected Type | Cardinality | Description |
|----------|---------------|-------------|-------------|
| `hasCategoryCode` | CategoryCode | MANY | Controlled vocabulary term (e.g., EC number) |
| `location` | PropertyValue, Text, URL | MANY | Position in sequence (residue number, range) |
| `isPartOfBioChemEntity` | BioChemEntity, URL | MANY | Protein this annotation belongs to |
| `subcellularLocation` | URL | MANY | Subcellular compartment |
| `additionalProperty` | PropertyValue | MANY | Extra annotation details |


---

## 3. Ontologies and Standards

### 3.1 NCBI Taxonomy

**Mandatory Requirements:**
- **NCBI TaxID:** Unique numerical identifier for each organism
- **Scientific Name:** Full binomial name (Genus species)
- **Taxonomic Lineage:** Complete classification path
  - Domain (Bacteria, Archaea, Eukarya)
  - Phylum
  - Class
  - Order
  - Family
  - Genus
  - Species

**Example:**
```yaml
organism:
  ncbi_taxid: 1351
  scientific_name: "Enterococcus faecalis"
  lineage:
    domain: "Bacteria"
    phylum: "Firmicutes"
    class: "Bacilli"
    order: "Lactobacillales"
    family: "Enterococcaceae"
    genus: "Enterococcus"
    species: "Enterococcus faecalis"
```

**Strain Level Information:**
```yaml
strain:
  strain_id: "ATCC 19433"
  strain_designation: "V583"
  type_strain: false
  genome_sequenced: true
  genome_assembly: "GCA_000007785.1"

  
```

### 3.2 Additional Ontology Requirements

- **Assay Ontology (BAO):** Biotransformation assay types
  - BAO:0000697 (metabolism assay)
  - BAO:0002989 (biotransformation assay)

- **Unit Ontology (UO):** Standardized units
  - UO:0000062 (molar concentration unit)
  - UO:0000031 (minute)
  - UO:0000027 (degree Celsius)

- **NCBI Taxonomy:** Microbial strain identification
  - Use NCBI TaxID for all organisms
  - Include strain information where applicable

### 3.3 MIxS (Minimum Information about any Sequence)

Compliance with [Genomic Standards Consortium (GSC)](https://www.gensc.org/pages/standards-intro.html) MIxS standards:

**Core MIxS Fields:**
- `source_mat_id`: Unique sample identifier
- `sample_collect_device`: Collection method
- `isol_growth_condt`: Isolation and growth conditions
- `cult_root_med`: Culture rooting medium
- `host_subject_id`: Host organism (if applicable)
- `isolation_source`: Source of isolation (e.g., human gut, soil)

**Environmental Context (MIxS-Env):**
- `env_broad_scale`: Biome (using ENVO terms)
- `env_local_scale`: Local environmental features
- `env_medium`: Material in which organism lives

**Example:**
```yaml
mixs_compliance:
  source_mat_id: "Sample_001_GutMicrobiome"
  isolation_source: "human fecal sample"
  env_broad_scale: "ENVO:00002018 (human-associated habitat)"
  env_local_scale: "ENVO:00002043 (gastrointestinal tract)"
  env_medium: "ENVO:00002003 (fecal material)"
  geo_loc_name: "Germany: Leipzig"
  collection_date: "2023-06-15"
  lat_lon: "51.3397° N, 12.3731° E"

  
```

### 3.4 Environment Ontology (ENVO)

**Required for Habitat Description:**
- **Biome:** ENVO biome classification
- **Environmental Feature:** Specific habitat
- **Environmental Material:** Substrate material

**Common ENVO Terms:**
```
Human-associated environments:
- ENVO:00002043 - gastrointestinal tract
- ENVO:00002042 - oral cavity
- ENVO:00002045 - skin

Environmental sources:
- ENVO:00002007 - sediment
- ENVO:00001998 - soil
- ENVO:00002019 - freshwater environment
- ENVO:00002030 - aquatic environment
```

### 3.5 Phenotype Ontology (PATO/OMP)

**Microbial Phenotype Characteristics:**
- **Gram stain:** PATO:0001654 (gram-positive) or PATO:0001655 (gram-negative)
- **Cell shape:** PATO terms for morphology
- **Motility:** OMP:0000001 (motile) vs non-motile
- **Spore formation:** Presence/absence
- **Oxygen requirement:**
  - Aerobic (PATO:0001903)
  - Anaerobic (PATO:0001904)
  - Facultative (PATO:0002224)

**Example:**
```yaml
phenotype:
  gram_stain: "PATO:0001655 (gram-negative)"
  cell_shape: "rod-shaped"
  motility: "motile"
  oxygen_requirement: "PATO:0002224 (facultative anaerobe)"
  spore_formation: false
  flagella: true
```

### 3.6 Gene Ontology (GO) & Enzyme Commission (EC)

**For Biotransformation Genes/Enzymes:**
- **GO Terms:** Molecular function, biological process
- **EC Numbers:** Enzyme classification
- **UniProt ID:** Protein identification

**Example:**
```yaml
enzyme_information:
  gene_name: "porA"
  locus_tag: "EF_1234"
  go_terms:
    - "GO:0016491 (oxidoreductase activity)"
    - "GO:0009058 (biosynthetic process)"
  ec_number: "EC 1.1.1.1"
  uniprot_id: "P12345"
  function: "Nitroreductase involved in drug metabolism"
```

### 3.7 Antibiotic Resistance Ontology (ARO)

**For Clinical/Environmental Strains:**
```yaml
antibiotic_resistance:
  profile: "ampicillin resistant, chloramphenicol sensitive"
  aro_terms:
    - "ARO:3000007 (beta-lactamase resistance)"
  resistance_genes:
    - gene: "blaZ"
      mechanism: "antibiotic inactivation"
```


---

## 7. Controlled Vocabularies

### 7.1 Oxygen Requirements

Standard terms:
- `obligate aerobe` - Requires oxygen
- `facultative anaerobe` - Grows with or without oxygen
- `obligate anaerobe` - Cannot tolerate oxygen
- `microaerophile` - Requires low oxygen (2-10%)
- `aerotolerant anaerobe` - Tolerates oxygen but doesn't use it

### 7.2 Cell Morphology

- `rod` / `bacillus` - Rod-shaped
- `coccus` - Spherical
- `spirillum` - Spiral
- `vibrio` - Comma-shaped
- `filamentous` - Long filaments
- `pleomorphic` - Variable shapes

### 7.3 Sample Types

- `pure culture` - Single strain isolation
- `enrichment culture` - Enriched for specific function
- `mixed culture` - Defined co-culture
- `community` - Complex microbial community
- `cell-free lysate` - Disrupted cells
- `membrane fraction` - Isolated membranes
- `cytoplasmic fraction` - Soluble proteins

### 7.4 Growth Phases

- `lag phase` - Adaptation period
- `exponential phase` / `log phase` - Rapid growth
- `stationary phase` - Growth plateau
- `death phase` - Cell death exceeds growth
- `early exponential` - Beginning of log phase (OD₆₀₀ 0.2-0.4)
- `mid exponential` - Middle log phase (OD₆₀₀ 0.4-0.8)
- `late stationary` - Extended stationary (>24h)

---

## 4. Data Validation Rules

Before submitting data, verify that all assay records pass the following checks. The pipeline (`generate_assay.R`) performs these checks automatically; they also apply to manually prepared submissions.

### 4.1 Organism Identifiers

| Rule | Check |
|------|-------|
| NCBI TaxID is present | Every assay row must have a non-empty `ASSAY_TAX_ID` |
| NCBI TaxID is numeric | Must be a positive integer (e.g. `1351`, not `"Enterococcus"`) |
| Scientific name is present | `ASSAY_ORGANISM` must contain the full binomial name (Genus species) |
| Name–TaxID consistency | The scientific name must match the registered name for that TaxID in NCBI Taxonomy |
| Novel isolates | If no strain-level TaxID exists, use the species-level TaxID and add a note in `ACTIVITY_COMMENT` |

### 4.2 Assay Index (AIDX)

| Rule | Check |
|------|-------|
| AIDX is present | Every row in `ASSAY.tsv` must have an AIDX |
| AIDX format | Must follow `[Author]_[Genus]_[species]_[Condition]`, using only ASCII letters, digits, underscores, and hyphens |
| AIDX uniqueness | Each AIDX must be unique within the study |
| No spaces | Spaces are not permitted in AIDX values |

### 4.3 Required Fields

The following fields must be non-empty in `ASSAY.tsv` for every assay record:

- `AIDX`, `RIDX`, `ASSAY_DESCRIPTION`, `ASSAY_TYPE`, `ASSAY_ORGANISM`, `ASSAY_TAX_ID`

### 4.4 Controlled Vocabulary Terms

| Field | Allowed values |
|-------|---------------|
| `ASSAY_TYPE` | `bacteria`, `enzyme`, `community` |
| `oxygen_requirement` | `obligate aerobe`, `facultative anaerobe`, `obligate anaerobe`, `microaerophile`, `aerotolerant anaerobe` (Section 7.1) |
| `sample_type` | `pure culture`, `enrichment culture`, `mixed culture`, `community`, `cell-free lysate`, `membrane fraction`, `cytoplasmic fraction` (Section 7.3) |
| `harvest_phase` | `lag phase`, `exponential phase`, `stationary phase`, `death phase`, `early exponential`, `mid exponential`, `late stationary` (Section 7.4) |

### 4.5 `sameAs` Linking

| Rule | Check |
|------|-------|
| NCBI Taxonomy URL | Required for all organisms with a registered TaxID (Gold tier) |
| No speculative links | Do not add `sameAs` for novel isolates without a registered external record |

---

## 5. Data Quality Tiers

MIX-MB(M) defines three compliance tiers for microbial organism data. Higher tiers enable broader reuse and interoperability with genomic and phenotypic databases.

### Tier 1 — Gold (Publication-Ready)

Meets all mandatory and recommended fields. Suitable for ChEMBL submission and FAIR data publications.

- NCBI TaxID present and verified
- Full binomial scientific name matching the TaxID
- Strain designation provided (e.g. ATCC, DSMZ, or culture collection number)
- Genome assembly accession available (`GCA_` or `GCF_` accession)
- `sameAs` link to NCBI Taxonomy URL provided; LPSN link included for prokaryotes
- All growth conditions documented: medium, temperature, oxygen requirement, harvest phase
- Full Bioschemas Taxon + Sample JSON-LD records (Sections 2.1 and 2.3)

### Tier 2 — Silver (Research-Grade)

Meets all mandatory fields with partial recommended fields. Suitable for internal data sharing and preprint deposition.

- NCBI TaxID present and verified
- Full binomial scientific name
- Strain designation provided
- `sameAs` link to NCBI Taxonomy URL
- Basic growth conditions: at minimum, medium and temperature

### Tier 3 — Bronze (Preliminary / Screening)

Meets only mandatory fields. Suitable for large-scale screening data where full strain characterisation is not yet available.

- NCBI TaxID present
- Scientific name present
- `AIDX` and `RIDX` assigned
- `ASSAY_TYPE` specified
- Minimal cultivation information; quantitative growth conditions not required

---


## 6. How to use the Template

The MIX-MB submission template is provided as [Templates/Template.xlsx](Templates/Template.xlsx). The **Assay** sheet covers the MIX-MB(M) standard.

### Colour coding

| Colour | Meaning |
|--------|---------|
| Green | Mandatory — must be filled for a valid submission |
| Blue | Recommended — strongly encouraged; required for Tier 1 (Gold) |
| Yellow | Optional — fill if available |

### Step-by-step

1. **Open** `Template.xlsx` and go to the **Assay** sheet.
2. **Add one row per organism × condition combination.** If the same organism is used under two different oxygen conditions or media, it gets two rows with distinct AIDXs.
3. **Look up the NCBI TaxID** for each organism:
   - Go to [https://www.ncbi.nlm.nih.gov/taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy)
   - Search by scientific name; copy the TaxID number into `ASSAY_TAX_ID`
4. **Assign the AIDX** using the format `[FirstAuthorLastName]_[Genus]_[species]_[Condition]`, e.g. `Zimmermann_Actinomyces_graevenitzii_biotransformation`.
5. **Fill in cultivation conditions** (medium, temperature, oxygen requirement) using the controlled vocabulary terms from Section 7.
6. **For community assays,** set `ASSAY_ORGANISM` to `mixed microbial community`, `ASSAY_TAX_ID` to `1` (root), and describe the community source in `ASSAY_DESCRIPTION`.
7. **Fill in `ASSAY_PARAM.tsv`** for quantitative experimental parameters (temperature, incubation time, pH, cell density, substrate concentration). Each parameter gets its own row linked by AIDX.
8. **Validate** your completed sheet against the rules in Section 4 before running the pipeline or submitting.

---


## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-05 | Draft |

---

## 8. Data Access and Repository Guidance

### 8.1 Repository and Standard Documents

The MIX-MB standard documents, submission template, and BioXend pipeline are openly available:

- **Standard documents:** [GitHub — zmahnoor14/BioXend](https://github.com/zmahnoor14/BioXend), under `Standards/`
- **Submission template:** `Standards/Templates/Template.xlsx` (see Section 6)
- **BioXend pipeline:** Nextflow workflow (`main.nf`) in the repository root

### 8.2 Files Generated by This Standard

MIX-MB(M) organism data feed the assay files required for ChEMBL deposition. The BioXend pipeline (`generate_assay.R`) produces:

| Output File | Content |
|-------------|---------|
| `ASSAY.tsv` | Assay descriptions per organism × condition, indexed by AIDX |
| `ASSAY_PARAM.tsv` | Quantitative experimental parameters (temperature, pH, incubation time, cell density) |

These files are linked to compound and activity records via AIDX (see MIX-MB(B)).

### 8.3 Submitting to ChEMBL

MIX-MB(M) assay files are deposited to [ChEMBL](https://www.ebi.ac.uk/chembl/) as part of a full MIX-MB submission package. For deposition enquiries, contact **chembl-help@ebi.ac.uk** or use the ChEMBL deposition portal.

**Pre-submission checklist for organism data:**
- All assay rows pass Section 4 validation rules
- Every `ASSAY_TAX_ID` is a valid, numeric NCBI TaxID
- Scientific name matches the registered NCBI name for that TaxID
- At least one `sameAs` URL to NCBI Taxonomy (Gold tier)

### 8.4 Supplementary Sequence Data Repositories

Sequencing data linked to strains used in a MIX-MB study should be deposited in:

| Repository | URL | Data type |
|------------|-----|-----------|
| NCBI SRA | https://www.ncbi.nlm.nih.gov/sra | Short-read and long-read sequencing |
| ENA | https://www.ebi.ac.uk/ena | Alternative / European submission |
| NCBI Assembly | https://www.ncbi.nlm.nih.gov/assembly | Genome assemblies (GCA/GCF accessions) |

Record the assembly accession in `additionalProperty` → `genome_assembly` (Section 2.3) and include it in the `sameAs` field of the Taxon record.

---

## 9. Licence and Reuse

### 9.1 Standard Documents

The MIX-MB standard documents are released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** licence ([https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)).

You are free to share, adapt, and build upon this standard for any purpose, provided you give appropriate credit:

> Zulfiqar M. *et al.* MIX-MB: Minimum Information about Xenobiotics-Microbiome Biotransformation (v0.1.0). GitHub: https://github.com/zmahnoor14/BioXend

### 9.2 Pipeline and Code

The BioXend Nextflow pipeline and associated scripts are released under the **MIT Licence**. See `LICENSE` in the repository root for full terms.

### 9.3 Submitted Data

Data deposited using MIX-MB formats in public repositories are subject to that repository's terms:

| Repository | Licence |
|------------|---------|
| ChEMBL | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/) |
| NCBI SRA / Assembly | NCBI data use policies (https://www.ncbi.nlm.nih.gov/home/about/policies/) |
| ENA | EMBL-EBI data access policies |

When reusing MIX-MB-formatted datasets, cite both the original study (via its RIDX/DOI) and the MIX-MB standard.

---

## 10. Provenance

Provenance records the origin, history, and chain of custody of microbial organism data reported under MIX-MB(M). Complete provenance supports the **Reusable** principle of FAIR and enables reproducibility of biotransformation experiments.

### 10.1 Study-Level Provenance

Every assay record is anchored to a **Reference record** (RIDX) in `REFERENCE.tsv`:

| Field | Description |
|-------|-------------|
| `RIDX` | Study-local identifier linking all submission files |
| `DOI` | Digital Object Identifier of the source publication |
| `TITLE`, `AUTHORS`, `YEAR` | Full bibliographic metadata |

The RIDX appears in every row of `ASSAY.tsv`, making the publication the root provenance node for all organism data.

### 10.2 Strain Identity Provenance

The organism identifiers documented in Section 1.4 serve as provenance anchors for strain identity:

| Identifier | Provenance Source |
|------------|------------------|
| **NCBI TaxID** | Verified against NCBI Taxonomy; links to authoritative taxonomy record |
| **LPSN name** | Valid scientific name from the List of Prokaryotic Names (https://lpsn.dsmz.de/) |
| **Culture collection ID** | Physical strain held at a registered biobank (ATCC, DSMZ, CGSC, etc.) |
| **Genome assembly accession** | Sequenced genome lodged in NCBI Assembly or ENA |
| `sameAs` URLs | Direct links to NCBI Taxonomy, LPSN, BacDive, or other authoritative records |

For novel isolates without a registered TaxID, the closest assigned TaxID plus a note in `ACTIVITY_COMMENT` constitutes the strain's provenance record until formal registration.

### 10.3 Environmental and Isolation Provenance

For strains isolated from environmental or clinical samples, document the following MIxS-compliant fields (Section 3.3) as part of strain provenance:

| Field | Provenance Aspect |
|-------|------------------|
| `isolation_source` | Biological or environmental matrix from which the strain was obtained |
| `collection_date` | ISO 8601 date of sample collection |
| `geo_loc_name` | Geographic origin of the sample |
| `env_broad_scale` / `env_local_scale` | ENVO-annotated habitat classification |

### 10.4 Pipeline Provenance

When generating submission files with BioXend, record in `REFERENCE.tsv` or `ASSAY_PARAM.tsv`:

- **BioXend pipeline version** — from `versions/pipeline.txt`
- **`generate_assay.R` version** — from the script header
- **Date of generation** — ISO 8601 format (YYYY-MM-DD)

---

## 11. References

1. NCBI Taxonomy Database: https://www.ncbi.nlm.nih.gov/taxonomy
2. Genomic Standards Consortium (GSC): https://www.gensc.org/
3. MIxS Standards: https://press3.mcs.anl.gov/gensc/mixs/
4. Bioschemas Specifications: https://bioschemas.org/
5. Environment Ontology (ENVO): http://www.environmentontology.org/
6. LPSN - List of Prokaryotic names: https://lpsn.dsmz.de/
7. BacDive - Bacterial Diversity Database: https://bacdive.dsmz.de/
8. FAIR Principles: https://www.go-fair.org/fair-principles/
9. ChEMBL Database: https://www.ebi.ac.uk/chembl/

---

## 12. Contact and Contributions

For questions, suggestions, or contributions to this standard, please contact:
- **Maintainer:** Mahnoor Zulfiqar
- **Institution:** NFDI4Microbiota
- **Email:** [Contact information](mailto:zmahnoor14@gmail.com)
- **Repository:** [[GitHub repository URL](https://github.com/zmahnoor14/BioXend)]

---