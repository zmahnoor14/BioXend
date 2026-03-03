# Minimum Information about Xenobiotics-Microbiome Biotransformation -- MIX-MB(M)
## Microbial Component Standards

This document identifies Minimum Information (MI) required to report microbial organisms involved in "Microbial Biotransformation of Xenobiotics", ensuring comprehensive documentation of bacterial, archaeal, and fungal species/strains used in biotransformation studies and information on the assays.

**Author:** Mahnoor Zulfiqar
**Version:** 0.1.0  
**Release Date:** February 5, 2026 (Draft)  
**Status:** Draft Standard  
**Part of:** MIX-MB Standard v0.1  
**Replaces:** N/A  
**Compatible with:** 
- MIX-MB(X) v0.1.0
- MIX-MB(B) v0.1.0

**Breaking Changes:** N/A  
**Alignment:** NCBI Taxonomy, MIxS, GSC Standards, ChEMBL, FAIR principles

---

## 1. Overview

MIX-MB(M) establishes minimum information standards for reporting microbial organisms in xenobiotic biotransformation studies, ensuring data is:
- **Findable:** Properly annotated with taxonomic identifiers and strain information
- **Accessible:** Standardized formats compatible with public databases
- **Interoperable:** Uses community ontologies and controlled vocabularies
- **Reusable:** Complete provenance, cultivation, and experimental conditions

This standard complements MIX-MB(X) for xenobiotics documentation.

### 1.1 How is this document organised?

### 1.2 Which sections are important for contributors?

### 1.3 Which sections are important for the data submitors?

---

## 2. Bioschemas
includes: Gene, Protein, 
### 2.1 Taxon Profile

