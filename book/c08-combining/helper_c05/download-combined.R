# Note: must be run after c08-combining/2-data (to get gxa_experiment_info)

exp_dir <- 'data/experiments/'
fantom_url <- 'http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/extra/CAGE_peaks_expression/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt.gz'
folder_names <- c('E-MTAB-2836'='hpa/','E-MTAB-3358'='fantom/','E-MTAB-5214'='gtex/','E-MTAB-4840'='hdbr/')

for(accession_number in gxa_experiment_info$experimentAccession){
    # Create the directories:
    ifelse(!dir.exists(paste(exp_dir, folder_names[accession_number], sep="")),
           dir.create(paste(exp_dir, folder_names[accession_number], sep="")), FALSE)
    if(accession_number == 'E-MTAB-3358'){
        # FANTOM is downloaded directly:
        fantom_path <- paste(exp_dir,
                             folder_names[accession_number],
                             basename(fantom_url),
                             sep="")
        download.file(fantom_url, fantom_path)
        # TODO: download other FANTOM files
    }
    else{
        # Other experiments are downloaded using `ExpressionAtlas`
        summary <- getAtlasExperiment(accession_number)
        write.table(assays(summary$rnaseq)$counts,
                    sep='\t',
                    file = paste(exp_dir,
                                 folder_names[accession_number],
                                 accession_number,
                                 "_counts.tsv",
                                 sep=""))
        write.table(colData(summary$rnaseq),
                    sep='\t',
                    file = paste(exp_dir,
                                 folder_names[accession_number],
                                 accession_number,
                                 "_colData.tsv",
                                 sep=""))

    # A messy way of saving the metadata because it's a list of different length lists:
        sink(paste(exp_dir,
                   folder_names[accession_number],
                   accession_number,
                   "_metadata.txt",
                   sep="")); print(metadata(summary$rnaseq)); sink()
    }
}