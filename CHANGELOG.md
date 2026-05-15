# Changelog
Versions follow semantic versioning: `MAJOR.MINOR.PATCH`.

> **Note:** The framework version (`versions/framework.txt`) and workflow version (`versions/workflow.txt`) are tracked independently. This changelog covers the **workflow/pipeline** (`versions/workflow.txt`).

---

## [Unreleased]

### Added
- Example input data files
- `envs/bioxend.yml`: conda environment file for `-profile conda` local runs; installs rdkit from conda-forge (preferred over pip for C++ dependency handling), plus pandas, odfpy, requests, and tomli-w
- `.github/workflows/docker-publish.yml`: CI workflow that builds and pushes `zmahnoor/bioxend:latest` to Docker Hub automatically on every merge to `main` that touches `Dockerfile` or `bin/`; requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets in the repository settings

### Fixed
- `nextflow_schema.json`: corrected `$schema` from `draft-07/hyper-schema` to `draft-07/schema`; the hyper-schema dialect was not recognised by the AJV validator used by CloWM, causing a `TypeError: b is not a function` crash on Launch; added test file config.
- `nextflow_schema.json`: removed `prefix` and `xenobiotic_class` from the `required` array; both parameters have defaults and should not be marked mandatory, which prevented their default values from pre-filling in the CloWM parameter form
- `bin/biotransformation.py`: added `CRIDX` to `CHEMBL_COLS` so it is written to `ACTIVITY.tsv`; previously `CRIDX` was populated in every record dict but absent from the output column list, causing a spurious "mandatory field CRIDX is empty" validation warning on every row (pipeline crash in strict mode)
- `bin/reference.py`: removed `RIDX` from `MANDATORY_FIELDS` in `validate()`; the template column is named `Reference_identifier`, not `RIDX`, so the loop check always returned empty and raised a false "mandatory field RIDX is empty" warning on every row (pipeline crash in strict mode)
- `nextflow.config`: added `docker.enabled = false` inside the `singularity` and `conda` profiles to prevent Docker activating alongside them when those profiles are selected; the global `docker.enabled = true` is intentional for default Docker and CloWM execution
- `main.nf`: removed redundant error guards for `--prefix` and `--xenobiotic_class`; both parameters have defaults in `nextflow.config` and the guards would crash the pipeline if an empty string was submitted for an unmodified optional field

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


