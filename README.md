![GitHub tag](https://img.shields.io/github/v/tag/zmahnoor14/BioXend?style=flat&label=version)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Issues](https://img.shields.io/github/issues/zmahnoor14/BioXend)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

# BioXend 
BioXend is a new computational framework for submitting Microbial Biotransformation of Xenobiotics data. 
- WP1: is to develop minimum reporting standards based on community consensus
- WP2: is to automate the metadata collection
- WP3: is to develop a submission workflow to [ChEMBL](https://www.ebi.ac.uk/chembl/)
- WP4: is to release this framework as part of NFDI4Micropbiota workflow
<br>

<p align="center">
  <img src="WP_BioXend.png" />
</p>

<br>
We welcome community participation especially for developing the minimum standards called Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB).

## MIX-MB Standards

**Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB)**

BioXend framework defines community-driven minimum reporting standards for xenobiotic microbial biotransformation data, enabling consistent data deposition to databases such as ChEMBL. <br>
We would like to invite you to participate in this community driven project. The standards are informed by 

- already existing standards, 
- ChEMBL submission guidelines, and 
- an [open survey](https://forms.gle/towuMVYYuqDi7pEJ7). 

Please view the current results from the survey in [Standards/MIX-MB_Survey_Analysis.ipynb](Standards/MIX-MB_Survey_Analysis.ipynb) notebook.

### Repository Structure for files important for contributors

```
BioXend/
├── .github/                          # GitHub Actions workflows, PR and issue templates
├── Standards/                        # MIX-MB standards documents and templates
│   ├── Templates/                    # Submission templates (Excel, CSV, JSON-LD)
│   ├── MIX-MB_Survey_Analysis.ipynb  # Community survey results and analysis
│   ├── MIXMB_Biotransformation.md    # MIX-MB(B): Biotransformation process standards
│   ├── MIXMB_Microbes.md             # MIX-MB(M): Microorganism standards
│   ├── MIXMB_Standards_main.md       # Top-level MIX-MB standards overview
│   ├── MIXMB_Xenobiotics.md          # MIX-MB(X): Chemical substrate standards
│   └── Versioning.md                 # Versioning policy for standards
├── bin/                              # Executable scripts and generated ChEMBL output files
├── modules/                          # Nextflow DSL2 process modules
├── notebooks/                        # Development notebooks (Jupyter + R)
├── versions/                         # Independent version tracking per component
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── README.md
└── VERSION.md
```

### How to participate:

All participants are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

### For contributors

We welcome contributions to the standards, template, and nf workflow for submission! See our [Contributing Guide](CONTRIBUTING.md) for details. You can:

- **Propose changes** by opening an [issue](https://github.com/zmahnoor14/BioXend/issues/new/choose)
- **Submit a pull request** targeting the `devel` branch
- **Endorse proposals** by adding 👍 to issues and PRs you support
- **Discuss ideas** in [GitHub Discussions](https://github.com/zmahnoor14/BioXend/discussions)

Also link to the current project board: [BioXend Project Board](https://github.com/users/zmahnoor14/projects/6)

### For future data submitters

1. Download the latest [`Template.xlsx`](Template.xlsx)
2. Read the `Template_Description` sheet for instructions
3. Fill in your data — green columns are mandatory, blue are recommended, purple are optional
4. Submit feedback on ease of use -- This template will be used as input to generate ready to submit ChEMBL files

## Versioning

Each standard document, the template, and the nf workflow are versioned independently. The framework version increments with any component release. See [VERSION.md](VERSION.md) for details.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- **Maintainers**: Mahnoor Zulfiqar — [ORCID](https://orcid.org/0000-0002-8330-4071), Eleonora Mastrorilli - [ORCID](https://orcid.org/0000-0003-2127-4150)
- **Institution**: EMBL, Molecular Systems Biology (MSB) Unit

## Funding
- [NFDI4Microbiota FlexFund 2026](https://nfdi4microbiota.de/newsroom/flexfunds/)
