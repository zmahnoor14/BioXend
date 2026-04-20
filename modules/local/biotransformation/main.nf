/*
 * MODULE: biotransformation
 * Reads the Biotransformation sheet from Template_open.ods and produces:
 *   - ACTIVITY.tsv  (ChEMBL deposition format)
 *
 * CIDX is resolved by matching Common_Name against COMPOUND_MAPPING.tsv
 * from GENERATE_CHEMICALS (NAME → CIDX), which contains both COMPOUND_KEY
 * and COMPOUND_NAME variants so all template name formats are covered.
 *
 * AIDX is resolved by matching ASSAY_Identifier against:
 *   ASSAY_MAPPING.tsv from GENERATE_ASSAY (USER_AIDX → AIDX),
 *   which converts the user's short key (e.g. 'assay1') to the
 *   pipeline-generated ChEMBL AIDX.  This file is an intermediate only
 *   and is not published to the output directory.
 *
 * ACTIVITY_COMMENT is auto-built by concatenating the free-text comment
 * with MIX-MB extension fields (reaction type, metabolite m/z, retention
 * time, annotation, and annotation level).
 */

process GENERATE_ACTIVITY {
    tag "biotransformation → ACTIVITY"
    label 'process_single'
    conda "${projectDir}/envs/environment.yml"

    input:
    path ods
    val  ridx
    path compound_mapping  // COMPOUND_MAPPING.tsv from GENERATE_CHEMICALS
    path assay_mapping     // ASSAY_MAPPING.tsv   from GENERATE_ASSAY (intermediate)

    output:
    path "ACTIVITY.tsv", emit: activity

    script:
    def args = task.ext.args ?: ''
    """
    biotransformation.py \\
        --input             "${ods}" \\
        --ridx              "${ridx}" \\
        --compound-mapping  "${compound_mapping}" \\
        --assays            "${assay_mapping}" \\
        --outdir            . \\
        ${args}
    """
}
