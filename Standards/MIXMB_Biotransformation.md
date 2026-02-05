# Minimum Information about Xenobiotics-Microbiome Biotransformation -- MIX-MB(B)
## Biotransformation Process Standards

This document identifies Minimum Information (MI) required to report the biotransformation process between microorganisms and xenobiotic compounds. MIX-MB(B) bridges MIX-MB(X) (xenobiotics) and MIX-MB(M) (microbes) by defining standards for the experimental assays, measurements, and outcomes.

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

## 1. Overview

MIX-MB(B) establishes minimum information standards for documenting biotransformation experiments where microorganisms metabolize xenobiotic compounds. This standard ensures:

- **Reproducibility:** Complete experimental protocols and conditions
- **Comparability:** Standardized measurements and reporting
- **Traceability:** Links between substrates, organisms, and products
- **Quality:** Validation and quality control measures

### 1.1 Scope

This standard covers:
- In vitro biotransformation assays (whole cells, lysates, purified enzymes)
- Ex vivo studies (tissue/organ preparations)
- In situ measurements (community-level biotransformation)
- Time-course experiments
- Dose-response studies
- Product identification and quantification

### 1.2 Relationship to Other Standards

```
MIX-MB(X)              MIX-MB(B)              MIX-MB(M)
[Xenobiotics] -----> [Biotransformation] <----- [Microbes]
   Substrate              Process               Organism
   Product               Assay                  Enzyme
   Structure             Activity               Strain
```

---

## 2. Bioschemas

### 2.1 BioChemEntity Profile (Biotransformation Reaction)

**Required Properties:**
- `@type`: BioChemEntity
- `identifier`: Reaction identifier
- `name`: Biotransformation reaction name
- `biochemicalInteraction`: Type of transformation
- `isInvolvedInBiologicalProcess`: GO term for process
- `hasBioChemEntityPart`: Substrate and product entities

**Example:**
```json
{
  "@context": "https://schema.org",
  "@type": "BioChemEntity",
  "identifier": "BTRANS_001",
  "name": "Reduction of ibuprofen to hydroxy-ibuprofen",
  "biochemicalInteraction": "reduction",
  "isInvolvedInBiologicalProcess": {
    "@type": "DefinedTerm",
    "identifier": "GO:0006805",
    "name": "xenobiotic metabolic process",
    "inDefinedTermSet": "Gene Ontology"
  },
  "hasBioChemEntityPart": [
    {
      "@type": "MolecularEntity",
      "identifier": "CHEMBL1201246",
      "name": "Ibuprofen",
      "roleInBiochemicalEntity": "substrate"
    },
    {
      "@type": "MolecularEntity",
      "identifier": "METABOLITE_001",
      "name": "Hydroxy-ibuprofen",
      "roleInBiochemicalEntity": "product"
    }
  ]
}
```

### 2.2 LabProtocol Profile

**Required Properties:**
- `@type`: LabProtocol
- `name`: Protocol name
- `purpose`: Biotransformation assay
- `protocolStep`: Sequential steps
- `reagent`: List of reagents used
- `instrument`: Equipment and instruments

**Example:**
```json
{
  "@context": "https://schema.org",
  "@type": "LabProtocol",
  "identifier": "PROTO_BT_001",
  "name": "Anaerobic bacterial biotransformation assay",
  "purpose": "Measure xenobiotic biotransformation by gut bacteria",
  "protocolStep": [
    {
      "@type": "HowToStep",
      "name": "Bacterial culture preparation",
      "text": "Grow bacteria to stationary phase in BHI medium"
    },
    {
      "@type": "HowToStep",
      "name": "Xenobiotic exposure",
      "text": "Add xenobiotic to final concentration of 100 µM"
    },
    {
      "@type": "HowToStep",
      "name": "Incubation",
      "text": "Incubate anaerobically at 37°C for 24 hours"
    },
    {
      "@type": "HowToStep",
      "name": "Sample extraction",
      "text": "Extract metabolites with acidified acetonitrile"
    },
    {
      "@type": "HowToStep",
      "name": "LC-MS analysis",
      "text": "Analyze by LC-MS/MS in negative ion mode"
    }
  ]
}
```

