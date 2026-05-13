# Templates & Downloads

The MIX-MB submission template is the primary entry point for researchers who want to deposit biotransformation data. It captures all mandatory, recommended, and optional fields across the three MIX-MB components in a single structured spreadsheet.

{% hint style="success" %}
**Download the submission template below.** Open it in LibreOffice Calc, Excel, or any spreadsheet application that supports the ODS format.
{% endhint %}

{% file src=".gitbook/assets/Template_open.ods" %}
MIX-MB Submission Template (ODS format)
{% endfile %}

> **Can't open ODS?** Use [LibreOffice](https://www.libreoffice.org/) (free, cross-platform) or import directly into Google Sheets via File → Import.

---

## Template Structure

The template has four sheets, one per MIX-MB component plus a study reference sheet:

| Sheet | Maps to | Covered by |
|-------|---------|-----------|
| **Reference** | `REFERENCE.tsv` | Study / publication metadata |
| **Chemicals** | `COMPOUND_RECORD.tsv` + `COMPOUND_CTAB.sdf` | [MIX-MB(X)](../MIXMB_Xenobiotics.md) |
| **Microbes / Experiment** | `ASSAY.tsv` + `ASSAY_PARAM.tsv` | [MIX-MB(M)](../MIXMB_Microbes.md) |
| **Biotransformation** | `ACTIVITY.tsv` | [MIX-MB(B)](../MIXMB_Biotransformation.md) |

---

## Colour Coding

Each column is colour-coded to indicate its requirement level:

| Colour | Meaning |
|--------|---------|
| 🟢 Green | **Mandatory** — must be filled for a valid submission |
| 🔵 Blue | **Recommended** — strongly encouraged; required for Gold (Tier 1) compliance |
| 🟡 Yellow | **Optional** — fill if available |

{% hint style="info" %}
Fields marked **Auto-filled by BioXend** can be left empty — the pipeline will populate them automatically using RDKit (chemical properties) and the NCBI Taxonomy API (organism TaxIDs).
{% endhint %}

---

## Filling the Template: Quick Steps

1. **Reference sheet** — fill one row for your study. The `Reference_identifier` (RIDX) ties all other sheets together. If left empty, BioXend will generate one.
2. **Chemicals sheet** — one row per compound. Provide at minimum: `Common_Name`, `SMILES`, and `Chemical_identifier` (CIDX). BioXend auto-fills `InChIKey`, `Molecular_formula`, and `Molecular_weight` from the SMILES.
3. **Microbes / Experiment sheet** — one row per organism × condition combination. Provide: `assay_identifier` (AIDX), `Bacteria_scientific_name`, and `ASSAY_TYPE`. BioXend looks up `NCBI_Tax_ID` automatically.
4. **Biotransformation sheet** — one row per compound–assay interaction. Fill `Chemical_identifier`, `ASSAY_identifier`, and either `TEXT_VALUE` (qualitative) or `VALUE` + `UNITS` (quantitative).

{% hint style="warning" %}
The `Chemical_identifier` (CIDX) in the Biotransformation sheet must exactly match the `Chemical_identifier` in the Chemicals sheet. The same applies to `assay_identifier` (AIDX) across the Microbes and Biotransformation sheets.
{% endhint %}

---

## Identifier Quick Reference

| Identifier | Format | Example | Defined in |
|-----------|--------|---------|-----------|
| **RIDX** — Reference Index | `[Author]_[Label]` | `Zimmermann_GutAtlas` | Reference sheet |
| **CIDX** — Compound Index | `CIDX[nnnn]` | `CIDX0001` | Chemicals sheet |
| **AIDX** — Assay Index | `[Author]_[Genus]_[species]_[Condition]` | `Zimmermann_Actinomyces_graevenitzii_anaerobic` | Microbes sheet |

All three must appear together in every row of the Biotransformation sheet.

---

## Further Reading

{% content-ref url="../MIXMB_Standards_main.md" %}
[MIX-MB Overview](../MIXMB_Standards_main.md)
{% endcontent-ref %}

{% content-ref url="../MIXMB_Xenobiotics.md" %}
[MIX-MB(X) — Xenobiotics Standard](../MIXMB_Xenobiotics.md)
{% endcontent-ref %}

{% content-ref url="../MIXMB_Microbes.md" %}
[MIX-MB(M) — Microbes Standard](../MIXMB_Microbes.md)
{% endcontent-ref %}

{% content-ref url="../MIXMB_Biotransformation.md" %}
[MIX-MB(B) — Biotransformation Standard](../MIXMB_Biotransformation.md)
{% endcontent-ref %}
