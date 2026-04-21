/*
 * MODULE: biotransformation
 * Reads the Biotransformation sheet from Template_open.ods and produces:
 *   - ACTIVITY.tsv  (ChEMBL deposition format)
 *
 * CIDX is resolved by matching Common_Name against COMPOUND_MAPPING.tsv
 * from GENERATE_CHEMICALS (NAME → CIDX), which contains COMPOUND_NAME variants
 *
 * AIDX is resolved by matching ASSAY_Identifier against:
 *   ASSAY_MAPPING.tsv from GENERATE_ASSAY (USER_AIDX → AIDX),
 *   which converts the user's short key (e.g. 'assay1') to the
 *   pipeline-generated ChEMBL AIDX.
 *
 * ACTIVITY_COMMENT is auto-built by concatenating the free-text comment
 * with MIX-MB extension fields (reaction type, metabolite m/z, retention
 * time, annotation, and annotation level).
 */

process GENERATE_ACTIVITY {
    tag "biotransformation"
    label 'process_single'

    input:
    path ods
    val  ridx
    path compound_mapping  
    path assay_mapping     

    output:
    path "ACTIVITY.tsv", emit: activity

    script:
    def args = task.ext.args ?: ''
    """
    biotransformation.py \\
        --input             "${ods}" \\
        --ridx              "${ridx}" \\
        --compounds         "${compound_mapping}" \\
        --assays            "${assay_mapping}" \\
        --outdir            . \\
        ${args}
    """
}
