# Research Notes — BioXend Manuscript

> Prepared: 2026-05-11. Covers six literature areas for the Introduction and Discussion of the BioXend / MIX-MB manuscript.

---

## 1. ChEMBL

**Covers:**
ChEMBL is a manually curated, open, FAIR bioactivity database of small molecules with drug-like properties maintained by EMBL-EBI. It contains more than 20.3 million bioactivity measurements across 2.4 million unique compounds, 17,000+ targets, and spans literature data from 1974 to the present. Data are sourced from peer-reviewed medicinal chemistry journals, deposited datasets (420 as of 2023), patents, and books. Data types include binding, functional, ADMET, and toxicity assays. The **ChEMBL Deposition Programme** accepts externally deposited datasets in a structured six-file format:

| File | Content |
|---|---|
| `REFERENCE.tsv` | Publication or dataset metadata (RIDX, TITLE, ABSTRACT, AUTHORS, YEAR, DOI, REF_TYPE) |
| `COMPOUND_RECORD.tsv` | Compound records indexed by depositor-defined CIDX |
| `COMPOUND_CTAB.sdf` | 2D chemical structures in V2000 mol format |
| `ASSAY.tsv` | Assay descriptions including organism, tissue, assay type |
| `ASSAY_PARAM.tsv` | Experimental parameters per assay |
| `ACTIVITY.tsv` | Numerical or text activity values linking CIDX to AIDX |

All deposited files must be UTF-8 encoded; tab-separated values are required for all `.tsv` files.

**Does NOT cover:**
ChEMBL's deposition framework assumes classical pharmacological assay designs (binding, inhibition, ADMET). There is no dedicated metadata standard, controlled vocabulary, or submission template for microbial biotransformation data specifically — no fields for recording microbial strain identity, anaerobic/aerobic conditions, transformation type (e.g. hydroxylation, reduction), or multi-organism community assays. Depositors must map biotransformation activity records onto generic bioactivity fields without standardised guidance. Intermediate metabolites of prodrugs are not stored, and the deposition guide does not document expected identifiers for microbial assay organisms.

**Primary citation:**
Zdrazil B, Felix E, Hunter F, Manners EJ, Blackshaw J, Corbett S, de Veij M, Ioannidis H, Mendez Lopez D, Mosquera JF, Magarinos MP, Bosc N, Arcila R, Kizilören T, Gaulton A, Bento AP, Adasme MF, Monecke P, Landrum GA, Leach AR. The ChEMBL Database in 2023: a drug discovery platform spanning multiple bioactivity data types and time periods. *Nucleic Acids Research* 2024; 52(D1): D1180–D1192. https://doi.org/10.1093/nar/gkad1004

**Key facts for manuscript:**
- ChEMBL is the primary public repository for small-molecule bioactivity data and the target deposition endpoint for the BioXend pipeline; framing BioXend as enabling ChEMBL-ready submission of biotransformation data is the central contribution.
- The six-file deposition format (REFERENCE, COMPOUND_RECORD, COMPOUND_CTAB, ASSAY, ASSAY_PARAM, ACTIVITY) is the technical scaffold around which the BioXend Nextflow pipeline is built.
- The absence of any dedicated metadata framework for microbial biotransformation within ChEMBL's existing guidelines is the primary gap that MIX-MB and BioXend address.

---

## 2. MIMARKS / MIxS

**Covers:**
MIMARKS (Minimum Information about a MARker gene Sequence) and MIxS (Minimum Information about any (x) Sequence) are specifications developed by the Genomic Standards Consortium (GSC) for reporting biological sequence data. MIMARKS defines minimum metadata for marker gene sequences (e.g. 16S rRNA), while MIxS provides a unified umbrella standard applicable to metagenomes, metatranscriptomes, and amplicon sequences. The framework includes 'environmental packages' that standardise the description of the environment from which a biological sample originates, applicable to any genome sequence of known origin.

**Does NOT cover:**
MIMARKS/MIxS focus entirely on sequence metadata (sample origin, sequencing platform, target gene) and do not define any fields for: (i) chemical substrate identity (no SMILES, InChIKey, or ChEBI reference), (ii) biotransformation outcomes (metabolite production, enzyme activity, action type), (iii) in vitro assay design parameters (oxygen conditions, incubation times), or (iv) linkage of microbial sequence data to chemical bioactivity records. A researcher depositing gut microbiota drug biotransformation data in ChEMBL cannot use MIMARKS to describe the microbial component of their experiment.

