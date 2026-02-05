setwd("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj")
#install.packages("stringr")
library("stringr")
library("dplyr")
#renv::init()

#### REFERENCE.tsv ####

# function to generate reference.tsv
write_reference_tsv <- function(RIDX, DOI, TITLE, AUTHORS, ABSTRACT, YEAR, 
                                JOURNAL_NAME = c(), VOLUME = c(), ISSUE = c(),
                                FIRST_PAGE = c(),LAST_PAGE = c(),REF_TYPE,PATENT_ID = c()){
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
PATENT_ID <- "" #optional = Any Patent Identifier up to a length of 200


ref_tbl <- write_reference_tsv(RIDX = RIDX, DOI = DOI, TITLE = TITLE, AUTHORS = AUTHORS, ABSTRACT = ABSTRACT, YEAR = YEAR, 
                               JOURNAL_NAME = JOURNAL_NAME, VOLUME = VOLUME, ISSUE = ISSUE,
                               FIRST_PAGE = FIRST_PAGE, LAST_PAGE = LAST_PAGE, REF_TYPE = REF_TYPE ,PATENT_ID = c())
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
  SMILES <- comp_data["SMILES"]
  Compound_RecordTSV_ChEMBL <- cbind(CIDX = CIDX, RIDX = RIDX, COMPOUND_KEY = COMPOUND_KEY, COMPOUND_NAME = COMPOUND_NAME)
  write.table(Compound_RecordTSV_ChEMBL, file='COMPOUND_RECORD.tsv', sep='\t', row.names=FALSE)
  Compound_RecordTSV_ChEMBL_with_SMILES <- cbind(CIDX = CIDX, RIDX = RIDX, COMPOUND_KEY = COMPOUND_KEY, COMPOUND_NAME = COMPOUND_NAME, SMILES = SMILES)
  write.table(Compound_RecordTSV_ChEMBL_with_SMILES, file='COMPOUND_RECORD_withSMILES.tsv', sep='\t', row.names=FALSE)
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

# how to easily convert SMILES to SDF by RDKit































#### ASSAY.tsv ####

## first condition


species_data_csv <- "supp_sheet1.csv"
species_col <- "Name"
strain_col <- "Reference"
ridx <- "HumanMicrobiome_DrugMetabolism"
# first sheet with organism information
species_data <- read.csv(species_data_csv)
species_list_all <- as.list(species_data[, species_col])
strain_list_all <- as.list(species_data[, strain_col])
tax_ids_csv <- "Retrieved_taxid_for_single_species.csv"
assay_type <- "A"
#cell_type <- "bacteria"
target <- "ADMET"
# combined name for species and strain to be included in the AIDX
AIDX<- paste(rep("Zimmermann", length(species_list_all)), strain_list_all, species_list_all, rep("biotransformation", length(species_list_all)), sep = "_")
AIDX[70] <- "Zimmermann_BW25113_Escherichia coli_biotransformation"
length(AIDX)

ASSAY_TYPE <- rep(assay_type, length(AIDX))
length(ASSAY_TYPE)

RIDX <- rep(ridx, length(AIDX))
length(RIDX)


x <- strsplit(AIDX, split = "_")
ASSAY_ORGANISM <- lapply(x, function(sublist) sublist[3])
ASSAY_ORGANISM <- unlist(ASSAY_ORGANISM) 
ASSAY_ORGANISM
ASSAY_STRAIN <- lapply(x, function(sublist) sublist[2])
ASSAY_STRAIN <- unlist(ASSAY_STRAIN) 
length(ASSAY_STRAIN)

ASSAY_DESCRIPTION <- paste(rep("The drug is tested on", length(AIDX)), 
                           ASSAY_ORGANISM, 
                           rep("strain:", length(AIDX)), 
                           ASSAY_STRAIN, 
                           rep("for biotransformation. The drug concentrations were measured before and after a 12-h incubation by liquid-chromatography-coupled mass spectrometry (LC–MS)", length(AIDX)), sep = " ")

length(ASSAY_DESCRIPTION)
# NCBI Tax ID
ASSAY_TAX_ID <- c() 
tax_ids <- read.csv(tax_ids_csv)

# # wrong: 4, 23, 25, 29, 35 index for species name wrong!!!!

for (j in 1:length(ASSAY_ORGANISM)){
  for (i in 1:nrow(tax_ids)){
    if (as.character(ASSAY_ORGANISM[j]) == tax_ids[i, "Species"]){
      ASSAY_TAX_ID <- c(ASSAY_TAX_ID, tax_ids[i, "taxid"])
    }
  }
}
length(ASSAY_TAX_ID)



ASSAY_SOURCE <- rep("Zimmermann", length(AIDX))
length(ASSAY_SOURCE)
TARGET_TYPE <- rep(target, length(AIDX))
length(TARGET_TYPE)

TARGET_NAME <- rep('', length(AIDX))
TARGET_ACCESSION <- rep('', length(AIDX)) 
TARGET_ORGANISM <- rep('', length(AIDX))
TARGET_TAX_ID <- rep('', length(AIDX)) 


assay_tsv <- cbind(AIDX, RIDX, ASSAY_DESCRIPTION, ASSAY_TYPE, ASSAY_ORGANISM, ASSAY_STRAIN, ASSAY_TAX_ID, ASSAY_SOURCE, TARGET_TYPE,
                   TARGET_NAME, TARGET_ACCESSION, TARGET_ORGANISM, TARGET_TAX_ID)


gene_data <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/supp_sheet13.csv")
gene_data <- gene_data[-c(14), ]
rownames(gene_data) <- 1:30
rownames(gene_data) 

colnames(gene_data)[2] <- "TARGET_NAME"
gene_data$ASSAY_ORGANISM <- NA
gene_data$ASSAY_STRAIN <- NA
gene_data$ASSAY_TAX_ID <- NA
gene_data[1:17, "ASSAY_ORGANISM"] <- "Bacteroides thetaiotaomicron"
gene_data[18:22, "ASSAY_ORGANISM"] <- "Collinsella aerofaciens"
gene_data[23:30, "ASSAY_ORGANISM"] <- "Bacteroides dorei"
gene_data[1:17, "ASSAY_STRAIN"] <- "VPI-5482"
gene_data[18:22, "ASSAY_STRAIN"] <- "ATCC25986"
gene_data[23:30, "ASSAY_STRAIN"] <- "DSM17855"
gene_data[1:17, "ASSAY_TAX_ID"] <- "818"
gene_data[18:22, "ASSAY_TAX_ID"] <- "74426"
gene_data[23:30, "ASSAY_TAX_ID"] <- "357276"
gene_data$TARGET_ORGANISM <- NA
gene_data$TARGET_TAX_ID <- NA
gene_data[1:17, "TARGET_ORGANISM"] <- "Bacteroides thetaiotaomicron"
gene_data[18:22, "TARGET_ORGANISM"] <- "Collinsella aerofaciens"
gene_data[23:30, "TARGET_ORGANISM"] <- "Bacteroides dorei"
gene_data[1:17, "TARGET_TAX_ID"] <- "818"
gene_data[18:22, "TARGET_TAX_ID"] <- "74426"
gene_data[23:30, "TARGET_TAX_ID"] <- "357276"


gene_data$TARGET_ACCESSION <- c("Q8ABF8", "Q8AB93", "Q8AAL9", "Q8AA96",
                                "Q8A911", "Q8A8L9", "Q8A8H5", "Q8A7U5", 
                                "Q8A618", "Q8A576", "Q8A575", "Q8A3J3",
                                "Q8A343", "Q8A331", "Q8A0E6", "Q8A0D0",
                                "Q8A0C5", "A4E7D0", "A4E8S4", "A4EB91",
                                "A4EBM5", "A4ED08", "B6VU18", "B6VTE7", 
                                "B6W0N3", "B6W1J1", "B6W293", "B6W2J3",
                                "B6W2J6", "B6W3P3")


gene_data$ASSAY_SOURCE <- rep("Zimmermann", nrow(gene_data))
gene_data$TARGET_TYPE <- rep("SINGLE PROTEIN", nrow(gene_data))
gene_data$ASSAY_TYPE <- rep("A", nrow(gene_data))
gene_data$RIDX <- rep(ridx, nrow(gene_data))
gene_data$AIDX <- paste(rep("Zimmermann", nrow(gene_data)), gene_data$ASSAY_STRAIN, gene_data$ASSAY_ORGANISM, rep("biotransformation",  nrow(gene_data)), gene_data$TARGET_ACCESSION, sep = "_")

gene_data$ASSAY_DESCRIPTION <- paste(rep("The drug is tested on", nrow(gene_data)), 
                                     gene_data$ASSAY_ORGANISM, 
                                     rep("strain:", nrow(gene_data)), 
                                     gene_data$ASSAY_STRAIN, 
                                     rep("for biotransformation. The drug concentrations were measured before and after a 12-h incubation by liquid-chromatography-coupled mass spectrometry (LC–MS)", nrow(gene_data)), sep = " ")
# combined name for species and strain to be included in the AIDX


assay_tsv_prot <- cbind(AIDX= gene_data$AIDX, 
                        RIDX = gene_data$RIDX, 
                        ASSAY_DESCRIPTION = gene_data$ASSAY_DESCRIPTION, 
                        ASSAY_TYPE = gene_data$ASSAY_TYPE, 
                        ASSAY_ORGANISM = gene_data$ASSAY_ORGANISM,
                        ASSAY_STRAIN = gene_data$ASSAY_STRAIN, 
                        ASSAY_TAX_ID = gene_data$ASSAY_TAX_ID, 
                        ASSAY_SOURCE = gene_data$ASSAY_SOURCE, 
                        TARGET_TYPE = gene_data$TARGET_TYPE, 
                        TARGET_NAME = gene_data$TARGET_NAME, 
                        TARGET_ACCESSION = gene_data$TARGET_ACCESSION, 
                        TARGET_ORGANISM = gene_data$TARGET_ORGANISM, 
                        TARGET_TAX_ID = gene_data$TARGET_TAX_ID)

length(colnames(assay_tsv))
length(colnames(assay_tsv_prot))
colnames(assay_tsv)
colnames(assay_tsv_prot)
assay_final <- rbind(assay_tsv, assay_tsv_prot)



ena_access <- read.csv("filereport_read_run_PRJEB31790.csv")
sorted_ena <- ena_access[order(ena_access$sample_title),]

colnames(sorted_ena)
community_data <- read.csv("supp_sheet16.csv", sep = ";")
nrow(community_data)

ASSAY_ORGANISM <- community_data$Community
length(ASSAY_ORGANISM)


ASSAY_TAX_ID <- rep("749906", nrow(community_data))
length(ASSAY_TAX_ID)
ASSAY_SOURCE <- rep("Zimmermann", nrow(community_data))
length(ASSAY_SOURCE)
TARGET_TYPE <- rep("ADMET", nrow(community_data))
length(TARGET_TYPE)
ASSAY_TYPE <- rep("A", nrow(community_data))
length(ASSAY_TYPE)
RIDX <- rep(ridx, nrow(community_data))
length(RIDX)
AIDX <- paste(rep("Zimmermann_Community", nrow(community_data)), 
              ASSAY_ORGANISM, 
              rep("biotransformation",  nrow(community_data)),
              sep = "_")
length(AIDX)

ASSAY_ORGANISM <- rep("gut metagenome", length(AIDX))
length(ASSAY_ORGANISM)
ASSAY_DESCRIPTION <- paste(
  rep("The drug is tested on the gut metagenome community of", nrow(community_data)), 
  community_data$Community,
  rep("with study accession number: PRJEB31790 and sample accession number: ", nrow(community_data)), 
  sorted_ena$sample_accession,
  rep("for biotransformation. The drug concentrations were measured over 9 timepoints collected between 0 and 24 hours of incubation by liquid-chromatography-coupled mass spectrometry (LC–MS)", nrow(community_data)), sep = " ")
length(ASSAY_DESCRIPTION)
# combined name for species and strain to be included in the AIDX
ASSAY_STRAIN <- rep('', length(AIDX))
TARGET_NAME  <- rep('', length(AIDX))
TARGET_ACCESSION  <- rep('', length(AIDX))
TARGET_ORGANISM  <- rep('', length(AIDX))
TARGET_TAX_ID <- rep('', length(AIDX))

COMMUNITY <- community_data$Community
assay_tsv_community <- cbind(AIDX, 
                   RIDX, 
                   ASSAY_DESCRIPTION, 
                   ASSAY_TYPE, 
                   ASSAY_ORGANISM, 
                   ASSAY_STRAIN, 
                   ASSAY_TAX_ID, 
                   ASSAY_SOURCE, 
                   TARGET_TYPE,
                   TARGET_NAME, 
                   TARGET_ACCESSION, 
                   TARGET_ORGANISM, 
                   TARGET_TAX_ID)#,COMMUNITY)


assay_final_com <- rbind(assay_final, assay_tsv_community)
write.table(assay_final_com, file='ASSAY.tsv', sep='\t', row.names=FALSE)





#### ASSAY_PARAM.tsv


param <- read.csv("ASSAY_PARAMINPUT.csv")

extracted_param <- param[1:14,-8]
extracted_param[c(2, 3, 7, 8, 11, 12), "RELATION"] <- "="
extracted_param[c(4, 9, 13), "TEXT_VALUE"] <- "Anaerobic condition at 37°C."
extracted_param[c(2, 7, 11), "COMMENTS"] <- "Tested drug concentrations in the bacterial assays."
extracted_param[c(3,8,12), "COMMENTS"] <- "Gut Microbiota Medium (GMM) used for bacterial assays at pH7."
## biotransformation
change_bio_for_Akkermansia_muciniphila <-"Frozen stocks of bacteria were plated on BHI blood agar and incubated at 37°C under anaerobic conditions. Single colonies were inoculated into 4 mL prereduced GMM and incubated anaerobically at 37°C for 48 h. Cultures were diluted (1:10) in 20% pre-reduced GMM containing drugs at 2 µM and further incubated at 37°C anaerobically."
extracted_param[1, "TEXT_VALUE"] <- "Frozen stocks of bacteria were plated on BHI blood agar and incubated at 37°C under anaerobic conditions. Single colonies were inoculated into 4 mL prereduced GMM and incubated anaerobically at 37°C for 24 h. Cultures were diluted (1:10) in 20% pre-reduced GMM containing drugs at 2 µM and further incubated at 37°C anaerobically."

bio_param <- extracted_param[1:5,-1]
bio_param_list <- list()

for (i in 1:nrow(assay_tsv)){
  bio_param$AIDX <- rep(assay_tsv[i, "AIDX"], 5)
  bio_param_list[[i]] <- bio_param
}
final_bio_param <- do.call(rbind, bio_param_list)
colnames(final_bio_param)
final_bio_param <- final_bio_param[c("AIDX", "TYPE", "RELATION", "VALUE", "UNITS", "TEXT_VALUE", "COMMENTS")]

final_bio_param["Akkermansia muciniphila" %in% final_bio_param$AIDX]

final_bio_param[376, "TEXT_VALUE"] <- change_bio_for_Akkermansia_muciniphila

## protein

prot_param <- extracted_param[6:9,-1]
prot_param_list <- list()

for (i in 1:nrow(assay_tsv_prot)){
  prot_param$AIDX <- rep(assay_tsv_prot[i, "AIDX"], 4)
  prot_param_list[[i]] <- prot_param
}
final_prot_param <- do.call(rbind, prot_param_list)
colnames(final_prot_param)
final_prot_param <- final_prot_param[c("AIDX", "TYPE", "RELATION", "VALUE", "UNITS", "TEXT_VALUE", "COMMENTS")]


## community
community_param <- extracted_param[10:14,-1]
community_param_list <- list()

for (i in 1:nrow(assay_tsv_community)){
  community_param$AIDX <- rep(assay_tsv_community[i, "AIDX"], 5)
  community_param_list[[i]] <- community_param
}
final_comm_param <- do.call(rbind, community_param_list)
colnames(final_comm_param)
final_comm_param <- final_comm_param[c("AIDX", "TYPE", "RELATION", "VALUE", "UNITS", "TEXT_VALUE", "COMMENTS")]

# Convert the lists to data frames
df_bio <- as.data.frame(final_bio_param)
df_prot <- as.data.frame(final_prot_param)
df_comm <- as.data.frame(final_comm_param)

# Combine the data frames using rbind
combined_df <- rbind(df_bio, df_prot, df_comm)
combined_df = data.frame(lapply(combined_df, as.character), stringsAsFactors=FALSE)

combined_df[is.na(combined_df)] = ""
write.table(combined_df, file='ASSAY_PARAM.tsv', sep = "\t", row.names=FALSE)














setwd("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj")


#### ACTIVITY.tsv ####
# correct activity data first

activity_csv <- read.csv("chembl_activity_input.csv")
colnames(activity_csv)
wrong_activity_data <- activity_csv[activity_csv["perc_consumed"] < activity_csv["Drug_adaptive_FC_threshold_perc"],]
activity_csv <- activity_csv[activity_csv["perc_consumed"] >= activity_csv["Drug_adaptive_FC_threshold_perc"],]

activity_csv_anti <- read.csv("chembl_activity_input_anti.csv")
activity_csv_anti[activity_csv_anti["perc_consumed"] < activity_csv_anti["Drug_adaptive_FC_threshold_perc"],]
activity_csv_anti <- rbind(activity_csv_anti, wrong_activity_data)


#assay tsv
assay_tsv
assay_tsv<- data.frame(assay_tsv)
#combine strain and species
assay_tsv$whole_organism <- paste(assay_tsv[,"ASSAY_ORGANISM"], assay_tsv[,"ASSAY_STRAIN"], sep = " ")
assay_tsv$whole_organism
#read the input from Mapping_DrugBug_identify_biodegradation.r

# add space between species name and strain instead of _
activity_csv[,"Strain"]<- str_replace_all(activity_csv[,"Strain"],"_", " ")
activity_csv[,"Strain"]
#### fix typos ####

# Create two example lists, to check typos
list1 <- unique(assay_tsv$whole_organism)
list2 <- unique(activity_csv$Strain)

# Find elements that are in list1 but not in list2
non_matching_elements1 <- list1[!(list1 %in% list2)]
non_matching_elements1
# Find elements that are in list2 but not in list1
non_matching_elements2 <- list2[!(list2 %in% list1)]
non_matching_elements2

activity_csv$Strain[activity_csv$Strain == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703" 
activity_csv$Strain[activity_csv$Strain == "Bifidobacterium ruminatum "] = "Bifidobacterium ruminantium fecal isolate"
activity_csv$Strain[activity_csv$Strain == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520"
activity_csv$Strain[activity_csv$Strain == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343"
activity_csv$Strain[activity_csv$Strain == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)" 
activity_csv$Strain[activity_csv$Strain == "Bacteroides fragilis TB9"] = "Bacteroides fragilis T(B)9"
activity_csv$Strain[activity_csv$Strain == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2"
activity_csv$Strain[activity_csv$Strain == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"
activity_csv$Strain[activity_csv$Strain == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"
activity_csv$Strain[activity_csv$Strain == "Anaerostipes sp. "] = "Anaerostipes sp. fecal isolate"
activity_csv$Strain[activity_csv$Strain == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"     
activity_csv$Strain[activity_csv$Strain == "Clostridium sp."] = "Clostridium sp. fecal isolate"            
activity_csv$Strain[activity_csv$Strain == "Lactobacillus reuteri CF48-3A BEI HM-102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102" 
activity_csv$Strain[activity_csv$Strain == "Escherichia coli K-12"] = "Escherichia coli BW25113"   # confirm             
activity_csv$Strain[activity_csv$Strain == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2"                
activity_csv$Strain[activity_csv$Strain == "Akkermansia muciniphila ATCCBAA-835"] = "Akkermansia muciniphila ATCC BAA-835" 


comp_rec_tbl <- data.frame(comp_rec_tbl)

activity_csv$CIDX <- comp_rec_tbl$CIDX[match(activity_csv$DrugName, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
activity_csv$AIDX <- assay_tsv$AIDX[match(activity_csv$Strain, assay_tsv$whole_organism, nomatch = 0)]
#activity_csv$AIDX <- unlist(activity_csv$AIDX)
activity_csv$CRIDX <- rep(unique(RIDX), nrow(activity_csv))
activity_csv$TYPE <- rep("Biotransformation", nrow(activity_csv))
activity_csv$TEXT_VALUE <- rep("Compound metabolized", nrow(activity_csv))
activity_csv$ACTION_TYPE <- rep("SUBSTRATE", nrow(activity_csv))
activity_csv$ACTIVITY_COMMENT <- paste(rep("The percentage of consumption of the drug", nrow(activity_csv)),
                                       activity_csv$DrugName,
                                       rep("i.e.", nrow(activity_csv)),
                                       activity_csv$perc_consumed,
                                       rep("% is higher than the Drug adaptive FC Threshold", nrow(activity_csv)),
                                       paste(activity_csv$Drug_adaptive_FC_threshold_perc, "%.", sep = ""),
                                       rep("Significant biotransformation is detected.", nrow(activity_csv)))



### data unfiltered (compound not metabolized)
#read the input from Mapping_DrugBug_identify_biodegradation.r

# add space between species name and strain instead of _
activity_csv_anti[,"Strain"]<- str_replace_all(activity_csv_anti[,"Strain"],"_", " ")
activity_csv_anti[,"Strain"]
#### fix typos ####
assay_tsv <- data.frame(assay_tsv)
# Create two example lists, to check typos
list1 <- unique(assay_tsv$whole_organism)
list2 <- unique(activity_csv_anti$Strain)

# Find elements that are in list1 but not in list2
non_matching_elements1 <- list1[!(list1 %in% list2)]
non_matching_elements1
# Find elements that are in list2 but not in list1
non_matching_elements2 <- list2[!(list2 %in% list1)]
non_matching_elements2

activity_csv_anti$Strain[activity_csv_anti$Strain == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703" 
activity_csv_anti$Strain[activity_csv_anti$Strain == "Bifidobacterium ruminatum "] = "Bifidobacterium ruminantium fecal isolate"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)" 
activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides fragilis TB9"] = "Bacteroides fragilis T(B)9"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Anaerostipes sp. "] = "Anaerostipes sp. fecal isolate"
activity_csv_anti$Strain[activity_csv_anti$Strain == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"     
activity_csv_anti$Strain[activity_csv_anti$Strain == "Clostridium sp."] = "Clostridium sp. fecal isolate"            
activity_csv_anti$Strain[activity_csv_anti$Strain == "Lactobacillus reuteri CF48-3A BEI HM-102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102" 
activity_csv_anti$Strain[activity_csv_anti$Strain == "Escherichia coli K-12"] = "Escherichia coli BW25113"   # confirm             
activity_csv_anti$Strain[activity_csv_anti$Strain == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2"                
activity_csv_anti$Strain[activity_csv_anti$Strain == "Akkermansia muciniphila ATCCBAA-835"] = "Akkermansia muciniphila ATCC BAA-835"


comp_rec_tbl <- data.frame(comp_rec_tbl)
assay_tsv <- data.frame(assay_tsv)

activity_csv_anti$CIDX <- comp_rec_tbl$CIDX[match(activity_csv_anti$DrugName, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
activity_csv_anti$AIDX <- assay_tsv$AIDX[match(activity_csv_anti$Strain, assay_tsv$whole_organism, nomatch = 0)]
activity_csv_anti$AIDX <- unlist(activity_csv_anti$AIDX)
activity_csv_anti$CRIDX <- rep(unique(RIDX), nrow(activity_csv_anti))
activity_csv_anti$TYPE <- rep("Biotransformation", nrow(activity_csv_anti))
activity_csv_anti$TEXT_VALUE <- rep("Compound NOT metabolized", nrow(activity_csv_anti))
activity_csv_anti$ACTION_TYPE <- rep("", nrow(activity_csv_anti))
activity_csv_anti$ACTIVITY_COMMENT <- paste(rep("The percentage of consumption of the drug", nrow(activity_csv_anti)),
                                       activity_csv_anti$DrugName,
                                       rep("i.e.", nrow(activity_csv_anti)),
                                       activity_csv_anti$perc_consumed,
                                       rep("% is lower than the Drug adaptive FC Threshold", nrow(activity_csv_anti)),
                                       paste(activity_csv_anti$Drug_adaptive_FC_threshold_perc, "%.", sep = ""),
                                       rep("No significant biotransformation is detected.", nrow(activity_csv_anti)))

colnames(activity_csv)
colnames(activity_csv_anti)
merged_activity_1A <- rbind(activity_csv, activity_csv_anti)

names(merged_activity_1A)

keeps <- c("CIDX", "CRIDX", "AIDX", "TYPE","TEXT_VALUE", "ACTIVITY_COMMENT", "ACTION_TYPE")

merged_activity_1Afinal<- merged_activity_1A[keeps]

write.table(merged_activity_1Afinal, file='ACTIVITY_met.tsv', sep='\t', row.names=FALSE)



##### Drug transformed metabolites with good filter #####
met_activity_tsv<- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/supp_sheet5_2.csv", sep = ";")

Goodfiltered_index <- met_activity_tsv %>%
  select(Index, ParentDrug, MZ, LeadingMZ,DrugMassDeltaSmoothed, GoodFilter, DrugMassFlag, DrugConsumedFlag, NumberOfDrugs, NumberOfIncreasedT12vsT0) %>%
  filter(DrugMassFlag == 0 & DrugConsumedFlag == 1 &
           NumberOfDrugs == 1 & GoodFilter == 1 & NumberOfIncreasedT12vsT0 >= 1)
print(nrow(Goodfiltered_index)) # this number should be 871
Goodfiltered_index

##### choose drug_bug_connection #####

# now let's use it in the context of Suppl_table_3 from the Mapping Paper
my_table = read.csv("supp_sheet6.csv",
                      sep = ';',
                      skip = 1
                      # , header = T
)


# keep only columns that have pFDR, remove the rest
selected_columns_fdr <- my_table[grep("p.FDR..t.12h.vs.t.0h.", names(my_table))]
colnames(selected_columns_fdr) <- gsub("p.FDR..t.12h.vs.t.0h.", "", colnames(selected_columns_fdr))
my_species <- colnames(selected_columns_fdr)
my_species
keep2 <- c("Index", "ParentDrug", "MZ", "RT", "MZdelta")
selected_columns_usual <- my_table[keep2]

drug_met <- cbind(selected_columns_usual, selected_columns_fdr)

selected_drug_met <- drug_met[drug_met$Index %in% Goodfiltered_index$Index, ]
names(selected_drug_met)


# Create the list that will contain results
dataframes_list <- list()

for(i in 1:length(my_species)){
  print(my_species[i])
  col_to_keep <- c("ParentDrug","MZ", "RT", "MZdelta", my_species[i])
  my_table_i <- selected_drug_met[col_to_keep]
  filtered_table <- my_table_i[as.character(my_table_i[[my_species[i]]]) != "NaN", , drop = FALSE]
  #filtered_table[as.character(my_species[i])][[1]] <- str_replace(filtered_table[as.character(my_species[i])][[1]], ",", ".")
  filtered_table$Species <- as.character(my_species[i])
  colnames(filtered_table)[5] <- "Values"
  final_filt_df <- filtered_table[filtered_table$Values <=0.05, ]
  dataframes_list[[i]] <- final_filt_df 
}


combined_dataframe <- do.call(rbind, dataframes_list)
combined_dataframe$Species<- gsub("\\.", " ", combined_dataframe$Species)

combined_dataframe <- subset(combined_dataframe, !grepl("Control pH ", Species))
combined_dataframe
# Create two example lists, to check typos
list1 <- unique(assay_tsv$whole_organism)
list2 <- unique(combined_dataframe$Species)

# Find elements that are in list1 but not in list2
non_matching_elements1 <- list1[!(list1 %in% list2)]
non_matching_elements1
# Find elements that are in list2 but not in list1
non_matching_elements2 <- list2[!(list2 %in% list1)]
non_matching_elements2

combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis DS 208"] = "Bacteroides fragilis DS-208"
combined_dataframe$Species[combined_dataframe$Species == "Victivallis vadensis ATCC BAA 548"] = "Victivallis vadensis ATCC BAA-548"
combined_dataframe$Species[combined_dataframe$Species == "Bacteroides thetaiotaomicron VPI 5482"] = "Bacteroides thetaiotaomicron VPI-5482"
combined_dataframe$Species[combined_dataframe$Species == "Odoribacter splanchnius"] = "Odoribacter splanchnicus fecal isolate"
combined_dataframe$Species[combined_dataframe$Species == "Roseburia intestinalis L1 82"] = "Roseburia intestinalis L1-82"
combined_dataframe$Species[combined_dataframe$Species == "Lactobacillus  reuteri CF48 3A BEI HM 102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102"
combined_dataframe$Species[combined_dataframe$Species == "Bifidobacterium longum subsp  infantis CCUG52486"] = "Bifidobacterium longum subsp. Infantis CCUG52486"
combined_dataframe$Species[combined_dataframe$Species == "Clostridium bolteae ATCCBAA 613"] = "Clostridium bolteae ATCCBAA-613"
combined_dataframe$Species[combined_dataframe$Species == "Bifidobacterium ruminatum"] = "Bifidobacterium ruminantium fecal isolate"
combined_dataframe$Species[combined_dataframe$Species == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520"
combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343"
combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)" 
combined_dataframe$Species[combined_dataframe$Species == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703" 
combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis T B 9"] = "Bacteroides fragilis T(B)9"
combined_dataframe$Species[combined_dataframe$Species == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2"
combined_dataframe$Species[combined_dataframe$Species == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"
combined_dataframe$Species[combined_dataframe$Species == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"
combined_dataframe$Species[combined_dataframe$Species == "Anaerostipes sp "] = "Anaerostipes sp. fecal isolate"
combined_dataframe$Species[combined_dataframe$Species == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"     
combined_dataframe$Species[combined_dataframe$Species == "Clostridium sp "] = "Clostridium sp. fecal isolate"            
combined_dataframe$Species[combined_dataframe$Species == "Lactobacillus reuteri CF48 3A BEI HM 102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102" 
combined_dataframe$Species[combined_dataframe$Species == "Escherichia coli  K 12"] = "Escherichia coli BW25113"   # confirm             
combined_dataframe$Species[combined_dataframe$Species == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2"                
combined_dataframe$Species[combined_dataframe$Species == "Akkermansia muciniphila ATCCBAA 835"] = "Akkermansia muciniphila ATCC BAA-835"


length(unique(combined_dataframe$ParentDrug))
length(unique(comp_rec_tbl$COMPOUND_KEY))

# Create two example lists, to check typos
list1 <- unique(comp_rec_tbl$COMPOUND_KEY)
list2 <- unique(combined_dataframe$ParentDrug)

# Find elements that are in list1 but not in list2
non_matching_elements1 <- list1[!(list1 %in% list2)]
non_matching_elements1
# Find elements that are in list2 but not in list1
non_matching_elements2 <- list2[!(list2 %in% list1)]
non_matching_elements2

comp_rec_tbl$COMPOUND_KEY[comp_rec_tbl$COMPOUND_KEY == "LOFEXIDINE "] = "LOFEXIDINE"







nonselected_drug_met <- drug_met[!drug_met$Index %in% Goodfiltered_index$Index, ]
names(nonselected_drug_met)


# Create the list that will contain results
dataframes_list2 <- list()

for(i in 1:length(my_species)){
  print(my_species[i])
  col_to_keep <- c("ParentDrug","MZ", "RT", "MZdelta", my_species[i])
  my_table_i <- nonselected_drug_met[col_to_keep]
  filtered_table <- my_table_i[as.character(my_table_i[[my_species[i]]]) != "NaN", , drop = FALSE]
  #filtered_table[as.character(my_species[i])][[1]] <- str_replace(filtered_table[as.character(my_species[i])][[1]], ",", ".")
  filtered_table$Species <- as.character(my_species[i])
  colnames(filtered_table)[5] <- "Values"
  final_filt_df <- filtered_table[filtered_table$Values <=0.05, ]
  dataframes_list2[[i]] <- final_filt_df 
}


combined_dataframe2 <- do.call(rbind, dataframes_list2)
combined_dataframe2$Species<- gsub("\\.", " ", combined_dataframe2$Species)

combined_dataframe2 <- subset(combined_dataframe2, !grepl("Control pH ", Species))
combined_dataframe2
# Create two example lists, to check typos
list1 <- unique(assay_tsv$whole_organism)
list2 <- unique(combined_dataframe2$Species)

# Find elements that are in list1 but not in list2
non_matching_elements1 <- list1[!(list1 %in% list2)]
sort(non_matching_elements1)
# Find elements that are in list2 but not in list1
non_matching_elements2 <- list2[!(list2 %in% list1)]
sort(non_matching_elements2)


combined_dataframe2$Species[combined_dataframe2$Species == "Victivallis vadensis ATCC BAA 548"] = "Victivallis vadensis ATCC BAA-548"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Akkermansia muciniphila ATCCBAA 835"] = "Akkermansia muciniphila ATCC BAA-835"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520" #C
combined_dataframe2$Species[combined_dataframe2$Species == "Anaerostipes sp "] = "Anaerostipes sp. fecal isolate"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)" #C
combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis DS 208"] = "Bacteroides fragilis DS-208"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343" #C
combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis T B 9"] = "Bacteroides fragilis T(B)9"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides thetaiotaomicron VPI 5482"] = "Bacteroides thetaiotaomicron VPI-5482"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2" #C
combined_dataframe2$Species[combined_dataframe2$Species == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703"#C 
combined_dataframe2$Species[combined_dataframe2$Species == "Bifidobacterium longum subsp  infantis CCUG52486"] = "Bifidobacterium longum subsp. Infantis CCUG52486"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Bifidobacterium ruminatum"] = "Bifidobacterium ruminantium fecal isolate"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"   #C  
combined_dataframe2$Species[combined_dataframe2$Species == "Clostridium bolteae ATCCBAA 613"] = "Clostridium bolteae ATCCBAA-613"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Clostridium sp "] = "Clostridium sp. fecal isolate"            #C#C
combined_dataframe2$Species[combined_dataframe2$Species == "Escherichia coli  K 12"] = "Escherichia coli BW25113"   ##C   
combined_dataframe2$Species[combined_dataframe2$Species == "Lactobacillus reuteri CF48 3A BEI HM 102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102" #C
combined_dataframe2$Species[combined_dataframe2$Species == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Roseburia intestinalis L1 82"] = "Roseburia intestinalis L1-82"#C
combined_dataframe2$Species[combined_dataframe2$Species == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2" #C    

length(unique(combined_dataframe2$ParentDrug))
length(unique(comp_rec_tbl$COMPOUND_KEY))

# Create two example lists, to check typos
list1 <- unique(comp_rec_tbl$COMPOUND_KEY)
list2 <- unique(combined_dataframe2$ParentDrug)

# Find elements that are in list1 but not in list2
non_matching_elements1 <- list1[!(list1 %in% list2)]
non_matching_elements1
# Find elements that are in list2 but not in list1
non_matching_elements2 <- list2[!(list2 %in% list1)]
non_matching_elements2



colnames(combined_dataframe)
colnames(combined_dataframe2)
nrow(combined_dataframe)
merged_activity_1A


# to remove biotransformation true entries and replace them with putative metabolite
# Use dplyr to join and filter duplicates
library("dplyr")
result <- combined_dataframe %>%
  left_join(comp_rec_tbl, by = c("ParentDrug" = "COMPOUND_KEY")) %>%
  group_by(ParentDrug) %>%
  mutate(CIDX = first(CIDX, order_by = ParentDrug)) %>%
  ungroup()
result
result["GoodFilter"] <- 1
result2 <- combined_dataframe2 %>%
  left_join(comp_rec_tbl, by = c("ParentDrug" = "COMPOUND_KEY")) %>%
  group_by(ParentDrug) %>%
  mutate(CIDX = first(CIDX, order_by = ParentDrug)) %>%
  ungroup()
result2["GoodFilter"] <- 0
comb_result <- rbind(result, result2)
comb_result <- data.frame(comb_result)
comb_result["combined_col"] <- paste(comb_result$ParentDrug, comb_result$Species, sep ="_")
merged_activity_1A["combined_col"] <- paste(merged_activity_1A$DrugName, merged_activity_1A$Strain, sep = "_")
merged_activity_1A["GoodFilter"] <- ""
check_mets <- anti_join(merged_activity_1A, comb_result, by = "combined_col")

assay_tsv$AIDX<- unlist(assay_tsv$AIDX)
#comb_result$AIDX <- assay_tsv$AIDX[match(comb_result$Species, assay_tsv$whole_organism, nomatch = 0)]
comb_result$AIDX <- assay_tsv$AIDX[match(comb_result$Species, assay_tsv$whole_organism, nomatch = NA)]

result <- data.frame(result)
result$combined_col <- paste(result$CIDX, result$AIDX, sep = "")
merged_activity_1Afinal$combined_col <- paste(merged_activity_1Afinal$CIDX, merged_activity_1Afinal$AIDX, sep = "")

filtered_df_wo <- anti_join(merged_activity_1Afinal, result, by = "combined_col")

result$CRIDX <- rep(unique(RIDX), nrow(result))
result$TYPE <- rep("Biotransformation", nrow(result))
result$TEXT_VALUE <- rep("Compound metabolized", nrow(result))
result$ACTION_TYPE <- "SUBSTRATE"
#result$MZdelta <- str_replace(result$MZdelta, ",", ".")
#result$MZ <- str_replace(result$MZ, ",", ".")
#result$RT <- str_replace(result$RT, ",", ".")

result$ACTIVITY_COMMENT <- paste(rep("Putative metabolite identification: The drug ", nrow(result)),
                                 result$ParentDrug,
                                 rep("is biotransformed by", nrow(result)),
                                 result$Species,
                                 rep("and a corresponding drug metabolite with m/z", nrow(result)),
                                 result$MZ,
                                 rep("at retention time", nrow(result)),
                                 result$RT,
                                 rep("minutes is detected.", nrow(result)))
  
  
  
  

col_keep_result <- c("CIDX", "CRIDX", "AIDX", "TYPE", "TEXT_VALUE", "ACTIVITY_COMMENT", "ACTION_TYPE") 
filtered_df_wo <- filtered_df_wo[col_keep_result]
result <- result[col_keep_result]
combined_met_bio <- rbind(result, filtered_df_wo)
nrow(result)+ nrow(filtered_df_wo)

write.table(combined_met_bio, file='ASSAY_typeA_bioANDmet.tsv', sep='\t', row.names=FALSE)

########

gene <- gene_data$Gene
gene
drugs_for_genes <- c("Artemisinin",
              "Bisacodyl",
              "Danazol",
              "Deflazacort",
              "Diacetamate",
              "Diflorasone.Diacetate",
              "Diltiazem",
              "Drospirenone",
              "Entacapone",
              "Famciclovir",
              "Levonorgestrel",
              "Nitrendipine",
              "Norethindrone.acetate",
              "Pantoprazole",
              "Pericyazine",
              "Phenazopyridine",
              "Racecadotril",
              "Roxatidine.acetate",
              "Sulfasalazine",
              "Tinidazole")

dataframes_list <- list()
colnames(gene_data)


for (i in 1:length(gene)){
  gene_transposed <- data.frame(t(gene_data[gene_data$Gene == gene[i],]))
  colnames(gene_transposed)[1] <- "Value"
  gene_transposed$drugs <- rownames(gene_transposed)
  gene_transposed$genes <- gene[i]
  gene_transposed <- gene_transposed[4:82, ]
  rownames(gene_transposed)<-NULL
  gene_transposed %>% relocate(genes, drugs)
  # Sample list of drug names
  drug_names <- list(gene_transposed$drugs)
  # Empty list to store dataframes
  single_drugs <- c()
  metabolite_mass <- c()
  # Loop through drug names, extract drug names and numbers, and create dataframes
  for (name in drug_names) {
    drug_name <- gsub("(_\\d+\\.\\d+)?", "", name)  # Extract drug name
    single_drugs <- c(single_drugs, drug_name)
    extracted_number <- as.numeric(gsub(".*_(\\d+\\.\\d+)", "\\1", name))  # Extract number or NA if not present
    metabolite_mass <- c(metabolite_mass, extracted_number)
  }
  gene_transposed$single_drugs <- single_drugs
  gene_transposed$metabolite_mass <- metabolite_mass
  gene_transposed[67, "single_drugs"] <- "Pericyazine"
  gene_transposed[68, "single_drugs"] <- "Pericyazine"
  gene_transposed[67, "metabolite_mass"] <- "407.166"
  gene_transposed[68, "metabolite_mass"] <- "421.182"

  dataframes_list[[i]] <- gene_transposed 
}

combined_dataframe_genes <- do.call(rbind, dataframes_list)

combined_dataframe_genes$single_drugs <- gsub("\\.", " ", toupper(combined_dataframe_genes$single_drugs))
combined_dataframe_genes <- combined_dataframe_genes %>% relocate(genes, drugs, single_drugs, metabolite_mass, Value)

combined_dataframe_genes_ones <- combined_dataframe_genes[combined_dataframe_genes$Value == "1", ] 

combined_dataframe_genes_ones_without_mets <- combined_dataframe_genes_ones[is.na(combined_dataframe_genes_ones["metabolite_mass"]), ] # use this for true analysis
combined_dataframe_genes_ones_mets <- combined_dataframe_genes_ones[!is.na(combined_dataframe_genes_ones["metabolite_mass"]), ] # use this for metabolites


combined_dataframe_genes_ones$combined <- paste(combined_dataframe_genes_ones$genes, combined_dataframe_genes_ones$single_drugs, sep = "_")

combined_dataframe_genes_ones_without_mets$combined <- paste(combined_dataframe_genes_ones_without_mets$genes, combined_dataframe_genes_ones_without_mets$single_drugs, sep = "_")

combined_dataframe_genes_zeroes <- combined_dataframe_genes[combined_dataframe_genes$Value == "0", ]

combined_dataframe_genes_zeroes_without_mets <- combined_dataframe_genes_zeroes[is.na(combined_dataframe_genes_zeroes["metabolite_mass"]), ] # use this for false analysis

assay_tsv_prot <- data.frame(assay_tsv_prot)

assay_tsv_prot$Gene <- gene_data$Gene

combined_dataframe_genes_ones_without_mets$CIDX <- comp_rec_tbl$CIDX[match(combined_dataframe_genes_ones_without_mets$single_drugs, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
combined_dataframe_genes_ones_without_mets$AIDX <- assay_tsv_prot$AIDX[match(combined_dataframe_genes_ones_without_mets$genes, assay_tsv_prot$Gene, nomatch = 0)]
combined_dataframe_genes_ones_without_mets$CRIDX <- rep(unique(RIDX), nrow(combined_dataframe_genes_ones_without_mets))
combined_dataframe_genes_ones_without_mets$TYPE <- rep("Biotransformation", nrow(combined_dataframe_genes_ones_without_mets))
combined_dataframe_genes_ones_without_mets$TEXT_VALUE <- rep("Compound metabolized", nrow(combined_dataframe_genes_ones_without_mets))
combined_dataframe_genes_ones_without_mets$ACTION_TYPE <- rep("SUBSTRATE", nrow(combined_dataframe_genes_ones_without_mets))
combined_dataframe_genes_ones_without_mets$ACTIVITY_COMMENT <- paste(rep("The oberved biotransformation of drug", nrow(combined_dataframe_genes_ones_without_mets)), 
                                                                     combined_dataframe_genes_ones_without_mets$single_drugs,
                                                                     rep("was proven to be mediated by", nrow(combined_dataframe_genes_ones_without_mets)),
                                                                     paste(combined_dataframe_genes_ones_without_mets$genes, rep(".", nrow(combined_dataframe_genes_ones_without_mets)), sep = ""))



combined_dataframe_genes_ones_mets$CIDX <- comp_rec_tbl$CIDX[match(combined_dataframe_genes_ones_mets$single_drugs, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
combined_dataframe_genes_ones_mets$AIDX <- assay_tsv_prot$AIDX[match(combined_dataframe_genes_ones_mets$genes, assay_tsv_prot$Gene, nomatch = 0)]
combined_dataframe_genes_ones_mets$CRIDX <- rep(unique(RIDX), nrow(combined_dataframe_genes_ones_mets))
combined_dataframe_genes_ones_mets$TYPE <- rep("Biotransformation", nrow(combined_dataframe_genes_ones_mets))
combined_dataframe_genes_ones_mets$TEXT_VALUE <- rep("Compound metabolized", nrow(combined_dataframe_genes_ones_mets))
combined_dataframe_genes_ones_mets$ACTION_TYPE <- rep("SUBSTRATE", nrow(combined_dataframe_genes_ones_mets))
combined_dataframe_genes_ones_mets$ACTIVITY_COMMENT <- paste(rep("Putative metabolite identification: The observed biotransformation of drug", nrow(combined_dataframe_genes_ones_mets)), 
                                                            combined_dataframe_genes_ones_mets$single_drugs,
                                                            rep("into metabolite with m/z", nrow(combined_dataframe_genes_ones_mets)),
                                                            combined_dataframe_genes_ones_mets$metabolite_mass,
                                                            rep("was proven to be mediated by", nrow(combined_dataframe_genes_ones_mets)),
                                                            paste(combined_dataframe_genes_ones_mets$genes, rep(".", nrow(combined_dataframe_genes_ones_mets)), sep = ""))

filtered_df1 <- subset(combined_dataframe_genes_ones_without_mets, !(combined %in% combined_dataframe_genes_ones_mets$combined))

combined_dataframe_genes_zeroes_without_mets$CIDX <- comp_rec_tbl$CIDX[match(combined_dataframe_genes_zeroes_without_mets$single_drugs, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
combined_dataframe_genes_zeroes_without_mets$AIDX <- assay_tsv_prot$AIDX[match(combined_dataframe_genes_zeroes_without_mets$genes, assay_tsv_prot$Gene, nomatch = 0)]
combined_dataframe_genes_zeroes_without_mets$CRIDX <- rep(unique(RIDX), nrow(combined_dataframe_genes_zeroes_without_mets))
combined_dataframe_genes_zeroes_without_mets$TYPE <- rep("Biotransformation", nrow(combined_dataframe_genes_zeroes_without_mets))
combined_dataframe_genes_zeroes_without_mets$TEXT_VALUE <- rep("Compound NOT metabolized", nrow(combined_dataframe_genes_zeroes_without_mets))
combined_dataframe_genes_zeroes_without_mets$ACTION_TYPE <- rep("", nrow(combined_dataframe_genes_zeroes_without_mets))
combined_dataframe_genes_zeroes_without_mets$ACTIVITY_COMMENT <- paste(rep("The biotransformation of drug", nrow(combined_dataframe_genes_zeroes_without_mets)), 
                                                                       combined_dataframe_genes_zeroes_without_mets$single_drugs,
                                                                       rep("could not be mediated by", nrow(combined_dataframe_genes_zeroes_without_mets)),
                                                                       paste(combined_dataframe_genes_zeroes_without_mets$genes, rep(".", nrow(combined_dataframe_genes_zeroes_without_mets)), sep = ""))

keep_cols <- c("CIDX", "CRIDX", "AIDX", "TYPE", "TEXT_VALUE", "ACTIVITY_COMMENT", "ACTION_TYPE")

filtered_df1_final <- filtered_df1[keep_cols]
combined_dataframe_genes_ones_mets_final <- combined_dataframe_genes_ones_mets[keep_cols]
colnames(combined_dataframe_genes_zeroes_without_mets)
combined_dataframe_genes_zeroes_without_mets_final <- combined_dataframe_genes_zeroes_without_mets[keep_cols]
final_prot_act <- rbind(rbind(filtered_df1_final, combined_dataframe_genes_ones_mets_final), combined_dataframe_genes_zeroes_without_mets_final)


write.table(final_prot_act, file='ASSAY_typeB_bioGeneANDmet.tsv', sep='\t', row.names=FALSE)




####

community_act <- read.csv("all_samples_metabolized_status_match_Mapping_supp_short.csv")
community_act$slope_rate <- community_act$Slope_Michael_negative*2

community_act$Drug[community_act$Drug == "DILTIAZEM_HYDROCHLORIDE"] = "DILTIAZEM"

community_act_ones <- community_act[community_act $Metabolized==1,]
community_act_zeroes <- community_act[community_act $Metabolized==0,]

community_act_ones$CIDX <- c(rep("HMDM0063", 5), rep("HMDM0092", 27), rep("HMDM0166", 27))
#community_act_ones$CIDX <- comp_rec_tbl$CIDX[match(community_act_ones$Drug, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]

assay_tsv_community <- data.frame(assay_tsv_community)
community_act_ones$AIDX <- assay_tsv_community$AIDX[match(community_act_ones$Sample, assay_tsv_community$COMMUNITY, nomatch = 0)]
community_act_ones$CRIDX <- rep(unique(RIDX), nrow(community_act_ones))
community_act_ones$TYPE <- rep("Biotransformation", nrow(community_act_ones))
community_act_ones$TEXT_VALUE <- rep("Compound metabolized", nrow(community_act_ones))
community_act_ones$ACTION_TYPE <- "SUBSTRATE"
community_act_ones$ACTIVITY_COMMENT <- paste(rep("Biotransformation occured for drug", nrow(community_act_ones)), 
                                             paste(community_act_ones$Drug, ",", sep = ""),
                                             rep("within community,", nrow(community_act_ones)), 
                                             community_act_ones$Sample,
                                             rep("surpassing drug threshold of", nrow(community_act_ones)), 
                                             community_act_ones$Per_drug_thresh,
                                             rep("and decreasing over time with a biotransformation rate of", nrow(community_act_ones)),
                                             community_act_ones$Slope_Michael_negative,
                                             rep("corresponding to", nrow(community_act_ones)),
                                             community_act_ones$slope_rate,
                                             rep("uM/h.", nrow(community_act_ones))
                                             )


colnames(community_act_ones)

community_act_zeroes$CIDX <- c(rep("HMDM0063", 23), rep("HMDM0070", 28), rep("HMDM0092", 1), rep("HMDM0166", 1))


community_act_zeroes$AIDX <- assay_tsv_community$AIDX[match(community_act_zeroes$Sample, assay_tsv_community$COMMUNITY, nomatch = 0)]
community_act_zeroes$CRIDX <- rep(unique(RIDX), nrow(community_act_zeroes))
community_act_zeroes$TYPE <- rep("Biotransformation", nrow(community_act_zeroes))
community_act_zeroes$TEXT_VALUE <- rep("Compound NOT metabolized", nrow(community_act_zeroes))
community_act_zeroes$ACTION_TYPE <- rep("", length=nrow(community_act_zeroes))
community_act_zeroes$ACTIVITY_COMMENT <- paste(rep("No biotransformation occured for drug", nrow(community_act_zeroes)), 
                                               paste(community_act_zeroes$Drug, ",", sep = ""),
                                               rep("within community,", nrow(community_act_zeroes)), 
                                               paste(community_act_zeroes$Sample, rep(".", nrow(community_act_zeroes)), sep = ""))
community_act_ones <- community_act_ones[keep_cols]
community_act_zeroes <- community_act_zeroes[keep_cols]
final_com_act <- rbind(community_act_ones, community_act_zeroes)

write.table(rbind(combined_met_bio, final_prot_act, final_com_act), file='ACTIVITY.tsv', sep='\t', row.names=FALSE)

#write.table(merged_activity_1Afinal, file='ACTIVITY.tsv', sep='\t', row.names=FALSE)



#### find validated metabolites
metabolite_name <- c("Acetyl pericyazine", "Propionyl pericyazine", "Deacetyldiltiazem", "Dexamethasone metabolite")
MZ <- c(407.166, 421.182, 372.151, 332.179)
parent <- c("PERICYAZINE", "PERICYAZINE", "DILTIAZEM", "DEXAMETHASONE")
cidx <- c("HMDM0185", "HMDM0185", "HMDM0070", "HMDM0063")
pericyazine <- 21541
diltiazem <- c(71, 833, 985, 1124, 1265, 1881, 1972, 2145, 2270, 2502, 2657, 2890, 2999, 3149, 3673, 3747, 3850,
         3940, 4049, 4243, 4497, 4851, 5439, 5546, 5639, 5734, 6198, 6272,
         6421, 6510, 6588, 6791, 6833)-1

dexamethasone <- 1577

fin_act_met_val <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ACTIVITY.tsv", sep = "\t")

fin_act_met_val[1578, "ACTIVITY_COMMENT"] <- "Validated metabolite identification: The drug  DEXAMETHASONE is biotransformed by Clostridium scindens ATCC35704 and a corresponding drug metabolite with m/z 332.179 at rerention time 4.033 minutes is detected."
fin_act_met_val[21540, "ACTIVITY_COMMENT"] <- "Validated metabolite identification: The observed biotransformation of drug PERICYAZINE into metabolite with m/z 407.166 corresponding to Acetyl pericyazine, was proven to be mediated by BT_2367."
library("stringr")
fin_act_met_val[diltiazem, "ACTIVITY_COMMENT"] <- str_replace(fin_act_met_val[diltiazem, "ACTIVITY_COMMENT"], "Putative", "Validated")
fin_act_met_val[diltiazem, "ACTIVITY_COMMENT"] <- str_replace(fin_act_met_val[diltiazem, "ACTIVITY_COMMENT"], "drug metabolite with", "drug metabolite Deacetyldiltiazem with")

write.table(fin_act_met_val, "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ACTIVITY.tsv", sep = "\t", row.names=FALSE)









#### Check differences between first and second submission for ASSAY
df1 <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ACTIVITY.tsv", sep = "\t")
df2 <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/HumanMicrobiome_DrugMetabolism_FINAL_SUBMISSION_folder/changed_AIDX_submission2/ACTIVITY.tsv", sep = "\t")
nrow(df1)
nrow(df2)
# Install and load the diffdf package
#install.packages("diffdf")
library(diffdf)

# Assuming df1 and df2 are your dataframes
diff_result <- diffdf(df1, df2)


AIDX_COMPARE <- as.data.frame(diff_result[["VarDiff_AIDX"]])
AIDX_COMPARE
ACTIVITY_COMMENT_COMPARE <- as.data.frame(diff_result[["VarDiff_ACTIVITY_COMMENT"]])
ACTION_TYPE_COMPARE <- as.data.frame(diff_result[["VarDiff_ACTION_TYPE"]])






AIDX_COMPARE <- as.data.frame(diff_result[["VarDiff_AIDX"]])
Assay_str_COMPARE <- as.data.frame(diff_result[["VarDiff_ASSAY_STRAIN"]])
TARGET_NAME_COMPARE <- as.data.frame(diff_result[["VarDiff_TARGET_NAME"]])
TARGET_ACCESSION_COMPARE <- as.data.frame(diff_result[["VarDiff_TARGET_ACCESSION"]])
TARGET_organism_COMPARE <- as.data.frame(diff_result[["VarDiff_TARGET_ORGANISM"]])




#### Check differences between first and second submission for ASSAY_PARAM
df1 <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/HumanMicrobiome_DrugMetabolism_FINAL_SUBMISSION_folder/ASSAY_PARAM.tsv", sep = "\t")
df2 <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/HumanMicrobiome_DrugMetabolism_FINAL_SUBMISSION_folder/changed_AIDX_submission2/ASSAY_PARAM.tsv", sep = "\t")

# Install and load the diffdf package
#install.packages("diffdf")
library(diffdf)

# Assuming df1 and df2 are your dataframes
diff_result <- diffdf(df1, df2)


AIDX_COMPARE <- as.data.frame(diff_result[["VarDiff_AIDX"]])


#### Check differences between first and second submission for ACTIVITY
df1 <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/HumanMicrobiome_DrugMetabolism_FINAL_SUBMISSION_folder/ACTIVITY.tsv", sep = "\t")
df2 <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/HumanMicrobiome_DrugMetabolism_FINAL_SUBMISSION_folder/changed_AIDX_submission2/ACTIVITY.tsv", sep = "\t")

library(diffdf)

# Assuming df1 and df2 are your dataframes
diff_result <- diffdf(df1, df2)

AIDX_COMPARE <- as.data.frame(diff_result[["VarDiff_AIDX"]])
ACTIVITY_COMMENT_COMPARE <- as.data.frame(diff_result[["VarDiff_ACTIVITY_COMMENT"]])
ACTION_TYPE_COMPARE <- as.data.frame(diff_result[["VarDiff_ACTION_TYPE"]])
AIDX_COMPARE



activity_ch <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/HumanMicrobiome_DrugMetabolism_FINAL_SUBMISSION_folder/changed_AIDX_submission2/ACTIVITY.tsv", sep = "\t")
colnames(activity_ch)
nrow(activity_ch[activity_ch["TEXT_VALUE"] == "Compound metabolized", ])
nrow(activity_ch[activity_ch["TEXT_VALUE"] == "Compound NOT metabolized", ])
nrow(activity_ch)
