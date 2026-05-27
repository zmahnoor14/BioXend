# Changelog
Versions follow semantic versioning: `MAJOR.MINOR.PATCH`.

> **Note:** The framework version (`versions/framework.txt`) and workflow version (`versions/workflow.txt`) are tracked independently. This changelog covers the **workflow/pipeline** (`versions/workflow.txt`).

---

## [0.8.0](https://github.com/zmahnoor14/BioXend/compare/v0.7.0...v0.8.0) (2026-05-27)


### Features

* **ci:** add PR version bump preview comment workflow ([8a206cf](https://github.com/zmahnoor14/BioXend/commit/8a206cfd57a8711e8d973242c3578be7166a7839))

## [0.7.0](https://github.com/zmahnoor14/BioXend/compare/v0.6.4...v0.7.0) (2026-05-19)


### Features

* Add GitHub Actions workflow for release management ([028adf9](https://github.com/zmahnoor14/BioXend/commit/028adf99f5fd242c4a281070be6037335af7ec31))
* Add GitHub Actions workflow for release management ([53651a8](https://github.com/zmahnoor14/BioXend/commit/53651a81b4fb962e51ec53b8dc2eea1fac8239d9))
* Add GitHub Actions workflow for release management ([d8d2fe2](https://github.com/zmahnoor14/BioXend/commit/d8d2fe25b24f42fa79b5bf862b68ffb49659e172))


### Bug Fixes

* fixed package name ([6b563dd](https://github.com/zmahnoor14/BioXend/commit/6b563dd338975d36e284779358caa8f00a9e9f5d))
* fixed package name ([f1cda54](https://github.com/zmahnoor14/BioXend/commit/f1cda5416a9010429074acc99ff31689157624e3))

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
