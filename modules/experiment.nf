/*
 * MODULE: experiment
 * Reads the Experiment sheet from Template_open.ods and produces:
 *   - ASSAY_PARAM.tsv  (ChEMBL deposition format)
 *
 * AIDXs are first resolved from the identifier column of the Experiment
 * sheet (user short keys, e.g. 'assay1'), then replaced with the
 * pipeline-generated ChEMBL AIDXs via ASSAY_MAPPING.tsv from GENERATE_ASSAY.
 * Optionally pass --dose / --dose_units to add a DOSE parameter row.
 */

process GENERATE_ASSAY_PARAM {
    tag "experiment → ASSAY_PARAM"
    publishDir "${params.outdir}", mode: 'copy'
    conda "${projectDir}/envs/py_env.yml"

    input:
    path ods
    val  dose
    val  dose_units
    val  dose_comments
    path assay_mapping   // ASSAY_MAPPING.tsv from GENERATE_ASSAY (intermediate)

    output:
    path "ASSAY_PARAM.tsv", emit: assay_param

    script:
    def strict_flag  = params.strict      ? "--strict"                              : ""
    def dose_flag    = dose               ? "--dose \"${dose}\""                    : ""
    def units_flag   = dose_units         ? "--dose_units \"${dose_units}\""        : ""
    def comment_flag = dose_comments      ? "--dose_comments \"${dose_comments}\""  : ""
    """
    python ${projectDir}/bin/experiment.py \\
        --input  "${ods}" \\
        --assays "${assay_mapping}" \\
        --outdir . \\
        ${dose_flag} \\
        ${units_flag} \\
        ${comment_flag} \\
        ${strict_flag}
    """
}
