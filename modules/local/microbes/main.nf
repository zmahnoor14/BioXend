/*
 * MODULE: microbes
 * Reads the Microbes + Experiment sheets from Template_open.ods and produces:
 *   - ASSAY.tsv          (ChEMBL deposition format — published to outdir)
 *   - ASSAY_MAPPING.tsv  (intermediate only — maps user keys to generated AIDXs;
 *                         passed to GENERATE_ACTIVITY via channel, NOT published)
 */

process GENERATE_ASSAY {
    tag "microbes → ASSAY"
    label 'process_single'
    // publishDir is defined in conf/modules.config
    // ASSAY_MAPPING.tsv is excluded there via saveAs; it stays as an intermediate channel input.
    conda "${projectDir}/envs/environment.yml"

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
