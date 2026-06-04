# MIX-MB Standards

**Minimum Information about Xenobiotics-Microbiome Biotransformation**

{% hint style="info" %}
**Version:** 0.1.1 · **Status:** Draft Standard · **Last updated:** March 2026\
**Maintainers:** Mahnoor Zulfiqar (EMBL, Molecular Systems Biology Unit)\
**Funding:** NFDI4Microbiota FlexFund 2026
{% endhint %}

MIX-MB defines the minimum metadata and data elements required to describe, share, and deposit xenobiotic microbial biotransformation experiments in a FAIR-compliant and reproducible way. It covers three interconnected aspects of every study:

* **MIX-MB(X)** — the chemical substrate (xenobiotic, drug, pesticide, dietary compound)
* **MIX-MB(M)** — the microbial organism or community
* **MIX-MB(B)** — the biotransformation assay, experimental conditions, and measured outcomes

Together these components ensure data can be directly deposited into community databases such as [ChEMBL](https://www.ebi.ac.uk/chembl/).

---

## Component Standards

| Component | Description | Version |
|-----------|-------------|---------|
| [MIX-MB(X) — Xenobiotics](MIXMB_Xenobiotics.md) | Chemical substrate identity, structure, and physicochemical properties | 0.1.1 |
| [MIX-MB(M) — Microbes](MIXMB_Microbes.md) | Microbial organism taxonomy, strain, and culture conditions | 0.1.1 |
| [MIX-MB(B) — Biotransformation](MIXMB_Biotransformation.md) | Assay design, experimental conditions, and activity outcomes | 0.1.1 |

For the full top-level overview including scope, ChEMBL file structure, and identifier conventions, see [MIX-MB Overview](MIXMB_Standards_main.md).

---

## How to Use These Standards

### If you are reporting data from a new study

1. **Assign identifiers first** — mint a RIDX (study), CIDXs (compounds), and AIDXs (assays) before entering any data. See the identifier conventions in [MIX-MB Overview](MIXMB_Standards_main.md).
2. **Fill in the submission template** — download the template from [Templates & Downloads](Templates/README.md) and complete the relevant sheets.
3. **Run BioXend** — the Nextflow pipeline converts your template into six ChEMBL-ready files (`REFERENCE.tsv`, `COMPOUND_RECORD.tsv`, `COMPOUND_CTAB.sdf`, `ASSAY.tsv`, `ASSAY_PARAM.tsv`, `ACTIVITY.tsv`).
4. **Deposit to ChEMBL** — contact chembl-help@ebi.ac.uk or use the ChEMBL deposition portal.

### Data quality tiers

Each component standard defines three compliance tiers:

| Tier | Label | Suitable for |
|------|-------|-------------|
| 1 | Gold — Publication-Ready | ChEMBL submission, FAIR data publications |
| 2 | Silver — Research-Grade | Internal data sharing, preprints |
| 3 | Bronze — Preliminary | Large-scale screening, initial deposits |

{% hint style="warning" %}
The **submission template** (`Template_open.ods`) is the primary user-facing file. Do not modify its column structure — changes must go through the community review process described in [Versioning Policy](Versioning.md).
{% endhint %}

---

## Scope

MIX-MB applies to experimental studies that measure the biotransformation of xenobiotic compounds by microbial organisms or microbial-derived systems. This includes in vitro single-strain assays, purified enzyme reactions, mixed microbial communities, time-course experiments, and product identification studies.

MIX-MB does **not** cover purely computational predictions of biotransformation, or metabolomics / genomics data (which have their own established standards).

---

## Licence and Citation

Standard documents are released under **CC BY 4.0**. The BioXend pipeline is released under the **MIT Licence**.

> Zulfiqar M. *et al.* MIX-MB: Minimum Information about Xenobiotics-Microbiome Biotransformation (v0.1.1). GitHub: https://github.com/zmahnoor14/BioXend

For questions, contributions, or endorsements: [zmahnoor14@gmail.com](mailto:zmahnoor14@gmail.com) · [GitHub Issues](https://github.com/zmahnoor14/BioXend/issues)
