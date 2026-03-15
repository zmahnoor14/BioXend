# Versioning Policy

BioXend / MIX-MB uses **independent semantic versioning** for each component, plus an overarching framework version. Version numbers are managed automatically — do not update them manually.

## Version Format

All versions follow [Semantic Versioning 2.0.0](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (e.g., removing a mandatory field, restructuring tables)
- **MINOR**: Backward-compatible additions (e.g., new optional/recommended field, new document section)
- **PATCH**: Corrections and clarifications (e.g., typo fixes, improved descriptions, example updates)

## Components

| Component | What it tracks |
|-----------|---------------|
| **Framework** | Overall BioXend/MIX-MB release. Increments whenever any component is released. |
| **Standards: Xenobiotics** | Minimum information standards for chemical/xenobiotic metadata |
| **Standards: Microbes** | Minimum information standards for microbe metadata |
| **Standards: Biotransformation** | Minimum information standards for biotransformation activity metadata |
| **Template** | The Excel data submission template |
| **Workflow** | The Nextflow BioXend data submission workflow |
