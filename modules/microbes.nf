/*
 * MODULE: microbes
 * Reads the Microbes + Experiment sheets from Template_open.ods and produces:
 *   - ASSAY.tsv          (ChEMBL deposition format — published to outdir)
 *   - ASSAY_MAPPING.tsv  (intermediate only — maps user keys to generated AIDXs;
 *                         passed to GENERATE_ACTIVITY via channel, NOT published)
 */

process GENERATE_ASSAY {
    tag "microbes → ASSAY"
    // Publish only ASSAY.tsv; ASSAY_MAPPING.tsv stays in the work directory
    // and is passed to GENERATE_ACTIVITY as an intermediate channel input.
    publishDir "${params.outdir}", mode: 'copy', saveAs: { fn ->
        fn == "ASSAY_MAPPING.tsv" ? null : fn
    }
    conda "${projectDir}/envs/py_env.yml"

    input:
    path ods
    val  ridx
    val  xenobiotic_class

    output:
    path "ASSAY.tsv",         emit: assay
    path "ASSAY_MAPPING.tsv", emit: assay_mapping

    script:
    def strict_flag = params.strict ? "--strict" : ""
    """
    python ${projectDir}/bin/microbes.py \\
        --input "${ods}" \\
        --ridx  "${ridx}" \\
        --xenobiotic_class "${xenobiotic_class}" \\
        --outdir . \\
        ${strict_flag}
    """
}
