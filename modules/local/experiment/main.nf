/*
 * MODULE: experiment
 * Reads the Experiment sheet from Template_open.ods and produces:
 *   - ASSAY_PARAM.tsv  (ChEMBL deposition format)
 *
 * AIDXs are first resolved from the identifier column of the Experiment
 * sheet (user short keys, e.g. 'assay1'), then replaced with the
 * pipeline-generated ChEMBL AIDXs via ASSAY_MAPPING.tsv from GENERATE_ASSAY.
 */

process GENERATE_ASSAY_PARAM {
    tag "experiment → ASSAY_PARAM"
    label 'process_single'
    conda "${projectDir}/envs/environment.yml"

    input:
    path ods
    path assay_mapping   // ASSAY_MAPPING.tsv from GENERATE_ASSAY (intermediate)

    output:
    path "ASSAY_PARAM.tsv", emit: assay_param

    script:
    def args = task.ext.args ?: ''
    """
    experiment.py \\
        --input  "${ods}" \\
        --assays "${assay_mapping}" \\
        --outdir . \\
        ${args}
    """
}
