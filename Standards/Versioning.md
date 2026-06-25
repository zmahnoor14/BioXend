# MIX-MB Standards Versioning Guide

**Document Version:** 2.0  
**Last Updated:** June 22, 2026  
**Status:** Active

---

## 1. Overview

The MIX-MB standard is maintained as a **single unified document** (`MIXMB_Standards_main.md`), covering all three components (xenobiotics, microbes, biotransformation). Its version is tracked in `versions/standards-main.txt`.

---

## 2. Version Numbering System

### 2.1 Semantic Versioning (SemVer)

MIX-MB follows **Semantic Versioning 2.0.0** (https://semver.org/):

```
MAJOR.MINOR.PATCH

Example: 1.2.1
         │ │ │
         │ │ └─── PATCH: Bug fixes, clarifications, typos
         │ └───── MINOR: New features, backward compatible
         └─────── MAJOR: Breaking changes, incompatible changes
```

### 2.2 Version Components

#### MAJOR Version (X.0.0)

Increment when making **incompatible changes**:

- Required fields become mandatory
- Field names or formats change
- Ontology terms are deprecated/replaced
- Data structure changes that break existing implementations
- Removal of previously supported features

#### MINOR Version (1.X.0)

Increment when adding **new features in a backward-compatible manner**:

- New optional fields added
- New ontology terms added to controlled vocabularies
- Extended examples or clarifications
- New data formats supported (alongside existing ones)
- Deprecated features (but still supported)

#### PATCH Version (1.2.X)

Increment for **backward-compatible fixes**:

- Typo corrections
- Clarifications to existing text
- Fixed broken links or references
- Corrected examples
- No functional changes to the standard

---

## 3. Standard Architecture

**Single document:** `Standards/MIXMB_Standards_main.md`  
**Version file:** `versions/standards-main.txt`  
**Current version:** 0.5.0 (Draft)

All three components (MIX-MB(X) — Xenobiotics, MIX-MB(M) — Microbes, MIX-MB(B) — Biotransformation) are described within this single document. There are no separate per-component version files.

**Status definitions:**
- **Draft (0.x.x):** Pre-release, breaking changes expected
- **Stable (1.x.x+):** Production-ready, semantic versioning enforced
- **Deprecated:** No longer maintained, migration path provided

---

## 4. Versioning Workflow

### 4.1 Which Version to Bump?

```
What changed?
│
├─ Fixed typo/broken link?         → PATCH (x.y.Z)
├─ Added optional field?           → MINOR (x.Y.0)
├─ Made optional field required?   → MAJOR (X.0.0)
├─ Changed field name?             → MAJOR (X.0.0)
├─ Removed deprecated feature?     → MAJOR (X.0.0)
├─ Added new ontology term?        → MINOR (x.Y.0)
├─ Changed ontology requirement?   → MAJOR (X.0.0)
└─ Documentation clarification?    → PATCH (x.y.Z)
```

### 4.2 Release Steps

1. Update version number in `versions/standards-main.txt`
2. Update the version header in `MIXMB_Standards_main.md`
3. Add a CHANGELOG entry with date and summary of changes
4. Open a PR against `development` (standards changes require a 14-day community review and 2 endorsements)
5. After merge, create a GitHub Release and update Zenodo DOI

### 4.3 PR Labels

Use PR labels to trigger automated version bumps via GitHub Actions (`auto-version.yml`):
- `bump:major` — MAJOR bump
- `bump:minor` — MINOR bump
- `bump:patch` — PATCH bump

---

## 5. Deprecation Policy

**Timeline:**
```
Version n     Version n+1     Version n+2
    │              │               │
    │         Deprecation     Removal (MAJOR)
    │          Announced
    └──────────────┴───────────────┘
          6 months        next MAJOR
```

Deprecation notices must include: what is deprecated, why, what to use instead, and the removal timeline.

---

## 6. Branching Strategy

```
main (stable releases)
└── development (integration branch)
    ├── feature/...
    └── bugfix/...
```

- **main:** Tagged stable releases only
- **development:** All active work targets this branch
- **feature/*:** New features (MINOR bumps)
- **bugfix/*:** Fixes (PATCH bumps)

---

## 7. Version Citation

**Cite the unified standard:**
```
Zulfiqar, M., et al. (2026). Minimum Information about Xenobiotics-Microbiome 
Biotransformation (MIX-MB) Standard. Zenodo. 
https://doi.org/10.5281/zenodo.XXXXXXX
```

**In submitted datasets:**
```json
{
  "metadata": {
    "standard": "MIX-MB",
    "standard_version": "0.5.0",
    "compliance_date": "2026-06-22"
  }
}
```

---

## 8. Release Checklist

- [ ] `versions/standards-main.txt` updated
- [ ] Version header in `MIXMB_Standards_main.md` updated
- [ ] CHANGELOG entry added with date
- [ ] Examples updated (if needed)
- [ ] Breaking changes documented (if MAJOR)
- [ ] Migration guide provided (if MAJOR)
- [ ] Community review completed (14 days + 2 endorsements for standards changes)
- [ ] GitHub Release created
- [ ] Zenodo DOI updated

---

## 9. Contact and Governance

**Lead:** Mahnoor Zulfiqar (EMBL / NFDI4Microbiota)

**Decision process:**
```
Proposal → Community Review (14 days) → 2 Endorsements → Merge → Release
```

Contribute via GitHub Issues or Pull Requests against the `development` branch.