**Primary citation:**
Yilmaz P, Kottmann R, Field D, et al. Minimum information about a marker gene sequence (MIMARKS) and minimum information about any (x) sequence (MIxS) specifications. *Nature Biotechnology* 2011; 29: 415–420. https://doi.org/10.1038/nbt.1823

**Key facts for manuscript:**
- MIxS is the closest existing community standard to what MIX-MB(M) addresses, but covers only sequencing metadata and not chemical or activity data.
- The gap between MIxS (sequence metadata) and ChEMBL (bioactivity data) is precisely the space that MIX-MB is designed to occupy: a cross-domain minimum information standard linking microbial identity to chemical biotransformation outcome.
- Citing MIxS in the Introduction establishes that the microbiome community already has mature metadata standards for sequencing, reinforcing that the gap is specifically at the chemistry-microbiology interface.

---

## 3. Metabolomics Reporting Standards (MSI Levels, MIAPE, MetaboLights)

### 3a. MSI Annotation Levels (Sumner et al. 2007)

**Covers:**
The Metabolomics Standards Initiative Chemical Analysis Working Group (CAWG-MSI) proposed four levels of metabolite identification confidence to standardise annotation reporting:
- **Level 1** — Identified compounds (confirmed with chemical reference standard, matching MS/MS, NMR, and retention time).
- **Level 2** — Putatively annotated compounds (no reference standard; based on physicochemical properties and/or spectral library matches).
- **Level 3** — Putatively characterised compound classes (characteristic class-level spectral features).
- **Level 4** — Unknown compounds (unidentified but quantifiable from spectral data).

A fifth level (Level 5 — exact mass only, no structural information) has been proposed in subsequent revisions.

**Does NOT cover:**
MSI levels define chemical annotation confidence for metabolomics datasets; they do not address microbial organism metadata, experimental assay design, or biotransformation activity records. A dataset reporting that bacterium X converts compound A to compound B cannot be fully described by MSI annotation levels alone.

**Primary citation:**
Sumner LW, Amberg A, Barrett D, et al. Proposed minimum reporting standards for chemical analysis. Chemical Analysis Working Group (CAWG) Metabolomics Standards Initiative (MSI). *Metabolomics* 2007; 3(3): 211–221. https://doi.org/10.1007/s11306-007-0082-2

### 3b. MetaboLights (Haug et al. 2013)

**Covers:**
MetaboLights is the first general-purpose, open-access repository for metabolomics studies maintained by EMBL-EBI. It accepts raw experimental data and associated metadata, uses the ISA-tab format for metadata capture, and requires MSI-compliant reporting. Submissions must include raw instrument data (preferably in open-source formats) and metadata supporting study design.

**Does NOT cover:**
MetaboLights submissions do not require or standardise: (i) microbial organism identity fields (no TaxID requirement), (ii) biotransformation outcome annotations (substrate vs. product vs. no-activity designations), (iii) links to chemical bioactivity databases such as ChEMBL. The repository is designed for untargeted metabolomics and does not include a deposition pathway for biotransformation activity data in ChEMBL-compatible format.

**Primary citation:**
Haug K, Salek RM, Conesa P, Hastings J, de Matos P, Rijnbeek M, Mahendraker T, Williams M, Neumann S, Rocca-Serra P, Maguire E, González-Beltrán A, Sansone SA, Griffin JL, Steinbeck C. MetaboLights — an open-access general-purpose repository for metabolomics studies and associated meta-data. *Nucleic Acids Research* 2013; 41(D1): D781–D786. https://doi.org/10.1093/nar/gks1004

**Key facts for manuscript (both standards):**
- MSI annotation levels are directly relevant to the chemical identification confidence of xenobiotic substrates and biotransformation products; MIX-MB(X) can be framed as extending MSI Level 1 requirements with additional biotransformation-specific fields.
- MetaboLights enforces MSI-compliance but has no mechanism for recording microbial biotransformation activity; this is a complementary rather than competing resource.
- Neither MSI annotation levels nor MetaboLights address the bioactivity recording dimension that ChEMBL requires — reinforcing the need for a cross-domain standard.

---

## 4. FAIR Principles

