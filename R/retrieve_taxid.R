# my_path = "/g/zimmermann/Members/emastrori/EM014_Pistoia_prj/EM014C_test_data/"
# setwd(my_path)

species_names = read.csv(file.path(my_path,'../Input/Single_species_names_from_Mapping.csv'))
resulting_taxid <- rep(NA, nrow(species_names))

# example on how the function will have to work
# retrieving the taxonomic hierarchy of "Arabidopsis thaliana"
# from NCBI Taxonomy
# res <- myTAI::taxonomy( organism = "Bifidobacterium adolescentis", 
#                         db       = "ncbi",
#                         output   = "taxid" )
# 
# res$id

# many species have been reassigned in the meantime, use the new names:
new_species_names <- rep(NA, nrow(species_names))
for(i in 1:nrow(species_names)){
  new_species_names[i] <- ifelse(species_names$Current_name[i]!="", species_names$Current_name[i], species_names$Species[i])
}
species_names <- data.frame(species_names, Full_name = new_species_names)
names(resulting_taxid) = species_names$Full_name

for(i in unique(names(resulting_taxid))){
  
  temp_res <- tryCatch(myTAI::taxonomy( organism = i, 
                                        db       = "ncbi",
                                        output   = "taxid" ),
                       error = function(e) { cat("ERROR :",conditionMessage(e), "\n")})
  if(length(temp_res$id)!=0)  resulting_taxid[i] <- temp_res$id
  
  Sys.sleep(30)
  rm(temp_res)
}

taxid_df <- data.frame(Species = species_names$Species, 
                       taxid = resulting_taxid, 
                       Current_name = names(resulting_taxid))

write.csv(taxid_df, file = file.path("../Output","Retrieved_taxid_for_single_species.csv"), row.names = F)
