## Data

### Criteria for choosing datasets
[//]: # (TODO: Expand on the metadata part below:)
Datasets were chosen from the EBI’s Gene Expression Atlas (GxA). A major benefit of the GxA is that raw data using the same sequencing technology are re-analysed by GxA using the same data analysis pipeline (iRAP{cite}`Fonseca2014-hp` for RNA-Seq). In addition to ensuring the quality of each data set included, and running it through the same pipeline, the GxA adds additional metadata for the experiments by using the literature to biologically and technically annotate each sample. 

Data sets from the GxA were chosen based on the following requirements.
- **Experiments must be measuring baseline, rather than differential gene expression**.
- **Samples must be sequenced using Next Generation Sequencing**, i.e. including RNA-Seq and CAGE, and excluding microarrays.
- **Data sets must contain a breadth of tissues and genes**. This is to aid batch correction by facilitating the most balanced data set design in terms of batch (experiment) to group (tissue), and in order to have good coverage of genes and tissues, which is necessary for downstream use. i.e. experiments must include "organism part" as an experimental factor (otherwise tissue would not be recorded) and must have at least 80 assays (samples).
- **Samples must not be disease-focused**. In practice, excluding cancer datasets was enough to exclude disease-focused datasets. 

#### Next Generation Sequencing
As described in the introduction chapter, there are many ways to measure which proteins are being created. Here, I justify my choices of measures to include in the combined dataset.

<!-- (TODO: explain why RNA-Seq not mircroarrays)-->

##### Gene expression vs protein abundance
Gene expression levels are not necessarily strongly correlated with protein abundance; this has been found in mice{cite}`Schwanhausser2011-tm`, yeast{cite}`Gygi1999-lr`, and human{cite}`Kosti2016-gt`. In human, Spearman correlations between protein abundance and gene expression levels vary between 0.36 and 0.50, depending on tissue, meaning that they are only weakly or moderately correlated{cite}`Kosti2016-gt`.
There are many interacting reasons why this is the case. One reason is that there is something preventing the mRNA from being translated, such as slow codons, the temperature, ribosome occupancy, or regulatory RNAs and proteins{cite}`Maier2009-vw`. In these cases, the DNA is transcribed into mRNA, but the protein is never produced, meaning that using gene expression data as a measure of how much protein is produced would be overestimating the protein abundance. If these factors were a large contribution to the weak correlation, it could provide better results to use protein abundance data instead of mRNA abundance data to make predictions about how proteins are affecting human phenotypes.
On the other hand, it could equally be possible that proteins are being produced, but not measured by protein abundance techniques. Protein half-lives range over orders of magnitude from seconds to days{cite}`Maier2009-vw,Beyer2004-ws`. In this case, gene expression data may be a more reliable measure of protein production than protein abundance, since proteins may degrade before being measured. In yeast, protein degradation was shown to be the largest contribution to the protein-mRNA correlation compared to codon and amino acid usage (the two other factors estimated in the study), and more influential than those other two factors combined{cite}`Wu2008-hb`.

In summary, there's no perfect measure of translation, but since gene expression data is more readily available, and protein degradation appears to account for most of the differences between correlations, gene expression data presents the best proxy for translation for the downstream uses discussed here.

##### Gene expression vs Transcript expression
It's likely that transcript expression data would provide more insight than gene expression data if it were available, since it is likely that there are tissue-specific transcripts which do not correspond to tissue-specific genes, e.g. where different transcripts from the same gene are expressed in different tissues. Transcript expression data, however, is harder to come by and this approach relies on a wealth of available data. Furthermore, transcript expression data can be straightforwardly converted to gene expression data (by summing over the transcripts), while the conversion of gene to transcript expression data is decidedly less accurate. When transcript-expression (CAGE) measurements are aggregated at the gene/protein level, measures of tissue-specificity have been found to largely (75-93%) match up with measures of tissue-specificity resulting from gene-expression measurements, as found in a comparison between the HPA and FANTOM5 experiments{cite}`Yu2015-uf`. 

For these reasons, I have taken a gene-centric approach here. It may be important, however, to consider whether a gene has multiple transcripts in downstream analysis, for example, if including tissue-specific gene expression information when predicting the function of a protein-coding SNV (since it may not be in the relevant transcript).

##### Inclusion of CAGE data
CAGE is transcript expression, rather than gene expression, and there are likely to be different transcripts measured by CAGE than by RNA-Seq. As mentioned above, however, it is possible to calculate gene expression from transcript expression. It’s also possible to map between CAGE transcription start sites and existing transcript IDs that may be featured in RNA-Seq arrays. When this is done, it has been observed that the results of CAGE are comparable to those of RNA-seq, so the inclusion of CAGE data in a combined dataset is reasonable.

“We found that the quantified levels of gene expression are largely comparable across platforms and conclude that CAGE and RNA-seq are complementary technologies that can be used to improve incomplete gene models”{cite}`Kawaji2014-tl`

#### Excluding disease-focused experiments
The decision to exclude disease-focused experiments was made primarily to reduce the complexity of the analysis and the resulting data set. The data set can now be interpreted as representing gene expression of healthy tissues. This was also a practical choice since most disease data sets (with the exception of cancer datasets) tended to have a narrow breadth of tissues. For example, experiments interested in heart disease would naturally contain measurements of healthy and non-healthy heart tissues, and not other tissues, so would be difficult to combine with existing data sets due to the "missing" data. This would not have been a proplem for cancer experiments, however cancer is known to be tissue-non-specific{cite}`Love2014-vx,Winter2004-rr`. 

### Method of searching
It would have been preferable to interrogate the GxA for datasets using the ExpressionAtlas R package, or the [AtlasExpress API](https://www.ebi.ac.uk/arrayexpress/help/programmatic_access.html) which it is built on. However, it was necessary to do so via the [website](https://www.ebi.ac.uk/gxa/experiments) since searches to the AtlasExpress API cannot differentiate between baseline and differential gene expression.  

For reproducibility, this was done by downloading [the json file](resources/gxa_experiments.json) used by the GxA experiment browser webservice and by choosing experiments with:
- baseline (rather than differential) expression measurements
- homo sapiens species
- RNA-Seq mRNA technology
- *organism part* as an experimental factor
- at least 80 assays. 
- no mention of "cancer" in the description

<!-- TODO: Add acquisition of Gtex extra data-->

libraries <- function(){
    library(httr)
    library(jsonlite)
    library(tidyverse)
    library(plotly)
    library(IRdisplay)
    library(ExpressionAtlas) 
    library(htmlwidgets)
}
suppressMessages(libraries())

analysis_date <- "2019-06-01"  #YYYY-mm-dd
min_assays <- 80

# Download data
gxa_json <- 'https://www.ebi.ac.uk/gxa/json/experiments'
req <- httr::GET(gxa_json)
text <- httr::content(req, "text", encoding="UTF-8")
gxa_experiment_info <- as_tibble(jsonlite::fromJSON(text)$experiments)

# All data at time of analysis:
gxa_experiment_info$loadDate <- as.Date(gxa_experiment_info$loadDate, "%d-%m-%Y")
gxa_experiment_info <- gxa_experiment_info %>% filter(loadDate<analysis_date)
funnel_info <- tibble(name="All experiments",
                      num_experiments=nrow(gxa_experiment_info))

# All next-gen sequencing experiments:
gxa_experiment_info<- gxa_experiment_info %>% 
  filter(technologyType=='RNA-Seq mRNA')
funnel_info <- funnel_info %>%
  add_row(name="RNA-Seq technology",
          num_experiments=nrow(gxa_experiment_info))

# All baseline expression experiments
gxa_experiment_info<- gxa_experiment_info %>%
  filter(experimentType=='Baseline')
baseline <- nrow(gxa_experiment_info)
funnel_info <- funnel_info %>%
  add_row(name="Baseline experiments",
          num_experiments=nrow(gxa_experiment_info))

# All human experiments
gxa_experiment_info<- gxa_experiment_info %>% 
  filter(species=='Homo sapiens')
funnel_info <- funnel_info %>%
  add_row(name="Human",
          num_experiments=nrow(gxa_experiment_info))

# All "organism part" experiments with > 80 assays:
gxa_experiment_info$experimentalFactors <- as.character(gxa_experiment_info$experimentalFactors)
gxa_experiment_info <- gxa_experiment_info %>% 
  filter(numberOfAssays>min_assays, 
         str_detect(experimentalFactors, 'organism part'))
funnel_info <- funnel_info %>%
  add_row(name="Contains tissues and >80 samples",
          num_experiments=nrow(gxa_experiment_info))

# Excluding cancer experiments:
gxa_experiment_info$experimentDescription <- as.character(gxa_experiment_info$experimentDescription)
gxa_experiment_info <- gxa_experiment_info %>% 
  filter(str_detect(experimentDescription,'[cC]ancer', negate=TRUE))
funnel_info <- funnel_info %>%
  add_row(name="Not cancer experiments",
          num_experiments=nrow(gxa_experiment_info))



create_fig <- function(){
    fig <- plot_ly()
    fig <- fig %>% add_trace(
        type = "funnel",
        y = as.character(funnel_info$name),
        x = as.integer(funnel_info$num_experiments))
    fig <- fig %>% layout(yaxis = list(categoryarray = as.character(funnel_info$name)))

    # orca(fig, 'figs/funnel.png', width=800)
    # IRdisplay::display_png(file='figs/funnel.png')
    # saveWidget(fig, "figs/funnel_interactive.html", selfcontained = FALSE)
    display(fig)
}

suppressWarnings(create_fig())

As {numref}`funnel-combine-gxa` shows, at the time of writing, there are over 3000 experiments in the GxA, and of these 27 are human baseline RNA-Seq experiments. Of these there are 4 which offer a good coverage of non-disease organism parts.

### Chosen data sets
[//]: # (TODO: cross-reference here, and maybe FANTOM5 should be in the background?)
The data sets that were chosen to be used in the combined data set are shown in {numref}`table-chosen-combine-gxa`, and described below.

gxa_experiment_info <- gxa_experiment_info %>% add_column(shortName=c("HPA", "FANTOM5", "GTEx", "HDBR")) %>% select(shortName, experimentAccession, experimentDescription, numberOfAssays, experimentalFactors)

head(gxa_experiment_info)

#### FANTOM5 
[//]: # (TODO: Explain FANTOM5 here in the same terms as the other projects and link to previous description.)
The FANTOM5 experiment was described in the previous chapter.

#### Human Protein Atlas
The Human Protein Atlas (HPA) project{cite}`Uhlen2010-mx,Uhlen2015-at` aims to map all human proteins in cells (including subcellular locations), tissues and organs. The HPA project’s data is not limited to the gene expression data that can be found in GxA, but that is the only part of the data that is used here. The gene expression data that was used (E-MTAB-2836 in GxA) excludes cell lines and includes tissue samples of 122 individuals and 32 different non-diseased tissue types. 

#### Genotype Tissue Expression
The Genotype Tissue Expression (GTEx) project{cite}`GTEx_Consortium2013-gl` was developed specifically for the purpose of studying tissue-specific gene expression in humans and gene expression data from over 18,000 samples, including 53 non-diseased tissue types and 550 individuals (ranging in age from 20s to 70s). 

#### Human Developmental Biology Resource
The Human Developmental Biology Resource (HDBR) Expression data{cite}`Lindsay2016-en` is slightly different from the other data sets in that contains a much narrower range of sample types. All HDBR samples are human brain samples at different stages of development, ranging from 3 to 20 weeks after conception.

(data-aquisition)=
### Data acquisition
Data was obtained, where possible via the *ExpressionAtlas* R package{cite}`Keays2018-pg`, which gives gene expression counts identified by ENSG IDs, metadata (containing pipeline, filtering, mapping and quantification information), and details of experimental design (containing for example organism part name, individual demographics, and replicate information, depending on the experiment). 

For the FANTOM experiment counts for transcript expression were downloaded directly [from the FANTOM website](http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/extra/CAGE_peaks_expression/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt.gz).  The downloaded FANTOM5 file has already undergone some quality control by FANTOM, it is limited to peaks which meet a “robust” threshold (>10 read counts and 1TPM for at least one sample).

<!-- TODO: turn back into a code cell IF I can make sure it doesn't get executed - takes forever-->
```{r}

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
```

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```