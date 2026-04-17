#!/usr/bin/env nextflow
/*
 * BioXend Pipeline — MIX-MB ChEMBL Submission Generator
 *
 * Reads a filled MIX-MB Template_open.ods and produces six ChEMBL-ready
 * deposition files in parallel (all modules read the same template):
 *
 *   REFERENCE.tsv       — publication metadata
 *   README.toml         — submission metadata
 *   COMPOUND_RECORD.tsv — compound records (CIDX-indexed)
 *   COMPOUND_CTAB.sdf   — 2D chemical structures (RDKit)
 *   ASSAY.tsv           — assay descriptions per organism/condition
 *   ASSAY_PARAM.tsv     — experimental parameters
 *   ACTIVITY.tsv        — compound–assay activity links
 *
 * Usage:
 *   nextflow run main.nf -profile conda \
 *     --input  Standards/Templates/Template_open.ods \
 *     --ridx   MyStudy_2024 \
 *     --outdir results/
 */

nextflow.enable.dsl = 2

// ─────────────────────────────────────────────────────────────────────────────
// Imports
// ─────────────────────────────────────────────────────────────────────────────

include { GENERATE_REFERENCE   } from './modules/reference'
include { GENERATE_CHEMICALS   } from './modules/chemicals'
include { GENERATE_ASSAY       } from './modules/microbes'
include { GENERATE_ASSAY_PARAM } from './modules/experiment'
include { GENERATE_ACTIVITY    } from './modules/biotransformation'

// ─────────────────────────────────────────────────────────────────────────────
// Parameters
// ─────────────────────────────────────────────────────────────────────────────

params.help   = false

// Required
params.input  = null   // Path to Template_open.ods
params.ridx   = null   // Reference identifier (matches Reference_identifier in template)

// Chemicals options
params.prefix = "CIDX" // Prefix for auto-generated compound identifiers

// Microbes / ASSAY options
params.xenobiotic_class = "xenobiotic compound"  // e.g. 'drug', 'pesticide'

// Pipeline options
params.outdir  = "${projectDir}/results"
params.strict  = false   // Exit non-zero on validation warnings

// ─────────────────────────────────────────────────────────────────────────────
// Help
// ─────────────────────────────────────────────────────────────────────────────

def helpMessage() {
    log.info """
    BioXend — MIX-MB ChEMBL Pipeline

    Usage:
      nextflow run main.nf -profile conda \\
        --input  Standards/Templates/Template_open.ods \\
        --ridx   MyStudy_2024 \\
        --outdir results/

    Required:
      --input   PATH    Filled MIX-MB Template_open.ods
      --ridx    STRING  Reference identifier (must match the
                        Reference_identifier column in the Reference sheet)

    Compound options:
      --prefix  STRING  Prefix for auto-generated CIDXs [default: CIDX]

    Assay options:
      --xenobiotic_class  STRING  Singular class name used in ASSAY_DESCRIPTION
                                   e.g. 'drug', 'pesticide' [default: xenobiotic compound]

    Pipeline options:
      --outdir  PATH   Output directory [default: ./results]
      --strict         Exit non-zero on any validation warning
      --help           Show this message and exit

    Profiles:
      -profile conda        Use conda environments (recommended for local use)
      -profile docker       Use Docker container
      -profile singularity  Use Singularity container
      -profile slurm        Submit jobs to a SLURM cluster

    Output files written to --outdir:
      REFERENCE.tsv       Publication / reference metadata
      README.toml         ChEMBL submission metadata
      COMPOUND_RECORD.tsv Compound records
      COMPOUND_CTAB.sdf   2D chemical structures (RDKit)
      ASSAY.tsv           Assay descriptions
      ASSAY_PARAM.tsv     Experimental parameters
      ACTIVITY.tsv        Compound-assay activity links
    """.stripIndent()
}

if (params.help) {
    helpMessage()
    exit 0
}

// ─────────────────────────────────────────────────────────────────────────────
// Parameter checks
// ─────────────────────────────────────────────────────────────────────────────

if (!params.input) {
    log.error "ERROR: --input is required. Provide the path to Template_open.ods."
    exit 1
}
if (!params.ridx) {
    log.error "ERROR: --ridx is required. Provide the Reference_identifier value (e.g. 'MyStudy_2024')."
    exit 1
}

// ─────────────────────────────────────────────────────────────────────────────
// Workflow
// ─────────────────────────────────────────────────────────────────────────────

workflow {

    log.info """
    BioXend — MIX-MB ChEMBL Pipeline
    Input template   : ${params.input}
    Reference ID     : ${params.ridx}
    Output directory : ${params.outdir}
    Strict mode      : ${params.strict}
    """.stripIndent()

    // Single channel — all modules read the same template file
    template_ch = Channel.fromPath(params.input, checkIfExists: true)

    // All five steps are independent and run in parallel
    GENERATE_REFERENCE(
        template_ch
    )

    GENERATE_CHEMICALS(
        template_ch,
        params.ridx,
        params.prefix
    )

    GENERATE_ASSAY(
        template_ch,
        params.ridx,
        params.xenobiotic_class
    )

    // GENERATE_ASSAY_PARAM depends on GENERATE_ASSAY for ASSAY_MAPPING.tsv
    // so it can replace user keys (assay1, assay2…) with generated ChEMBL AIDXs.
    // DOSE is read from the Experiment sheet; --dose/--dose_units are fallbacks.
    GENERATE_ASSAY_PARAM(
        template_ch,
        params.dose,
        params.dose_units,
        params.dose_comments,
        GENERATE_ASSAY.out.assay_mapping
    )

    // GENERATE_ACTIVITY depends on both upstream steps:
    //   - GENERATE_CHEMICALS: COMPOUND_MAPPING.tsv for CIDX lookup by Common_Name
    //   - GENERATE_ASSAY:     ASSAY_MAPPING.tsv for AIDX lookup by user key
    //     (both mapping files are intermediates, not published to outdir)
    GENERATE_ACTIVITY(
        template_ch,
        params.ridx,
        GENERATE_CHEMICALS.out.compound_mapping,
        GENERATE_ASSAY.out.assay_mapping
    )
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