**Primary citation:**
Wilkinson MD, Dumontier M, Aalbersberg IJJ, Appleton G, Axton M, Baak A, Blomberg N, Boiten JW, da Silva Santos LB, Bourne PE, Bouwman J, Brookes AJ, Clark T, Crosas M, Dillo I, Dumon O, Edmunds S, Evelo CT, Finkers R, Gonzalez-Beltran A, Gray AJG, Groth P, Goble C, Grethe JS, Heringa J, 't Hoen PAC, Hooft R, Kuhn T, Kok R, Kok J, Lusher SJ, Martone ME, Mons A, Packer AL, Persson B, Rocca-Serra P, Roos M, van Schaik R, Sansone SA, Schultes E, Sengstag T, Slater T, Strawn G, Swertz MA, Thompson M, Van Der Lei J, Van Mulligen E, Velterop J, Waagmeester A, Wittenburg P, Wolstencroft K, Zhao J, Mons B. The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data* 2016; 3: 160018. https://doi.org/10.1038/sdata.2016.18

**Recent applications:**

1. Rocca-Serra P, et al. (Implementation of FAIR Practices in Computational Metabolomics Workflows — A Case Study). *Metabolites* 2024; 14(2): 118. https://doi.org/10.3390/metabo14020118
   — Demonstrates how FAIR principles can be applied to metabolomics data analysis workflows using the Common Workflow Language, WorkflowHub, and RO-Crate packaging.

2. The Chemistry Implementation Network (ChIN) under the GO FAIR initiative has formalised FAIRification approaches for chemical data, including defining persistent identifiers (InChIKey, SMILES) and semantic data models for chemical substance representation.

**Key facts for manuscript:**
- **Findable:** MIX-MB mandates globally unique compound identifiers (CIDX linked to ChEMBL, InChIKey, SMILES) and NCBI TaxIDs for microbial organisms, directly implementing the F1 and F2 FAIR sub-principles.
- **Accessible:** BioXend outputs ChEMBL-ready deposition files that are openly archived; ChEMBL itself is a Global Core Biodata Resource with open access, satisfying FAIR principle A.
- **Interoperable:** MIX-MB uses controlled vocabularies (ChEBI for chemical roles, NCBI Taxonomy for organisms, ChEMBL assay types) and aligns with Bioschemas profiles (MolecularEntity, Taxon, BioChemEntity), satisfying FAIR principle I.
- **Reusable:** Mandatory metadata fields (assay conditions, organism identity, transformation type, action type) ensure that datasets deposited via BioXend contain sufficient context for reuse and cross-study comparison, satisfying FAIR principle R.

---

## 5. Absence of Biotransformation-Specific Reporting Standard

**Search evidence:**

The following searches were conducted and no dedicated minimum information standard was identified:

- "minimum information standard xenobiotic biotransformation reporting" — returned general biotransformation research papers but no reporting standard.
- "reporting standard drug biotransformation microbiome minimum information checklist" — returned STORMS (microbiome study reporting) and STREAMS, neither of which includes chemical substrate or bioactivity fields.
- "MIBBI biotransformation standard minimum information gut microbiota drug" — MIBBI (Minimum Information for Biological and Biomedical Investigations) lists approximately 40 checklists, none of which covers xenobiotic microbial biotransformation. The MIBBI portal includes CIMR (Core Information for Metabolomics Reporting), MIMARKS/MIxS (sequencing), and STRENDA (enzyme data), but no standard at their intersection relevant to microbial drug biotransformation.
- "reporting standard gut microbiota drug metabolism checklist" — returned pharmacomicrobiomics reviews and database resources but no dedicated minimum information specification.

Adjacent standards that partially cover the domain but do not address it fully:
- **STORMS** (Mirzayi et al., *Nature Medicine* 2021; 27: 1885–1892) — covers microbiome study design and sequencing reporting but not chemical bioactivity data.
- **ChEMBL deposition guidelines** — cover bioactivity data format but provide no controlled vocabulary or mandatory fields specific to microbial biotransformation experimental design.
- **STRENDA** (within MIBBI) — covers enzyme kinetics data but not microbiome-level community experiments or in vivo/ex vivo biotransformation outcomes.

**Conclusion:**
As of May 2026, no dedicated minimum information standard exists for reporting xenobiotic microbial biotransformation data in a form that is simultaneously interoperable with chemical bioactivity databases (ChEMBL) and consistent with microbiome metadata standards (MIxS/MIMARKS); this gap is the primary justification for MIX-MB and BioXend.

