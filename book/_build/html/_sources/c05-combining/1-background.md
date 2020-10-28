
## Background

### Tissue and cell-specific gene expression
We’re yet to fully understand the intricacies of the human transcriptome, but if there is one factor that we know plays a huge role, it’s cell type. We know that the same DNA is in every cell, and yet the morphology and function of each cell is determined by its cell type, due to its gene expression. 

While we may prefer to look at the gene expression of a cell type, we currently have much less scRNA-seq data than bulk RNA-seq data. Bulk RNA-seq also gives us the ability to measure the gene expression of tissues as they appear in humans. The average supply of a protein to a tissue (averaged over multiple cell types) may well influence a tissue’s phenotype, in these circumstances gene expression at the level of a tissue may give us information that we can’t retrieve from cell-line cells.

Figure 17:  Images of smooth muscle tissue from the stomach wall (left) and lung tissue (right), examples of homogeneous and heterogeneous tissue types respectively, taken from the Human Tissue Atlas website(The Human Protein Atlas ).

Tissues can be made up of various cell types. Some tissue types (e.g. smooth muscle) are quite homogeneous, comprising of predominantly one cell type and/or lacking structural features. Other tissues (e.g. lung) are heterogeneous, consisting of multiple cell types and features. Figure 17 shows the different structure of two example tissue types. The bronchioles of the lung alone consist of six different cell types (basal cells, neuroendocrine cells, ciliated cells, serous cells, Clara cells and goblet cells), while smooth muscle tissue consists almost exclusively of tightly packed smooth muscle cells. The varying proportions of constituent cell types in heterogeneous tissues can influence tissue function.

Tissue and cell type is only one source of variation in gene expression, which can also vary by, for example, individual organism{cite}`Cortijo2019-wi`, age{cite}`vinuela2018age,Yang2015-mo`, sex{cite}`Reinius2009-ir,Stone2019-fk`, time of day{cite}`Cortijo2019-wi,Schibler2007-jx`, and spatial location within a tissue or culture{cite}`Svensson2018-oa`. There are also interactions between these different sources of variation, for example certain genes may only exhibit differential expression based on time of day in certain cell types.

Such information can be used to check if genes are expressed in a given cell/tissue, which may indicate the gene function, to identify housekeeping genes, and to build models of gene regulatory networks. 

### Why one experiment isn’t enough - why combine gene expression data
Falling costs and rapid advances in sequencing technologies have resulted in what many have described as a deluge of -omics data{cite}`Bell2009-uq`. For a typical (human) next-generation sequencing transcriptomics experiment, data will be collected for 20,000+ genes, but generally far fewer samples, and very few replicates of a certain kind of sample (e.g. tissue). For context, the largest experiment in the Ensembl Gene Expression Atlas (GxA) is the Genotype-Tissue Expression (GTEx) Project with 18736 samples, but this is of course across many tissues. This is another example of data which is subject to the curse of dimensionality.

There is general agreement that integrating omics datasets is one of the primary challenges to overcome if we wish to harness the full information contained within them{cite}`Gomez-Cabrero2014-gk`. When it comes to gene expression, we have “big data”, but not enough and not appropriately aggregated to answer the questions we wish to answer. Having more repeated measurements, and more variation in samples would allow researchers to apply additional statistical techniques, and ask additional questions. Combining gene expression data sets, however, is not trivial: a major problem is their well known susceptibility to batch effects (differences in measurements due to technical artefacts of sequencing batch) {cite}`Leek2010-yw`. There are also further problems, for example, having enough meaningful information recorded per sample, access to data in raw count format, and mapping between the data that is given and similar samples in other datasets, as well as computational problems (data storage, optimisation of running operations on many or large files, etc). 

Due to these complications, many of the important questions that we seek to answer through gene expression are difficult to get an accurate measurement of. However, batch correction methodologies, biological ontologies, and curated databases of gene expression data are constantly evolving, and are now at a point where combining datasets in order to get an improved global picture of gene expression is feasible. Attempting to combine datasets has the added bonus of contributing to the accuracy of these databases and ontologies by drawing attention to inconsistencies.


---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```