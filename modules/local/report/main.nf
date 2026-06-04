/*
 * MODULE: report
 * Reads all sheets from Template_open.ods and produces:
 *   - report.html  Self-contained interactive HTML report
 *
 * Runs after GENERATE_ACTIVITY so all ChEMBL submission files exist
 * before the report is emitted. The script reads from the ODS template
 * directly; activity_tsv is declared as input only to enforce ordering.
 */

process GENERATE_REPORT {
    tag "report"
    label 'process_low'
    container 'zmahnoor/bioxend:latest'

    input:
    path ods
    path activity_tsv   // ordering dependency — ensures report runs last

    output:
    path "report.html", emit: report

    script:
    def args = task.ext.args ?: ''
    """
    generate_report.py \\
        --input  "${ods}" \\
        --outdir . \\
        ${args}
    """
}
