# Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB)

**Author:** Mahnoor Zulfiqar

**Version:** please refer to [versions/standards-main.txt](https://github.com/zmahnoor14/BioXend/blob/main/versions/standards-main.txt) for latest version

**Status:** Draft Standard  

## Abstract
Microbial biotransformation of xenobiotics — the enzymatic conversion of drugs, environmental contaminants, and dietary compounds by microorganisms — is a research area of growing importance for human health, toxicology, and drug development. Despite increasing scientific output, data from these studies are rarely reported in a standardised or FAIR-compliant manner, limiting their reuse and integration across laboratories and databases.

The **Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB)** standard defines the minimum metadata and data elements required to describe, share, and deposit xenobiotic biotransformation experiments. MIX-MB covers three interconnected aspects of every study: 
- the chemical substrate, 
- the microbial organism or community, and 
- the biotransformation assay and its outcomes. <br>

Together, these components prepare and present the study results as reproducible, comparable across research groups that follow the standards and submission template, and directly depositable into community database: [ChEMBL](https://www.ebi.ac.uk/chembl/).

This document describes:
- scope of the standards,
- component sub-standards, 
- the template and how it maps to ChEMBL submission file, 
- controlled vocabularies,
- domain-specific FAQs

It is intended for researchers generating biotransformation data, data curators, and software developers building tools that process or submit such data.

## Scope and Applicability
### In scope
MIX-MB applies to experimental studies that measure the biotransformation of one or more xenobiotic compounds by microbial organisms or microbial-derived systems. This includes:

- **In vitro assays** — single bacterial strain, and purified enzyme reactions
- **Community-level/ in-vivo assays** — mixed microbial communities (e.g. gut microbiota, soil communities)
- **Time-course experiments** — measuring substrate depletion or product formation over time
<!--- - **Dose-response experiments** — measuring activity across a range of substrate concentrations --->
<!--- - **Ex vivo assays** — tissue or organ preparations with microbial activity --->
- **Product identification studies** — structural annotation and identification of biotransformation products using mass spectrometry. 
- **Non-xenobiotic substrates** — The standard focuses on Xenobiotics, however, the same framework can also be used for endogenous metabolites transformed by the bacteria
- **Microbial Kingdom** - The standard currently focuses on bacteria but can be applied to all microbial kingdoms: bacteria, archaea, and fungi.

### Out of scope

MIX-MB does not currently cover:

- **Purely computational predictions** of biotransformation (e.g. metabolite prediction tools with no experimental validation)
- **Metabolomics, Genomics or transcriptomics data** describing biotransformation enzymes or metabolites or equivalent sequence standards. This standard is for reporting biotransformation (bioactivity), and not for the experimental omics data (which have already their own established standards).

## Template 

The [template](exampledata/Template_filled.ods) covers the MIX-MB standard described in this document and maps to the [ChEMBL submission guidelines](https://chembl.gitbook.io/chembl-data-deposition-guide). [**ChEMBL**](https://www.ebi.ac.uk/chembl/) is a database of bioactivity associated with small molecules, used within academia and industry as a highly curated repository.

<p align="center">
  <img src="Chembl_Files.png" />
</p>

### 1. Study metadata files/ Reference sheet in template

**1.1. REFERENCE.tsv:** <br>
Reference file provides metadata regarding the study, including the DOI/ PMID, title, abstract, authors, journal, or dataset (if unpublished). For details please refer to the tutorial provided by ChEMBL on how to generate the [REFERENCE.tsv file](https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/reference.tsv). 

> **_NOTE 1 ON DOI:_** If you would like to submit unpublished dataset, and don't already have a DOI for it, you can either contact ChEMBL team before to provide you one. Or you can submit your data to Zenodo (embargoed or not - depends on the confidentiality of the data decided by the depositor). Zenodo generates a DOI for the dataset whether its private (embragoed) or public.
 
**1.2. README.toml:** <br>
Optional configuration file to mention any additional information about the study. For details please refer to the tutorial provided by ChEMBL on how to generate the [README.toml file](https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/readme.toml)

#### How are study data files from ChEMBL integrated into the Reference sheet in [Template_filled.ods](exampledata/Template_filled.ods)

The **Reference** sheet in [`Template_filled.ods`](exampledata/Template_filled.ods) maps directly to `REFERENCE.tsv` and `README.toml`. Fill in one row per study. Columns marked **Mandatory** must be completed; all others are optional or even can be automatically extracted by BioXend.

| Template Column | Maps to ChEMBL's REFERENCE.tsv | Required | Description |
|----------------|----------------------|----------|-------------|
| `DOI` | `DOI` | **Mandatory** | Must be present; if no DOI exists, contact ChEMBL to provide one |
| `DATA_LICENCE` | `DATA_LICENCE` | **Mandatory** | Licence for the deposited data, always use `CC0` for public domain |
| `CONTACT` | `CONTACT` | **Mandatory**  | Contact person ORCID and/or email (e.g. `https://orcid.org/0000-0000-0000-0000`) |
| `Reference_identifier` | `RIDX` | **Mandatory** | Meaningful unique identifier for each reference e.g: `HumanMicrobial_DrugMetabolism` |
| `PUBMED_ID` | `PUBMED_ID` | **Mandatory only if no DOI** | PubMed identifier for the asscoaited publication; if DOI is present this field can be left empty |
| `REF_TYPE` | `REF_TYPE` | **Mandatory** | Type of reference: `Publication`, `Patent`, `Dataset`, or `Book` |
| `YEAR` | `YEAR` | **Mandatory** | Year of publication, dataset or submission |
| `AUTHORS` | `AUTHORS` | **Mandatory** | List of the authors |
| `TITLE` | `TITLE` | **Mandatory** | Title of the article or dataset description |
| `ABSTRACT` | `ABSTRACT` | **Mandatory** | Abstract of the article or dataset description |
| `VOLUME` | `VOLUME` | Optional | Volume number of the publication |
| `ISSUE` | `ISSUE` | Optional | Issue number of the publication |
| `FIRST_PAGE` | `FIRST_PAGE` | Optional | First page of the article |
| `LAST_PAGE` | `LAST_PAGE` | Optional | Last page of the article |
| `PATENT_ID` | `PATENT_ID` | Optional | Patent identifier (only relevant for ChEMBL internal use) |
| `JOURNAL_NAME` | `JOURNAL_NAME` | Optional | If published: use the standard NIH NLM Catalog abbreviated journal name |



For **README.toml**, all fields are mentioned as mandatory. However, if something doesnt apply to your case you can simply mention "Not applicable" or ask ChEMBL team via: [chembl-depositors-request@ebi.ac.uk](mailto:chembl-depositors-request@ebi.ac.uk).

| Template Column | Maps to README.toml | Required | Description |
|----------------|----------------------|----------|-------------|
| `Endpoints` | `Endpoints` | **Mandatory** | Assay endpoints measured E.g. bacterial biotransformation, IC50, cytotoxicity, etc. if your deposition contains multiple different categories of assay, it will be better to subset these into different datasets. |
| `Compounds` | `Compounds` | **Mandatory** | Number of compounds tested |
| `Assays` | `Assays` | **Mandatory**  | Number of assays performed |
| `Goal_of_submission` | `Goal_of_submission` | **Mandatory** | Briefly describe what is your goal in submitting your data source to ChEMBL.|
| `Names` | `Names` | **Mandatory** | Submittors, could be different than authors of the paper |
| `Institutions` | `Institutions` | **Mandatory** | Name of your institute |
| `Links` | `Links` | **Mandatory** | any link associated with your data |
| `Description` | `Description` | **Mandatory** | Please briefly describe your dataset: study aim, organism(s), and scientific audience |
| `Recent_changes` | `Recent_changes` | **Mandatory** | List any changes since you submitted the last dataset related to this project or mention no |
| `Multiplexed` | `Multiplexed` | **Mandatory** | Do your data contain multiple assays that were performed in the same plate well? simply write TRUE/FALSE  |
| `Chembl_version` | `Chembl_version` | **Mandatory** | Ask Chembl team which version you are submitting your data for. |


### 2. Xenobiotics metadata files/ Chemicals sheet in template

**2.1. COMPOUND_RECORD.tsv:** <br>

These files contain reference identifiers and chemical identifiers, along with the name of the compound. For details please refer to the tutorial provided by ChEMBL on how to generate the [COMPOUND_RECORD.tsv file](https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/compound_record.tsv).

**2.2. COMPOUND_CTAB.sdf:** <br> 

The CTAB is an sdf file (V2000 molfile format) storing the chemical strcuture of the compounds mentioned in the `COMPOUNDS_RECORD.tsv`, together with the same chemical identifiers. For details please refer to the tutorial provided by ChEMBL on how to generate the [COMPOUND_CTAB.sdf file](https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/compound_ctab.sdf).

#### How are xenobiotics data files integrated into the Chemicals sheet in [Template_filled.ods](exampledata/Template_filled.ods)

The **Chemicals** sheet in `Template_filled.ods` maps to `COMPOUND_RECORD.tsv` and `COMPOUND_CTAB.sdf`. Fill in one row per compound. Columns auto-filled by BioXend (powered by RDKit) can be left empty; all others should be completed where available.

> **_NOTE 2 ON ADDITIONAL CHEMICAL METADATA:_** ChEMBL only requires chemical structure (.sdf file), compound names, and mass spec endpoints and metadata, however the template mentions other metadata categories such as InChI, molecular formula, monoisotopic mass etc. This additional metadata could be useful if you plan to submit this template as a supplmenetary file along with your manuscript. Use [ChEMET webapp](chemet.embl.org) to include even more metadata already available in different databases. 


| Template Column | Maps to | Required | Auto-filled by BioXend | Description |
|----------------|---------|----------|------------------------|-------------|
| `Common_Name` | `COMPOUND_NAME` | **Mandatory** | No | Common name of the xenobiotic, chemical, drug, or pesticide |
| `SMILES` | `COMPOUND_CTAB.sdf file` | **Mandatory** | No | SMILES string of the compound. Use [ChEMET](chemet.embl.org) web app to check whether SMILES you collected are all valid. |
| `Chemical_identifier` | `CIDX` | Recommended | Yes (if left empty) | Unique compound index; BioXend auto-generates if not provided. `prefix` parameter in the workflow defines the prefix for the compounds, e.g: if `prefix` is `CIDX`, then the first compound would be: `CIDX001`. |
| `IUPAC_Name` | - | Recommended | Yes (if left empty) | Systematic IUPAC name; auto-filled by BioXend if not provided |
| `InChI` | - | Recommended | Yes (if left empty) | Standard InChI; auto-filled by BioXend if not provided |
| `InChIKey` | - | Recommended | Yes (if left empty) | InChIKey; auto-filled by BioXend if not provided |
| `CAS_number` | — | Recommended | No | CAS registry number of the xenobiotic |
| `Local_Synonym` | `COMPOUND_KEY` | Optional | Yes (if left empty, COMPOUND_NAME will be used) | Any local synonym used in the manuscript (e.g. "compound 23") |
| `database_ID` | - | Optional | No | ChEMBL, PubChem, or other database identifier; prefix with database name (e.g. `pubchem:441384`, `chebi:2361`) |
| `Stock_concentration` | — | Recommended | No | Concentration of the stock solution |
| `Stock_solvent` | — | Recommended | No | Solvent used to prepare the stock solution |
| `Purity` | — | Recommended | No | Purity of the compound (%) |
| `Solubility` | — | Recommended | No | Solubility value |
| `Vendor` | `COMPOUND_SOURCE` | Optional | No | Vendor who supplied the compound |
| `Molecular_formula` | - | Recommended | Yes (if left empty) | Molecular formula; auto-filled by BioXend if empty |
| `Molecular_weight` | - | Recommended | Yes (if left empty) | Molecular weight; auto-filled by BioXend if empty |
| `Monoisotopic_mass` | — | Recommended | Yes (if left empty) | Monoisotopic mass; auto-filled by BioXend if empty |
| `Physicochemical properties columns` | — | Optional | No | Physicochemical properties can include more than one column, you can add any relevant physicochemical properties column here, such as number of hydrogen bond acceptors/ donors etc. Addition of columns won't disrupt BioXend workflow. You can calculate different sets of these properties from chemet.embl.org |
| `m/z` | - | Optional/ Mandatory if mass spec used | No | Measured m/z of the xenobiotic |
| `Column_separation` | — | Optional/ Mandatory if mass spec used | No | Separation technique used (e.g. LC, GC) |
| `Retention_time` | - | Optional/ Mandatory if mass spec used | No | Retention time recorded; fill if `Column_separation` is provided |
| `Time_unit` | - | Optional/ Mandatory if mass spec used | No | Unit for retention time: `sec`, `min`, or `hr` |
| `Eluted_compound` | — | Optional/ Mandatory if original compound with salt formulation | No | Was the eluted compound the same as the original? Note if different (relevant for MS/biotransformation studies) |
| `Eluted_compound_SMILES` | — | Optional/ Mandatory if original compound with salt formulation | No | SMILES of the eluted compound if different from the original |

> **_NOTE 3 ON MASS SPECTROMETRY:_** If mass spectrometry was used to measure the endpoints, which is a major component of the stanadards, and hence will be mandatory in most cases, please fill out the relevant columns even if they are mentioned as optional columns.

 **_NOTE 4 ON SALT FORMULATIONS:_** Mass spec measures the biotransformation of the active compound, and not the whole formulation. In certain cases, the drugs are sold with salt formulations, e.g: `ABACAVIR SULFATE` with SMILES: `C1CC1NC2=C3C(=NC(=N2)N)N(C=N3)[C@@H]4C[C@@H](C=C4)CO.C1CC1NC2=C3C(=NC(=N2)N)N(C=N3)[C@@H]4C[C@@H](C=C4)CO.OS(=O)(=O)O`. The `.OS(=O)(=O)O` of the SMILES represents the sulfate part which is dissociated from the main compound `ABACAVIR` during LC-MS. So technically the activity of bacteria is reported only for the main compound, i.e. `ABACAVIR`, but to properly report this, ChEMBL asks for the whole SMILES for the compound administered, i.e. `ABACAVIR SULFATE` in their SDF file, and hence should be filled in SMILES column of the Chemicals sheet in the template. For such compounds, also fill out the column called: `Eluted_compound` with TRUE, and fill out the main component SMILES `C1CC1NC2=C3C(=NC(=N2)N)N(C=N3)[C@@H]4C[C@@H](C=C4)CO`. If such as a case doesnt apply, you can fill the `Eluted_compound` as FALSE.

### 3. Microbe or Assay metadata files / Micorbes sheet in template

**3.1. ASSAY.tsv:** 
`ASSAY.tsv` file gives description of the assay along with the microorganism, microbial community or microbial protein. For details please refer to the tutorial provided by ChEMBL on how to generate the [ASSAY.tsv file](https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/assay.tsv). 


**3.2. ASSAY_PARAM.tsv:**  
Assay parameters associated with `ASSAY.tsv` are mentioned within this optional file. For details please refer to the tutorial provided by ChEMBL on how to generate the [ASSAY_PARAM.tsv file](https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/supplementary-data-files/assay_param.tsv-adding-additional-assay-information.).

#### How are assay/microbe data files are integrated into the Micorbes and Experiment sheet in [Template_filled.ods](exampledata/Template_filled.ods)

The **Microbes** and **Experiment** sheets in [Template_filled.ods](exampledata/Template_filled.ods) map to `ASSAY.tsv` and `ASSAY_PARAM.tsv`. 

**Assay identity and sample metadata** (map to `ASSAY.tsv`):

| Template Column | Maps to | Required | Auto-filled by BioXend | Description |
|----------------|---------|----------|------------------------|-------------|
| `assay_identifier` | `AIDX` | **Mandatory** | No | to be filled by user; any unique identifier is fine. This identifier will be used to differentiate between different assays |
| `ASSAY_ORGANISM` | `ASSAY_ORGANISM` | Recommended | Yes (if left empty) | Bacteria scientific name if single bacteria was tested OR type of the community if community tested, in case if empty, `ASSAY_TAX_ID` will be used to fetch the name from NCBI |
| `ASSAY_TAX_ID` | `ASSAY_TAX_ID` | **Mandatory** | No| NCBI Taxonomy id, please fill |
| `ASSAY_STRAIN` | `ASSAY_STRAIN` | Recommended | Yes (if left empty)| Strain ID, if left empty, [StrainInfo](https://straininfo.dsmz.de) will be used to fill it. |
| `ENAorSRA_project_Accession_number` | — | Recommended | No | ENA or SRA project accession number for deposited sequencing data |
| `ENAorSRA_sample_Accession_number` | — | Recommended | No | ENA or SRA sample accession number |
| `Vendor` | — | Optional | No | Vendor or source from whom the strain/sample was obtained |
| `internal_sample_identifier` | — | Optional | No | Internal identifier used in the manuscript or lab for the sample/assay |
| `ASSAY_TYPE` | `ASSAY_TYPE` | **Mandatory** | No | ChEMBL assay type code; for MIX-MB use `B` (Biotransformation) and `F` = Functional for bacterial enzyme assays. Other codes: `A` = ADMET,  `T` = Toxicity, `U` = Unclassified, `P` = Physicochemical |
| `ASSAY_TISSUE` | `ASSAY_TISSUE` | Optional | No | type if tissue used in assay, if used at all |
| `ASSAY_CELL_TYPE` | `ASSAY_CELL_TYPE` | Optional | No | if applicable assay_cell_type is either a cell-line name (e.g. MRC-5) or endogenous cell type (e.g. fibroblasts).  |
| `ASSAY_SUBCELLULAR_FRACTION` | `ASSAY_SUBCELLULAR_FRACTION` | Optional | No | if applicable subcellular fraction used in the assay  |
| `ASSAY_SOURCE` | `ASSAY_SOURCE` | Recommended | No | Source of the assay, e.g: research group name or group leader name. This is an identifier, so no spaces or special characters should be included. |
| `ASSAY_GROUP` | `ASSAY_GROUP` | Optional | No | Group label for assays considered comparable by the depositor |
| `TARGET_TYPE` | `TARGET_TYPE` | Recommended | No | Type of target being assayed. Please use `ADMET` for all biotransformation assays where enzyme is not isolated and tested for biotransformation. In case if enzyme biotransformation is tested, please use `SINGLE PROTEIN`. Please refer to ChEMBL for all TARGET_TYPES. |
| `TARGET_ORGANISM` | `TARGET_ORGANISM` | Recommended | If left empty: Yes (from `Bacteria_scientific_name`) but if the target organism is different then dont leave empty and fill the scientific name of the organism | Auto-filled from scientific name if not provided |
| `Protein_name` | — | Optional | No | Name of the protein if a protein/enzyme assay |
| `UniProt_ID` | — | Optional | Yes (from protein name via UniProt API) | BioXend will look up from `Protein_name` if left empty |

| `TARGET_TAX_ID` | `TARGET_TAX_ID` | Recommended | Yes (from `NCBI_Tax_ID`) | Auto-filled from `NCBI_Tax_ID` if not provided |
| `Gene_name` | — | Optional | No | Gene name associated with the target protein |



**Experimental conditions** (maps to `ASSAY_PARAM.tsv`):

You can ass more columns and they will appear as assay parameters for all your files.

| Template Column | Required | Description |
|----------------|----------|-------------|
| `Oxygen_conditions` | Recommended | if these conditions apply to all your assays, write `all` or `most` if most of the assays have these conditions; add another row if some of the assays have different conditions, and mention your self defined assay_identifier here, wither single, or a list of idenfiers with those conditions as a comma separated list |
| `Oxygen_conditions` | Recommended | Oxygen conditions (e.g., anaerobic/aerobic/CO2)|
| `Media_composition` | Recommended | Growth medium used (e.g., GMM, mBHI, minimal media) |
| `Incubation_temperature_celsius` | Recommended | Incubation temperature in °C |
| `Shaking_speed` | Optional | Shaking speed (rpm) during incubation |
| `Negative_controls` | Recommended | Negative controls used (e.g., heat-killed or sterile media) |
| `Pre-culture_preparation_and_conditions` | Optional | Pre-culture conditions before the main assay |
| `Antibiotic_pre-treatment` | Optional | Whether antibiotics were used; include name(s) of antibiotic(s) |
| `Biomass_inoculum_density_at_start` | Recommended | Biomass or inoculum density at the start of incubation |
| `Incubation_duration` | **Mandatory** | Total incubation time (numeric value, e.g., `24`) |
| `Time_unit` | **Mandatory** | Unit for incubation duration: `hr` or `day`; use one consistently |
| `Time-course_information` | Optional | Number and timing of timepoints for time-course studies (e.g., 0, 3, 6, 12, 24 hr) |
| `Biomass_inoculum_density_at_end` | Optional | Biomass or inoculum density at end of incubation |
| `Sample_storage` | Recommended | How and where samples were stored |
| `Sample_preparation` | Recommended | Details of how the sample was prepared for analysis |
| `Instrument_and_measurement` | Recommended | Instrument used for measurement; mention technology and instrument name (e.g., LC-MS, Orbitrap) |

### 4. Biotransformation metadata file(s)

**4.1. ACTIVITY.tsv:**
All biotransformation events occurring between `COMPOUND` and `ASSAY`, are mentioned in the `ACTIVITY.tsv`, including `no biotransformation` events. For details please refer to the tutorial provided by ChEMBL on how to generate the [ACTIVITY.tsv file](https://chembl.gitbook.io/chembl-data-deposition-guide/file-structure/field-names-and-data-types-minimal-data-submission/activity.tsv).


**4.2. Other optional activity files -  not part of the MIX-MB template**
- `ACTIVITY_PROPERTIES.tsv` - Adding context to experimental results. <br>
- `ACTIVITY_SUPP.tsv` - Multiplex assays, supporting data, and complex results sets. <br>

#### How are biotransformation data files are integrated into the Template.xlsx

The **Biotransformation** sheet in `Template.xlsx` maps to `ACTIVITY.tsv`. Each row links one compound to one assay and records the outcome of the biotransformation event.

| Template Column | Maps to | Required | Auto-filled by BioXend | Description |
|----------------|---------|----------|------------------------|-------------|
| `Chemical_identifier` | `CIDX` | **Mandatory** | Yes (from Xenobiotics sheet) | Auto-filled from the Xenobiotics sheet; supply your own defined identifier if preferred |
| `Common_Name` | — | **Mandatory**  | Yes (from Xenobiotics sheet) | Common name of the compound; auto-filled by BioXend |
| `SMILES` | — | Optional | Yes (from Xenobiotics sheet) | SMILES of the compound; auto-filled by BioXend |
| `ASSAY_identifier` | `AIDX` | **Mandatory** | No | Must match the `assay_identifier` from the Microbes sheet exactly; used to link activities to assays |
| `TEXT_VALUE` | `TEXT_VALUE` | Conditional | No | Use for non-numerical activity values (e.g., "biotransformed", "not detected"); leave empty if filling `VALUE` |
| `VALUE` | `VALUE` | Conditional | No | Numerical value of the activity measurement (e.g., IC50, % biotransformation); leave empty if filling `TEXT_VALUE` |
| `RELATION` | `RELATION` | Optional | No | Relational symbol for the `VALUE` (e.g., `=`, `>`, `<`, `~`) |
| `UPPER_VALUE` | `UPPER_VALUE` | Optional | No | Upper limit if the activity measurement is a range; use `VALUE` for the lower limit in that case |
| `UNITS` | `UNITS` | Recommended | No | Unit of the activity value (e.g., `%`, `µM`, `nM`) |
| `ACTIVITY_COMMENT` | `ACTIVITY_COMMENT` | Recommended | Yes (partial, if left empty) | Free-text details: thresholds, p-values, which rows are actives; BioXend will auto-populate from `VALUE` or `TEXT_VALUE` if left empty |
| `Metabolite_mz` | — | Optional | No | Measured m/z of the xenobiotic metabolite |
| `Metabolite_retention_time` | — | Optional | No | Measured retention time of the xenobiotic metabolite |
| `Metabolite_annotation` | — | Optional | No | Top annotation as SMILES, compound name, or chemical class (ChemONT); leave empty if no annotation was performed |
| `Metabolite_annotation_level` | — | Optional | No | Annotation confidence level 1–5; refer to MIX-MB documentation for level definitions |
| `Kinetic_parameter_type` | — | Optional | No | Type of kinetic parameter measured (e.g., `Km`, `Vmax`, `kcat`); fill only if kinetic data are available |
| `Kinetic_parameter_value` | — | Optional | No | Numerical value associated with the kinetic parameter type |
| `Reaction_type` | — | Recommended | No | Type of biotransformation reaction (e.g., hydrolysis, hydroxylation, reduction); for biotransformation assays only |
| `Activity_type` | `ACTIVITY_TYPE` | Recommended | No | User-defined activity label (e.g., `biotransformation`, `inhibition`); populate only for confirmed active compounds |
| `ACTION_TYPE` | `ACTION_TYPE` | Optional | No | ChEMBL-controlled vocabulary for the effect on the target (e.g., `INHIBITOR`, `SUBSTRATE`); populate only for confirmed active compounds; must match the ChEMBL ACTION_TYPE list |
| `Classify_activity` | — | Optional | No | Binary or categorical activity label (e.g., `0` = no activity, `1` = active); populate only for confirmed outcomes |

> **Note on TEXT_VALUE vs VALUE:** Use `TEXT_VALUE` when the result is qualitative (e.g., "metabolised", "no biotransformation detected"). Use `VALUE` when you have a quantitative measurement. Do not fill both columns in the same row.

## Naming convention for identifiers and cross-referencing in ChEMBL

**This is the first practical step before entering any data: assign identifiers to every entity in your study.**

MIX-MB uses a three-layer identifier system based on ChEMBL submission guidelines. Every biotransformation event is a record that links all three layers:

| Identifier | Abbreviation | Entity | Defined in | One example |
|-----------|-------------|--------|-----------|-----------|
| Reference Index | **RIDX** | Study / publication | `REFERENCE.tsv` | HumanDrugMetabolism |
| Compound Index | **CIDX** | Chemical compound |`COMPOUND_RECORD.tsv` | HDM001 |
| Assay Index | **AIDX** | Organism × condition | `ASSAY.tsv` | Bacteriodetes_theta_microaerobic |

All three identifiers must appear together in every row of `ACTIVITY.tsv` to create an unambiguous, linkable record of a biotransformation event.

### RIDX Minting Rules

- Format: `[FirstAuthorLastName]_[DescriptiveLabel]`, e.g. `Zimmermann_GutBiotransformationAtlas`
- Must be unique across all submissions; use only ASCII letters, digits, underscores, and hyphens — no spaces
- Set the RIDX once at the start of data preparation; do not change it after any file references it

### CIDX Minting Rules

- Format: user-defined prefix + zero-padded integer, e.g. `HMDM001`, `HMDM002`
- The `--prefix` pipeline parameter defines the prefix (e.g. `--prefix HMDM`)
- Assign one CIDX per distinct chemical structure (identical canonical SMILES = same CIDX)
- BioXend auto-generates CIDXs if `Chemical_identifier` is left blank in the template

### AIDX Minting Rules

- Format: `[FirstAuthorLastName]_[Genus]_[species]_[ConditionOrNote]_biotransformation`, e.g. `Zimmermann_Actinomyces_graevenitzii_anaerobic_biotransformation`
- Each distinct organism × condition combination gets its own AIDX
- Use only ASCII letters, digits, underscores, and hyphens — no spaces
- For protein/enzyme assays, append the UniProt ID or gene name
- BioXend auto-builds AIDXs from the organism name and conditions if `assay_identifier` follows a consistent pattern

| Situation | AIDX format | `ASSAY_ORGANISM` | `ASSAY_TAX_ID` |
|-----------|------------|------------------|----------------|
| Known species, known strain | `[Author]_[Genus]_[species]_[Strain]` | Full binomial name | Registered species TaxID |
| Known species, undesignated strain | `[Author]_[Genus]_[species]_unknown_strain` | Full binomial name | Species-level TaxID |
| Novel isolate (unclassified) | `[Author]_unclassified_[IsolateID]` | `unclassified bacteria` | `2` (root Bacteria) or closest TaxID |
| Mixed / community assay | `[Author]_mixed_community_[SourceDescription]` | `mixed microbial community` | `1` (root) or metagenome TaxID |

### Minting Scheme for Unknown Compounds and Biotransformation Events

Not all entities will have established external identifiers at the time of submission. Use study-local identifiers with the following prefixes:

| Situation | CIDX / prefix | `ACTION_TYPE` | Notes |
|-----------|--------------|---------------|-------|
| Known compound (MSI Level 1–2) | `CIDX[nnnn]` as usual | `SUBSTRATE` or `PRODUCT` | InChIKey required |
| Putatively characterised product (MSI Level 3) | `PUTATIVE_[RIDX]_[n]` | `PRODUCT` | Add structural class and MSI level in `ACTIVITY_COMMENT` |
| Unknown product (MSI Level 4–5) | `UNKNOWN_[RIDX]_[n]` | `PRODUCT` | Add m/z, adduct type, and MSI level in `ACTIVITY_COMMENT` |
| No biotransformation detected | Substrate CIDX | `No Activity` | Set `TEXT_VALUE` to `"Compound NOT metabolized"` |
| Novel microbial isolate (no TaxID) | — | — | Report at nearest known rank; note absence of strain-level TaxID in `ACTIVITY_COMMENT` |

Once an unknown entity is formally identified and registered in an external database, update its identifier across all affected files before resubmission.

---

## Chemical Identity Guidelines

### External Identifier Priority

When a compound exists in an external database, use the following priority order for the `database_ID` field:

| Priority | Identifier | Example |
|----------|-----------|---------|
| 1 | **InChIKey** | `HEFNNWSXXWATRW-UHFFFAOYSA-N` |
| 2 | **ChEMBL ID** | `chembl:CHEMBL1201246` |
| 3 | **PubChem CID** | `pubchem:4583` |
| 4 | **ChEBI ID** | `chebi:3686` |
| 5 | **CAS Number** | `cas:42399-41-7` |

The InChIKey is the canonical structure identifier and is **strongly recommended** for all known compounds — it identifies structure independently of naming conventions or database numbering. BioXend auto-generates InChI, InChIKey, and molecular formula from the SMILES if left empty.

### Salt and Prodrug Handling

Many drugs are supplied or measured as salts or prodrugs where the submitted structure and the analytically detected form differ (e.g., sodium ibuprofen supplied but the free acid detected by MS).

- **`SMILES`** — enter the structure you have (including counter-ion / salt form if known)
- **`Eluted_compound`** — set to `yes` if the MS detects a different form than the submitted structure
- **`Eluted_compound_SMILES`** — enter the SMILES of the form actually detected by the instrument

BioXend generates InChI/InChIKey from the `SMILES` field. The `Eluted_compound_SMILES` is recorded as supplementary context and is not used for structure generation.

### MSI Annotation Levels for Biotransformation Products

Use these confidence levels in `Metabolite_annotation_level` for any detected biotransformation product:

| Level | Description | Minimum Evidence Required |
|-------|-------------|--------------------------|
| **1** | Identified | Authentic reference standard with matching retention time (± 0.05 min) and MS² spectrum (similarity > 0.95) |
| **2** | Putatively annotated | Database or spectral library MS² match (similarity ≥ 0.7); no authentic standard required |
| **3** | Putatively characterised | Chemical class identified from accurate mass and fragmentation; partial structure known |
| **4** | Unknown | Exact mass measured; no formula or structural information available |
| **5** | Unidentified | Spectral data only; no structural hypothesis possible |

For Levels 4–5, use the `UNKNOWN_[RIDX]_[n]` CIDX prefix and record the m/z and adduct type in `ACTIVITY_COMMENT`.

---

## Assay Types

Specify the biological system in `ASSAY_TYPE` and describe it in `ASSAY_DESCRIPTION`. Use one of the following types in `ASSAY_TYPE` column (ChEMBL code `B` for all biotransformation assays):

| Assay system | Description | `ASSAY_TYPE` |
|-------------|-------------|-------------|
| Whole cell (pure culture) | Intact living bacterial cells; single strain | `B` |
| Cell lysate | Disrupted cells; crude enzyme mixture | `B` |
| Purified enzyme | Isolated single enzyme or protein | `B` |
| Community / mixed culture | Mixed microbial population (e.g., gut microbiota) | `B` |
| In vivo (animal/human) | Metabolic data from whole organisms | `B` |

> The `ASSAY_TYPE` code is always `B` (Biotransformation) for MIX-MB submissions. The distinction between assay systems is captured in `ASSAY_DESCRIPTION` and `TARGET_TYPE`.

---

## Controlled Vocabularies

Use these terms **exactly as written** in the respective template columns.

### Reaction Types (`Reaction_type` column)

| Term | Description | GO ID | EC class |
|------|-------------|-------|----------|
| `hydroxylation` | Addition of –OH group | GO:0018126 | EC 1.14.x.x |
| `oxidation` | Removal of H or addition of O | GO:0055114 | EC 1.x.x.x |
| `reduction` | Addition of H or removal of O | GO:0055114 | EC 1.x.x.x |
| `hydrolysis` | Cleavage by water | GO:0016787 | EC 3.x.x.x |
| `decarboxylation` | Loss of CO₂ | GO:0017001 | EC 4.1.1.x |
| `deamination` | Loss of amino group (–NH₂) | GO:0018133 | EC 3.5.x.x |
| `demethylation` | Loss of methyl group (–CH₃) | GO:0032259 | EC 1.14.x.x |
| `dehalogenation` | Loss of halogen | — | EC 3.8.x.x |
| `N-reduction` | Reduction of nitrogen-containing groups | — | EC 1.7.x.x |
| `azo_reduction` | Cleavage of N=N bonds | — | EC 1.7.1.17 |
| `conjugation` | Addition of a larger molecular group | GO:0016757 | EC 2.x.x.x |
| `acetylation` | Addition of acetyl group | GO:0016408 | EC 2.3.1.x |
| `glucuronidation` | Addition of glucuronic acid | GO:0008194 | EC 2.4.1.17 |
| `sulfation` | Addition of sulfate group | GO:0008146 | EC 2.8.2.x |

### Activity Result (`TEXT_VALUE` column)

Use `TEXT_VALUE` for qualitative results. Do **not** fill both `TEXT_VALUE` and `VALUE` in the same row.

| TEXT_VALUE | Meaning |
|------------|---------|
| `Compound metabolized` | Parent compound consumed or depleted |
| `Compound NOT metabolized` | No measurable transformation detected |
| `Product detected` | Biotransformation product observed |
| `Partial transformation` | Incomplete conversion (< 95%) |
| `Complete transformation` | Full conversion (≥ 95%) |

### Effect Classification (`ACTION_TYPE` column)

Leave empty if no confirmed activity — do not guess.

| ACTION_TYPE | Use when |
|-------------|----------|
| `SUBSTRATE` | Compound is consumed as a substrate |
| `PRODUCT` | Compound is a detected biotransformation product |
| `No Activity` | No transformation detected |
| `INHIBITOR` | Compound inhibits a microbial enzyme or process |
| `STIMULATION` | Compound stimulates a microbial process |

### Oxygen Conditions (`Oxygen_conditions` column)

| Term | Meaning |
|------|---------|
| `obligate aerobe` | Requires oxygen |
| `facultative anaerobe` | Grows with or without oxygen |
| `obligate anaerobe` | Cannot tolerate oxygen |
| `microaerophile` | Requires low oxygen (2–10%) |
| `aerotolerant anaerobe` | Tolerates oxygen but does not use it |

### Sample Types (`sample_type` — for `ASSAY_DESCRIPTION` context)

`pure culture` | `enrichment culture` | `mixed culture` | `community` | `cell-free lysate` | `membrane fraction` | `cytoplasmic fraction`

### Growth Phases (for `ASSAY_DESCRIPTION` or `Pre-culture_preparation_and_conditions`)

`lag phase` | `exponential phase` | `stationary phase` | `early exponential` | `mid exponential` | `late stationary`

---

## Data Quality Tiers

MIX-MB defines three compliance tiers. Higher tiers enable broader reuse and ChEMBL deposition.

### Tier 1 — Gold (Publication-Ready)

All mandatory **and** recommended fields complete across all sheets.

- Valid SMILES + InChIKey verified for all compounds
- At least one external database ID (ChEMBL, PubChem, or ChEBI)
- NCBI TaxID present and verified for all organisms
- Strain designation (culture collection number) provided
- Quantitative activity data with biological replicates (n ≥ 3)
- Detected products annotated at MSI Level 1 or 2
- Negative controls and internal standard documented

### Tier 2 — Silver (Research-Grade)

All mandatory fields complete; partial recommended fields.

- Valid SMILES + InChIKey for all compounds
- NCBI TaxID present for all organisms
- Quantitative or semi-quantitative activity (n ≥ 2 biological replicates)
- Detected products at MSI Level 2 or 3 acceptable
- Basic growth conditions documented (medium and temperature at minimum)

### Tier 3 — Bronze (Preliminary / Screening)

Mandatory fields only. Suitable for large-scale screens.

- Valid SMILES and compound name present
- CIDX and RIDX assigned
- NCBI TaxID present
- Qualitative activity only (`TEXT_VALUE` filled; `VALUE` optional)
- Single measurement acceptable; no replication required

---

## ChEMBL links and FAQs
Here are some details on different files required by ChEMBL.
### Links: 
* Information on ChEMBL: https://chembl.gitbook.io/chembl-interface-documentation 
* ChEMBL submission guidelines: https://chembl.gitbook.io/chembl-data-deposition-guide 
### FAQs: 
1. General Questions: https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/general-questions
2. Compounds: https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/drug-and-compound-questions
3. Assay and activities: https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/chembl-data-questions
4. Targets: https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/target-questions