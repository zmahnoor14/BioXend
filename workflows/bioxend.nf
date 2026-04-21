/*
 * BioXend — core workflow
 * Reads a filled MIX-MB Template_open.ods and produces seven ChEMBL-ready
 * deposition files:
 *
 *   REFERENCE.tsv       — publication metadata
 *   README.toml         — submission metadata
 *   COMPOUND_RECORD.tsv — compound records 
 *   COMPOUND_CTAB.sdf   — 2D chemical structures (RDKit)
 *   ASSAY.tsv           — assay descriptions per organism/condition
 *   ASSAY_PARAM.tsv     — experimental parameters
 *   ACTIVITY.tsv        — compound–assay activity links
 */

// ─────────────────────────────────────────────────────────────────────────────
// Imports
// ─────────────────────────────────────────────────────────────────────────────

include { GENERATE_REFERENCE   } from '../modules/local/reference'
include { GENERATE_CHEMICALS   } from '../modules/local/chemicals'
include { GENERATE_ASSAY       } from '../modules/local/microbes'
include { GENERATE_ASSAY_PARAM } from '../modules/local/experiment'
include { GENERATE_ACTIVITY    } from '../modules/local/biotransformation'

// ─────────────────────────────────────────────────────────────────────────────
// Workflow
// ─────────────────────────────────────────────────────────────────────────────

workflow BIOXEND {

    log.info """
    BioXend — MIX-MB ChEMBL Pipeline
    Input template   : ${params.input}
    Output directory : ${params.outdir}
    Strict mode      : ${params.strict}
    """.stripIndent()

    // Single channel — all modules read the same template file
    template_ch = Channel.fromPath(params.input, checkIfExists: true)

    // GENERATE_REFERENCE reads Reference_identifier from the template;
    // RIDX.txt is emitted and used by all downstream modules.
    GENERATE_REFERENCE(
        template_ch
    )

    // Extract RIDX as a reusable value channel from RIDX.txt
    ridx_ch = GENERATE_REFERENCE.out.ridx_txt.map { it.text.trim() }

    GENERATE_CHEMICALS(
        template_ch,
        ridx_ch,
        params.prefix
    )

    // GENERATE_ASSAY runs independently; its ASSAY_MAPPING.tsv intermediate
    // is passed downstream to GENERATE_ASSAY_PARAM and GENERATE_ACTIVITY
    GENERATE_ASSAY(
        template_ch,
        ridx_ch,
        params.xenobiotic_class
    )

    // GENERATE_ASSAY_PARAM depends on GENERATE_ASSAY for ASSAY_MAPPING.tsv
    GENERATE_ASSAY_PARAM(
        template_ch,
        GENERATE_ASSAY.out.assay_mapping
    )

    // GENERATE_ACTIVITY depends on both:
    //   GENERATE_CHEMICALS → COMPOUND_MAPPING.tsv (CIDX lookup by Common_Name)
    //   GENERATE_ASSAY     → ASSAY_MAPPING.tsv    (AIDX lookup by user key)
    GENERATE_ACTIVITY(
        template_ch,
        ridx_ch,
        GENERATE_CHEMICALS.out.compound_mapping,
        GENERATE_ASSAY.out.assay_mapping
    )
}
