#!/usr/bin/env nextflow
/*
 * BioXend Pipeline — MIX-MB ChEMBL Submission Generator
 *
 * Usage:
 *   nextflow run main.nf -profile docker \
 *     --input  Standards/Templates/Template_open.ods \
 *     --outdir results/ \
 *     --prefix HMDM
 *     --xenobiotic_class drug
 */

include { BIOXEND } from './workflows/bioxend'

// ─────────────────────────────────────────────────────────────────────────────
// Entry point
// ─────────────────────────────────────────────────────────────────────────────

workflow {
    if (!params.input) {
        error "ERROR: --input is required. Provide the path to Template_open.ods."
    }
    if (!params.prefix) {
        error "ERROR: --prefix is required. Provide a prefix for the output files."
    }
    if (!params.xenobiotic_class) {
        error "ERROR: --xenobiotic_class is required. Provide the xenobiotic class."
    }

    BIOXEND()
}