### 2.3 Dataset Profile

For biotransformation results:

**Required Properties:**
- `@type`: Dataset
- `name`: Dataset title
- `description`: Biotransformation data description
- `about`: Links to substrates and organisms
- `measurementTechnique`: Analytical method
- `variableMeasured`: Parameters measured

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

### 8.1 ChEMBL ACTIVITY.tsv Structure

**Complete Column Definitions:**

| Column | Required | Type | Description | Example |
|--------|----------|------|-------------|---------|
| CIDX | Yes | String | Compound identifier | C001 |
| CRIDX | No | String | Compound record index | CREC_001 |
| SRC_ID_CIDX | No | String | Source database compound ID | CHEMBL1201246 |
| AIDX | Yes | String | Assay identifier | A001_Ecoli_K12 |
| SRC_ID_AIDX | No | String | Source assay ID | ASSAY_001 |
| RIDX | Yes | String | Reference identifier | REF_001 |
| TEXT_VALUE | No | String | Qualitative result | Compound metabolized |
| RELATION | No | String | Relationship symbol | =, <, >, ~, <= |
| VALUE | No | Numeric | Quantitative value | 85 |
| UPPER_VALUE | No | Numeric | Upper range value | 90 |
| UNITS | No | String | Unit of measurement | % |
| SD_MINUS | No | Numeric | Standard deviation (lower) | 5.2 |
| SD_PLUS | No | Numeric | Standard deviation (upper) | 5.2 |
| ACTIVITY_COMMENT | No | Text | Additional notes | Anaerobic conditions |
| CRIDX_CHEMBLID | No | String | ChEMBL compound ID | CHEMBL1201246 |
| CRIDX_DOCID | No | String | Document identifier | DOC_001 |
| ACT_ID | No | String | Activity record ID | ACT_001 |
| TEOID | No | String | Target ontology ID | |
| TYPE | Yes | String | Activity type | Biotransformation |
| ACTION_TYPE | No | String | Action description | SUBSTRATE, PRODUCT |

### 8.2 Example ACTIVITY.tsv Entries

**Substrate Depletion:**
```tsv
CIDX	AIDX	RIDX	TEXT_VALUE	RELATION	VALUE	UNITS	SD_MINUS	SD_PLUS	TYPE	ACTION_TYPE	ACTIVITY_COMMENT
C001	A001_Ecoli_K12	REF_001	Compound metabolized	=	85	%	5.2	5.2	Biotransformation	SUBSTRATE	After 24h anaerobic incubation
```

**Product Formation:**
```tsv
CIDX	AIDX	RIDX	TEXT_VALUE	RELATION	VALUE	UNITS	TYPE	ACTION_TYPE	ACTIVITY_COMMENT
P001	A001_Ecoli_K12	REF_001	Product detected	=	72	µM	Biotransformation	PRODUCT	Hydroxy-ibuprofen formed
```

**Transformation Rate:**
```tsv
CIDX	AIDX	RIDX	RELATION	VALUE	UNITS	SD_MINUS	SD_PLUS	TYPE	ACTIVITY_COMMENT
C001	A001_Ecoli_K12	REF_001	=	3.5	µM/hour	0.4	0.4	Biotransformation	Linear rate 0-24h, R²=0.98
```

**No Activity:**
```tsv
CIDX	AIDX	RIDX	TEXT_VALUE	TYPE	ACTION_TYPE	ACTIVITY_COMMENT
C002	A001_Ecoli_K12	REF_001	No biotransformation detected	Biotransformation	No Activity	No change after 48h
```

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

## 11. Minimum Required Information Checklist

### 11.1 Assay Design (Level A - Essential)

- [ ] Assay identifier (AIDX) with naming convention
- [ ] Complete assay description
- [ ] Assay type (whole cell, lysate, enzyme)
- [ ] Experimental format (endpoint, time-course, dose-response)
- [ ] Link to organism (NCBI TaxID, strain)
- [ ] Link to substrate (CIDX, chemical structure)

### 11.2 Experimental Conditions (Level A - Essential)

- [ ] Substrate concentration with units
- [ ] Cell/protein concentration
- [ ] Reaction volume
- [ ] Temperature
- [ ] Atmosphere (aerobic/anaerobic)
- [ ] Incubation time
- [ ] pH (if controlled)

