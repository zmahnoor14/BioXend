#!/usr/bin/env Rscript

################################################################################
# generate_assay.R
# Author: Mahnoor Zulfiqar
# Description: Generate assay.tsv file with validated metadata for ChEMBL
################################################################################

# Suppress warnings 
options(warn = -1)

# Load optparse for argument parsing
suppressPackageStartupMessages(library(optparse))

# -------------------------
# Define command-line options
# -------------------------

option_list <- list(
  make_option("--assay_input_csv", type="character"),
  make_option("--ridx", type="character"),
  make_option("--category", type="list", default=c("bacteria", "enzyme", "community")),
  make_option("--group", type="character", default=NA),
  make_option("--source", type="character", default=NA)
)



write_assay_tsv <- function(assay_input_csv, ridx, category = c("bacteria", "enzyme", "community"), group=NA, source = NA){
  input_assay <- read.csv(assay_input_csv)
  ASSAY <- data.frame(matrix(ncol = 16, nrow = nrow(input_assay)))
  colnames(ASSAY) <- c("AIDX", "RIDX", "ASSAY_DESCRIPTION", "ASSAY_TYPE", "ASSAY_GROUP",
                       "ASSAY_ORGANISM", "ASSAY_STRAIN", "ASSAY_TAX_ID",
                       "ASSAY_SOURCE", "ASSAY_TISSUE", "ASSAY_CELL_TYPE", 
                       "ASSAY_SUBCELLULAR_FRACTION", "TARGET_TYPE",
                       "TARGET_NAME", "TARGET_ACCESSION", "TARGET_ORGANISM", "TARGET_TAX_ID")
  ASSAY$RIDX <- ridx
  ASSAY$ASSAY_DESCRIPTION <- input_assay$assay_description
  ASSAY$ASSAY_TYPE <- "A"
  ASSAY$ASSAY_ORGANISM <- input_assay$Species
  ASSAY$ASSAY_STRAIN <- input_assay$Strain
  ASSAY$ASSAY_TAX_ID <- input_assay$organismTAXID
  ASSAY$TARGET_TYPE <- "ADMET"
  ASSAY$TARGET_NAME <- input_assay$target_name
  ASSAY$TARGET_ACCESSION <- input_assay$target_accession

  if ("source" %in% colnames(input_assay)){
    ASSAY$ASSAY_SOURCE <- input_assay$source
  }else{
    ASSAY$ASSAY_SOURCE <- source
  }
  # second category specific - enzyme
  if ("enzyme" %in% category){

    rows_indices <- as.numeric(rownames(input_assay[!is.na(input_assay$target_name), ]))
    ASSAY[rows_indices,"TARGET_TYPE"] <- "SINGLE_PROTEIN"
    ASSAY[rows_indices, "TARGET_ORGANISM"] <- input_assay[rows_indices, "Species"]
    ASSAY[rows_indices, "TARGET_TAX_ID"] <- input_assay[rows_indices, "organismTAXID"]
    unlist(ASSAY[rows_indices, "TARGET_ORGANISM"])
    ASSAY[rows_indices, "AIDX"] <- paste(rep("Zimmermann", length(rows_indices)), unlist(ASSAY[rows_indices, "ASSAY_STRAIN"]), unlist(ASSAY[rows_indices, "ASSAY_ORGANISM"]), rep("biotransformation",  length(rows_indices)), unlist(ASSAY[rows_indices, "TARGET_ACCESSION"]), sep = "_")
  }
  # third category specific - community
  if ("community" %in% category){
    rows_indices_comm <- as.numeric(rownames(input_assay[!is.na(input_assay$Specimen), ]))
    ASSAY[rows_indices_comm, "AIDX"] <- paste(rep("Zimmermann_Community", length(rows_indices_comm)),
                                              unlist(input_assay[rows_indices_comm, "Specimen"]),
                                              rep("biotransformation",  length(rows_indices_comm)),
                                              sep = "_")
  }

  # first category - single strain
  if ("bacteria" %in% category){

    rows_indices_bac <- as.numeric(rownames(ASSAY[is.na(ASSAY$AIDX), ]))
    ASSAY[rows_indices_bac, "AIDX"] <- paste(rep("Zimmermann", length(rows_indices_bac)),
                                             unlist(ASSAY[rows_indices_bac, "ASSAY_STRAIN"]),
                                             unlist(ASSAY[rows_indices_bac, "ASSAY_ORGANISM"]),
                                             rep("biotransformation",  length(rows_indices_bac)),
                                             sep = "_")
  }
  ASSAY <- ASSAY %>%
    mutate(across(everything(), ~ replace(.x, is.na(.x), "")))

  write.csv(ASSAY, paste(output_dir, "/ASSAY.tsv", sep =""))
  return(ASSAY)
}

