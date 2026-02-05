setwd("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj")
#install.packages("stringr")
library("stringr")

#renv::init()

#### REFERENCE.tsv ####


write_reference_tsv <- function(RIDX, DOI, TITLE, AUTHORS, ABSTRACT, YEAR, 
                                JOURNAL_NAME = NA, VOLUME = NA, ISSUE = NA,
                                FIRST_PAGE = NA,LAST_PAGE = NA,REF_TYPE,PATENT_ID = NA){
  ReferenceTSV_ChEMBL <- cbind(RIDX, DOI,JOURNAL_NAME,YEAR,
                               VOLUME,ISSUE,FIRST_PAGE,LAST_PAGE,REF_TYPE,
                               TITLE,AUTHORS,ABSTRACT,PATENT_ID)
  write.table(ReferenceTSV_ChEMBL, file='REFERENCE.tsv', sep='\t', row.names=FALSE)
  return(ReferenceTSV_ChEMBL)
}


RIDX <- c("HumanMicrobiome_DrugMetabolism")
DOI <- c("10.1038/s41586-019-1291-3") #or PUBMED_ID, whichever one is present
JOURNAL_NAME<- c("Nature") #optional
YEAR <- c("2019") #mandatory
VOLUME <- c("570") #optional
ISSUE <- c("7762") #optional
FIRST_PAGE <- c("462") #optional
LAST_PAGE<- c("467") #optional
REF_TYPE <- c("Publication") #mandatory either of the following category: Patent, Publication, Dataset or Book
TITLE <- c("Mapping human microbiome drug metabolism by gut bacteria and their genes") #mandatory
AUTHORS	<- c("Michael Zimmermann, Maria Zimmermann-Kogadeeva, Rebekka Wegmann & Andrew L. Goodman") #mandatory
ABSTRACT <- c("Individuals vary widely in their responses to medicinal drugs, which can be dangerous and expensive owing to treatment delays and adverse effects. Although increasing evidence implicates the gut microbiome in this variability, the molecular mechanisms involved remain largely unknown. Here we show, by measuring the ability of 76 human gut bacteria from diverse clades to metabolize 271 orally administered drugs, that many drugs are chemically modified by microorganisms. We combined high-throughput genetic analyses with mass spectrometry to systematically identify microbial gene products that metabolize drugs. These microbiome-encoded enzymes can directly and substantially affect intestinal and systemic drug metabolism in mice, and can explain the drug-metabolizing activities of human gut bacteria and communities on the basis of their genomic contents. These causal links between the gene content and metabolic activities of the microbiota connect interpersonal variability in microbiomes to interpersonal differences in drug metabolism, which has implications for medical therapy and drug development across multiple disease indications.")#mandatory
#PATENT_ID <- "" #optional = Any Patent Identifier up to a length of 200


ref_tbl <- write_reference_tsv(RIDX, DOI,JOURNAL_NAME,YEAR,
                               VOLUME,ISSUE,FIRST_PAGE,LAST_PAGE,REF_TYPE,
                               TITLE,AUTHORS,ABSTRACT)
ref_tbl

#### COMPOUND_RECORD.tsv ####

write_compoundRecord_tsv <- function(prefix, num_comp, RIDX, name_column, comp_data_csv, csv_sep = ";", digits = 4){
  # Function to generate the next ID
  counter = 1
  generate_next_id <- function(prefix, digits, num_comp) {
    ids<- c()
    
    for (i in 1:num_comp){
      ids[i] <- paste0(prefix, sprintf("%0*d", digits, counter))
      counter <<- counter + 1
    }
    
    return(ids)
  }
  comp_data <- read.csv(comp_data_csv, sep = ";")
  CIDX <- generate_next_id(prefix, digits, num_comp)
  COMPOUND_KEY <- list(comp_data[name_column])[[1]][1:num_comp,]
  COMPOUND_NAME <- COMPOUND_KEY
  Compound_RecordTSV_ChEMBL <- cbind(CIDX = CIDX, RIDX = RIDX, COMPOUND_KEY = COMPOUND_KEY, COMPOUND_NAME = COMPOUND_NAME)
  write.table(Compound_RecordTSV_ChEMBL, file='COMPOUND_RECORD.tsv', sep='\t', row.names=FALSE)
  return(Compound_RecordTSV_ChEMBL)
}

prefix <- "HMDM"
num_comp <- 271
digits <- 3  # Specify the number of zero-padding digits
RIDX <- rep("HumanMicrobiome_DrugMetabolism", num_comp)
comp_data_csv <- "supp_sheet2.csv"
name_column <- "MOLENAME"

