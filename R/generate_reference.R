#!/usr/bin/env Rscript

################################################################################
# generate_reference.R
# Author: Mahnoor Zulfiqar
# Description: Generate reference.tsv file with validated metadata for ChEMBL
################################################################################

# Suppress warnings 
options(warn = -1)

# Load optparse for argument parsing
suppressPackageStartupMessages(library(optparse))

# -------------------------
# Define command-line options
# -------------------------

option_list <- list(
  make_option("--RIDX", type="character"),
  make_option("--DOI", type="character"),
  make_option("--TITLE", type="character"),
  make_option("--AUTHORS", type="character"),
  make_option("--ABSTRACT", type="character"),
  make_option("--REF_TYPE", type="character"),
  make_option("--YEAR", type="integer"),
  make_option("--DATA_LICENCE", type="character", default="CC0"),
  make_option("--PUBMED_ID", type="character", default=NA),
  make_option("--JOURNAL_NAME", type="character", default=NA),
  make_option("--VOLUME", type="character", default=NA),
  make_option("--ISSUE", type="character", default=NA),
  make_option("--FIRST_PAGE", type="character", default=NA),
  make_option("--LAST_PAGE", type="character", default=NA),
  make_option("--PATENT_ID", type="character", default=NA),
  make_option("--CONTACT", type="character", default=NA)
  )

# -------------------------
# Main Function
# -------------------------

write_reference_tsv <- function(RIDX, DOI, TITLE, AUTHORS, ABSTRACT, REF_TYPE, YEAR,
                                DATA_LICENCE = "CC0", PUBMED_ID = NA, 
                                JOURNAL_NAME = NA, VOLUME = NA, ISSUE = NA, FIRST_PAGE = NA, 
                                LAST_PAGE = NA, PATENT_ID = NA, CONTACT = NA) {

  # Validate mandatory fields
  if (any(is.na(c(RIDX, TITLE, YEAR, ABSTRACT, AUTHORS, REF_TYPE, DOI)))) {
    stop("ERROR: RIDX, TITLE, YEAR, ABSTRACT, AUTHORS, REF_TYPE and DOI are mandatory fields.")
  }

  if (REF_TYPE == "Publication" && is.na(FIRST_PAGE)) {
    stop("ERROR: FIRST_PAGE is mandatory if the dataset is a Publication.")
  }

  # Create data frame
  ReferenceTSV_ChEMBL <- data.frame(
    RIDX = RIDX,
    DOI = DOI,
    TITLE = TITLE,
    AUTHORS = AUTHORS,
    ABSTRACT = ABSTRACT,
    REF_TYPE = REF_TYPE,
    YEAR = YEAR,
    DATA_LICENCE = DATA_LICENCE,
    PUBMED_ID = ifelse(is.na(PUBMED_ID), "", PUBMED_ID),
    JOURNAL_NAME = ifelse(is.na(JOURNAL_NAME), "", JOURNAL_NAME),
    VOLUME = ifelse(is.na(VOLUME), "", VOLUME),
    ISSUE = ifelse(is.na(ISSUE), "", ISSUE),
    FIRST_PAGE = ifelse(is.na(FIRST_PAGE), "", FIRST_PAGE),
    LAST_PAGE = ifelse(is.na(LAST_PAGE), "", LAST_PAGE),
    PATENT_ID = ifelse(is.na(PATENT_ID), "", PATENT_ID),
    CONTACT = ifelse(is.na(CONTACT), "", CONTACT),
    stringsAsFactors = FALSE
  )

  # Write to file
  write.table(ReferenceTSV_ChEMBL, 
              file = "REFERENCE.tsv", 
              sep = '\t', 
              row.names = FALSE,
              quote = FALSE)
  
  cat(sprintf("SUCCESS: Reference TSV written"))
  
  return(invisible(ReferenceTSV_ChEMBL))
}

# -------------------------
# Run the function
# -------------------------
write_reference_tsv(
  RIDX        = opt$RIDX,
  DOI         = opt$DOI,
  TITLE       = opt$TITLE,
  AUTHORS     = opt$AUTHORS,
  ABSTRACT    = opt$ABSTRACT,
  REF_TYPE    = opt$REF_TYPE,
  YEAR        = opt$YEAR,
  DATA_LICENCE = opt$DATA_LICENCE,
  PUBMED_ID    = opt$PUBMED_ID,
  JOURNAL_NAME = opt$JOURNAL_NAME,
  VOLUME       = opt$VOLUME,
  ISSUE        = opt$ISSUE,
  FIRST_PAGE   = opt$FIRST_PAGE,
  LAST_PAGE    = opt$LAST_PAGE,
  PATENT_ID    = opt$PATENT_ID,
  CONTACT      = opt$CONTACT
)