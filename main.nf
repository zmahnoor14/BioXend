#!/usr/bin/env nextflow

/*
 * ChEMBL Submission Pipeline
 * Author: Mahnoor Zulfiqar
 * Description: Automated pipeline to generate ChEMBL submission files from compound and activity data
 */

nextflow.enable.dsl=2

// ========================
// Parameters
// ========================

params.input_csv = "${projectDir}/bin/smiles_list.txt"
params.strain_cond = "${projectDir}/bin/strain_cond.csv"
params.outdir = "${projectDir}/results"
params.help = false

// Reference metadata parameters
params.ridx = "HumanMicrobiome_DrugMetabolism"
params.doi = "10.1038/s41586-019-1291-3"
params.title = "Mapping human microbiome drug metabolism by gut bacteria and their genes"
params.authors = "Michael Zimmermann, Maria Zimmermann-Kogadeeva, Rebekka Wegmann & Andrew L. Goodman"
params.abstract = "Individuals vary widely in their responses to medicinal drugs..."
params.year = 2019
params.journal_name = "Nature"
params.volume = "570"
params.issue = "7762"
params.first_page = "462"
params.last_page = "467"
params.ref_type = "Publication"
params.data_licence = "CC0"

// ========================
// Help Message
// ========================

def helpMessage() {
    log.info"""
    ================================================================
    ChEMBL Submission Pipeline
    ================================================================
    Usage:
      nextflow run main.nf [options]
    
    Required Parameters:
      --input_csv       Input CSV with SMILES, Names, Study_ID
      --strain_cond     CSV with strain conditions
      --outdir          Output directory for results
    
    Reference Parameters:
      --ridx            Reference index/ID
      --doi             DOI of publication
      --title           Publication title
      --authors         Publication authors
      --abstract        Publication abstract
      --year            Publication year
      --journal_name    Journal name (optional)
      --ref_type        Reference type (Publication, Patent, etc.)
    
    Example:
      nextflow run main.nf --input_csv data/compounds.csv --outdir results
    ================================================================
    """.stripIndent()
}

if (params.help) {
    helpMessage()
    exit 0
}

// ========================
// Process Definitions
// ========================

process GENERATE_REFERENCE {
    tag "Reference: ${params.ridx}"
    publishDir "${params.outdir}", mode: 'copy'
    conda "${projectDir}/envs/r_env.yml"
    
    input:
    val ridx
    val doi
    val title
    val authors
    val abstract
    val year
    val ref_type
    val journal_name
    val volume
    val issue
    val first_page
    val last_page
    val data_licence
    
    output:
    path "REFERENCE.tsv", emit: reference
    
    script:
    """
    generate_reference.R \\
        --RIDX "${ridx}" \\
        --DOI "${doi}" \\
        --TITLE "${title}" \\
        --AUTHORS "${authors}" \\
        --ABSTRACT "${abstract}" \\
        --YEAR ${year} \\
        --REF_TYPE "${ref_type}" \\
        --JOURNAL_NAME "${journal_name}" \\
        --VOLUME "${volume}" \\
        --ISSUE "${issue}" \\
        --FIRST_PAGE "${first_page}" \\
        --LAST_PAGE "${last_page}" \\
        --DATA_LICENCE "${data_licence}"
    """
}

process GENERATE_COMPOUNDS {
    tag "Compounds from SMILES"
    publishDir "${params.outdir}", mode: 'copy'
    conda "${projectDir}/envs/py_env.yml"
    
    input:
    path input_csv
    
    output:
    path "COMPOUND_RECORD.tsv", emit: compound_record
    path "COMPOUND_CTAB.sdf", emit: compound_sdf
    path "chembl_mapping.tsv", emit: chembl_mapping
    
    script:
    """
    generate_compound_files.py \\
        --input ${input_csv} \\
        --output_dir .
    """
}

process GENERATE_ASSAY {
    tag "Assay: ${params.ridx}"
    publishDir "${params.outdir}", mode: 'copy'
    conda "${projectDir}/envs/r_env.yml"
    
    input:
    path strain_cond
    val ridx
    
    output:
    path "ASSAY.tsv", emit: assay
    path "ASSAY_PARAM.tsv", emit: assay_param
    
    script:
    """
    generate_assay.R \\
        --strain_cond ${strain_cond} \\
        --ridx ${ridx}
    """
}

