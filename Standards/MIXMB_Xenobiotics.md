# MIX-MB(X): Xenobiotics Component Standard
**Author:** Mahnoor Zulfiqar
**Version:** 0.1.0  
**Release Date:** February 5, 2026 (Draft)  
**Status:** Draft Standard  
**Part of:** MIX-MB Standard v0.1  
**Replaces:** N/A  
**Compatible with:** 
- MIX-MB(M) v0.1.0
- MIX-MB(B) v0.1.0

**Breaking Changes:** N/A

---

## 1. Overview

MIX-MB(X) establishes minimum information standards for reporting microbial biotransformation of xenobiotics, ensuring data is:
- **Findable:** Properly annotated with identifiers and metadata
- **Accessible:** Standardized formats for submission to public repositories
- **Interoperable:** Uses community ontologies and controlled vocabularies
- **Reusable:** Complete provenance and methodology information

### 1.1 How is this document organised?

### 1.2 Which sections are important for contributors?

### 1.3 Which sections are important for the data submitors?


---


## 2. Bioschemas
MIX-MB(X) integrates already established standards such as BioSchema profile [Bioschemas MolecularEntity](https://bioschemas.org/types/MolecularEntity/). BioSchemas fulfils Findability aspect of FAIR. Note that MolecularEntity is not inclusive of all fields present in the Bioschemas MolecularEntity Profile, some are specific to this use case.

### 2.1 Xenobiotics -- MolecularEntity Profile with Concentration

The parent compound or xenobiotic used within the research follows [Bioschemas MolecularEntity](https://bioschemas.org/types/MolecularEntity/) with concentration and sample information captured as properties:

**Required Properties:**
- `@context`: https://schema.org/
- `@type`: MolecularEntity
- `inChIKey`: Standard InChI Key
- `identifier`: Compound identifier (ChEMBL ID, PubChem CID, InChI Key)
- `smiles`: Canonical SMILES string
- `molecularFormula`: Chemical formula
- `molecularWeight`: Molecular weight with unit [Units should be included in the form ‘ ‘, for example ‘12 amu’ or as ‘.]

**Recommended Properties:**
- `url`: Link to compound in databases (ChEMBL, PubChem, ChEBI)
- `iupacName`: IUPAC systematic name
- `alternateName`: preferred compound name
- `monoisotopicMolecularWeight`: Exact mass
- `chemicalRole`: Role classification from ChEBI (xenobiotic, drug, metabolite)
- `associatedDisease`: a disease can be a MedicalCondition or a URL
- `bioChemInteraction`:
- `bioChemSimilarity`:
- `biologicalRole`:
- `description`:
- `image`:
- `isInvolvedInBiologicalProcess`

**Sample Properties (using `additionalProperty`) not available in the MolecularEntity Profile:**
- `purity`: Purity percentage and measurement method
- `manufacturer`: Source/vendor information
- `stock_concentration`: Initial concentration with unit
- `storage_conditions`: Storage conditions and stability notes

**Example - Xenobiotic Substrate:**
```json
{
  "@context": "https://schema.org",
  "@type": "MolecularEntity",
  "identifier": "CHEMBL1201246",
  "inChIKey": "HEFNNWSXXWATRW-UHFFFAOYSA-N",
  "iupacName": "2-(4-isobutylphenyl)propionic acid",
  "alternateName": ["Advil", "Brufen", "Nurofen"],
  "smiles": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
  "molecularFormula": "C13H18O2",
  "molecularWeight": {
    "@type": "QuantitativeValue",
    "value": "206.28",
    "unitCode": "GM"
  },
  "monoisotopicMolecularWeight": {
    "@type": "QuantitativeValue",
    "value": "206.1307",
    "unitCode": "DA"
  },
  "chemicalRole": ["xenobiotic", "non-steroidal anti-inflammatory drug"],
  "biologicalRole": [
    "http://purl.obolibrary.org/obo/CHEBI_50906",
    "http://purl.obolibrary.org/obo/CHEBI_35480"
  ],
  "url": "https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1201246/",
  "description": "Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) used to treat pain, fever, and inflammation. It is widely used as a model compound for studying xenobiotic biotransformation by gut microbiota.",
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "Purity",
      "value": "≥98%",
      "measurementTechnique": "High-Performance Liquid Chromatography"
    },
    {
      "@type": "PropertyValue",
      "name": "Vendor",
      "value": "Sigma-Aldrich"
    },
    {
      "@type": "PropertyValue",
      "name": "Stock Concentration",
      "value": "100",
      "unitCode": "MMO"
    },
    {
      "@type": "PropertyValue",
      "name": "Storage Conditions",
      "value": "Room temperature, dry conditions"
    }
  ]
}
```

### 2.2 Products and Metabolites with MSI Levels

For biotransformation products characterised with mass spectrometry (MS), use the same **MolecularEntity profile** with **MSI identification confidence levels** to indicate the degree of characterization. This profile is optional and is only important in case of a xenobiotics product is measured and detected. 

**MSI Level Guidelines:**

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
- `molecularWeight`: Molecular weight with unit [Units should be included in the form ‘ ‘, for example ‘12 amu’ or as ‘.]
- `identifier`: Product identifier (or "UNKNOWN_" prefix if unknown)
- `isPartOfBioChemEntity`: Reference to parent xenobiotic
- `chemicalRole`: Must include "metabolite" and/or "biotransformation product"
- `additionalProperty`: Must include MSI identification level

**Recommended Properties (if known):**
- `inChIKey`: Standard InChI Key
- `alternateName`: Product name or systematic designation
- `smiles`: Canonical SMILES string
- `molecularFormula`: Chemical formula
- `inChIKey`: Standard InChI Key
- `smiles`: Canonical SMILES string
- `monoisotopicMolecularWeight`: Exact mass
- `chemicalRole`: Role classification from ChEBI (xenobiotic, drug, metabolite)
- `associatedDisease`: a disease can be a MedicalCondition or a URL
- `bioChemInteraction`:
- `bioChemSimilarity`:
- `biologicalRole`:
- `description`:
- `image`:
- `isInvolvedInBiologicalProcess`:


**Level 1 Example - Identified Product (Confirmed with Standard):**
```json
{
  "@context": "https://schema.org",
  "@type": "MolecularEntity",
  "identifier": "HMDB0001923",
  "alternateName": "2-Hydroxyibuprofen",
  "inChIKey": "ZISAWCKPVBGBBM-UHFFFAOYSA-N",
  "smiles": "CC(C)Cc1ccc(cc1)C(C)(O)C(=O)O",
  "molecularFormula": "C13H18O3",
  "molecularWeight": {
    "@type": "QuantitativeValue",
    "value": "222.28",
    "unitCode": "GM"
  },
  "monoisotopicMolecularWeight": {
    "@type": "QuantitativeValue",
    "value": "222.1256",
    "unitCode": "DA"
  },
  "chemicalRole": [
    "metabolite",
    "biotransformation product",
    "hydroxylated derivative"
  ],
  "biologicalRole": [
    "http://purl.obolibrary.org/obo/CHEBI_25212"
  ],
  "isPartOfBioChemEntity": {
    "@type": "MolecularEntity",
    "identifier": "CHEMBL1201246",
    "alternateName": "Ibuprofen"
  },
  "description": "Phase I metabolite of Ibuprofen formed via hydroxylation. Detected with authentic reference standard.",
  "url": "https://www.hmdb.ca/metabolites/HMDB0001923",
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "MSI Identification Level",
      "value": "Level 1",
      "description": "Identified - Confirmed with authentic reference standard"
    },
    {
      "@type": "PropertyValue",
      "name": "Retention Time",
      "value": "4.32",
      "unitCode": "MIN"
    },
    {
      "@type": "PropertyValue",
      "name": "Retention Time Match",
      "value": "0.01 min difference from standard",
      "description": "Reference standard: 4.33 min"
    },
    {
      "@type": "PropertyValue",
      "name": "MS/MS Similarity Score",
      "value": "0.99",
      "description": "Match to standard MS/MS spectrum"
    },
    {
      "@type": "PropertyValue",
      "name": "Reference Standard",
      "value": "Sigma-Aldrich, Catalog #H7629",
      "description": "Authentic 2-Hydroxyibuprofen standard used for confirmation"
    },
    {
      "@type": "PropertyValue",
      "name": "Transformation Type",
      "value": "hydroxylation",
      "valueReference": "http://purl.obolibrary.org/obo/GO_0018126"
    },
    {
      "@type": "PropertyValue",
      "name": "Quantitation",
      "value": "45.2",
      "unitCode": "UMO",
      "description": "µM after 24 hours incubation"
    }
  ]
}
```

**Level 2 Example - Putatively Annotated (Library Match):**
```json
{
  "@context": "https://schema.org",
  "@type": "MolecularEntity",
  "identifier": "M1_PUTATIVE",
  "alternateName": "Ibuprofen metabolite M1 (putative)",
  "molecularFormula": "C13H18O3",
  "molecularWeight": {
    "@type": "QuantitativeValue",
    "value": "222.28",
    "unitCode": "GM"
  },
  "monoisotopicMolecularWeight": {
    "@type": "QuantitativeValue",
    "value": "222.1256",
    "unitCode": "DA"
  },
  "chemicalRole": [
    "metabolite",
    "biotransformation product",
    "putative structure"
  ],
  "isPartOfBioChemEntity": {
    "@type": "MolecularEntity",
    "identifier": "CHEMBL1201246",
    "alternateName": "Ibuprofen"
  },
  "description": "Putative Ibuprofen metabolite identified via MS/MS spectral library matching with high confidence.",
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "MSI Identification Level",
      "value": "Level 2",
      "description": "Putatively annotated via MS/MS spectral library match"
    },
    {
      "@type": "PropertyValue",
      "name": "MS/MS Similarity Score",
      "value": "0.82",
      "description": "GNPS library match (normalized dot product)"
    },
    {
      "@type": "PropertyValue",
      "name": "Library Match",
      "value": "MassBank (MB009246)",
      "description": "Best hit: 2-Hydroxyibuprofen with cosine similarity 0.82"
    },
    {
      "@type": "PropertyValue",
      "name": "Retention Time",
      "value": "4.35",
      "unitCode": "MIN"
    },
    {
      "@type": "PropertyValue",
      "name": "Retention Index Match",
      "value": "Agreement within 5 RI units",
      "description": "Experimental RI: 1245, Literature RI: 1248"
    },
    {
      "@type": "PropertyValue",
      "name": "Exact Mass",
      "value": "222.1256",
      "unitCode": "DA"
    },
    {
      "@type": "PropertyValue",
      "name": "Structural Hypothesis",
      "value": "hydroxylation",
      "description": "Most probable based on MS/MS fragmentation pattern"
    },
    {
      "@type": "PropertyValue",
      "name": "Confidence",
      "value": "High",
      "description": "Strong MS/MS and retention time agreement"
    },
    {
      "@type": "PropertyValue",
      "name": "Quantitation",
      "value": "38.5",
      "unitCode": "UMO",
      "description": "µM after 24 hours (semi-quantitative)"
    }
  ]
}
```

**Level 3 Example - Putatively Characterized (Chemical Class Known):**
```json
{
  "@context": "https://schema.org",
  "@type": "MolecularEntity",
  "identifier": "M2_PUTATIVE",
  "alternateName": "Ibuprofen dihydroxy metabolite (putative)",
  "molecularFormula": "C13H18O4",
  "molecularWeight": {
    "@type": "QuantitativeValue",
    "value": "238.28",
    "unitCode": "GM"
  },
  "monoisotopicMolecularWeight": {
    "@type": "QuantitativeValue",
    "value": "238.1205",
    "unitCode": "DA"
  },
  "chemicalRole": [
    "metabolite",
    "biotransformation product",
    "polyhydroxylated derivative"
  ],
  "isPartOfBioChemEntity": {
    "@type": "MolecularEntity",
    "identifier": "CHEMBL1201246",
    "alternateName": "Ibuprofen"
  },
  "description": "Putatively characterized Ibuprofen metabolite with confirmed molecular formula and functional group assignment based on MS/MS fragmentation.",
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "MSI Identification Level",
      "value": "Level 3",
      "description": "Putatively characterized - Chemical class identified"
    },
    {
      "@type": "PropertyValue",
      "name": "Molecular Formula",
      "value": "C13H18O4",
      "description": "Confirmed via accurate mass measurement"
    },
    {
      "@type": "PropertyValue",
      "name": "Mass Difference from Parent",
      "value": "+32 Da",
      "description": "Indicates double hydroxylation from parent (M+32)"
    },
    {
      "@type": "PropertyValue",
      "name": "Chemical Class",
      "value": "Dihydroxylated phenylpropionic acid",
      "description": "Functional group assignment based on MS/MS fragmentation"
    },
    {
      "@type": "PropertyValue",
      "name": "Fragment Pattern",
      "value": "Consistent with dihydroxy-ibuprofen",
      "description": "Key fragments at m/z 177, 159, 137 match expected fragmentation"
    },
    {
      "@type": "PropertyValue",
      "name": "Degree of Unsaturation",
      "value": "5",
      "description": "Benzene ring (4) + carboxylic acid (1)"
    },
    {
      "@type": "PropertyValue",
      "name": "Retention Time",
      "value": "3.87",
      "unitCode": "MIN"
    },
    {
      "@type": "PropertyValue",
      "name": "Exact Mass",
      "value": "238.1205",
      "unitCode": "DA"
    },
    {
      "@type": "PropertyValue",
      "name": "Structural Hypothesis",
      "value": "Double hydroxylation at aliphatic side chains",
      "description": "Most consistent with oxidative metabolism"
    },
    {
      "@type": "PropertyValue",
      "name": "Confidence",
      "value": "Medium-High",
      "description": "Chemical class confirmed but exact hydroxylation sites unknown"
    },
    {
      "@type": "PropertyValue",
      "name": "Quantitation",
      "value": "12.3",
      "unitCode": "UMO",
      "description": "µM after 24 hours (semi-quantitative)"
    }
  ]
}
```

**Level 4 Example - Unknown Compound (Minimal Information):**
```json
{
  "@context": "https://schema.org",
  "@type": "MolecularEntity",
  "identifier": "UNKNOWN_M3",
  "alternateName": "Unknown biotransformation product M3",
  "chemicalRole": [
    "metabolite",
    "biotransformation product",
    "unknown structure"
  ],
  "isPartOfBioChemEntity": {
    "@type": "MolecularEntity",
    "identifier": "CHEMBL1201246",
    "alternateName": "Ibuprofen"
  },
  "description": "Unknown Ibuprofen metabolite detected with minimal structural information available. Only exact mass measurement performed.",
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "MSI Identification Level",
      "value": "Level 4",
      "description": "Unknown compound - Minimal structural information available"
    },
    {
      "@type": "PropertyValue",
      "name": "Detected Mass",
      "value": "254.1154",
      "unitCode": "DA"
    },
    {
      "@type": "PropertyValue",
      "name": "Retention Time",
      "value": "2.45",
      "unitCode": "MIN"
    },
    {
      "@type": "PropertyValue",
      "name": "MS/MS Available",
      "value": "No",
      "description": "Insufficient intensity for MS/MS acquisition"
    },
    {
      "@type": "PropertyValue",
      "name": "Possible Molecular Formula",
      "value": "C13H18O5",
      "description": "Calculated from exact mass (m/z ± 5 ppm)"
    },
    {
      "@type": "PropertyValue",
      "name": "Signal-to-Noise Ratio",
      "value": "25"
    },
    {
      "@type": "PropertyValue",
      "name": "Detection Consistency",
      "value": "2 out of 3 replicates"
    },
    {
      "@type": "PropertyValue",
      "name": "Confidence in Detection",
      "value": "Medium",
      "description": "Reproducible but low intensity signal"
    },
    {
      "@type": "PropertyValue",
      "name": "Quantitation",
      "value": "5.7",
      "unitCode": "UMO",
      "description": "µM after 24 hours (detection only, approximate)"
    },
    {
      "@type": "PropertyValue",
      "name": "Recommendations for Further Study",
      "value": "Increase sample enrichment, high-resolution MS fragmentation, NMR characterization, isolation and purification"
    }
  ]
}
```
**Level 5 Example - Unidentified Compound (Spectral Data Only):**
```json
{
  "@context": "https://schema.org",
  "@type": "MolecularEntity",
  "identifier": "UNIDENTIFIED_M1",
  "alternateName": "Unknown biotransformation product M1",
  "chemicalRole": [
    "metabolite",
    "biotransformation product",
    "unidentified"
  ],
  "isPartOfBioChemEntity": {
    "@type": "MolecularEntity",
    "identifier": "CHEMBL1201246",
    "alternateName": "Ibuprofen"
  },
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "MSI Identification Level",
      "value": "Level 0",
      "description": "Unidentified - Spectral data only, no structural hypothesis"
    },
    {
      "@type": "PropertyValue",
      "name": "Detected Mass",
      "value": "254.1154",
      "unitCode": "DA"
    },
    {
      "@type": "PropertyValue",
      "name": "Retention Time",
      "value": "2.12",
      "unitCode": "MIN"
    },
    {
      "@type": "PropertyValue",
      "name": "Signal-to-Noise Ratio",
      "value": "45"
    },
    {
      "@type": "PropertyValue",
      "name": "Detection Frequency",
      "value": "All replicates (n=3)",
      "description": "Consistent detection across biological replicates"
    },
    {
      "@type": "PropertyValue",
      "name": "Quantitation",
      "value": "2.1",
      "unitCode": "UMO",
      "description": "µM after 24 hours (detection only)"
    },
    {
      "@type": "PropertyValue",
      "name": "Recommendations for Further Study",
      "value": "High-resolution accurate mass measurement, MS/MS fragmentation, NMR characterization"
    }
  ]
}
```

### 2.3 Concentration Documentation

**Concentration is documented in `additionalProperty` for both substrates and products:**

| Parameter | Type | Unit | Example |
|-----------|------|------|---------|
| **stock_concentration** | Initial compound concentration | mmol/L, mg/mL, µg/µL | 100 mmol/L |
| **initial_concentration** | Starting concentration in assay | mmol/L, µM, µg/mL | 50 µM |
| **final_concentration** | Measured concentration at timepoint | mmol/L, µM, µg/mL | 2.5 µM (at 24h) |
| **concentration_change** | Absolute or relative change | mmol/L, %, fold-change | 95% degradation |
| **detection_limit** | Lower limit of quantitation | nmol/L, µg/mL, ppm | 10 nM |

**Example - Quantitation Fields:**
```json
"additionalProperty": [
  {
    "@type": "PropertyValue",
    "name": "Initial Substrate Concentration",
    "value": "100",
    "unitCode": "UMO",
    "description": "µM Ibuprofen at time 0"
  },
  {
    "@type": "PropertyValue",
    "name": "Final Substrate Concentration",
    "value": "5",
    "unitCode": "UMO",
    "description": "µM Ibuprofen after 24 hours"
  },
  {
    "@type": "PropertyValue",
    "name": "Substrate Degradation",
    "value": "95",
    "unitCode": "%",
    "description": "Percentage of parent compound consumed"
  },
  {
    "@type": "PropertyValue",
    "name": "Product Formation",
    "value": "45.2",
    "unitCode": "UMO",
    "description": "µM 2-Hydroxyibuprofen formed"
  },
  {
    "@type": "PropertyValue",
    "name": "Mass Balance",
    "value": "85",
    "unitCode": "%",
    "description": "Percentage of initial substrate recovered as products"
  }
]
```

---

## 3. Ontologies

### 3.1 ChEBI (Chemical Entities of Biological Interest)

**Required ChEBI Classifications:**
- **Chemical Class:** Parent chemical class (e.g., CHEBI:50906 'xenobiotic')
- **Role:** Biochemical role (e.g., CHEBI:35610 'drug', CHEBI:49295 'pharmaceutical')
- **Application:** Intended use (e.g., CHEBI:35842 'analgesic', CHEBI:33281 'antimicrobial')

**Example Annotations:**
```
Ibuprofen:
  - CHEBI:5855 (ibuprofen)
  - CHEBI:35842 (analgesic)
  - CHEBI:35480 (anti-inflammatory agent)
  - CHEBI:50906 (xenobiotic)
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
Ibuprofen:
  Kingdom: Organic compounds
  Superclass: Benzenoids
  Class: Benzene and substituted derivatives
  Subclass: Phenylpropanoic acids
  Direct Parent: Phenylpropanoic acids
```

### 3.3 Unit Ontology (UO)

Use [Unit Ontology](https://bioportal.bioontology.org/ontologies/UO) for standardized unit codes in quantitative measurements. UO ensures interoperability of measurement data across databases and computational tools.

**Required Unit Codes:**
- **Mass:** `GM` (gram), `DA` (dalton), `MGM` (milligram), `UGM` (microgram)
- **Volume:** `ML` (milliliter), `UL` (microliter), `NL` (nanoliter)
- **Concentration:** `MMO` (millimolar), `UMO` (micromolar), `NMO` (nanomolar), `PMO` (picomolar)
- **Time:** `MIN` (minute), `HOUR` (hour), `DAY (day), `SEC` (second)
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

**Implementation in JSON:**
```json
{
  "molecularWeight": {
    "@type": "QuantitativeValue",
    "value": "206.28",
    "unitCode": "GM"
  },
  "monoisotopicMolecularWeight": {
    "@type": "QuantitativeValue",
    "value": "206.1307",
    "unitCode": "DA"
  }
}
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

**Example - Biotransformation Annotation:**
```json
{
  "@type": "PropertyValue",
  "name": "Biotransformation Type",
  "value": "hydroxylation",
  "valueReference": "http://purl.obolibrary.org/obo/GO_0018126",
  "description": "Addition of hydroxyl group (-OH) catalyzed by cytochrome P450 monooxygenase"
}
```

**Multi-step Biotransformation Example:**
```yaml
biotransformation_pathway:
  - step_1:
      process: "Phase I - Hydroxylation"
      go_term: "GO:0018126"
      enzyme: "CYP2E1"
      product: "2-Hydroxyibuprofen"
  
  - step_2:
      process: "Phase II - Glucuronidation"
      go_term: "GO:0008194"
      enzyme: "UDP-glucuronosyltransferase"
      product: "2-Hydroxyibuprofen glucuronide"
```

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

---

## 4. MSI Metabolomics Standards

MSI metabolite annotation levels of confidence are already mentioned in the BioSchemas section. [Metabolomics Standards Initiative (MSI)](https://metabolomicssociety.org/resources/metabolomics-standards-initiative) are minimum standards developed to report metabolomics data and studies:

### 4.1 Chemical Analysis

**Required Information:**
- **Xenobiotic Substrate:**
  - Chemical identifier (ChEMBL ID, PubChem CID, InChI Key)
  - Concentration with units
  - Purity (%)
  - Source/vendor
  
- **Detection Method:**
  - Analytical platform (LC-MS, GC-MS, NMR, UV-Vis)
  - Instrument model
  - Column/separation method (if applicable)
  - Detection mode (e.g., positive/negative ionization)

**Example:**
```yaml
substrate:
  compound: "Ibuprofen"
  chembl_id: "CHEMBL1201246"
  inchi_key: "HEFNNWSXXWATRW-UHFFFAOYSA-N"
  concentration: "100 µM"
  purity: "≥98%"
  vendor: "Sigma-Aldrich"
  catalog_number: "I4883"

analytical_method:
  platform: "LC-MS"
  instrument: "Thermo Q Exactive Plus Orbitrap"
  column: "Waters Acquity UPLC BEH C18 (2.1 x 100 mm, 1.7 µm)"
  ionization: "ESI negative mode"
  mass_range: "50-1000 m/z"
  resolution: "70,000 FWHM"
```

### 4.2 Data Processing

**Required Information:**
- **Quantification method:**
  - Standard curve vs. semi-quantitative
  - Internal standards used
  - Calibration range
  
- **Quality control:**
  - Blank controls
  - Positive/negative controls
  - Replication (biological and technical)
  
- **Data processing:**
  - Software used
  - Peak detection parameters
  - Normalization method

**Example:**
```yaml
quantification:
  method: "external standard curve"
  standard_range: "1-500 µM"
  internal_standard: "13C6-Ibuprofen"
  linearity_r2: 0.998

quality_control:
  blank_controls: "media without bacteria"
  positive_control: "E. coli with xenobiotic"
  negative_control: "E. coli without xenobiotic"
  biological_replicates: 3
  technical_replicates: 2

data_processing:
  software: "Xcalibur v4.1, MZmine 2.53"
  peak_detection: "mass tolerance 5 ppm"
  normalization: "cell density (OD600)"
```

### 4.4 Metabolite Identification

Use MSI identification confidence levels:

- **Level 1:** Identified compounds (match to authentic standard)
- **Level 2:** Putatively annotated (MS² or library match)
- **Level 3:** Putatively characterized (chemical class)
- **Level 4:** Unknown compounds

**Required for Each Metabolite:**
```yaml
metabolite_id: "M1"
identification_level: "Level 2"
compound_name: "Hydroxy-ibuprofen"
exact_mass: 222.1256
retention_time: "4.32 min"
ms2_similarity: 0.85
reference_database: "MassBank, HMDB"
confidence_score: "High"
```

---

## 5. Data Formats


### 5.2 ISA-Tab Format

For complex experimental metadata, use [ISA-Tab](https://isa-tools.org/) format:

**Structure:**
- `i_investigation.txt` - Study overview
- `s_study.txt` - Sample information
- `a_assay.txt` - Assay details

**Key Characteristics:**
```
Study Characteristic[Organism]: Escherichia coli
Study Characteristic[Strain]: K-12 MG1655
Study Characteristic[Growth Medium]: M9 minimal medium
Protocol REF: Biotransformation Protocol
Parameter Value[Substrate]: Ibuprofen
Parameter Value[Concentration]: 100 µM
Parameter Value[Incubation Time]: 24 hours
```

### 5.3 mzML Format

For mass spectrometry data, use [mzML](http://www.psidev.info/mzml) (Proteomics Standards Initiative):

**Requirements:**
- Instrument metadata
- Acquisition parameters
- Peak lists (m/z, intensity, retention time)
- CV terms from PSI-MS ontology

### 5.4 nmrML Format

For NMR spectroscopy data, use [nmrML](http://nmrml.org/):

**Requirements:**
- Acquisition parameters (pulse sequence, field strength)
- Processing parameters
- Spectral data (chemical shift, intensity)
- Sample metadata

---


---

## 8. Data Validation Rules

### 8.1 Chemical Structure Validation

- SMILES must be valid and canonical
- InChI Key must match SMILES structure
- Molecular formula must be calculable from structure
- Molecular weight must be within 0.1 Da of calculated value

### 8.2 Biological Data Validation

- NCBI TaxID must be valid and current
- Genus and species must match TaxID
- Temperature must be between -20°C and 100°C
- pH must be between 0 and 14

### 8.3 Quantitative Data Validation

- Concentrations must be positive values
- Units must be from Unit Ontology (UO)
- Standard deviation cannot exceed mean value
- Replicates required (n≥3 for statistical analysis)

### 8.4 Cross-referencing Validation

- All CIDX in ACTIVITY.tsv must exist in COMPOUND_RECORD.tsv
- All AIDX in ACTIVITY.tsv must exist in ASSAY.tsv
- All RIDX must exist in REFERENCE.tsv
- ChEMBL IDs must be valid (if provided)

---

## 9. Data Quality Tiers

### Tier 1: Gold Standard (Publication-Ready)
- All Level A and B information complete
- Level 1 MSI metabolite identification
- Raw data deposited in public repository
- Quality control passed (blanks, standards, replicates)
- Peer-reviewed or preprint available

### Tier 2: Silver Standard (Research-Grade)
- All Level A information complete
- Level 2 MSI metabolite identification
- Technical replicates (n≥2)
- Method validation documented

### Tier 3: Bronze Standard (Preliminary)
- All Level A essential information
- Single experimental replicate
- Basic quality control
- Suitable for initial screening data

---

## 11. Implementation Guidelines

### 11.1 Data Collection Workflow

1. **Pre-experiment:** Define experimental design, ensure all metadata fields can be captured
2. **During experiment:** Record all parameters in real-time using electronic lab notebooks
3. **Post-experiment:** Process data according to MSI standards
4. **Validation:** Check all required fields before submission
5. **Deposition:** Submit to appropriate repositories (ChEMBL, MetaboLights, etc.)

### 11.2 Software Tools

**Recommended Tools:**
- **Chemical structure handling:** RDKit, OpenBabel, ChemDraw
- **Ontology annotation:** Zooma, OLS (Ontology Lookup Service)
- **Data validation:** ISA tools, ChEMBL loader validation
- **MS data processing:** MZmine, XCMS, MS-DIAL
- **NMR data processing:** NMRProcFlow, Chenomx

### 11.3 Repository Submission

**Primary Repositories:**
- **ChEMBL:** Bioactivity data submission portal
- **MetaboLights:** Metabolomics experiments and derived data
- **GNPS:** Mass spectrometry data and molecular networking
- **Zenodo:** General scientific data with DOI assignment

---

## 12. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-05 | Initial release: Core standards defined |
| 1.2.1 | 2026-03-15 | Stable release: Updated and refined standards |

---

## 13. References

1. ChEMBL Database Guidelines: https://www.ebi.ac.uk/chembl/
2. Metabolomics Standards Initiative: https://metabolomicssociety.org/resources/metabolomics-standards-initiative
3. Bioschemas Specifications: https://bioschemas.org/
4. ChEBI Ontology: https://www.ebi.ac.uk/chebi/
5. ClassyFire Chemical Taxonomy: http://classyfire.wishartlab.com/
6. ISA Framework: https://isa-tools.org/
7. FAIR Principles: https://www.go-fair.org/fair-principles/
8. Unit Ontology: https://bioportal.bioontology.org/ontologies/UO
9. BioAssay Ontology: http://www.bioassayontology.org/

---

## 14. Contact and Contributions

For questions, suggestions, or contributions to this standard, please contact:
- **Maintainer:** Mahnoor Zulfiqar
- **Institution:** NFDI4Microbiota
- **Email:** [Contact information]
- **Repository:** [GitHub repository URL]

This standard is a living document and will be updated based on community feedback and evolving best practices.