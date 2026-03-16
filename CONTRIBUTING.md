# Contributing to BioXend / MIX-MB

Thank you for your interest in contributing to the Minimum Information about Xenobiotics-Microbiome Biotransformation (MIX-MB) standards! This is a community-driven project, and we welcome contributions from researchers, bioinformaticians, data curators, and anyone working in xenobiotic microbial biotransformation. 

**First time here?** 
- Here is the link to the current project board: [BioXend Project Board](https://github.com/users/zmahnoor14/projects/6) to get oriented.
- Look for issues labeled [`good-first-issue`](https://github.com/zmahnoor14/BioXend/issues?q=label%3Agood-first-issue)
- Browse the [Discussions board](https://github.com/zmahnoor14/BioXend/discussions) 

## How to Contribute

There are several ways to participate, depending on your comfort level with(/out) GitHub:

### 1. No GitHub account - Contribute Without GitHub

You don't need a GitHub account to help shape MIX-MB. The current Non-github contributions are integrated via the [MIX-MB Survey](https://forms.gle/towuMVYYuqDi7pEJ7). Feedback collected through the survey will be triaged by a maintainer and converted into GitHub Issues so it enters the formal review process. Current results from the survey can be viewed with the notebook: [Standards/MIX-MB_Survey_Analysis.ipynb](Standards
/MIX-MB_Survey_Analysis.ipynb).

### 2. With GitHub account

#### 2.1. Suggest Changes via Issues (No Git Knowledge Needed)

If you have feedback on the standards documentation and template, but aren't familiar with Git:

- Go to the [Issues tab](https://github.com/zmahnoor14/BioXend/issues)
- Click **"New Issue"** and choose the appropriate template:
  - **Standards Feedback** — for proposing changes to the MIX-MB minimum information checklists
  - **Template Modification** — for suggesting changes to data submission template columns, descriptions, or controlled vocabularies
  - **Bug Report** — for reporting errors in the pipeline or documentation
  - **Feature Request** — for requesting new functionality or data fields
  - **Blank issue** - if it's a general issue you would like to report
- Fill out the template and submit. A maintainer will review, and the community can discuss and endorse.

#### 2.2. Submit a Pull Request (For Git Users)

For direct contributions to the standards documents, templates, or nf workflow, all external contributors must work from a **fork**. Only maintainers added to the project can push branches directly to this repository.

##### Step-by-step for external contributors

1. **Fork** the repository by clicking the **Fork** button on the [BioXend GitHub page](https://github.com/zmahnoor14/BioXend). This creates a copy of the repo under your own GitHub account.

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/BioXend.git
   cd BioXend
   ```

3. **Add the upstream remote** so you can stay up to date:
   ```bash
   git remote add upstream https://github.com/zmahnoor14/BioXend.git
   ```

4. **Sync with the latest `devel` branch** before starting any work:
   ```bash
   git fetch upstream
   git checkout devel
   git merge upstream/devel
   ```

5. **Create a new branch** from `devel` (never work directly on `devel` or `main`):
   ```bash
   git checkout -b your-branch-name
   ```

6. **Make your changes**. Please follow the [versioning and file conventions](#branching-and-versioning) described below.

7. **Commit** with a clear message following the convention:
   ```
   [component] Brief description

   Examples:
   [standards] Add recommendation for pH reporting in Experiment table
   [template] Add new column for enzyme commission number in Biotransformation
   [workflow] Fix SMILES validation step
   ```

8. **Push to your fork**:
   ```bash
   git push origin your-branch-name
   ```

9. **Open a Pull Request** from your fork's branch to `zmahnoor14/BioXend:devel`. GitHub will usually suggest the upstream repo as the target automatically — confirm the base repository is `zmahnoor14/BioXend` and the base branch is `devel`, not `main`.

10. **Reference the originating issue (if you were working on an issue)** in your PR description using `Closes #XX` or `Relates to #XX`. For best practices, generally there should be an open issue to which this PR is related to. If the issue doesnt exist, you can enter the issue and then after adding your contribution, mnetion that issue. This way changes are tracked properly.

11. **Apply a version-bump label** to your PR (see [Branching and Versioning](#branching-and-versioning) below): `bump:patch`, `bump:minor`, or `bump:major`.

12. Your PR will be reviewed by at least one maintainer. Community endorsement (thumbs-up reactions or comments) is encouraged.

#### 2.3. Endorse or Comment on Existing Proposals

Browse [open issues](https://github.com/zmahnoor14/BioXend/issues) and [pull requests](https://github.com/zmahnoor14/BioXend/pulls). You can:

- Add a 👍 reaction to endorse a proposal
- Leave a comment with your perspective or additional evidence
- Reference relevant literature or datasets

Community consensus matters — proposals with broader endorsement will be prioritized.


#### 2.4. Discuss and Propose via GitHub Discussions

[GitHub Discussions](https://github.com/zmahnoor14/BioXend/discussions) is a first-class contribution channel for open-ended conversation that doesn't yet belong in an issue:

- **Standards Proposals** — Float ideas for new fields or classification changes before writing a formal issue
- **Template Questions** — Ask about column meanings, controlled vocabularies, or submission format
- **General** — Introduce yourself, share related work, or ask where to start

Discussions that reach consensus can be converted into issues and enter the review process.

#### 2.5. Review and Endorsement Process

1. A proposal is submitted as an Issue or Pull Request.
2. The community discusses and can endorse with 👍 reactions independently.
3. After a **minimum review period of 14 days**, the maintainer evaluates community feedback.
4. If endorsed by at least **1-2 independent contributors** (besides the proposer), the change proceeds.
5. The maintainer incorporates the change, updates the relevant version, and merges to `devel`.
6. Periodically, `devel` is merged to `main` as a new release.

For urgent fixes i.e `bump:patch` versioning updates (typos, broken links, clear errors), no review period is necessary.

## Branching and Versioning

This project uses a structured versioning system. Please see `VERSION.md` at the root of the repository for full details. In brief:

- **`main`** branch contains only stable, endorsed releases
- **`devel`** branch is the active working branch for all contributions
- Each document (standards docs, template) and the workflow carry independent version numbers
- The overall framework version increments when any component has a new release

When making changes, **do not manually update version numbers** — this is handled automatically by GitHub Actions when changes are merged to `main`.

**Pull Request authors are responsible for applying a version-bump label** to their pull request so the automation knows what kind of change is being made:

| Label | When to use |
|-------|-------------|
| `bump:patch` | Typo fixes, clarifications, broken links — no change to data requirements |
| `bump:minor` | New optional/recommended fields, backward-compatible additions |
| `bump:major` | Breaking changes: new mandatory fields, removed fields, renamed columns |

### How to add the version-bump labels:

1. Open your Pull Request on GitHub.
2. In the right-hand sidebar, click **Labels**.
3. Search for and select the appropriate label: `bump:patch`, `bump:minor`, or `bump:major`.

## What Makes a Good Standards Proposal?

When proposing changes to the MIX-MB minimum information checklists, please include the following, (sections are already present in the issue templates):

- **Rationale**: Why is this field/change necessary? Reference survey data or literature if possible.
- **Classification**: Should the field be Mandatory, Recommended, or Optional?
- **Affected table(s)**: Which template sheet(s) would be impacted (Reference, Chemicals, Microbes, Experiment, Biotransformation)?
- **Controlled vocabulary**: If the field requires controlled terms, propose them or reference an existing ontology.
- **Backward compatibility**: Will this change break existing submitted data?

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

## Citing This Work

Releases of BioXend / MIX-MB will be soon archived on [Zenodo](https://zenodo.org) and will be assigned a DOI, making the standards citable in academic publications. 

## Questions?

If you're unsure where to start or how to contribute, open a [Discussion](https://github.com/zmahnoor14/BioXend/discussions) or reach out to the main maintainer at **mahnoor.zulfiqar@embl.de**. We're happy to help!