comp_rec_tbl <- write_compoundRecord_tsv(prefix, num_comp, RIDX, name_column, comp_data_csv, digits)

#### COMPOUND_CTAB.sdf ####

# how to easily convert SMILES to SDF


#### ASSAY.tsv ####

#species data
species_data_csv <- "supp_sheet1.csv"

species_data <- read.csv("supp_sheet1.csv", sep = ";")

species_list_all <- as.list(species_data[, "Name"])
strain_list_all <- as.list(species_data[, "Reference"])
sp_st <- paste(strain_list_all, species_list_all, sep = "_")

#species_list <- unlist(unique(species_list_all))
#species_list

#species_list_mod <- str_replace(species_list, " ", "--")
#species_list_mod


# compound data
comp_list <- comp_rec_tbl[,"COMPOUND_KEY"]
length(unique(comp_list))
# activities data
activity_list <- c("bio", "met", "gen")
activity_list

combinations <- expand.grid(sp_st, comp_list, activity_list)
nrow(combinations)
combinations
# Use apply and paste to concatenate the elements in each row
AIDX <- apply(combinations, 1, function(row, index) paste(row, collapse = "_"), index = 1:nrow(combinations))
AIDX


RIDX <- rep("HumanMicrobiome_DrugMetabolism", length(AIDX))
RIDX
ASSAY_DESCRIPTION <- c()
#change
aidx_sep <- str_split(AIDX, "_")
for (i in 1:length(aidx_sep)){
  st <- aidx_sep[[i]][1]
  cp <- aidx_sep[[i]][3]
  sp <- aidx_sep[[i]][2]
  ac<- aidx_sep[[i]][4]
  if (ac == "bio"){
    assay_des <- paste("The drug", cp, "is tested on", sp, "strain:", st, "for biotransformation")
    ASSAY_DESCRIPTION <- c(ASSAY_DESCRIPTION, assay_des)
  }
  else if (ac == "met"){
    assay_des <- paste("The drug", cp, "is tested on", sp,  "strain:", st, "for metabolite identification")
    ASSAY_DESCRIPTION <- c(ASSAY_DESCRIPTION, assay_des)
  }
  else if (ac == "gen"){
    assay_des <- paste("The drug", cp, "is tested on", sp,  "strain:", st, "for protein identification")
    ASSAY_DESCRIPTION <- c(ASSAY_DESCRIPTION, assay_des)
  }
}
ASSAY_DESCRIPTION

ASSAY_TYPE <- "A"
ASSAY_TEST_TYPE <- "in vitro"


#change
x <- strsplit(AIDX, split = "_")
ASSAY_ORGANISM <- lapply(x, function(sublist) sublist[2])


ASSAY_STRAIN <- lapply(x, function(sublist) sublist[1])
ASSAY_STRAIN

install.packages("taxize")
# NCBI Tax ID
ASSAY_TAX_ID <- 


ASSAY_SOURCE <- "Zimmermann_Hamburg"

# no info in the example
#ASSAY_TISSUE
#ASSAY_CELL_TYPE
#ASSAY_SUBCELLULAR_FRACTION

#change, probably not needed
#TARGET_TYPE # check https://chembl.gitbook.io/chembl-data-deposition-guide/untitled-10/field-names-and-data-types-basic-submission/target_type-list
#TARGET_NAME
#TARGET_ACCESSION
#TARGET_ORGANISM
#TARGET_TAX_ID

#### ASSAY_PARAM.tsv ####


AIDX #mandatory

# type of parameter (very flexible) mandatory
TYPE

#Symbol indicating relationship between the Type and the Value (permitted: '>','<','=','~','<=','>=','<<','>>')
RELATION

# numeric value: Any number (including decimals, negatives and scientific notation (e.g. 3×10^2))
VALUE
UNITS

#The text value of non-numerical values
TEXT_VALUE
COMMENTS

#### ACTIVITY.tsv ####

CIDX

#The RIDX to be associated with the CIDX in the creation of the compound record. Must belong to SRC_ID_CIDX.
CRIDX


#The SRC_ID for the CIDX. 
SRC_ID_CIDX


AIDX

#The SRC_ID for the AIDX. 
SRC_ID_AIDX

RIDX

#The text value of non-numerical values. Do not use for value ranges. 
TEXT_VALUE
RELATION
VALUE


UPPER_VALUE
UNITS
SD_MINUS
SD_PLUS
ACTIVITY_COMMENT
CRIDX_CHEMBLID
CRIDX_CHEMBLID
ACT_ID
TEOID
TYPE
ACTION_TYPE









renv::restore()