Use [Bioschemas Taxon](https://bioschemas.org/types/Taxon/) for microorganism annotation:

**Required Properties:**
- `@type`: Taxon
- `identifier`: NCBI Taxonomy ID (mandatory)
- `name`: Scientific binomial name (Genus species)
- `taxonRank`: Taxonomic rank (species, subspecies, strain)
- `parentTaxon`: Higher taxonomic classification

**Recommended Properties:**
- `alternateName`: Synonyms, former names
- `url`: Link to taxonomy databases (NCBI, LPSN, MycoBank)
- `childTaxon`: Known subspecies or strains
- `hasDefinedTerm`: Associated ontology terms (e.g., habitat, phenotype)

**Example:**
```json
{
  "@context": "https://schema.org",
  "@type": "Taxon",
  "identifier": "txid562",
  "name": "Escherichia coli",
  "alternateName": ["E. coli", "Bacterium coli"],
  "taxonRank": "species",
  "parentTaxon": {
    "@type": "Taxon",
    "name": "Escherichia",
    "identifier": "txid561",
    "taxonRank": "genus"
  },
  "url": "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=562"
}
```

### 2.2 BioSample Profile

Use [Bioschemas BioSample](https://bioschemas.org/types/BioSample/) for strain-specific information:

**Required Properties:**
- `@type`: BioSample
- `identifier`: Strain identifier (culture collection number)
- `name`: Strain designation
- `taxonomicRange`: Link to Taxon
- `additionalProperty`: Key characteristics (antibiotic resistance, auxotrophy)

**Example:**
```json
{
  "@context": "https://schema.org",
  "@type": "BioSample",
  "identifier": "ATCC 25922",
  "name": "Escherichia coli ATCC 25922",
  "taxonomicRange": {
    "@type": "Taxon",
    "identifier": "txid562",
    "name": "Escherichia coli"
  },
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "gram_stain",
      "value": "negative"
    },
    {
      "@type": "PropertyValue",
      "name": "oxygen_requirement",
      "value": "facultative anaerobe"
    }
  ],
  "url": "https://www.atcc.org/products/25922"
}
```

### 2.3 Study Profile

Use for experimental context:

**Required Properties:**
- `@type`: Study
- `studySubject`: BioSample being studied
- `studyDesign`: Experimental design description
- `studyDomain`: "microbiology", "biotransformation"

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

## 4. MSI Metabolomics Standards

Compliance with [Metabolomics Standards Initiative (MSI)](https://metabolomicssociety.org/resources/metabolomics-standards-initiative):

### 4.1 Biological Context (MSI Level 1)

**Required Information:**
- **Organism:**
  - Scientific name
  - NCBI Taxonomy ID
  - Strain designation
  - Growth conditions (medium, temperature, oxygen)
  
- **Sample Information:**
  - Sample type (pure culture, cell lysate, supernatant)
  - Biomass or cell density
  - Growth phase (exponential, stationary)
  - Sample preparation method

**Example:**
```yaml
organism:
  species: "Escherichia coli"
  ncbi_taxid: 562
  strain: "K-12 MG1655"
  growth_conditions:
    medium: "M9 minimal medium"
    temperature: "37°C"
    oxygen: "aerobic"
    incubation_time: "16h"
sample:
  type: "culture supernatant"
  od600: 1.2
  growth_phase: "stationary"
  volume: "50 mL"
```

## 5. Growth and Cultivation Standards

### 5.1 Culture Medium Specification

**Required Information:**
- **Medium Type:** Defined/complex/synthetic
- **Medium Name:** Standard name (e.g., LB, TSB, M9)
- **Composition:** Complete list of components with concentrations
- **pH:** Initial and final (if measured)
- **Sterilization Method:** Autoclaving, filter sterilization

**Example:**
```yaml
culture_medium:
  medium_name: "Brain Heart Infusion (BHI)"
  medium_type: "complex"
  supplier: "BD Difco"
  catalog_number: "237500"
  preparation:
    powder_concentration: "37 g/L"
    distilled_water: "1 L"
    ph_adjustment: "7.4 ± 0.2"
    sterilization: "autoclave 121°C, 15 min"
  
  supplements:
    - compound: "hemin"
      concentration: "5 µg/mL"
    - compound: "vitamin K1"
      concentration: "1 µg/mL"
```

**Minimal Medium Example:**
```yaml
culture_medium:
  medium_name: "M9 minimal medium"
  medium_type: "defined"
  base_salts:
    - "Na2HPO4·7H2O: 12.8 g/L"
    - "KH2PO4: 3 g/L"
    - "NaCl: 0.5 g/L"
    - "NH4Cl: 1 g/L"
  supplements:
    - "MgSO4: 2 mM"
    - "CaCl2: 0.1 mM"
    - "glucose: 0.4% (w/v)"
    - "thiamine: 1 mg/L"
  ph: 7.0
```

### 5.2 Growth Conditions

**Required Parameters:**

| Parameter | Required | Unit | Description |
|-----------|----------|------|-------------|
| Temperature | Yes | °C | Incubation temperature |
| Atmosphere | Yes | Text | Aerobic, anaerobic, microaerophilic |
| Oxygen level | If anaerobic | % | O₂ concentration |
| CO₂ level | If applicable | % | CO₂ concentration |
| Shaking/agitation | Yes | rpm | Shaking speed (if applicable) |
| Culture volume | Yes | mL | Volume in vessel |
| Vessel type | Yes | Text | Flask type, tube, plate |
| Inoculum size | Yes | CFU/mL or % | Starting cell density |
| Growth duration | Yes | hours | Total incubation time |

**Example:**
```yaml
growth_conditions:
  temperature: "37°C"
  atmosphere: "anaerobic"
  oxygen_level: "<0.1%"
  co2_level: "10%"
  h2_level: "5%"
  anaerobic_method: "anaerobic chamber (Coy Laboratory Products)"
  shaking: "static (no shaking)"
  culture_volume: "50 mL"
  vessel_type: "serum bottle (125 mL, sealed with butyl rubber stopper)"
  inoculum:
    source: "overnight culture"
    size: "1% (v/v)"
    initial_od600: "0.05"
  growth_duration: "24 hours"
  sampling_timepoint: "stationary phase"
```

### 5.3 Growth Phase Documentation

**Required:**
- **Growth Phase:** Lag, exponential, stationary, death
- **Cell Density:** OD₆₀₀ or CFU/mL
- **Measurement Method:** Spectrophotometry, plate counting
- **Viability:** Live/dead cell count (if applicable)

**Example:**
```yaml
growth_phase:
  harvest_phase: "stationary phase"
  harvest_time: "24 hours post-inoculation"
  od600: "1.2 ± 0.1"
  cfu_per_ml: "2.5 × 10⁹"
  viability: ">95% (live/dead staining)"
  doubling_time: "45 minutes (exponential phase)"
```

### 5.4 Quality Control

**Required Checks:**
- **Purity:** Contamination testing
- **Identity:** Verification method (16S rRNA, MALDI-TOF)
- **Viability:** CFU counts, microscopy
- **Reproducibility:** Batch-to-batch consistency

**Example:**
```yaml
quality_control:
  contamination_check:
    method: "plating on selective media"
    result: "no contamination detected"
  identity_verification:
    method: "16S rRNA gene sequencing"
    result: "99.8% identity to Escherichia coli"
    accession: "NR_024570.1"
  morphology_check:
    method: "Gram staining and microscopy"
    result: "gram-negative rods, typical morphology"
  storage:
    method: "glycerol stock at -80°C"
    glycerol_concentration: "15% (v/v)"
```

---

## 6. Data Formats

1. https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/chembl-data-questions
2. 


### 6.1 ChEMBL ASSAY.tsv Format

Microbial information in biotransformation assays:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| AIDX | Yes | String | Assay identifier (include strain in ID) |
| DESCRIPTION | Yes | String | Full assay description |
| ASSAY_TYPE | Yes | String | "Biotransformation", "Metabolism" |
| ASSAY_ORGANISM | Yes | String | Scientific name (Genus species) |
| ASSAY_TAX_ID | Yes | Integer | NCBI Taxonomy ID |
| ASSAY_STRAIN | Recommended | String | Strain designation |
| ASSAY_TISSUE | No | String | Tissue/organ (for host-associated) |
| ASSAY_CELL_TYPE | Recommended | String | Cell type or compartment |
| ASSAY_SUBCELLULAR_FRACTION | No | String | Lysate, membrane, cytosol, etc. |
| SRC_ASSAY_ID | No | String | Source database assay ID |
| RIDX | Yes | String | Reference identifier |

**Example:**
```tsv
AIDX	DESCRIPTION	ASSAY_TYPE	ASSAY_ORGANISM	ASSAY_TAX_ID	ASSAY_STRAIN	ASSAY_CELL_TYPE	RIDX
A001_Ecoli_K12	Biotransformation of ibuprofen by E. coli K-12 MG1655 in anaerobic conditions	Biotransformation	Escherichia coli	562	K-12 MG1655	whole cell	REF_001
A002_Csporogenes	Metabolism of diclofenac by Clostridium sporogenes ATCC 15579	Metabolism	Clostridium sporogenes	1509	ATCC 15579	whole cell	REF_001
```

### 6.2 Extended Microbial Metadata (JSON/YAML)

**Comprehensive strain information:**

```yaml
# Strain Record
strain_id: "ECOLI_K12_MG1655"
biosample_accession: "SAMN02604091"

# Taxonomy
taxonomy:
  ncbi_taxid: 511145
  scientific_name: "Escherichia coli str. K-12 substr. MG1655"
  common_name: "E. coli K-12"
  rank: "no rank"
  lineage:
    - "Bacteria"
    - "Pseudomonadota"
    - "Gammaproteobacteria"
    - "Enterobacterales"
    - "Enterobacteriaceae"
    - "Escherichia"

# Strain Information
strain_info:
  strain_designation: "K-12 substr. MG1655"
  type_strain: false
  collection_numbers:
    - "ATCC 47076"
    - "CGSC 7740"
  isolation_source: "Human intestinal isolate K-12, F- lambda-"
  geographic_origin: "Stanford, California, USA"
  isolation_year: 1922
  isolated_by: "d'Herelle"

# Genomic Information
genome:
  sequenced: true
  assembly_accession: "GCA_000005845.2"
  refseq_accession: "NC_000913.3"
  genome_size: "4.64 Mb"
  gc_content: "50.8%"
  chromosome_count: 1
  plasmid_count: 0
  gene_count: 4321

# Phenotype
phenotype:
  gram_stain: "negative"
  cell_shape: "rod"
  motility: "motile"
  flagella: "peritrichous"
  oxygen_requirement: "facultative anaerobe"
  optimal_temperature: "37°C"
  temperature_range: "20-42°C"
  optimal_ph: "7.0"
  ph_range: "6.0-8.0"

# Safety & Regulation
biosafety:
  biosafety_level: "BSL-1"
  risk_group: "1"
  pathogenicity: "non-pathogenic laboratory strain"
  gmo_status: "not genetically modified (wild-type)"

# Availability
availability:
  culture_collections:
    - name: "ATCC"
      catalog_id: "47076"
      url: "https://www.atcc.org/products/47076"
    - name: "CGSC"
      catalog_id: "7740"
      url: "https://cgsc.biology.yale.edu/"
  
# Growth Requirements
cultivation:
  recommended_medium: "LB broth"
  alternative_media: ["M9 minimal medium", "TSB"]
  growth_temperature: "37°C"
  atmosphere: "aerobic with shaking"
  doubling_time: "~20 minutes (rich medium)"

# Historical Context
history:
  parent_strain: "Escherichia coli K-12"
  derivative_of: "E. coli K-12 F- lambda-"
  notable_features:
    - "Most widely studied bacterial organism"
    - "Model organism for molecular biology"
    - "Complete genome sequence available since 1997"
```

### 6.3 ISA-Tab Sample File (s_samples.txt)

Microbial sample metadata in ISA-Tab format:

```
Source Name	Characteristics[Organism]	Characteristics[Strain]	Characteristics[NCBI Taxonomy ID]	Characteristics[Growth Medium]	Characteristics[Temperature]	Characteristics[Atmosphere]	Protocol REF	Sample Name
Culture_001	Escherichia coli	K-12 MG1655	511145	LB broth	37°C	aerobic	P001_cultivation	Sample_001
Culture_002	Clostridium sporogenes	ATCC 15579	1509	BHI + hemin	37°C	anaerobic	P002_anaerobic_cultivation	Sample_002
```

### 6.4 Microbial Database Submission Formats

#### 6.4.1 BioSample (NCBI) XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<BioSample schema_version="2.0">
  <SampleId>
    <SPUID spuid_namespace="NFDI4Microbiota">Sample_001</SPUID>
  </SampleId>
  <Descriptor>
    <Title>Escherichia coli K-12 MG1655 for drug biotransformation study</Title>
    <Description>Pure culture of E. coli K-12 used in xenobiotic metabolism screen</Description>
  </Descriptor>
  <Organism taxonomy_id="511145">
    <OrganismName>Escherichia coli str. K-12 substr. MG1655</OrganismName>
  </Organism>
  <Attributes>
    <Attribute attribute_name="strain">K-12 substr. MG1655</Attribute>
    <Attribute attribute_name="isolation source">laboratory stock</Attribute>
    <Attribute attribute_name="collection date">2023-06-15</Attribute>
    <Attribute attribute_name="geographic location">Germany</Attribute>
    <Attribute attribute_name="culture collection">ATCC 47076</Attribute>
  </Attributes>
</BioSample>
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

## 8. Data Validation Rules

### 8.1 Taxonomic Validation

- NCBI TaxID must be valid and current (check against NCBI Taxonomy database)
- Scientific name must match TaxID exactly
- Strain designation should be from recognized culture collections
- Taxonomic lineage must be complete and consistent

### 8.2 Cultivation Parameters Validation

- Temperature: Must be between -20°C and 100°C
- pH: Must be between 0 and 14
- Cell density (OD₆₀₀): Must be positive, typically 0.001-10.0
- CFU/mL: Must be positive, typically 10⁴-10¹² range
- Growth time: Must be positive

### 8.3 Metadata Completeness

- All Level A (Essential) fields must be present
- At least 50% of Level B (Recommended) fields for high-quality submissions
- Cross-references must be valid (culture collection IDs, accessions)

### 8.4 Ontology Term Validation

- NCBI TaxID format: must be integer
- ENVO terms: Must follow "ENVO:" prefix with 7-digit number
- GO terms: Must follow "GO:" prefix with 7-digit number
- All ontology terms should be current (not obsolete)

---

## 9. Data Quality Tiers

### Tier 1: Gold Standard (Publication-Ready)
- All Level A and B information complete
- Genome sequenced with public accession
- Deposited in international culture collection
- 16S rRNA sequence verified (>99% match)
- Comprehensive phenotypic characterization
- Multiple independent biological replicates

### Tier 2: Silver Standard (Research-Grade)
- All Level A information complete
- Most Level B information present
- Identity confirmed by 16S rRNA or MALDI-TOF
- Basic phenotypic characterization
- Biological replicates (n≥2)

### Tier 3: Bronze Standard (Preliminary)
- All Level A essential information
- Basic cultivation data
- Identity presumed from morphology/biochemical tests
- Suitable for screening studies

---

## 10. Example Complete Record

```yaml
# MIX-MB(M) Compliant Microbial Record

# Basic Identification
organism_id: "ORG_001"
scientific_name: "Bacteroides thetaiotaomicron"
common_name: "B. theta"
ncbi_taxid: 818
strain_designation: "VPI-5482"

# Taxonomy
taxonomy:
  domain: "Bacteria"
  phylum: "Bacteroidota"
  class: "Bacteroidia"
  order: "Bacteroidales"
  family: "Bacteroidaceae"
  genus: "Bacteroides"
  species: "Bacteroides thetaiotaomicron"

# Strain Information
strain_info:
  type_strain: true
  culture_collections:
    - collection: "ATCC"
      accession: "29148"
      url: "https://www.atcc.org/products/29148"
    - collection: "DSM"
      accession: "2079"
  isolation_source: "human fecal sample"
  isolation_location: "USA"
  host: "Homo sapiens"
  isolation_year: 1972

# Genomic Data
genome:
  sequenced: true
  assembly_accession: "GCA_000011065.1"
  refseq_accession: "NC_004663.1"
  genome_size: "6.26 Mb"
  gc_content: "42.8%"
  chromosome_count: 1
  plasmid_count: 0
  annotation: "Complete genome, 4816 protein-coding genes"

# Phenotype
phenotype:
  gram_stain: "negative"
  cell_shape: "rod"
  cell_size: "0.5-0.8 × 2-6 µm"
  motility: "non-motile"
  flagella: false
  spore_formation: false
  oxygen_requirement: "obligate anaerobe"
  optimal_temperature: "37°C"
  temperature_range: "30-42°C"
  optimal_ph: "6.5-7.5"
  
# Environmental Context
environment:
  habitat: "ENVO:00002043 (gastrointestinal tract)"
  host_association: "human gut microbiome"
  abundance: "major constituent (>10% in some individuals)"
  ecological_role: "polysaccharide degradation"

# Cultivation
cultivation:
  recommended_medium: "BHI supplemented with hemin and vitamin K"
  alternative_media:
    - "YCFA (Yeast Casitone Fatty Acid) medium"
    - "Anaerobe Basal Broth + supplements"
  growth_conditions:
    temperature: "37°C"
    atmosphere: "anaerobic (85% N₂, 10% CO₂, 5% H₂)"
    vessel: "serum bottle with butyl rubber stopper"
    shaking: "static (no shaking)"
  growth_characteristics:
    doubling_time: "90-120 minutes"
    max_od600: "2.5-3.0"
    growth_curve_shape: "typical sigmoidal"

# Experimental Conditions (for biotransformation study)
experimental_setup:
  culture_medium:
    name: "BHI"
    supplements:
      - "hemin: 5 µg/mL"
      - "vitamin K1: 1 µg/mL"
      - "L-cysteine: 0.5 g/L"
  inoculum:
    source: "overnight culture"
    initial_od600: "0.05"
  growth_duration: "24 hours"
  harvest_phase: "stationary phase"
  harvest_od600: "2.2"
  cell_concentration: "5.0 × 10⁹ CFU/mL"

# Quality Control
quality_control:
  purity_check:
    method: "colony morphology on blood agar"
    result: "pure culture, no contamination"
  identity_verification:
    method: "16S rRNA gene sequencing (full length)"
    result: "100% match to B. thetaiotaomicron VPI-5482"
    accession: "NR_074376.1"
  viability:
    method: "serial dilution plating"
    result: ">99% viable cells"
  microscopy:
    method: "Gram stain"
    observation: "gram-negative rods, typical morphology"

# Safety
biosafety:
  biosafety_level: "BSL-2"
  risk_group: "2"
  pathogenicity: "opportunistic pathogen"
  special_precautions: "handle in anaerobic chamber"

# Metabolic Capabilities
metabolism:
  key_pathways:
    - "polysaccharide utilization loci (PULs)"
    - "glycan degradation"
    - "short-chain fatty acid production"
  biotransformation_enzymes:
    - enzyme: "azoreductase"
      ec_number: "EC 1.7.1.17"
      function: "azo bond reduction"
    - enzyme: "nitroreductase"
      ec_number: "EC 1.7.1.12"
      function: "nitro group reduction"
  known_substrates:
    - "polysaccharides (diverse)"
    - "xenobiotics (limited studies)"

# Previous Studies
references:
  - study: "Genome analysis"
    pmid: "14660578"
    doi: "10.1126/science.1088727"
  - study: "Polysaccharide utilization"
    pmid: "16172379"
    doi: "10.1073/pnas.0504002102"

# Data Quality
quality_tier: "Gold Standard"
validation_status: "Passed"
completeness_score: "98%"
last_updated: "2026-02-05"
```

---

## 11. Integration with MIX-MB(X)

### 11.1 Linking Microbes to Xenobiotics

**Cross-Reference Structure:**
```yaml
biotransformation_experiment:
  experiment_id: "EXP_001"
  
  # Xenobiotic (from MIX-MB(X))
  substrate:
    cidx: "C001"
    compound_name: "Ibuprofen"
    chembl_id: "CHEMBL1201246"
  
  # Microbe (from MIX-MB(M))
  organism:
    organism_id: "ORG_001"
    scientific_name: "Bacteroides thetaiotaomicron"
    ncbi_taxid: 818
    strain: "VPI-5482"
  
  # Assay linking both
  assay:
    aidx: "A001_Btheta_VPI5482"
    description: "Biotransformation of ibuprofen by B. theta VPI-5482"
```

### 11.2 Unified Submission

For ChEMBL submission, combine information:
- REFERENCE.tsv (publication info)
- COMPOUND files (xenobiotic - MIX-MB(X))
- ASSAY files (includes organism - MIX-MB(M))
- ACTIVITY files (links compound + organism)

---

## 12. Software Tools & Resources

### 12.1 Taxonomic Identification

- **16S rRNA Analysis:** EzBioCloud, SILVA, RDP Classifier
- **MALDI-TOF:** Bruker MALDI Biotyper, bioMérieux VITEK MS
- **Whole Genome:** ANI calculator, TYGS (Type Strain Genome Server)

### 12.2 Database Resources

- **NCBI Taxonomy:** https://www.ncbi.nlm.nih.gov/taxonomy
- **LPSN (List of Prokaryotic names):** https://lpsn.dsmz.de/
- **BacDive:** https://bacdive.dsmz.de/
- **ATCC:** https://www.atcc.org/
- **DSMZ:** https://www.dsmz.de/

### 12.3 Ontology Tools

- **OLS (Ontology Lookup Service):** https://www.ebi.ac.uk/ols/
- **BioPortal:** https://bioportal.bioontology.org/
- **ENVO Browser:** http://www.environmentontology.org/

### 12.4 Metadata Management

- **ISA Tools:** https://isa-tools.org/
- **NCBI BioSample submission:** https://submit.ncbi.nlm.nih.gov/
- **ENA (European Nucleotide Archive):** https://www.ebi.ac.uk/ena/

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-05 | Initial draft: Core microbial standards defined |

---

## 14. References

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

## 15. Contact and Contributions

For questions, suggestions, or contributions to this standard, please contact:
- **Maintainer:** Mahnoor Zulfiqar
- **Institution:** NFDI4Microbiota
- **Email:** [Contact information](mailto:zmahnoor14@gmail.com)
- **Repository:** [[GitHub repository URL](https://github.com/zmahnoor14/BioXend)]

---

