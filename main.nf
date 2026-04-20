#!/usr/bin/env nextflow
/*
 * BioXend Pipeline — MIX-MB ChEMBL Submission Generator
 *
 * Usage:
 *   nextflow run main.nf -profile docker \
 *     --input  Standards/Templates/Template_open.ods \
 *     --outdir results/
 */

nextflow.enable.dsl = 2

include { BIOXEND } from './workflows/bioxend'

// ─────────────────────────────────────────────────────────────────────────────
// Parameter validation
// ─────────────────────────────────────────────────────────────────────────────

if (!params.input) {
    log.error "ERROR: --input is required. Provide the path to Template_open.ods."
    exit 1
}

// ─────────────────────────────────────────────────────────────────────────────
// Entry point
// ─────────────────────────────────────────────────────────────────────────────

workflow {
    BIOXEND()
}

// ─────────────────────────────────────────────────────────────────────────────
// Completion hooks
// ─────────────────────────────────────────────────────────────────────────────

workflow.onComplete {
    def status = workflow.success ? "SUCCESS" : "FAILED"
    log.info """
    Pipeline ${status}
    Duration   : ${workflow.duration}
    Output dir : ${params.outdir}
    Exit status: ${workflow.exitStatus}
    """.stripIndent()
}

workflow.onError {
    log.error "Pipeline failed: ${workflow.errorMessage}"
}
