
## Background
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

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```