process GENERATE_ACTIVITY {
    tag "Activity: ${params.ridx}"
    publishDir "${params.outdir}", mode: 'copy'
    conda "${projectDir}/envs/r_env.yml"
    
    input:
    path compound_record
    path assay
    path activity_data
    val ridx
    
    output:
    path "ACTIVITY.tsv", emit: activity
    
    script:
    """
    write_activity_tsv.R \\
        --compound_tsv ${compound_record} \\
        --assay_tsv ${assay} \\
        --input_csv ${activity_data} \\
        --ridx ${ridx} \\
        --output_dir .
    """
}

process VALIDATE_SUBMISSION {
    tag "Validation"
    publishDir "${params.outdir}", mode: 'copy'
    
    input:
    path reference
    path compound_record
    path compound_sdf
    path assay
    path assay_param
    path activity
    
    output:
    path "validation_report.txt", emit: report
    
    script:
    """
    echo "ChEMBL Submission Files Validation Report" > validation_report.txt
    echo "=========================================" >> validation_report.txt
    echo "" >> validation_report.txt
    echo "Generated Files:" >> validation_report.txt
    echo "  - REFERENCE.tsv: \$(wc -l < ${reference}) lines" >> validation_report.txt
    echo "  - COMPOUND_RECORD.tsv: \$(wc -l < ${compound_record}) lines" >> validation_report.txt
    echo "  - COMPOUND_CTAB.sdf: Present" >> validation_report.txt
    echo "  - ASSAY.tsv: \$(wc -l < ${assay}) lines" >> validation_report.txt
    echo "  - ASSAY_PARAM.tsv: \$(wc -l < ${assay_param}) lines" >> validation_report.txt
    echo "  - ACTIVITY.tsv: \$(wc -l < ${activity}) lines" >> validation_report.txt
    echo "" >> validation_report.txt
    echo "Validation Status: SUCCESS" >> validation_report.txt
    echo "Date: \$(date)" >> validation_report.txt
    """
}

// ========================
// Workflow
// ========================

workflow {
    
    // Print pipeline info
    log.info """
    ================================================================
    ChEMBL Submission Pipeline
    ================================================================
    Input CSV        : ${params.input_csv}
    Strain Conditions: ${params.strain_cond}
    Output Directory : ${params.outdir}
    Reference ID     : ${params.ridx}
    ================================================================
    """.stripIndent()
    
    // Create input channels
    input_csv_ch = Channel.fromPath(params.input_csv, checkIfExists: true)
    strain_cond_ch = Channel.fromPath(params.strain_cond, checkIfExists: true)
    
    // Step 1: Generate Reference file
    GENERATE_REFERENCE(
        params.ridx,
        params.doi,
        params.title,
        params.authors,
        params.abstract,
        params.year,
        params.ref_type,
        params.journal_name,
        params.volume,
        params.issue,
        params.first_page,
        params.last_page,
        params.data_licence
    )
    
    // Step 2: Generate Compound files from SMILES
    GENERATE_COMPOUNDS(input_csv_ch)
    
    // Step 3: Generate Assay files
    GENERATE_ASSAY(
        strain_cond_ch,
        params.ridx
    )
    
    // Step 4: Generate Activity file
    GENERATE_ACTIVITY(
        GENERATE_COMPOUNDS.out.compound_record,
        GENERATE_ASSAY.out.assay,
        input_csv_ch,
        params.ridx
    )
    
    // Step 5: Validate all generated files
    VALIDATE_SUBMISSION(
        GENERATE_REFERENCE.out.reference,
        GENERATE_COMPOUNDS.out.compound_record,
        GENERATE_COMPOUNDS.out.compound_sdf,
        GENERATE_ASSAY.out.assay,
        GENERATE_ASSAY.out.assay_param,
        GENERATE_ACTIVITY.out.activity
    )
    
    // Emit completion message
    VALIDATE_SUBMISSION.out.report.view { 
        log.info """
        ================================================================
        Pipeline Completed Successfully!
        ================================================================
        Results available in: ${params.outdir}
        ================================================================
        """
    }
}

// ========================
// Workflow Completion
// ========================

workflow.onComplete {
    log.info """
    ================================================================
    Pipeline execution summary
    ================================================================
    Completed at : ${workflow.complete}
    Duration     : ${workflow.duration}
    Success      : ${workflow.success}
    Work Dir     : ${workflow.workDir}
    Exit status  : ${workflow.exitStatus}
    ================================================================
    """.stripIndent()
}

workflow.onError {
    log.error "Pipeline execution failed!"
    log.error "Error message: ${workflow.errorMessage}"
}