---

## 6. Landmark Biotransformation Papers

1. **Zimmermann et al. 2019 (Nature) — primary motivating study:**
   Zimmermann M, Zimmermann-Kogadeeva M, Wegmann R, Goodman AL. Mapping human microbiome drug metabolism by gut bacteria and their genes. *Nature* 2019; 570(7762): 462–467. https://doi.org/10.1038/s41586-019-1291-3
   — By screening 76 human gut bacterial strains against 271 orally administered drugs, this study showed that the gut microbiome broadly and systematically modifies drug molecules, identifying specific bacterial genes responsible and demonstrating direct impacts on intestinal and systemic drug metabolism.

2. **Zimmermann et al. 2019 (Science):**
   Zimmermann M, Zimmermann-Kogadeeva M, Wegmann R, Goodman AL. Separating host and microbiome contributions to drug pharmacokinetics and toxicity. *Science* 2019; 363(6427): eaat9931. https://doi.org/10.1126/science.aat9931
   — Using gnotobiotic mouse models and computational integration, this companion study experimentally disentangled host hepatic metabolism from gut microbial metabolism for multiple drugs, establishing quantitative attribution of pharmacokinetic variability to the microbiome.

3. **Rekdal, Maini Rekdal, Bess et al. 2019 (Science):**
   Rekdal VM, Bess EN, Bisanz JE, Turnbaugh PJ, Balskus EP. Discovery and inhibition of an interspecies gut bacterial pathway for Levodopa metabolism. *Science* 2019; 364(6445): eaau6323. https://doi.org/10.1126/science.aau6323
   — This study identified and mechanistically characterised a two-step interspecies gut bacterial pathway (Enterococcus faecalis PLP-dependent decarboxylase followed by Eggerthella lenta molybdenum-dependent dehydroxylase) that deactivates the Parkinson's disease drug levodopa, providing a causal molecular mechanism linking gut microbiota composition to drug efficacy.

4. **Koppel, Maini Rekdal, and Balskus 2017 (Science):**
   Koppel N, Maini Rekdal V, Balskus EP. Chemical transformation of xenobiotics by the human gut microbiota. *Science* 2017; 356(6344): eaag2770. https://doi.org/10.1126/science.aag2770
   — This landmark review synthesised the state of knowledge on direct microbial chemical modification of xenobiotics in the human gut, cataloguing the types of reactions performed, the microbial enzymes involved, and the consequences for drug efficacy and toxicity, and highlighted the profound gap in systematic characterisation of these activities.

5. **Roje, Zhang, Mastrorilli et al. 2024 (Nature):**
   Roje B, Zhang B, Mastrorilli E, Kovačić A, Sušak L, Ljubenkov I, Ćosić E, Vilović K, Meštrović A, Lozo Vukovac E, Bučević-Popović V, Puljiz Ž, Karaman I, Terzić J, Zimmermann M. Gut microbiota carcinogen metabolism causes distal tissue tumours. *Nature* 2024; 632(8027): 1137–1144. https://doi.org/10.1038/s41586-024-07754-w
   — Using a combination of germ-free and gnotobiotic mouse models, this study demonstrated that gut microbial biotransformation of dietary/environmental carcinogens generates systemically distributed mutagenic metabolites that cause tumours in distal tissues, establishing a causal link between gut microbiome composition, xenobiotic metabolism, and cancer.

6. **Verdegaal and Goodman 2024 (Science Translational Medicine):**
   Verdegaal AA, Goodman AL. Integrating the gut microbiome and pharmacology. *Science Translational Medicine* 2024; 16(732): eadg8357. https://doi.org/10.1126/scitranslmed.adg8357
   — This review synthesises the current understanding of microbiome-host-drug interactions across the full pharmacokinetic spectrum (absorption, distribution, metabolism, excretion, toxicity), arguing for systematic integration of microbiome data into drug discovery and clinical pharmacology and highlighting the lack of standardised data resources enabling such integration.

---

*Notes compiled from web searches of PubMed, Nature, Science, Nucleic Acids Research, and ChEMBL documentation. All DOIs verified against primary publisher pages or PubMed records. Citations are formatted in Vancouver style consistent with ChEMBL and EMBL publication conventions.*
