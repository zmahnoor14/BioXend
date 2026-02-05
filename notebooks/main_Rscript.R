#### go to python notebook to generate COMPOUND_RECORD.tsv and COMPOUND_CTAB.sdf ####

#install.packages(c("dplyr", "stringr", "tidyverse"))
library("stringr")
library("dplyr")
library("tidyverse")
source("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/R/write_reference_tsv.R")
source("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/R/write_assay_tsv.R")
source("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/R/write_activity_tsv.R")
#### REFERENCE.tsv ####

# function to generate reference.tsv

#arguments for reference
RIDX <- c("HumanMicrobiome_DrugMetabolism")
DOI <- c("10.1038/s41586-019-1291-3")
JOURNAL_NAME <- c("Nature")
YEAR <- c("2019")
VOLUME <- c("570")
ISSUE <- c("7762")
FIRST_PAGE <- c("462")
LAST_PAGE<- c("467")
REF_TYPE <- c("Publication")
TITLE <- c("Mapping human microbiome drug metabolism by gut bacteria and their genes") #mandatory
AUTHORS	<- c("Michael Zimmermann, Maria Zimmermann-Kogadeeva, Rebekka Wegmann & Andrew L. Goodman") #mandatory
ABSTRACT <- c("Individuals vary widely in their responses to medicinal drugs, which can be dangerous and expensive owing to treatment delays and adverse effects. Although increasing evidence implicates the gut microbiome in this variability, the molecular mechanisms involved remain largely unknown. Here we show, by measuring the ability of 76 human gut bacteria from diverse clades to metabolize 271 orally administered drugs, that many drugs are chemically modified by microorganisms. We combined high-throughput genetic analyses with mass spectrometry to systematically identify microbial gene products that metabolize drugs. These microbiome-encoded enzymes can directly and substantially affect intestinal and systemic drug metabolism in mice, and can explain the drug-metabolizing activities of human gut bacteria and communities on the basis of their genomic contents. These causal links between the gene content and metabolic activities of the microbiota connect interpersonal variability in microbiomes to interpersonal differences in drug metabolism, which has implications for medical therapy and drug development across multiple disease indications.")
output_dir <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/outputs"

ref_tbl <- write_reference_tsv(output_dir, RIDX, DOI, TITLE, AUTHORS, ABSTRACT, REF_TYPE, YEAR,
                               JOURNAL_NAME, VOLUME, ISSUE, FIRST_PAGE, LAST_PAGE)

ref_tbl


#### ASSAY.tsv ####

# ## table from 1st category
# species_data <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/supp_sheet1.csv")
# nrow(species_data)
# tax_ids <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/Retrieved_taxid_for_single_species.csv")
# nrow(tax_ids)
# colnames(tax_ids) <- c("X", "Name", "taxid", "Current_name")
# #
# taxid <- NA
# for (j in 1:nrow(species_data)){
#   for (i in 1:nrow(tax_ids)){
#     if (as.character(species_data[j, "Name"]) == tax_ids[i, "Name"]){
#       taxid <- c(taxid, tax_ids[i, "taxid"])
#     }
#   }
# }
# species_data$taxid <- taxid
# species_data[1, "taxid"] <- 1680
# species_data.df <- species_data
# species_data.df <- species_data.df[c("Name", "Reference", "taxid")]
# colnames(species_data.df) <- c("Species", "Strain", "organismTAXID")
# species_data.df["assay_description"] <- paste(rep("The drug is tested on", nrow(species_data.df)),
#                                              species_data.df$Species,
#                                               rep("strain:", nrow(species_data.df)),
#                                               species_data.df$Strain,
#                                               rep("for biotransformation. The drug concentrations were measured before and after a 12-h incubation by liquid-chromatography-coupled mass spectrometry (LC–MS)", nrow(species_data.df)), sep = " ")
# species_data.df["target_name"] <- NA
# species_data.df["target_accession"] <- NA
# species_data.df["Specimen"] <- NA
# #
# # ## table from 2nd category
# #
# gene_data <- data.frame(matrix(ncol = 7, nrow = 0))
# colnames(gene_data) <- c("Species", "Strain", "organismTAXID", "assay_description", "target_name", "target_accession", "Specimen")
# gene_data[1:17, "Species"] <- "Bacteroides thetaiotaomicron"
# gene_data[18:22, "Species"] <- "Collinsella aerofaciens"
# gene_data[23:30, "Species"] <- "Bacteroides dorei"
# gene_data[1:17, "Strain"] <- "VPI-5482"
# gene_data[18:22, "Strain"] <- "ATCC25986"
# gene_data[23:30, "Strain"] <- "DSM17855"
# gene_data[1:17, "organismTAXID"] <- "818"
# gene_data[18:22, "organismTAXID"] <- "74426"
# gene_data[23:30, "organismTAXID"] <- "357276"
# gene_data$target_name <- c("acetyl esterase (acetylxylosidase)",
#                   "NADH oxidase",
#                   "endoglucanase E precursor (EGE)",
#                   "Lysophospholipase L1 and related esterases",
#                  "Putative nitroreductase",
#                   "Nitroreductase",
#                   "putative xylanase",
#                  "putative general stress protein",
#                  "3-oxo-5-alpha-steroid 4-dehydrogenase",
#                  "cAMP-binding proteins - catabolite gene activator and regulatory subunit of cAMP-dependent protein kinases",
#                   "Acyltransferase",
#                  "hypothetical protein",
#                   "Hydrolase, HAD superfamily",
#                   "putative sialic acid-specific acetylesterase",
#                   "hypothetical protein",
#                  "sialic acid-specific 9-O-acetylesterase",
#                   "hypothetical protein",
#                   "hypothetical protein",
#                   "Lj928 prophage protein",
#                   "hypothetical protein",
#                   "hypothetical protein",
#                   "hypothetical protein",
#                   "Oxygen-insensitive NADPH nitroreductase (EC 1.-.-.-)",
#                  "sialate O-acetylesterase",
#                   "3-oxo-5-alpha-steroid 4-dehydrogenase",
#                  "Lipase/acylhydrolase domain protein",
#                  "hypothetical protein",
#                  "Acyltransferase",
#                   "Acetyl esterase",
#                  "NADPH nitroreductase")
# gene_data$target_accession <- c("Q8ABF8", "Q8AB93", "Q8AAL9", "Q8AA96",
#                                 "Q8A911", "Q8A8L9", "Q8A8H5", "Q8A7U5",
#                                 "Q8A618", "Q8A576", "Q8A575", "Q8A3J3",
#                                 "Q8A343", "Q8A331", "Q8A0E6", "Q8A0D0",
#                                 "Q8A0C5", "A4E7D0", "A4E8S4", "A4EB91",
#                                 "A4EBM5", "A4ED08", "B6VU18", "B6VTE7",
#                                 "B6W0N3", "B6W1J1", "B6W293", "B6W2J3",
#                                 "B6W2J6", "B6W3P3")
#
# gene_data$assay_description <- paste(rep("The drug is tested on", nrow(gene_data)),
#                                      gene_data$Species,
#                                      rep("strain:", nrow(gene_data)),
#                                      gene_data$Strain,
#                                      rep("for biotransformation. The drug concentrations were measured before and after a 12-h incubation by liquid-chromatography-coupled mass spectrometry (LC–MS)", nrow(gene_data)), sep = " ")
# # ## table from 3rd category
# comm_data <- data.frame(matrix(ncol = 7, nrow = 0))
# colnames(comm_data) <- c("Species", "Strain", "organismTAXID", "assay_description", "target_name", "target_accession", "Specimen")
#
#
# comm_data[1:28, "Specimen"] <- c("MV01", "MV02", "MV03", "MV04", "MV05", "MV06", "MV07", "MV08", "MV09",
#                          "MV10", "MV11", "MV12", "MV13", "MV14", "MV15", "MV16", "MV17", "MV18",
#                          "MV19", "MV20", "MV21", "MV22", "MV23", "MV24", "MV25", "MV26", "MV27",
#                          "MV28")
#
# ena_access <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/filereport_read_run_PRJEB31790.csv")
#
# comm_data$Species <- rep("Gut metagenome", 28)
# comm_data$organismTAXID <- rep("749906", 28)
# comm_data$assay_description <- paste(rep("The drug is tested on the gut metagenome community of", nrow(comm_data)),
#                                     comm_data$Specimen,
#                                     rep("with study accession number: PRJEB31790 and sample accession number: ", nrow(comm_data)),
#                                     sorted_ena$sample_accession,
#                                     rep("for biotransformation. The drug concentrations were measured over 9 timepoints collected between 0 and 24 hours of incubation by liquid-chromatography-coupled mass spectrometry (LC–MS)", nrow(comm_data)), sep = " ")
# input_assay <- rbind(species_data.df, gene_data, comm_data)
#
# write.csv(input_assay, "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/assay_input.csv")
#
#
# input_csv <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/assay_input.csv"

