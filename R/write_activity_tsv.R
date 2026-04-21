write_activity_tsv <- function(output_dir, input_csv, compound_tsv, assay_tsv,
                               ridx, type = "Biotransformation"){
  # INPUT CSV SHOULD HAVE ATLEAST THE FOLLOWING COLUMNS: compound names, bacteria/strain (when applied), binary_activity, activity comment;
  # For additional ChEMBL defined columns, please use exactly the same name of the column as mentioned by ChEMBL!

  input_assay <- read.csv(assay_tsv)
  input_activity <- read.csv(input_csv)
  input_compound <- read.csv(compound_tsv, sep = "\t")
  ACTIVITY <- data.frame(matrix(ncol = 20, nrow = nrow(input_activity)))
  colnames(ACTIVITY) <- c("CIDX", "CRIDX", "SRC_ID_CIDX", "AIDX", "SRC_ID_AIDX", "RIDX", "TEXT_VALUE",
                          "RELATION", "VALUE", "UPPER_VALUE", "UNITS", "SD_MINUS",
                          "SD_PLUS", "ACTIVITY_COMMENT", "CRIDX_CHEMBLID", "CRIDX_DOCID",
                          "ACT_ID", "TEOID", "TYPE", "ACTION_TYPE")
  ACTIVITY$CRIDX <- ridx
  ACTIVITY$TYPE <- "Biotransformation"
  ACTIVITY$ACTIVITY_COMMENT <- input_activity$Comment
  ACTIVITY[which(input_activity$Biotransformation == "Compound Metabolized"), "ACTION_TYPE"] <- "SUBSTRATE"
  ACTIVITY$TEXT_VALUE <- input_activity$Biotransformation
  ACTIVITY$CIDX <- input_compound$CIDX[match(input_activity$DrugName, input_compound$COMPOUND_NAME)]
  ACTIVITY$RIDX <- ridx
  input_activity$Sample[input_activity$Sample == ""] <- input_activity$Protein[input_activity$Sample == ""]



  #<- input_activity$now[is.na(input_activity$Sample)]
  # Pre-allocate with NA
  input_activity$matched_AIDX <- NA

  # Correctly splitting and extracting the first two parts of the Sample column
  input_activity$first_split <- sapply(input_activity$Sample, function(x) {
    if (grepl(" ", x)) {
      # Split by space and extract the first two parts
      parts <- strsplit(x, " ")[[1]]  # Split the string
      if (length(parts) >= 2) {
        return(paste(parts[1:2], collapse = " "))  # Return the first two parts as a single string
      } else {
        return(parts[1])  # Return the only part if there's less than two
      }
    } else {
      return(x[1])  # Return the original string if no spaces are found
    }
  })


  # Use sapply to vectorize the matching process
  input_activity$matched_AIDX <- sapply(input_activity$first_split, function(split_string) {

    # Find matching AIDX in input_assay for the current split_string
    match_idx <- grepl(split_string, input_assay$AIDX)

    # If a match is found, return the first matching AIDX, otherwise return NA
    if (any(match_idx)) {
      return(input_assay$AIDX[match_idx][1])  # Return the first match
    } else {
      return(NA)
    }
  })

  ACTIVITY$AIDX <- input_activity$matched_AIDX

  write.csv(ACTIVITY, paste(output_dir, "/ASSAY.tsv", sep =""))
  return(ACTIVITY)

}


