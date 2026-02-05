#install.packages("stringr")
#install.packages("dplyr")
#install.packages("cli")
#install.packages("profvis")
#install.packages("devtools")
#install.packages("tidyverse")
install.packages("roxygen2")

input_dir <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj"
setwd(input_dir)

library("stringr")
library("dplyr")
library("cli")
library("profvis")
library("devtools")
library("tidyr")
library("tidyverse")

# check
.libPaths()

#### REFERENCE.tsv ####

# function to generate reference.tsv
write_reference_tsv <- function(RIDX, DOI, TITLE, AUTHORS, ABSTRACT, YEAR, 
                                JOURNAL_NAME = NA, VOLUME = NA, ISSUE = NA,
                                FIRST_PAGE = NA,LAST_PAGE = NA,REF_TYPE,PATENT_ID = NA){
  ReferenceTSV_ChEMBL <- cbind(RIDX, DOI,JOURNAL_NAME,YEAR,
                               VOLUME,ISSUE,FIRST_PAGE,LAST_PAGE,REF_TYPE,
                               TITLE,AUTHORS,ABSTRACT,PATENT_ID)
  write.table(ReferenceTSV_ChEMBL, file='REFERENCE.tsv', sep='\t', row.names=FALSE)
  return(ReferenceTSV_ChEMBL)
}