input_csv <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/assay_input.csv"
output_dir <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/outputs"
ridx <- "HumanMicrobiome_DrugMetabolism"
source <- "Zimmermann"

assay_tbl <- write_assay_tsv(output_dir, input_csv, ridx, category = c("bacteria", "enzyme", "community"), source)


#### ASSAY_PARAM.tsv ####
## should be catered individually as this section is highly depositor dependent, check the rules at ChEMBL website



assay_tsv_bac <- assay_tbl[1:76, ]
assay_tsv_prot <- assay_tbl[77:106, ]
assay_tsv_community <- assay_tbl[107:134, ]



param <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/assay_paraminput.csv")
#
extracted_param <- param[1:14,-8]
extracted_param[c(2, 3, 7, 8, 11, 12), "RELATION"] <- "="
extracted_param[c(4, 9, 13), "TEXT_VALUE"] <- "Anaerobic condition at 37°C."
extracted_param[c(2, 7, 11), "COMMENTS"] <- "Tested drug concentrations in the bacterial assays."
extracted_param[c(3,8,12), "COMMENTS"] <- "Gut Microbiota Medium (GMM) used for bacterial assays at pH7."
# ## biotransformation
change_bio_for_Akkermansia_muciniphila <-"Frozen stocks of bacteria were plated on BHI blood agar and incubated at 37°C under anaerobic conditions. Single colonies were inoculated into 4 mL prereduced GMM and incubated anaerobically at 37°C for 48 h. Cultures were diluted (1:10) in 20% pre-reduced GMM containing drugs at 2 µM and further incubated at 37°C anaerobically."
extracted_param[1, "TEXT_VALUE"] <- "Frozen stocks of bacteria were plated on BHI blood agar and incubated at 37°C under anaerobic conditions. Single colonies were inoculated into 4 mL prereduced GMM and incubated anaerobically at 37°C for 24 h. Cultures were diluted (1:10) in 20% pre-reduced GMM containing drugs at 2 µM and further incubated at 37°C anaerobically."

bio_param <- extracted_param[1:5,-1]
bio_param_list <- list()

