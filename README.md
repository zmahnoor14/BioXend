# BioXend — MIX-MB Standards

**Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB)**

<!-- Uncomment these badges once the repo is set up -->
<!-- ![GitHub release](https://img.shields.io/github/v/release/zmahnoor14/BioXend) -->
<!-- ![License](https://img.shields.io/github/license/zmahnoor14/BioXend) -->
<!-- ![Issues](https://img.shields.io/github/issues/zmahnoor14/BioXend) -->
<!-- ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg) -->

BioXend defines community-driven minimum reporting standards for xenobiotic microbial biotransformation data, enabling consistent data deposition to databases such as ChEMBL.

## Overview

The MIX-MB framework specifies what metadata should accompany biotransformation data across five categories:

| Table | Covers |
|-------|--------|
| **Reference** | Publication, DOI, authors, data license |
| **Chemicals** | Xenobiotic identity (SMILES, InChI), vendor, analytical measurements |
| **Microbes** | Organism identity, strain, sequencing accessions, protein targets |
| **Experiment** | Culture conditions, controls, incubation, sample preparation |
| **Biotransformation** | Activity values, metabolite identification, reaction type |

Each field is classified as **Mandatory**, **Recommended**, or **Optional** based on community consensus and survey feedback from 23 respondents.

## Repository Structure

```
BioXend/
├── Standards/              # MIX-MB standards documents (one per table)
├── Standards/Templates/Template.xlsx           # Data submission template
├── versions/               # Component version tracking
├── pipeline/               # Data processing pipeline (future)
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── VERSION.md
└── README.md
```

## Getting Started

## Community Standards

This project will be built on community consensus. The standards are informed by already existing standards, ChEMBL submission guidelines, an [open survey](https://forms.gle/towuMVYYuqDi7pEJ7) and ongoing feedback from researchers in xenobiotic microbial biotransformation (via collaboration and this GitHub repository).

All participants are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).


### For contributors

We welcome contributions to the standards, template, and pipeline! See our [Contributing Guide](CONTRIBUTING.md) for details. You can:

- **Propose changes** by opening an [issue](https://github.com/zmahnoor14/BioXend/issues/new/choose)
- **Submit a pull request** targeting the `devel` branch
- **Endorse proposals** by adding 👍 to issues and PRs you support
- **Discuss ideas** in [GitHub Discussions](https://github.com/zmahnoor14/BioXend/discussions)

### For future data submitters

1. Download the latest [`Template.xlsx`](Template.xlsx)
2. Read the `Template_Description` sheet for instructions
3. Fill in your data — green columns are mandatory, blue are recommended, purple are optional
4. Submit feedback on ease of use -- This template will be used as input to generate ready to submit ChEMBL files


## Versioning

Each standard document, the template, and the pipeline are versioned independently. The framework version increments with any component release. See [VERSION.md](VERSION.md) for details.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- **Maintainer**: Mahnoor Zulfiqar — [ORCID](https://orcid.org/0000-0002-8330-4071), Eleonora Mastrorilli - [ORCID](https://orcid.org/0000-0003-2127-4150)
- **Institution**: EMBL, Molecular Systems Biology (MSB) Unit

## Funding
- [NFDI4Microbiota FlexFund 2026](https://nfdi4microbiota.de/newsroom/flexfunds/)