### 11.3 Analytical Method (Level A - Essential)

- [ ] Detection platform (LC-MS, GC-MS, NMR, etc.)
- [ ] Instrument details
- [ ] Method parameters (column, gradient, etc.)
- [ ] Quantification method (standard curve, internal standard)
- [ ] LOQ and LOD

### 11.4 Activity Data (Level A - Essential)

- [ ] Activity type (substrate depletion, product formation)
- [ ] Quantitative value with units
- [ ] Standard deviation or error
- [ ] Number of replicates (biological and technical)
- [ ] Statistical significance (p-value)

### 11.5 Controls (Level A - Essential)

- [ ] Negative control (heat-killed or medium only)
- [ ] Positive control (known transformation)
- [ ] Blank samples
- [ ] Internal standard (for quantitative assays)

### 11.6 Product Information (Level B - Recommended)

- [ ] Product identification (name, structure)
- [ ] MSI identification level
- [ ] MS² or NMR data
- [ ] Transformation type (hydroxylation, reduction, etc.)
- [ ] Proposed pathway

### 11.7 Quality Assurance (Level B - Recommended)

- [ ] Method validation parameters
- [ ] Recovery percentages
- [ ] Reproducibility (CV%)
- [ ] Acceptance criteria met
- [ ] Outlier handling

### 11.8 Enhanced Data (Level C - Optional)

- [ ] Kinetic parameters (Km, Vmax, kcat)
- [ ] Mechanistic studies (inhibitors, cofactor requirements)
- [ ] Enzyme identification (gene, protein)
- [ ] Computational modeling
- [ ] Additional analytical techniques

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

## 14. Software and Tools

### 14.1 Recommended Software

**Data Acquisition:**
- **LC-MS:** Xcalibur, MassLynx, Analyst
- **GC-MS:** ChemStation, GCMSsolution
- **NMR:** TopSpin, VnmrJ

**Data Processing:**
- **Peak detection:** MZmine, XCMS, MS-DIAL
- **Structure elucidation:** MassBank, SIRIUS, MetFrag
- **Statistics:** R, Python (scipy, statsmodels)
- **Visualization:** GraphPad Prism, ggplot2, matplotlib

**Data Management:**
- **ISA-Tools:** Metadata management
- **GNPS:** Molecular networking
- **MetaboLights:** Data deposition
- **ChEMBL Loader:** Submission validation

### 14.2 Computational Tools

**Pathway Prediction:**
- BioTransformer
- GLORYx
- MetaPrint2D-React
- SyGMa

**Data Analysis Pipelines:**
```bash
# Example R workflow
library(xcms)
library(CAMERA)
library(MetaboAnalystR)

# Process LC-MS data
xdata <- readMSData("data.mzML", mode="onDisk")
peaks <- findChromPeaks(xdata, param=CentWaveParam())
results <- groupChromPeaks(peaks, param=PeakDensityParam())
```

---

## 15. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-05 | Initial release: Core biotransformation standards |

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
- **Email:** [Contact information]
- **Repository:** [GitHub repository URL]

This standard bridges MIX-MB(X) and MIX-MB(M) to provide comprehensive documentation of microbial xenobiotic biotransformation processes. It is a living document that will be updated based on community feedback and evolving best practices.

---

## Appendix: Quick Start Guide

### For Experimentalists

**Before Starting:**
1. ✓ Read MIX-MB(X) for substrate preparation
2. ✓ Read MIX-MB(M) for organism cultivation
3. ✓ Design assay with all required controls
4. ✓ Plan sampling strategy and timepoints

**During Experiment:**
5. ✓ Record all parameters in real-time
6. ✓ Include internal standards
7. ✓ Run all controls
8. ✓ Document deviations

**After Experiment:**
9. ✓ Process data according to Section 5
10. ✓ Complete all Level A checklist items
11. ✓ Validate against QC criteria
12. ✓ Prepare submission files

**Minimum for Publication:**
- All Level A (Essential) items complete
- Gold or Silver quality tier
- Raw data deposited in public repository
- Statistical analysis included