for (i in 1:nrow(assay_tsv_bac)){
  bio_param$AIDX <- rep(assay_tsv_bac[i, "AIDX"], 5)
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

#
# ## community
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
write.table(combined_df, file='/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/outputs/ASSAY_PARAM.tsv', sep = "\t", row.names=FALSE)


#### ACTIVITY.tsv ####

# #now let's use it in the context of Suppl_table_3 from the Mapping Paper
# my_table = read.table("/g/zimmermann/Members/emastrori/EM014_Pistoia_prj/EM014C_test_data/ZM000_Pistoia/Input/NIHMS1530152-supplement-Supplementary_Tables_3.txt",
#                       sep = '\t',
#                       skip = 1
#                       # , header = T
# )
# my_table
#
# colnames(my_table) <- my_table[1,]
# colnames(my_table)
# my_table =  my_table[-1,]
# my_table
#
# # retrieve the names
# my_strains = sapply(grep('% consumed STD ',colnames(my_table), fixed = T, value = T),
#                     function(x) gsub('% consumed STD ','',x))
# my_strains
# names(my_strains) =  NULL
# # few double spaces avoiding match later on
# my_strains[my_strains == 'Lactobacillus  reuteri CF48-3A BEI HM-102'] = 'Lactobacillus reuteri CF48-3A BEI HM-102'
# my_strains[my_strains == 'Escherichia coli  K-12'] = 'Escherichia coli K-12'
# my_strains[my_strains == 'Bifidobacterium longum subsp. infantis CCUG52486'] = 'Bifidobacterium longum subsp. Infantis CCUG52486'
# colnames(my_table)[grep('Bifidobacterium longum subsp. infantis CCUG52486',colnames(my_table))] = sapply(colnames(my_table)[grep('Bifidobacterium longum subsp. infantis CCUG52486',colnames(my_table))],
#                                                                                                          function(x) gsub('infantis','Infantis', x, fixed = T))
# my_strains
# # to match with taxonomy, we need species and not strain
# my_species <- sapply(my_strains,
#                      function (x) paste0(unlist(strsplit(x, split = ' '))[1:2], collapse = ' '))
# my_species[my_species == 'Bifidobacterium longum'] = 'Bifidobacterium longum subsp. Infantis'
# my_species[my_species == 'Lactobacillus reuteri'] = 'Lactobacillus  reuteri CF48-3A'
# my_species[my_species == 'Salmonella Typhimurium'] = 'Salmonella typhimurium'
# my_species[my_species == 'Bryantia formatexigens'] = "Bryantia formataxigens"
#
#
# # adjust colnames (sub all spaces with underscores)
# colnames(my_table) = sapply(colnames(my_table), function(x) gsub("\\s+","_",
#                                                                  gsub("^\\s","",x, perl = T), # and remove any trailing space
#                                                                  perl = T))
# # % is a special char!!! messing things up ater
# colnames(my_table) = sapply(colnames(my_table), function(x) gsub("%","perc",
#                                                                  x,
#                                                                  fixed = T))
# # () are special char!!! messing things up ater
# colnames(my_table) = sapply(colnames(my_table), function(x) gsub(")","",
#                                                                  gsub("(","",x,fixed = T),
#                                                                  fixed = T))
# # equally adjust names(my_species)
# names(my_species) <- sapply(names(my_species), function(x) gsub("\\s+","_",
#                                                                 gsub("^\\s","",x, perl = T), # and remove any trailing space
#                                                                 perl = T))
# names(my_species) <- sapply(names(my_species), function(x) gsub(")","",
#                                                                 gsub("(","",x,fixed = T),
#                                                                 fixed = T))
# my_species
# my_table
#
# # Create the list that will contain results
# mylist.names <- names(my_species)
#
# mylist <- vector("list", length(mylist.names))
#
# names(mylist) <- mylist.names
# mylist
# mylist_anti <- mylist
#
# # save(my_table, file = file.path("../Output","Mapping_PercConsumption.rds"))
# # save(my_species, file = file.path("../Output","my_species.rds"))
#
#
# length(names(my_species))
#
#
# for(i in names(my_species)){
#   col_to_keep = paste("perc_consumed_", gsub(" ","_",i, fixed = T) , sep = '')
#   col_to_check = paste("pFDR_", gsub(" ","_",i, fixed = T) , sep = '')
#   # columns important as thresholds for bioactivity
#   vars <- c(col_to_keep, col_to_check)
#
#   # filter table on the basis of p-value which should be less than or equal to 0.05 and on whether consumed % is higher than the drug threshold
#   my_filt_table = my_table %>% select("DrugName","Drug_adaptive_FC_threshold_perc",contains(gsub(" ","_",i, fixed = T))) %>%
#     filter((.data[[vars[[1]]]] >= Drug_adaptive_FC_threshold_perc) & .data[[vars[[2]]]] <= 0.05) %>%
#     select("DrugName","Drug_adaptive_FC_threshold_perc",all_of(col_to_keep))
#
#   my_filt_table_anti = my_table %>% select("DrugName","Drug_adaptive_FC_threshold_perc",contains(gsub(" ","_",i, fixed = T))) %>%
#     filter(.data[[vars[[1]]]] < Drug_adaptive_FC_threshold_perc) %>%
#     select("DrugName","Drug_adaptive_FC_threshold_perc",all_of(col_to_keep))
#
#   my_red_table = data.frame(Strain = i, my_filt_table)
#   colnames(my_red_table)[4] = 'perc_consumed'
#   mylist[[i]] = my_red_table
#
#   my_red_table_anti = data.frame(Strain = i, my_filt_table_anti)
#   colnames(my_red_table_anti)[4] = 'perc_consumed'
#   mylist_anti[[i]] = my_red_table_anti
# }
#
#
#
# stopifnot(dim(bind_rows(mylist))[1]==sum(unlist(lapply(mylist, function(x) dim(x)[1]))))
# my_filtered_table = bind_rows(mylist)
# my_table_percmet <- my_filtered_table  # change
#
# stopifnot(dim(bind_rows(mylist_anti))[1]==sum(unlist(lapply(mylist_anti, function(x) dim(x)[1]))))
# my_filtered_table_anti = bind_rows(mylist_anti)
# my_table_percmet_anti <- my_filtered_table_anti  # change
# ####
# # table without threshold
# # my_table_percmet = my_filtered_table %>% select(Strain | DrugName | perc_consumed)
# colnames(my_table_percmet)
#
#
# # rm controls
# my_table_percmet = my_table_percmet %>% filter(!grepl('Control', Strain))
# #write.csv(my_table_percmet, "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/chembl_activity_input.csv")
#
# # rm controls
# my_table_percmet_anti = my_table_percmet_anti %>% filter(!grepl('Control', Strain))
# #write.csv(my_table_percmet_anti, "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/chembl_activity_input_anti.csv")
#
#
#
# activity_csv <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/chembl_activity_input.csv")
# colnames(activity_csv)
# wrong_activity_data <- activity_csv[activity_csv["perc_consumed"] < activity_csv["Drug_adaptive_FC_threshold_perc"],]
# activity_csv <- activity_csv[activity_csv["perc_consumed"] >= activity_csv["Drug_adaptive_FC_threshold_perc"],]
#
# activity_csv_anti <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/chembl_activity_input_anti.csv")
# activity_csv_anti[activity_csv_anti["perc_consumed"] < activity_csv_anti["Drug_adaptive_FC_threshold_perc"],]
# activity_csv_anti <- rbind(activity_csv_anti, wrong_activity_data)
#
#
# comp_rec_tbl <- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/outputs/COMPOUND_RECORD.tsv", sep = "\t")
# assay_tsv_bac <- assay_tbl[1:76, ]
# assay_tsv_prot <- assay_tbl[77:106, ]
# assay_tsv_community <- assay_tbl[107:134, ]
#
# #assay tsv
# assay_tsv<- assay_tsv_bac
# #combine strain and species
# assay_tsv$whole_organism <- paste(assay_tsv[,"ASSAY_ORGANISM"], assay_tsv[,"ASSAY_STRAIN"], sep = " ")
# assay_tsv$whole_organism
# #read the input from Mapping_DrugBug_identify_biodegradation.r
#
# # add space between species name and strain instead of _
# activity_csv[,"Strain"]<- str_replace_all(activity_csv[,"Strain"],"_", " ")
# activity_csv[,"Strain"]
#
# # Create two example lists, to check typos
# list1 <- unique(assay_tsv$whole_organism)
# list2 <- unique(activity_csv$Strain)
#
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# non_matching_elements1
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# non_matching_elements2
#
#
#
# activity_csv$Strain[activity_csv$Strain == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703"
# activity_csv$Strain[activity_csv$Strain == "Bifidobacterium ruminatum "] = "Bifidobacterium ruminantium fecal isolate"
# activity_csv$Strain[activity_csv$Strain == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520"
# activity_csv$Strain[activity_csv$Strain == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343"
# activity_csv$Strain[activity_csv$Strain == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)"
# activity_csv$Strain[activity_csv$Strain == "Bacteroides fragilis TB9"] = "Bacteroides fragilis T(B)9"
# activity_csv$Strain[activity_csv$Strain == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2"
# activity_csv$Strain[activity_csv$Strain == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"
# activity_csv$Strain[activity_csv$Strain == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"
# activity_csv$Strain[activity_csv$Strain == "Anaerostipes sp. "] = "Anaerostipes sp. fecal isolate"
# activity_csv$Strain[activity_csv$Strain == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"
# activity_csv$Strain[activity_csv$Strain == "Clostridium sp."] = "Clostridium sp. fecal isolate"
# activity_csv$Strain[activity_csv$Strain == "Lactobacillus reuteri CF48-3A BEI HM-102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102"
# activity_csv$Strain[activity_csv$Strain == "Escherichia coli K-12"] = "Escherichia coli BW25113"   # confirm
# activity_csv$Strain[activity_csv$Strain == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2"
# activity_csv$Strain[activity_csv$Strain == "Akkermansia muciniphila ATCCBAA-835"] = "Akkermansia muciniphila ATCC BAA-835"
#
# list1 <- unique(activity_csv$DrugName)
# list2 <- unique(comp_rec_tbl$COMPOUND_NAME)
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# non_matching_elements1
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# non_matching_elements2
#
#
# # add space between species name and strain instead of _
# activity_csv_anti[,"Strain"]<- str_replace_all(activity_csv_anti[,"Strain"],"_", " ")
# activity_csv_anti[,"Strain"]
# #### fix typos ####
# assay_tsv <- data.frame(assay_tsv)
# # Create two example lists, to check typos
# list1 <- unique(assay_tsv$whole_organism)
# list2 <- unique(activity_csv_anti$Strain)
#
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# non_matching_elements1
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# non_matching_elements2
#
#
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Bifidobacterium ruminatum "] = "Bifidobacterium ruminantium fecal isolate"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides fragilis TB9"] = "Bacteroides fragilis T(B)9"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Anaerostipes sp. "] = "Anaerostipes sp. fecal isolate"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Clostridium sp."] = "Clostridium sp. fecal isolate"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Lactobacillus reuteri CF48-3A BEI HM-102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Escherichia coli K-12"] = "Escherichia coli BW25113"   # confirm
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2"
# activity_csv_anti$Strain[activity_csv_anti$Strain == "Akkermansia muciniphila ATCCBAA-835"] = "Akkermansia muciniphila ATCC BAA-835"
#
#
# list1 <- unique(activity_csv_anti$DrugName)
# list2 <- unique(comp_rec_tbl$COMPOUND_NAME)
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# non_matching_elements1
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# non_matching_elements2
#
# merged_activity_1A <- rbind(activity_csv, activity_csv_anti)
#
# colnames(merged_activity_1A)
#
#
#
#
#
#
#
#
# ##### Drug transformed metabolites with good filter #####
# met_activity_tsv<- read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/supp_sheet5_2.csv", sep = ";")
#
# Goodfiltered_index <- met_activity_tsv %>%
#   select(Index, ParentDrug, MZ, LeadingMZ,DrugMassDeltaSmoothed, GoodFilter, DrugMassFlag, DrugConsumedFlag, NumberOfDrugs, NumberOfIncreasedT12vsT0) %>%
#   filter(DrugMassFlag == 0 & DrugConsumedFlag == 1 &
#            NumberOfDrugs == 1 & GoodFilter == 1 & NumberOfIncreasedT12vsT0 >= 1)
# print(nrow(Goodfiltered_index)) # this number should be 871
# Goodfiltered_index
#
# ##### choose drug_bug_connection #####
#
# # now let's use it in the context of Suppl_table_3 from the Mapping Paper
# my_table = read.csv("/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/supp_sheet6.csv",
#                     sep = ';',
#                     skip = 1
#                     # , header = T
# )
#
#
# # keep only columns that have pFDR, remove the rest
# selected_columns_fdr <- my_table[grep("p.FDR..t.12h.vs.t.0h.", names(my_table))]
# colnames(selected_columns_fdr) <- gsub("p.FDR..t.12h.vs.t.0h.", "", colnames(selected_columns_fdr))
# my_species <- colnames(selected_columns_fdr)
# my_species
# keep2 <- c("Index", "ParentDrug", "MZ", "RT", "MZdelta")
# selected_columns_usual <- my_table[keep2]
#
# drug_met <- cbind(selected_columns_usual, selected_columns_fdr)
#
# selected_drug_met <- drug_met[drug_met$Index %in% Goodfiltered_index$Index, ]
# names(selected_drug_met)
#
#
# # Create the list that will contain results
# dataframes_list <- list()
#
# for(i in 1:length(my_species)){
#   print(my_species[i])
#   col_to_keep <- c("ParentDrug","MZ", "RT", "MZdelta", my_species[i])
#   my_table_i <- selected_drug_met[col_to_keep]
#   filtered_table <- my_table_i[as.character(my_table_i[[my_species[i]]]) != "NaN", , drop = FALSE]
#   #filtered_table[as.character(my_species[i])][[1]] <- str_replace(filtered_table[as.character(my_species[i])][[1]], ",", ".")
#   filtered_table$Species <- as.character(my_species[i])
#   colnames(filtered_table)[5] <- "Values"
#   final_filt_df <- filtered_table[filtered_table$Values <=0.05, ]
#   dataframes_list[[i]] <- final_filt_df
# }
#
#
# combined_dataframe <- do.call(rbind, dataframes_list)
# combined_dataframe$Species<- gsub("\\.", " ", combined_dataframe$Species)
#
# combined_dataframe <- subset(combined_dataframe, !grepl("Control pH ", Species))
# combined_dataframe
#
# # Create two example lists, to check typos
# list1 <- unique(assay_tsv$whole_organism)
# list2 <- unique(combined_dataframe$Species)
#
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# non_matching_elements1
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# non_matching_elements2
#
# combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis DS 208"] = "Bacteroides fragilis DS-208"
# combined_dataframe$Species[combined_dataframe$Species == "Victivallis vadensis ATCC BAA 548"] = "Victivallis vadensis ATCC BAA-548"
# combined_dataframe$Species[combined_dataframe$Species == "Bacteroides thetaiotaomicron VPI 5482"] = "Bacteroides thetaiotaomicron VPI-5482"
# combined_dataframe$Species[combined_dataframe$Species == "Odoribacter splanchnius"] = "Odoribacter splanchnicus fecal isolate"
# combined_dataframe$Species[combined_dataframe$Species == "Roseburia intestinalis L1 82"] = "Roseburia intestinalis L1-82"
# combined_dataframe$Species[combined_dataframe$Species == "Lactobacillus  reuteri CF48 3A BEI HM 102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102"
# combined_dataframe$Species[combined_dataframe$Species == "Bifidobacterium longum subsp  infantis CCUG52486"] = "Bifidobacterium longum subsp. Infantis CCUG52486"
# combined_dataframe$Species[combined_dataframe$Species == "Clostridium bolteae ATCCBAA 613"] = "Clostridium bolteae ATCCBAA-613"
# combined_dataframe$Species[combined_dataframe$Species == "Bifidobacterium ruminatum"] = "Bifidobacterium ruminantium fecal isolate"
# combined_dataframe$Species[combined_dataframe$Species == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520"
# combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343"
# combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)"
# combined_dataframe$Species[combined_dataframe$Species == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703"
# combined_dataframe$Species[combined_dataframe$Species == "Bacteroides fragilis T B 9"] = "Bacteroides fragilis T(B)9"
# combined_dataframe$Species[combined_dataframe$Species == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2"
# combined_dataframe$Species[combined_dataframe$Species == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"
# combined_dataframe$Species[combined_dataframe$Species == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"
# combined_dataframe$Species[combined_dataframe$Species == "Anaerostipes sp "] = "Anaerostipes sp. fecal isolate"
# combined_dataframe$Species[combined_dataframe$Species == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"
# combined_dataframe$Species[combined_dataframe$Species == "Clostridium sp "] = "Clostridium sp. fecal isolate"
# combined_dataframe$Species[combined_dataframe$Species == "Lactobacillus reuteri CF48 3A BEI HM 102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102"
# combined_dataframe$Species[combined_dataframe$Species == "Escherichia coli  K 12"] = "Escherichia coli BW25113"   # confirm
# combined_dataframe$Species[combined_dataframe$Species == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2"
# combined_dataframe$Species[combined_dataframe$Species == "Akkermansia muciniphila ATCCBAA 835"] = "Akkermansia muciniphila ATCC BAA-835"
#
# length(unique(combined_dataframe$ParentDrug))
# length(unique(comp_rec_tbl$COMPOUND_KEY))
#
# # Create two example lists, to check typos
# list1 <- unique(comp_rec_tbl$COMPOUND_KEY)
# list2 <- unique(combined_dataframe$ParentDrug)
#
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# non_matching_elements1
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# non_matching_elements2
#
# comp_rec_tbl$COMPOUND_KEY[comp_rec_tbl$COMPOUND_KEY == "LOFEXIDINE "] = "LOFEXIDINE"
#
#
#
#
#
#
#
#
# # length(unique(combined_dataframe$ParentDrug))
# # #length(unique(full_act$DrugName))
# #
# # # Create two example lists, to check typos
# # list1 <- unique(comp_rec_tbl$COMPOUND_KEY)
# # list2 <- unique(combined_dataframe$ParentDrug)
# #
# # # Find elements that are in list1 but not in list2
# # non_matching_elements1 <- list1[!(list1 %in% list2)]
# # non_matching_elements1
# # # Find elements that are in list2 but not in list1
# # non_matching_elements2 <- list2[!(list2 %in% list1)]
# # non_matching_elements2
# #
# #
# # full_act$DrugName[full_act$DrugName == "LOFEXIDINE "] = "LOFEXIDINE"
#
# nonselected_drug_met <- drug_met[!drug_met$Index %in% Goodfiltered_index$Index, ]
# names(nonselected_drug_met)
#
#
# # Create the list that will contain results
# dataframes_list2 <- list()
#
# for(i in 1:length(my_species)){
#   print(my_species[i])
#   col_to_keep <- c("ParentDrug","MZ", "RT", "MZdelta", my_species[i])
#   my_table_i <- nonselected_drug_met[col_to_keep]
#   filtered_table <- my_table_i[as.character(my_table_i[[my_species[i]]]) != "NaN", , drop = FALSE]
#   #filtered_table[as.character(my_species[i])][[1]] <- str_replace(filtered_table[as.character(my_species[i])][[1]], ",", ".")
#   filtered_table$Species <- as.character(my_species[i])
#   colnames(filtered_table)[5] <- "Values"
#   final_filt_df <- filtered_table[filtered_table$Values <=0.05, ]
#   dataframes_list2[[i]] <- final_filt_df
# }
#
#
# combined_dataframe2 <- do.call(rbind, dataframes_list2)
# combined_dataframe2$Species<- gsub("\\.", " ", combined_dataframe2$Species)
#
# combined_dataframe2 <- subset(combined_dataframe2, !grepl("Control pH ", Species))
# combined_dataframe2
#
#
# # Create two example lists, to check typos
# list1 <- unique(assay_tsv$whole_organism)
# list2 <- unique(combined_dataframe2$Species)
#
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# sort(non_matching_elements1)
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# sort(non_matching_elements2)
#
# combined_dataframe2$Species[combined_dataframe2$Species == "Victivallis vadensis ATCC BAA 548"] = "Victivallis vadensis ATCC BAA-548"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Akkermansia muciniphila ATCCBAA 835"] = "Akkermansia muciniphila ATCC BAA-835"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Alistipes indistinctus DSM 22520"] = "Alistipes indistinctus DSM22520" #C
# combined_dataframe2$Species[combined_dataframe2$Species == "Anaerostipes sp "] = "Anaerostipes sp. fecal isolate"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis 3397 T10"] = "Bacteroides fragilis 3397 (T10)" #C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis DS 208"] = "Bacteroides fragilis DS-208"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis NCTC9343"] = "Bacteroides fragilis NCTC 9343" #C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides fragilis T B 9"] = "Bacteroides fragilis T(B)9"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides thetaiotaomicron VPI 5482"] = "Bacteroides thetaiotaomicron VPI-5482"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bacteroides WH2 WH2"] = "Bacteroides sp. WH2 WH2" #C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bifidobacterium adolescentis ATCC15703"] = "Bifidobacterium adolescentis ATCC 15703"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bifidobacterium longum subsp  infantis CCUG52486"] = "Bifidobacterium longum subsp. Infantis CCUG52486"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bifidobacterium ruminatum"] = "Bifidobacterium ruminantium fecal isolate"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Bryantia formatexigens DSM14469"] = "Marvinbryantia formatexigens DSM14469"   #C
# combined_dataframe2$Species[combined_dataframe2$Species == "Clostridium bolteae ATCCBAA 613"] = "Clostridium bolteae ATCCBAA-613"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Clostridium sp "] = "Clostridium sp. fecal isolate"            #C#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Escherichia coli  K 12"] = "Escherichia coli BW25113"   ##C
# combined_dataframe2$Species[combined_dataframe2$Species == "Lactobacillus reuteri CF48 3A BEI HM 102"] = "Lactobacillus  reuteri CF48-3A BEI HM-102" #C
# combined_dataframe2$Species[combined_dataframe2$Species == "Odoribacter splanchnius "] = "Odoribacter splanchnicus fecal isolate"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Pretovella copri DSM18205"] = "Prevotella copri DSM18205"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Roseburia intestinalis L1 82"] = "Roseburia intestinalis L1-82"#C
# combined_dataframe2$Species[combined_dataframe2$Species == "Salmonella Typhimurium LT2"] = "Salmonella typhimurium LT2" #C
#
# length(unique(combined_dataframe2$ParentDrug))
# length(unique(comp_rec_tbl$COMPOUND_KEY))
#
# # Create two example lists, to check typos
# list1 <- unique(comp_rec_tbl$COMPOUND_KEY)
# list2 <- unique(combined_dataframe2$ParentDrug)
#
# # Find elements that are in list1 but not in list2
# non_matching_elements1 <- list1[!(list1 %in% list2)]
# non_matching_elements1
# # Find elements that are in list2 but not in list1
# non_matching_elements2 <- list2[!(list2 %in% list1)]
# non_matching_elements2
#
#
#
# colnames(combined_dataframe)
# colnames(combined_dataframe2)
# nrow(combined_dataframe2)+ nrow(combined_dataframe)
#
#
#
# result <- combined_dataframe %>%
#   left_join(comp_rec_tbl, by = c("ParentDrug" = "COMPOUND_KEY")) %>%
#   group_by(ParentDrug) %>%
#   mutate(CIDX = first(CIDX, order_by = ParentDrug)) %>%
#   ungroup()
# result
# result["GoodFilter"] <- 1
# result2 <- combined_dataframe2 %>%
#   left_join(comp_rec_tbl, by = c("ParentDrug" = "COMPOUND_KEY")) %>%
#   group_by(ParentDrug) %>%
#   mutate(CIDX = first(CIDX, order_by = ParentDrug)) %>%
#   ungroup()
# result2["GoodFilter"] <- 0
# comb_result <- rbind(result, result2)
# comb_result <- data.frame(comb_result)
#
# comb_result["combined_col"] <- paste(comb_result$ParentDrug, comb_result$Species, sep ="_")
# merged_activity_1A["combined_col"] <- paste(merged_activity_1A$DrugName, merged_activity_1A$Strain, sep = "_")
# merged_activity_1A["GoodFilter"] <- ""
# check_mets <- anti_join(merged_activity_1A, comb_result, by = "combined_col")
#
# result <- data.frame(result)
#
# result$combined_col <- paste(result$ParentDrug, result$Species, sep = "_")
#
#
# filtered_df_wo <- anti_join(merged_activity_1A, result, by = "combined_col")
# colnames(filtered_df_wo)[2] <- "Species"
# colnames(result)[1] <- "DrugName"
#
# colnames(filtered_df_wo)
# colnames(result)
#
#
# result[, "Protein"] <- ""
# result[, "Biotransformation"] <- ""
# result[, "Comment"] <- ""
#
# for (i in 1:nrow(result)){
#
#   result[i, "Biotransformation"] <- "Compound Metabolized"
#   result[i, "Comment"] <- paste("Putative metabolite identification: The drug ", result [i, "DrugName"], " is biotransformed by ", result[i, "Species"], " and a corresponding drug metabolite with m/z ",
#                                 result[i, "MZ"], " at retention time ", result[i, "RT"], "minutes is detected.")
# }
#
#
#
#
#
# filtered_df_wo[, "Protein"] <- ""
# filtered_df_wo[, "Biotransformation"] <- ""
# filtered_df_wo[, "Comment"] <- ""
#
# for (i in 1:nrow(filtered_df_wo)){
#   if (filtered_df_wo[i, "perc_consumed"] > filtered_df_wo[i, "Drug_adaptive_FC_threshold_perc"]){
#     filtered_df_wo[i, "Biotransformation"] <- "Compound Metabolized"
#     filtered_df_wo[i, "Comment"] <- paste("The percentage of consumption of the drug ", filtered_df_wo [i, "DrugName"], " i.e. ", filtered_df_wo[i, "perc_consumed"], "% is higher than the Drug adaptive FC Threshold ",
#                                           filtered_df_wo[i, "Drug_adaptive_FC_threshold_perc"], "%. Significant biotransformation is detected.")
#   }
#   else{
#     filtered_df_wo[i, "Biotransformation"] <- "Compound NOT Metabolized"
#     filtered_df_wo[i, "Comment"] <- paste("The percentage of consumption of the drug ", filtered_df_wo [i, "DrugName"], " i.e. ", filtered_df_wo[i, "perc_consumed"], "% is lower than the Drug adaptive FC Threshold ",
#                                           filtered_df_wo[i, "Drug_adaptive_FC_threshold_perc"], "%. No significant biotransformation is detected.")
#   }
# }
#
#
#
# col_to_keep <- c("DrugName", "Species", "Protein", "Biotransformation", "Comment")
# filtered_df_wo <- filtered_df_wo[col_to_keep]
# result <- result[col_to_keep]
#
#
# combined_met_bio <- rbind(result, filtered_df_wo) # --> 21388 but its 21431 here
# #
# #
# # ########
# gene_data
# gene <- gene_data$Gene
# gene
# drugs_for_genes <- c("Artemisinin",
#                      "Bisacodyl",
#                      "Danazol",
#                      "Deflazacort",
#                      "Diacetamate",
#                      "Diflorasone.Diacetate",
#                      "Diltiazem",
#                      "Drospirenone",
#                      "Entacapone",
#                      "Famciclovir",
#                      "Levonorgestrel",
#                      "Nitrendipine",
#                      "Norethindrone.acetate",
#                      "Pantoprazole",
#                      "Pericyazine",
#                      "Phenazopyridine",
#                      "Racecadotril",
#                      "Roxatidine.acetate",
#                      "Sulfasalazine",
#                      "Tinidazole")
#
# dataframes_list <- list()
# colnames(gene_data)
#
#
# for (i in 1:length(gene)){
#   gene_transposed <- data.frame(t(gene_data[gene_data$Gene == gene[i],]))
#   colnames(gene_transposed)[1] <- "Value"
#   gene_transposed$drugs <- rownames(gene_transposed)
#   gene_transposed$genes <- gene[i]
#   gene_transposed <- gene_transposed[4:82, ]
#   rownames(gene_transposed)<-NULL
#   gene_transposed %>% relocate(genes, drugs)
#   # Sample list of drug names
#   drug_names <- list(gene_transposed$drugs)
#   # Empty list to store dataframes
#   single_drugs <- c()
#   metabolite_mass <- c()
#   # Loop through drug names, extract drug names and numbers, and create dataframes
#   for (name in drug_names) {
#     drug_name <- gsub("(_\\d+\\.\\d+)?", "", name)  # Extract drug name
#     single_drugs <- c(single_drugs, drug_name)
#     extracted_number <- as.numeric(gsub(".*_(\\d+\\.\\d+)", "\\1", name))  # Extract number or NA if not present
#     metabolite_mass <- c(metabolite_mass, extracted_number)
#   }
#   gene_transposed$single_drugs <- single_drugs
#   gene_transposed$metabolite_mass <- metabolite_mass
#   gene_transposed[67, "single_drugs"] <- "Pericyazine"
#   gene_transposed[68, "single_drugs"] <- "Pericyazine"
#   gene_transposed[67, "metabolite_mass"] <- "407.166"
#   gene_transposed[68, "metabolite_mass"] <- "421.182"
#
#   dataframes_list[[i]] <- gene_transposed
# }
#
# combined_dataframe_genes <- do.call(rbind, dataframes_list)
#
# #### replace genes ####
#
# combined_dataframe_genes$single_drugs <- gsub("\\.", " ", toupper(combined_dataframe_genes$single_drugs))
# combined_dataframe_genes <- combined_dataframe_genes %>% relocate(genes, drugs, single_drugs, metabolite_mass, Value)
#
# combined_dataframe_genes_ones <- combined_dataframe_genes[combined_dataframe_genes$Value == "1", ]
#
# combined_dataframe_genes_ones_without_mets <- combined_dataframe_genes_ones[is.na(combined_dataframe_genes_ones["metabolite_mass"]), ] # use this for true analysis
# combined_dataframe_genes_ones_mets <- combined_dataframe_genes_ones[!is.na(combined_dataframe_genes_ones["metabolite_mass"]), ] # use this for metabolites
#
#
# combined_dataframe_genes_ones$combined <- paste(combined_dataframe_genes_ones$genes, combined_dataframe_genes_ones$single_drugs, sep = "_")
#
# combined_dataframe_genes_ones_without_mets$combined <- paste(combined_dataframe_genes_ones_without_mets$genes, combined_dataframe_genes_ones_without_mets$single_drugs, sep = "_")
#
# combined_dataframe_genes_zeroes <- combined_dataframe_genes[combined_dataframe_genes$Value == "0", ]
#
# combined_dataframe_genes_zeroes_without_mets <- combined_dataframe_genes_zeroes[is.na(combined_dataframe_genes_zeroes["metabolite_mass"]), ] # use this for false analysis
#
# assay_tsv_prot <- data.frame(assay_tsv_prot)
#
# assay_tsv_prot$Gene <- gene_data$TARGET_ACCESSION
#
# colnames(assay_tsv_prot)
#
# # combined_dataframe_genes_ones_without_mets$CIDX <- comp_rec_tbl$CIDX[match(combined_dataframe_genes_ones_without_mets$single_drugs, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
# # combined_dataframe_genes_ones_without_mets$AIDX <- assay_tsv_prot$AIDX[match(combined_dataframe_genes_ones_without_mets$genes, assay_tsv_prot$Gene, nomatch = 0)]
# # combined_dataframe_genes_ones_without_mets$CRIDX <- rep(unique(RIDX), nrow(combined_dataframe_genes_ones_without_mets))
# # combined_dataframe_genes_ones_without_mets$TYPE <- rep("Biotransformation", nrow(combined_dataframe_genes_ones_without_mets))
# combined_dataframe_genes_ones_without_mets$Biotransformation <- rep("Compound metabolized", nrow(combined_dataframe_genes_ones_without_mets))
# #combined_dataframe_genes_ones_without_mets$ACTION_TYPE <- rep("SUBSTRATE", nrow(combined_dataframe_genes_ones_without_mets))
# combined_dataframe_genes_ones_without_mets$Comment <- paste(rep("The oberved biotransformation of drug", nrow(combined_dataframe_genes_ones_without_mets)),
#                                                                      combined_dataframe_genes_ones_without_mets$single_drugs,
#                                                                      rep("was proven to be mediated by", nrow(combined_dataframe_genes_ones_without_mets)),
#                                                                      paste(combined_dataframe_genes_ones_without_mets$genes, rep(".", nrow(combined_dataframe_genes_ones_without_mets)), sep = ""))
#
#
#
# # combined_dataframe_genes_ones_mets$CIDX <- comp_rec_tbl$CIDX[match(combined_dataframe_genes_ones_mets$single_drugs, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
# # combined_dataframe_genes_ones_mets$AIDX <- assay_tsv_prot$AIDX[match(combined_dataframe_genes_ones_mets$genes, assay_tsv_prot$Gene, nomatch = 0)]
# # combined_dataframe_genes_ones_mets$CRIDX <- rep(unique(RIDX), nrow(combined_dataframe_genes_ones_mets))
# # combined_dataframe_genes_ones_mets$TYPE <- rep("Biotransformation", nrow(combined_dataframe_genes_ones_mets))
# combined_dataframe_genes_ones_mets$Biotransformation <- rep("Compound metabolized", nrow(combined_dataframe_genes_ones_mets))
# #combined_dataframe_genes_ones_mets$ACTION_TYPE <- rep("SUBSTRATE", nrow(combined_dataframe_genes_ones_mets))
# combined_dataframe_genes_ones_mets$Comment <- paste(rep("Putative metabolite identification: The observed biotransformation of drug", nrow(combined_dataframe_genes_ones_mets)),
#                                                              combined_dataframe_genes_ones_mets$single_drugs,
#                                                              rep("into metabolite with m/z", nrow(combined_dataframe_genes_ones_mets)),
#                                                              combined_dataframe_genes_ones_mets$metabolite_mass,
#                                                              rep("was proven to be mediated by", nrow(combined_dataframe_genes_ones_mets)),
#                                                              paste(combined_dataframe_genes_ones_mets$genes, rep(".", nrow(combined_dataframe_genes_ones_mets)), sep = ""))
#
# filtered_df1 <- subset(combined_dataframe_genes_ones_without_mets, !(combined %in% combined_dataframe_genes_ones_mets$combined))
#
# # combined_dataframe_genes_zeroes_without_mets$CIDX <- comp_rec_tbl$CIDX[match(combined_dataframe_genes_zeroes_without_mets$single_drugs, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
# # combined_dataframe_genes_zeroes_without_mets$AIDX <- assay_tsv_prot$AIDX[match(combined_dataframe_genes_zeroes_without_mets$genes, assay_tsv_prot$Gene, nomatch = 0)]
# # combined_dataframe_genes_zeroes_without_mets$CRIDX <- rep(unique(RIDX), nrow(combined_dataframe_genes_zeroes_without_mets))
# # combined_dataframe_genes_zeroes_without_mets$TYPE <- rep("Biotransformation", nrow(combined_dataframe_genes_zeroes_without_mets))
# combined_dataframe_genes_zeroes_without_mets$Biotransformation <- rep("Compound NOT metabolized", nrow(combined_dataframe_genes_zeroes_without_mets))
# #combined_dataframe_genes_zeroes_without_mets$ACTION_TYPE <- rep("", nrow(combined_dataframe_genes_zeroes_without_mets))
# combined_dataframe_genes_zeroes_without_mets$Comment <- paste(rep("The biotransformation of drug", nrow(combined_dataframe_genes_zeroes_without_mets)),
#                                                                        combined_dataframe_genes_zeroes_without_mets$single_drugs,
#                                                                        rep("could not be mediated by", nrow(combined_dataframe_genes_zeroes_without_mets)),
#                                                                        paste(combined_dataframe_genes_zeroes_without_mets$genes, rep(".", nrow(combined_dataframe_genes_zeroes_without_mets)), sep = ""))
#
# colnames(combined_dataframe_genes_zeroes_without_mets)
# keep_cols <- c("single_drugs", "genes", "Biotransformation", "Comment")
#
# filtered_df1_final <- filtered_df1[keep_cols]
# combined_dataframe_genes_ones_mets_final <- combined_dataframe_genes_ones_mets[keep_cols]
# colnames(combined_dataframe_genes_zeroes_without_mets)
# combined_dataframe_genes_zeroes_without_mets_final <- combined_dataframe_genes_zeroes_without_mets[keep_cols]
# final_prot_act <- rbind(rbind(filtered_df1_final, combined_dataframe_genes_ones_mets_final), combined_dataframe_genes_zeroes_without_mets_final)
#
#
# colnames(final_prot_act) <- c("DrugName", "Protein", "Biotransformation", "Comment")
# final_prot_act["Species"] <- ""
# colnames(final_prot_act)
#
# bac_prot_act <- rbind(combined_met_bio, final_prot_act)
# #write.table(final_prot_act, file='ASSAY_typeB_bioGeneANDmet.tsv', sep='\t', row.names=FALSE)
#
#
#
#
# ####
#
# community_act <- read.csv("all_samples_metabolized_status_match_Mapping_supp_short.csv")
# community_act$slope_rate <- community_act$Slope_Michael_negative*2
#
# community_act$Drug[community_act$Drug == "DILTIAZEM_HYDROCHLORIDE"] = "DILTIAZEM"
#
# community_act_ones <- community_act[community_act $Metabolized==1,]
# community_act_zeroes <- community_act[community_act $Metabolized==0,]
#
# #community_act_ones$CIDX <- c(rep("HMDM0063", 5), rep("HMDM0092", 27), rep("HMDM0166", 27))
# #community_act_ones$CIDX <- comp_rec_tbl$CIDX[match(community_act_ones$Drug, comp_rec_tbl$COMPOUND_KEY, nomatch = 0)]
#
# # assay_tsv_community <- data.frame(assay_tsv_community)
# # community_act_ones$AIDX <- assay_tsv_community$AIDX[match(community_act_ones$Sample, assay_tsv_community$COMMUNITY, nomatch = 0)]
# # community_act_ones$CRIDX <- rep(unique(RIDX), nrow(community_act_ones))
# # community_act_ones$TYPE <- rep("Biotransformation", nrow(community_act_ones))
# community_act_ones$Biotransformation <- rep("Compound metabolized", nrow(community_act_ones))
# # community_act_ones$ACTION_TYPE <- "SUBSTRATE"
# community_act_ones$comment <- paste(rep("Biotransformation occured for drug", nrow(community_act_ones)),
#                                              paste(community_act_ones$Drug, ",", sep = ""),
#                                              rep("within community,", nrow(community_act_ones)),
#                                              community_act_ones$Sample,
#                                              rep("surpassing drug threshold of", nrow(community_act_ones)),
#                                              community_act_ones$Per_drug_thresh,
#                                              rep("and decreasing over time with a biotransformation rate of", nrow(community_act_ones)),
#                                              community_act_ones$Slope_Michael_negative,
#                                              rep("corresponding to", nrow(community_act_ones)),
#                                              community_act_ones$slope_rate,
#                                              rep("uM/h.", nrow(community_act_ones))
# )
#
#
# #colnames(community_act_ones)
#
# #community_act_zeroes$CIDX <- c(rep("HMDM0063", 23), rep("HMDM0070", 28), rep("HMDM0092", 1), rep("HMDM0166", 1))
#
#
# #community_act_zeroes$AIDX <- assay_tsv_community$AIDX[match(community_act_zeroes$Sample, assay_tsv_community$COMMUNITY, nomatch = 0)]
# # community_act_zeroes$CRIDX <- rep(unique(RIDX), nrow(community_act_zeroes))
# # community_act_zeroes$TYPE <- rep("Biotransformation", nrow(community_act_zeroes))
# community_act_zeroes$Biotransformation <- rep("Compound NOT metabolized", nrow(community_act_zeroes))
# #community_act_zeroes$ACTION_TYPE <- rep("", length=nrow(community_act_zeroes))
# community_act_zeroes$comment <- paste(rep("No biotransformation occured for drug", nrow(community_act_zeroes)),
#                                                paste(community_act_zeroes$Drug, ",", sep = ""),
#                                                rep("within community,", nrow(community_act_zeroes)),
#                                                paste(community_act_zeroes$Sample, rep(".", nrow(community_act_zeroes)), sep = ""))
#
# colnames(community_act_ones)
# keep_cols <- c("Drug", "Sample", "Biotransformation", "comment")
#
# community_act_ones <- community_act_ones[keep_cols]
# community_act_zeroes <- community_act_zeroes[keep_cols]
# final_com_act <- rbind(community_act_ones, community_act_zeroes)
# final_com_act["Protein"] <- ""
# colnames(bac_prot_act)
# colnames(final_com_act) <- c("DrugName", "Species", "Biotransformation", "Comment", "Protein")
# final_com_act <- final_com_act[c("DrugName", "Species", "Protein", "Biotransformation", "Comment")]
# colnames(bac_prot_act)
# colnames(final_com_act)
# fin_act_met_val <- rbind(bac_prot_act, final_com_act)
# colnames(fin_act_met_val)
# write.csv(rbind(bac_prot_act, final_com_act), file='/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/activity_input.csv', row.names=FALSE)
#
# #### find validated metabolites
# metabolite_name <- c("Acetyl pericyazine", "Propionyl pericyazine", "Deacetyldiltiazem", "Dexamethasone metabolite")
# MZ <- c(407.166, 421.182, 372.151, 332.179)
# parent <- c("PERICYAZINE", "PERICYAZINE", "DILTIAZEM", "DEXAMETHASONE")
# cidx <- c("HMDM0185", "HMDM0185", "HMDM0070", "HMDM0063")
# pericyazine <- 21584
# diltiazem <- c(71, 833, 985, 1124, 1265, 1881, 1972, 2145, 2270, 2502, 2657, 2890, 2999, 3149, 3673, 3747, 3850,
#                3940, 4049, 4243, 4497, 4851, 5439, 5546, 5639, 5734, 6198, 6272,
#                6421, 6510, 6588, 6791, 6833)-1
#
# dexamethasone <- 1578
#
# fin_act_met_val[21584, "Comment"]
#
# fin_act_met_val[1578, "Comment"] <- "Validated metabolite identification: The drug  DEXAMETHASONE is biotransformed by Clostridium scindens ATCC35704 and a corresponding drug metabolite with m/z 332.179 at rerention time 4.033 minutes is detected."
# fin_act_met_val[21584, "Comment"] <- "Validated metabolite identification: The observed biotransformation of drug PERICYAZINE into metabolite with m/z 407.166 corresponding to Acetyl pericyazine, was proven to be mediated by BT_2367."
# fin_act_met_val[diltiazem, "Comment"] <- str_replace(fin_act_met_val[diltiazem, "Comment"], "Putative", "Validated")
# fin_act_met_val[diltiazem, "Comment"] <- str_replace(fin_act_met_val[diltiazem, "Comment"], "drug metabolite with", "drug metabolite Deacetyldiltiazem with")
#
# # fin_act_met_val <- subset( fin_act_met_val, select = -Comment )
# # fin_act_met_val
# # fin_act_met_val$merged_column <- ifelse(fin_act_met_val$Species != "", fin_act_met_val$Species, fin_act_met_val$Protein)
# # fin_act_met_val <- fin_act_met_val[c("DrugName", "Biotransformation", "Comment", "merged_column")]
# # colnames(fin_act_met_val)[4] <- "Sample"
#
#
#
# write.csv(rbind(fin_act_met_val), file='/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/activity_input.csv', row.names=FALSE)
# act_input <- read.csv('/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/activity_input.csv')
# target_name <- c("BT_0152",
#                  "BT_0217",
#                  "BT_0445",
#                  "BT_0569",
#                  "BT_1006",
#                  "BT_1148",
#                  "BT_1192",
#                  "BT_1429",
#                  "BT_2068",
#                  "BT_2366",
#                  "BT_2367",
#                  "BT_2961",
#                  "BT_3112",
#                  "BT_3124",
#                  "BT_4075",
#                  "BT_4091",
#                  "BT_4096",
#                  "COLAER_00311",
#                  "COLAER_00815",
#                  "COLAER_01707",
#                  "COLAER_01846",
#                  "COLAER_02348",
#                  "BACDOR_00571",
#                  "BACDOR_00665",
#                  "BACDOR_03091",
#                  "BACDOR_03379",
#                  "BACDOR_03642",
#                  "BACDOR_03934",
#                  "BACDOR_03937",
#                  "BACDOR_03988")
# target_accession <- c("Q8ABF8", "Q8AB93", "Q8AAL9", "Q8AA96",
#                                 "Q8A911", "Q8A8L9", "Q8A8H5", "Q8A7U5",
#                                 "Q8A618", "Q8A576", "Q8A575", "Q8A3J3",
#                                 "Q8A343", "Q8A331", "Q8A0E6", "Q8A0D0",
#                                 "Q8A0C5", "A4E7D0", "A4E8S4", "A4EB91",
#                                 "A4EBM5", "A4ED08", "B6VU18", "B6VTE7",
#                                 "B6W0N3", "B6W1J1", "B6W293", "B6W2J3",
#                                 "B6W2J6", "B6W3P3")
# #
# #
# genelist <- cbind(target_name, target_accession)
#
# for (i in 1:nrow(act_input)){
#   for (j in 1:nrow(genelist)){
#     if (!is.na(act_input[i, "Protein"])){
#       if (act_input[i, "Protein"] == genelist[j, "target_name"]){
#         act_input[i, "Protein"] <- genelist[j, "target_accession"]
#       }
#     }
#   }
# }
# colnames(act_input)[2] <- "Sample"
# write.csv(act_input, file='/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/activity_input.csv', row.names=FALSE)
#
output_dir <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/outputs"
input_csv <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/inputs/activity_input.csv"
compound_tsv <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/outputs/COMPOUND_RECORD.tsv"
assay_tsv <- "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/ChEMBL_Submission_Pipeline/ChEMBL_Submission_Pipeline/outputs/ASSAY.tsv"
ridx <- "HumanMicrobiome_DrugMetabolism"

write_activity_tsv(output_dir, input_csv, compound_tsv, assay_tsv,
                   ridx, type = "Biotransformation")
