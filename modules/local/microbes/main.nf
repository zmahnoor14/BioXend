/*
 * MODULE: microbes
 * Reads the Microbes + Experiment sheets from Template_open.ods and produces:
 *   - ASSAY.tsv          (ChEMBL deposition format — published to outdir)
 *   - ASSAY_MAPPING.tsv  (intermediate only — maps user keys to generated AIDXs)
 */

process GENERATE_ASSAY {
    tag "microbes"
    label 'process_single'
    container 'bioxend:0.1.0'

    input:
    path ods
    val  ridx
    val  xenobiotic_class

    output:
    path "ASSAY.tsv",         emit: assay
    path "ASSAY_MAPPING.tsv", emit: assay_mapping

    script:
    def args = task.ext.args ?: ''
    """
    microbes.py \\
        --input "${ods}" \\
        --ridx  "${ridx}" \\
        --xenobiotic_class "${xenobiotic_class}" \\
        --outdir . \\
        ${args}
    """
}
