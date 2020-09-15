(c05-combining)=
# Combining RNA-seq datasets

This chapter describes my attempts to create a simulated tissue-specific dataset and to combine gene expression data from 4 large tissue-specific RNA-Seq experiments. All work in this chapter is my own.

[//]: # (TODO: Explain the structure of this chapter here)
[//]: # (TODO: Add figures)
[//]: # (TODO: Update config to include notebooks)

## Introduction and background
Gene expression data measures the number of transcribed proteins in a sample at a specific time. It's a popular experimental technique as demonstrated by the 3,564 studies and 112,225 assays currently available on Gene Expression Atlas website(Petryszak et al. 2016). Researchers use this data to characterise gene function.

Yet each individual measure of expression is only a snapshot of what a gene can do. It only tells us about the transcription of proteins at that one time. If we want a full understanding of what a gene does, we must understand how it's expressed in a variety of scenarios. For example, in different tissues, from different people, at different times of day, and across many repeats. That kind of data would allow us to answer questions that aren't currently possible. Data to enable this is not easy to come by. It would be too expensive for one experiment to measure so many samples. 

Combining expression data from many different experiments could overcome this problem. There are already an example of this happening for two experiments(Wang et al. 2018). It would result in the rich information about genes that we desire. Unfortunately, this approach reveals another problem: batch effects. Batch effects are measurement artifacts that appear due to differences in experimental protocol. Their prevalence makes gene expression experiments very difficult to compare or combine.

This chapter combines four gene expression data sets, collating sample and tissue information about them into a common format. A simulated dataset for tissue-specific batch-effected data is created as a starting point for exploring batch effect removal for this combined dataset.

### Tissue and cell-specific gene expression
We’re yet to fully understand the intricacies of the human transcriptome, but if there is one factor that we know plays a huge role, it’s cell type. We know that the same DNA is in every cell, and yet the morphology and function of each cell is determined by its cell type, due to its gene expression. 

While we may prefer to look at the gene expression of a cell type, we currently have much less scRNA-seq data than bulk RNA-seq data. Bulk RNA-seq also gives us the ability to measure the gene expression of tissues as they appear in humans. The average supply of a protein to a tissue (averaged over multiple cell types) may well influence a tissue’s phenotype, in these circumstances gene expression at the level of a tissue may give us information that we can’t retrieve from cell-line cells.


Figure 17:  Images of smooth muscle tissue from the stomach wall (left) and lung tissue (right), examples of homogeneous and heterogeneous tissue types respectively, taken from the Human Tissue Atlas website(The Human Protein Atlas ).

Tissues can be made up of various cell types. Some tissue types (e.g. smooth muscle) are quite homogeneous, comprising of predominantly one cell type and/or lacking structural features. Other tissues (e.g. lung) are heterogeneous, consisting of multiple cell types and features. Figure 17 shows the different structure of two example tissue types. The bronchioles of the lung alone consist of six different cell types (basal cells, neuroendocrine cells, ciliated cells, serous cells, Clara cells and goblet cells), while smooth muscle tissue consists almost exclusively of tightly packed smooth muscle cells. The varying proportions of constituent cell types in heterogeneous tissues can influence tissue function.

Tissue and cell type is only one source of variation in gene expression, which can also vary by, for example, individual organism[81], age[82,83], sex[84,85], time of day[81,86], and spatial location within a tissue or culture[87]. There are also interactions between these different sources of variation, for example certain genes may only exhibit differential expression based on time of day in certain cell types.

Such information can be used to check if genes are expressed in a given cell/tissue, which may indicate the gene function, to identify housekeeping genes, and to build models of gene regulatory networks. 

### Why one experiment isn’t enough - why combine gene expression data
Falling costs and rapid advances in sequencing technologies have resulted in what many have described as a deluge of -omics data[88]. For a typical (human) next-generation sequencing transcriptomics experiment, data will be collected for 20,000+ genes, but generally far fewer samples, and very few replicates of a certain kind of sample (e.g. tissue). For context, the largest experiment in the Ensembl Gene Expression Atlas (GxA) is the Genotype-Tissue Expression (GTEx) Project with 18736 samples, but this is of course across many tissues. This is another example of data which is subject to the curse of dimensionality.

There is general agreement that integrating omics datasets is one of the primary challenges to overcome if we wish to harness the full information contained within them[89]. When it comes to gene expression, we have “big data”, but not enough and not appropriately aggregated to answer the questions we wish to answer. Having more repeated measurements, and more variation in samples would allow researchers to apply additional statistical techniques, and ask additional questions. Combining gene expression data sets, however, is not trivial: a major problem is their well known susceptibility to batch effects (differences in measurements due to technical artefacts of sequencing batch) [50]. There are also further problems, for example, having enough meaningful information recorded per sample, access to data in raw count format, and mapping between the data that is given and similar samples in other datasets, as well as computational problems (data storage, optimisation of running operations on many or large files, etc). 

Due to these complications, many of the important questions that we seek to answer through gene expression are difficult to get an accurate measurement of. However, batch correction methodologies, biological ontologies, and curated databases of gene expression data are constantly evolving, and are now at a point where combining datasets in order to get an improved global picture of gene expression is feasible. Attempting to combine datasets has the added bonus of contributing to the accuracy of these databases and ontologies by drawing attention to inconsistencies.
### Batch-effect removal 
There are a number of batch correction analyses which attempt to remove batch effects from RNA-seq data. Batch correction can be very useful for understanding baseline gene expression, but can lead to inflated p-values for downstream analysis (notably for differential gene expression, using ComBat[90]), where a more sensible approach is to include batch as a confounder for statistical tests. 

#### Surrogate Variable Analysis
Surrogate Variable Analysis (SVA)[91] is used in cases where you do not have a covariate that drives batch effect (i.e. you do not have information about processing date, technicians, processing centres, etc), but you expect that batch effects will be present. SVA estimates which samples belong to which batches, before using ComBat to remove the effect due to those batches.

#### ComBat
ComBat[90] is a popular batch effect removal procedure, which was first developed for use with microarray data, but continues to be a popular choice for RNA-seq data. Generally, it is a well-trusted method for both of these types of gene expression data[92], but more recently has been shown to “overcorrect” batches for RNA-seq data[93].

ComBat is an Empirical Bayes method, meaning that the prior distribution is estimated from the data. It is designed to “borrow/share information” between genes in order to get a better estimate of batch effects, and assumes that batch effects affect many genes in similar ways. 

## Data
### Criteria for choosing datasets
Datasets were chosen from the EBI’s Gene Expression Atlas (GxA). A major benefit of the GxA is that experiments using the same sequencing technology are re-analysed by GxA using the same data analysis pipeline (iRAP[94] for RNA-Seq). In addition to ensuring the quality of each dataset included, and running it through the same pipeline, the GxA adds additional metadata for the experiments by using the literature to biologically and technically annotate each sample. 

Datasets from the GxA were chosen based on the following requirements: 
Next generation sequencing, including RNA-Seq and CAGE (no microarrays).
Breadth of tissues and genes included (after quality control) to aid batch correction by facilitating the most balanced dataset design in terms of batch (experiment) to group (tissue), and in order to have good coverage of genes and tissues, which is necessary for downstream use.

Not disease-focused. In order to reduce the complexity of the analysis and the interpretation of the resulting dataset, samples of diseased tissues or cell lines were discarded. Experiments where the focus of the dataset was to investigate a particular disease or classes of diseases were discarded. Besides reducing the complexity of the analysis, this choice also made sense based on the previous guideline, since most disease datasets (with the exception of cancer datasets) tended to have a narrow breadth of tissues. I feel that including disease gene expression would be a natural extension to this work if the data allowed for it, but most GxA baseline gene expression experiments which listed organism part as a variable were focused on cancer, which is known to be tissue-non-specific[49,77].

Of the over 3000 experiments in the GxA, 1134 contain human samples, and just less than 3% of those (30 experiments) are baseline gene expression experiments. Of these there are 4 which offer a good coverage of non-disease organism parts. The data sets that were chosen to be used in the combined data set are detailed below.

#### Measures of gene expression
As described in the introduction chapter, there are many ways to measure which proteins are being created. Here, I justify my choices of measures to include in the combined dataset.

##### Gene expression vs protein abundance
Gene expression levels are not necessarily strongly correlated with protein abundance; this has been found in mice[95], yeast[96], and human[97]. In human, spearman correlations between protein abundance and gene expression levels vary between 0.36 and 0.50, depending on tissue, meaning that they are only weakly or moderately correlated[97].
There are many interacting reasons why this is the case. One reason is that there is something preventing the mRNA from being translated, such as slow codons, the temperature, ribosome occupancy, or regulatory RNAs and proteins[98]. In these cases, the DNA is transcribed into mRNA, but the protein is never produced, meaning that using gene expression data as a measure of how much protein is produced would be overestimating the protein abundance. If these factors were a large contribution to the weak correlation, it could provide better results to use protein abundance data instead of mRNA abundance data to make predictions about how proteins are affecting human phenotypes.
On the other hand, it could equally be possible that proteins are being produced, but not measured by protein abundance techniques. Protein half-lives range over orders of magnitude from seconds to days[98,99]. In this case, gene expression data may be a more reliable measure of protein production than protein abundance, since proteins may degrade before being measured. In yeast, protein degradation was shown to be the largest contribution to the protein-mRNA correlation compared to codon and amino acid usage (the two other factors estimated in the study), and more influential than those other two factors combined[100].
In summary, there's no perfect measure of translation, but since gene expression data is more readily available, and protein degradation appears to account for most of the differences between correlations, gene expression data presents the best proxy for translation for the downstream uses discussed here.
##### Gene expression vs Transcript expression
It's likely that transcript expression data would provide more insight than gene expression data if it were available, since it is likely that there are tissue-specific transcripts which do not correspond to tissue-specific genes, e.g. where different transcripts from the same gene are expressed in different tissues. Transcript expression data, however, is harder to come by and this approach relies on a wealth of available data. Furthermore, transcript expression data can be straightforwardly converted to gene expression data (by summing over the transcripts), while the conversion of gene to transcript expression data is decidedly less accurate. When transcript-expression (CAGE) measurements are aggregated at the gene/protein level, measures of tissue-specificity have been found to largely (75-93%) match up with measures of tissue-specificity resulting from gene-expression measurements, as found in a comparison between the HPA and FANTOM5 experiments[101]. 
For these reasons, I have taken a gene-centric approach here. It may be important, however, to consider whether a gene has multiple transcripts in downstream analysis, for example, if including tissue-specific gene expression information when predicting the function of a protein-coding SNV (since it may not be in the relevant transcript).

##### Inclusion of CAGE data
CAGE is transcript expression, rather than gene expression, and there are likely to be different transcripts measured by CAGE than by RNA-Seq. As mentioned above, however, it is possible to calculate gene expression from transcript expression. It’s also possible to map between CAGE transcription start sites and existing transcript IDs that may be featured in RNA-Seq arrays. When this is done, it has been observed that the results of CAGE are comparable to those of RNA-seq, so the inclusion of CAGE data in a combined dataset is reasonable.

“We found that the quantified levels of gene expression are largely comparable across platforms and conclude that CAGE and RNA-seq are complementary technologies that can be used to improve incomplete gene models”[102]

### Chosen data sets
In addition to the FANTOM5 data (described in the previous chapter), three other large gene expression experiments were chosen:

#### Human Protein Atlas
The Human Protein Atlas (HPA) project[103,104] aims to map all human proteins in cells (including subcellular locations), tissues and organs. The HPA project’s data is not limited to the gene expression data that can be found in GxA, but that is the only part of the data that is used here. The gene expression data that was used (E-MTAB-2836 in GxA) excludes cell lines and includes tissue samples of 122 individuals and 32 different non-diseased tissue types. 

#### Genotype Tissue Expression
The Genotype Tissue Expression (GTEx) project[105] was developed specifically for the purpose of studying tissue-specific gene expression in humans and gene expression data from over 18,000 samples, including 53 non-diseased tissue types and 550 individuals (ranging in age from 20s to 70s). 

#### Human Developmental Biology Resource
The Human Developmental Biology Resource (HDBR) Expression data[106] is slightly different from the other data sets in that contains a much narrower range of sample types. All HDBR samples are human brain samples at different stages of development, ranging from 3 to 20 weeks after conception. 

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```