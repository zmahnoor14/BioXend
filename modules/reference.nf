/*
 * MODULE: reference
 * Reads the Reference sheet from Template_open.ods and produces:
 *   - REFERENCE.tsv  (ChEMBL deposition format)
 *   - README.toml    (submission metadata)
 */

process GENERATE_REFERENCE {
    tag "reference"
    publishDir "${params.outdir}", mode: 'copy'
    conda "${projectDir}/envs/py_env.yml"

    input:
    path ods

    output:
    path "REFERENCE.tsv", emit: reference
    path "README.toml",   emit: readme

    script:
    def strict_flag = params.strict ? "--strict" : ""
    """
    python ${projectDir}/bin/reference.py \\
        --input ${ods} \\
        --outdir . \\
        ${strict_flag}
    """
}
