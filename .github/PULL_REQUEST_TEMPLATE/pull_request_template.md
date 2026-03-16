## Description

<!-- Briefly describe what this PR does and why. -->

## Related Issue(s)

<!-- Reference any related issues. Use "Closes #123" to auto-close on merge. -->

Closes #

## Type of Change

<!-- Check all that apply. -->

- [ ] Bug fix
- [ ] New feature / enhancement
- [ ] Standards update (requires 14-day community review + 2 endorsements)
- [ ] Pipeline / workflow change
- [ ] Documentation update
- [ ] Refactor / cleanup

## Checklist

- [ ] This PR targets the `devel` branch (never `main` directly)
- [ ] Commit messages follow the convention: `[component] Brief description`
      e.g. `[standards] update MIX-MB(X) mandatory fields`
- [ ] I have **not** manually edited any file in `versions/` — version bumps are automated via PR labels
- [ ] I have **not** modified `Standards/Templates/Template.xlsx` unless this PR is explicitly a template release
- [ ] If standards were changed, a GitHub Issue is open for the 14-day community review period

## Version Bump Label

<!-- Add one of the following labels to this PR to trigger an automated version bump:
     bump:patch  — backwards-compatible fixes
     bump:minor  — new backwards-compatible features
     bump:major  — breaking changes
     Do NOT edit version files manually. -->

**Intended bump:** `bump:patch` / `bump:minor` / `bump:major` _(delete as appropriate)_

## Testing

<!-- Describe how you tested your changes. -->

- [ ] Pipeline runs end-to-end (`nextflow run main.nf -profile conda`)
- [ ] Relevant scripts run individually without errors
- [ ] Output files validated against ChEMBL deposition format

## Additional Notes

<!-- Anything else reviewers should know? -->