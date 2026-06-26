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
    container 'zmahnoor/bioxend:1.0.1'

    input:
    path ods
    path activity_tsv       // ordering dependency — ensures report runs last
    path name_changes_tsv   // organism name corrections from microbes.py

    output:
    path "report.html", emit: report

    script:
    def args = task.ext.args ?: ''
    """
    generate_report.py \\
        --input        "${ods}" \\
        --name_changes "${name_changes_tsv}" \\
        --outdir . \\
        ${args}
    """
}
