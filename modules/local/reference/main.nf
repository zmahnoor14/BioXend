/*
 * MODULE: reference
 * Reads the Reference sheet from Template_open.ods and produces:
 *   - REFERENCE.tsv  (ChEMBL deposition format)
 *   - README.toml    (submission metadata)
 */

process GENERATE_REFERENCE {
    tag "reference"
    label 'process_single'

    input:
    path ods

    output:
    path "REFERENCE.tsv", emit: reference
    path "README.toml",   emit: readme
    path "RIDX.txt",      emit: ridx_txt

    script:
    def args = task.ext.args ?: ''
    """
    reference.py \\
        --input ${ods} \\
        --outdir . \\
        ${args}
    """
}
