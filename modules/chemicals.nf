/*
 * MODULE: chemicals
 * Reads the Chemicals sheet from Template_open.ods and produces:
 *   - COMPOUND_RECORD.tsv  (ChEMBL deposition format)
 *   - COMPOUND_CTAB.sdf    (2D structures via RDKit)
 */

process GENERATE_CHEMICALS {
    tag "chemicals"
    publishDir "${params.outdir}", mode: 'copy'
    conda "${projectDir}/envs/py_env.yml"

    input:
    path ods
    val  ridx
    val  prefix

    output:
    path "COMPOUND_RECORD.tsv",  emit: compound_record
    path "COMPOUND_MAPPING.tsv", emit: compound_mapping
    path "COMPOUND_CTAB.sdf",    emit: compound_sdf

    script:
    def strict_flag = params.strict ? "--strict" : ""
    """
    python ${projectDir}/bin/chemicals.py \\
        --input ${ods} \\
        --ridx  "${ridx}" \\
        --prefix "${prefix}" \\
        --outdir . \\
        ${strict_flag}
    """
}
