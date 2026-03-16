# Contributing to BioXend / MIX-MB

Thank you for your interest in contributing to the Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB) standards! This is a community-driven project, and we welcome contributions from researchers, bioinformaticians, data curators, and anyone working in xenobiotic microbial biotransformation. here is the link to the current project board: Also link to the currnt project board: https://github.com/users/zmahnoor14/projects/6.

**First time here?** Look for issues labeled [`good-first-issue`](https://github.com/zmahnoor14/BioXend/issues/2) or browse the [Discussions board](https://github.com/zmahnoor14/BioXend/discussions) to get oriented before diving in.

## How to Contribute

There are several ways to participate, depending on your comfort level with GitHub:

### 1. Suggest Changes via Issues (No Git Knowledge Needed)

If you have feedback on the standards documentation and template, but aren't familiar with Git:

- Go to the [Issues tab](https://github.com/zmahnoor14/BioXend/issues)
- Click **"New Issue"** and choose the appropriate template:
  - **Standards Feedback** — for proposing changes to the MIX-MB minimum information checklists
  - **Template Modification** — for suggesting changes to data submission template columns, descriptions, or controlled vocabularies
  - **Bug Report** — for reporting errors in the pipeline or documentation
  - **Feature Request** — for requesting new functionality or data fields
- Fill out the template and submit. A maintainer will review, and the community can discuss and endorse.

### 2. Submit a Pull Request (For Git Users)

For direct contributions to the standards documents, templates, or code:

1. **Fork** the repository
2. **Create a branch** from `devel` (not `main`):
   ```bash
   git checkout devel
   git checkout -b your-branch-name
   ```
3. **Make your changes**. Please follow the versioning and file conventions described below.
4. **Commit** with a clear message following the convention:
   ```
   [component] Brief description

   Examples:
   [standards] Add recommendation for pH reporting in Experiment table
   [template] Add new column for enzyme commission number in Biotransformation
   [pipeline] Fix SMILES validation step
   ```
5. **Push** and open a Pull Request targeting the `devel` branch.
6. **Reference the originating issue** in your pull request(PR) description using `Closes #XX` or `Relates to #XX`. Every change should trace back to a tracked issue.
7. **Apply a version-bump label** to your PR (see [Branching and Versioning](#branching-and-versioning) below): `bump:patch`, `bump:minor`, or `bump:major`.
8. Your PR will be reviewed by at least one maintainer. Community endorsement (thumbs-up reactions or comments) is encouraged.

### 3. Endorse or Comment on Existing Proposals

Browse [open issues](https://github.com/zmahnoor14/BioXend/issues) and [pull requests](https://github.com/zmahnoor14/BioXend/pulls). You can:

- Add a 👍 reaction to endorse a proposal
- Leave a comment with your perspective or additional evidence
- Reference relevant literature or datasets

Community consensus matters — proposals with broader endorsement will be prioritized.

### 4. Contribute Without GitHub

You don't need a GitHub account to help shape MIX-MB. Non-code contributions are just as valuable:

- **Google Form** *(coming soon)* — Submit structured feedback on field classifications and controlled vocabularies without any account required. Link will be posted in the README once available.
- **Google Docs open consultation** — Comment-enabled drafts of proposed standards revisions will be shared periodically for community input. Watch the [Announcements discussion category](https://github.com/zmahnoor14/BioXend/discussions/categories/announcements) for links.

Feedback collected through these channels will be triaged by a maintainer and converted into GitHub Issues so it enters the formal review process.

### 5. Discuss and Propose via GitHub Discussions

[GitHub Discussions](https://github.com/zmahnoor14/BioXend/discussions) is a first-class contribution channel for open-ended conversation that doesn't yet belong in an issue:

- **Standards Proposals** — Float ideas for new fields or classification changes before writing a formal issue
- **Template Questions** — Ask about column meanings, controlled vocabularies, or submission format
- **General** — Introduce yourself, share related work, or ask where to start

Discussions that reach consensus can be converted into issues and enter the review process.

## Branching and Versioning

This project uses a structured versioning system. Please see `VERSION.md` at the root of the repository for full details. In brief:

- **`main`** branch contains only stable, endorsed releases
- **`devel`** branch is the active working branch for all contributions
- Each document (standards docs, template) and the pipeline carry independent version numbers
- The overall framework version increments when any component has a new release

When making changes, **do not manually update version numbers** — this is handled automatically by GitHub Actions when changes are merged to `main`.

**Pull Request authors are responsible for applying a version-bump label** to their pull request so the automation knows what kind of change is being made:

| Label | When to use |
|-------|-------------|
| `bump:patch` | Typo fixes, clarifications, broken links — no change to data requirements |
| `bump:minor` | New optional/recommended fields, backward-compatible additions |
| `bump:major` | Breaking changes: new mandatory fields, removed fields, renamed columns |

## What Makes a Good Standards Proposal?

When proposing changes to the MIX-MB minimum information checklists, please include:

- **Rationale**: Why is this field/change necessary? Reference survey data or literature if possible.
- **Classification**: Should the field be Mandatory, Recommended, or Optional?
- **Affected table(s)**: Which template sheet(s) would be impacted (Reference, Chemicals, Microbes, Experiment, Biotransformation)?
- **Controlled vocabulary**: If the field requires controlled terms, propose them or reference an existing ontology.
- **Backward compatibility**: Will this change break existing submitted data?

## Review and Endorsement Process

1. A proposal is submitted as an Issue or Pull Request.
2. The community discusses and can endorse with 👍 reactions.
3. After a **minimum review period of 14 days**, the maintainer evaluates community feedback.
4. If endorsed by at least **1-2 independent contributors** (besides the proposer), the change proceeds.
5. The maintainer incorporates the change, updates the relevant version, and merges to `devel`.
6. Periodically, `devel` is merged to `main` as a new release.

For urgent fixes (typos, broken links, clear errors), the review period may be shortened.

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

## Citing This Work

Releases of BioXend / MIX-MB are archived on [Zenodo](https://zenodo.org) and assigned a DOI, making the standards citable in academic publications. The citation for the current release can be found in the `CITATION.cff` file or on the repository's sidebar under **"Cite this repository"**. If you publish work that builds on or uses MIX-MB, please cite the relevant versioned release.

## Questions?

If you're unsure where to start or how to contribute, open a [Discussion](https://github.com/zmahnoor14/BioXend/discussions) or reach out to the maintainer at **mahnoor.zulfiqar@embl.de**. We're happy to help!
