/*
 * MODULE: fill_template
 * Reads the processed TSV outputs and writes back a copy of the user's
 * Template_open.ods with auto-resolved metadata fields pre-filled.
 * All cell styles (color-coding, fonts, borders) are preserved.
 *
 * Inputs:
 *   ods              — original Template_open.ods
 *   compound_mapping — COMPOUND_MAPPING.tsv (Common_Name → CIDX)
 *   assay_tsv        — ASSAY.tsv (resolved organism names, TaxIDs, targets)
 *   assay_mapping    — ASSAY_MAPPING.tsv (assay_identifier → AIDX)
 *   name_changes     — ORGANISM_NAME_CHANGES.tsv (canonical name corrections)
 *
 * Output:
 *   Template_BioXend_completed.ods — copy of input template with blanks filled
 */

process FILL_TEMPLATE {
    tag "fill_template"
    label 'process_single'
    container 'zmahnoor/bioxend:latest'

    input:
    path ods
    path compound_mapping
    path assay_tsv
    path assay_mapping
    path name_changes

    output:
    path "Template_BioXend_completed.ods", emit: filled_template

    script:
    """
    fill_template.py \\
        --input            "${ods}" \\
        --compound_mapping "${compound_mapping}" \\
        --assay_tsv        "${assay_tsv}" \\
        --assay_mapping    "${assay_mapping}" \\
        --name_changes     "${name_changes}" \\
        --outdir .
    """
}
