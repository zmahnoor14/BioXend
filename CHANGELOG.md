# Changelog
Versions follow semantic versioning: `MAJOR.MINOR.PATCH`.

> **Note:** The framework version (`versions/framework.txt`) and workflow version (`versions/workflow.txt`) are tracked independently. This changelog covers the **workflow/pipeline** (`versions/workflow.txt`).

---

## [Unreleased]

---

## [0.1.1] - 2026-03-16

### Fixed
- Corrected release date metadata in standards components

---

## [0.1.0] - 2026-03-15

### Added
- Initial Nextflow DSL2 pipeline with five modules: `reference`, `chemicals`, `microbes`, `experiment`, `biotransformation`
- Seven ChEMBL-ready deposition outputs: `REFERENCE.tsv`, `README.toml`,`COMPOUND_RECORD.tsv`, `COMPOUND_CTAB.sdf`, `ASSAY.tsv`, `ASSAY_PARAM.tsv`, `ACTIVITY.tsv`
- Python scripts in `bin/` for all pipeline steps (replacing legacy R scripts)
- Docker image `bioxend:latest` based on `python:3.10-slim` with RDKit, pandas, requests, odfpy, tomli-w
- `nextflow.config` with docker and singularity profiles
- `conf/base.config` for resource labels and retry 
- `conf/modules.config` for publishDir and ext.args per process
- `nextflow_schema.json` for parameter documentation
- nf-core style module structure with `main.nf`, and `meta.yml` per module
- Dynamic versioning: version read from `versions/workflow.txt`
- MIX-MB submission template at `Standards/Templates/Template_open.ods`
- Docs: `docs/usage.md` and `docs/output.md`

---

## How to update CHANGELOG.md:

When opening a PR to `main`, use these section labels:

- **Added** — new features or files
- **Changed** — changes to existing functionality
- **Fixed** — bug fixes
- **Removed** — removed features or files
- **Deprecated** — features to be removed in future versions


