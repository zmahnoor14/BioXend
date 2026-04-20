/*
 * MODULE: chemicals
 * Reads the Chemicals sheet from Template_open.ods and produces:
 *   - COMPOUND_RECORD.tsv  (ChEMBL deposition format)
 *   - COMPOUND_CTAB.sdf    (2D structures via RDKit)
 *   - COMPOUND_MAPPING.tsv (mapping between COMPOUND_RECORD and chemicals sheet names)
 */

process GENERATE_CHEMICALS {
    tag "chemicals"
    label 'process_low'
    container 'bioxend:0.1.0'

    input:
    path ods
    val  ridx
    val  prefix

    output:
    path "COMPOUND_RECORD.tsv",  emit: compound_record
    path "COMPOUND_MAPPING.tsv", emit: compound_mapping
    path "COMPOUND_CTAB.sdf",    emit: compound_sdf

    script:
    def args = task.ext.args ?: ''
    """
    chemicals.py \\
        --input ${ods} \\
        --ridx  "${ridx}" \\
        --prefix "${prefix}" \\
        --outdir . \\
        ${args}
    """
}
