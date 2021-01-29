# Background
[//]: # (TODO: Edit down: too long)
[//]: # (TODO: Write here: the basic idea - combined gene expression data set with as much meta data as possible: unaltered and with batch effect correction)
[//]: # (TODO: Add link to FILP)
[//]: # (TODO: cross ref to Ch3)
[//]: # (TODO: Rewrite: combine motivation and why 1 exp isn't enough: so much overlap!)
[//]: # (TODO: Make sure I have already mentioned "omics" - or put it in a margin)
[//]: # (TODO: Check: Have I mentioned EMBL before?)
[//]: # (TODO: Check: Have I mentioned pathways?)
[//]: # (TODO: Check: is simulated data set available?)
## Motivation

### Genotype to phenotype
As we explored in {ref}`Chapter 2<c02-biology-bg>`, there is a complex web of interactions between proteins and other molecular machinery that lead to phenotype. 

The {ref}`inconclusive results of the Snowflake<snowflake-results>` led me to pursue an answer to a much smaller piece of the genotype-to-phenotype puzzle. 
As mentioned in {ref}`the previous Chapter's discussion<dcgo-expression-problem>`, it could be possible that some predictions of a protein's phenotype are incorrect because the protein is not produced, even though they do have a structure that means that they could be involved in the pathway if they were present.
To understand if this is the case, we need to know as a minimum if a gene is *ever* expressed a relevant context. 
This would rule out, for example, proteins that are predicted to be associated with eye health, but are only ever produced in the developing limbs.

### Tissue-specific gene expression data
To answer these questions, we need gene expression data.
Falling costs and rapid advances in sequencing technologies have resulted in what many have described as a deluge of omics data{cite}`Bell2009-uq`. 
And this includes huge amount of {ref}`gene expression data<rna-measurements>`, as demonstrated by the 3,564 studies and 112,225 assays currently available through the European Molecular Biology Laboratory's (EMBL) Gene Expression Atlas (GxA) website {cite}`Petryszak2016-je`.

Yet each individual measure of expression is only a snapshot of what a gene can do. 
It only tells us about the transcription of proteins at that one time, in that one sample.
Gene expression can also vary by tissue and cell type, individual organism{cite}`Cortijo2019-wi`, age{cite}`vinuela2018age,Yang2015-mo`, sex{cite}`Reinius2009-ir,Stone2019-fk`, time of day{cite}`Cortijo2019-wi,Schibler2007-jx`, and spatial location within a tissue or culture{cite}`Svensson2018-oa`. 
There are also interactions between these different sources of variation, for example certain genes may only exhibit differential expression based on time of day in certain cell types.
If we want a full understanding of what a gene does, we must understand how it's expressed in a variety of scenarios, for example, in different tissues, from different people, at different times of day, and across many repeats. 

Many phenotypes are naturally linked to certain locations.
Humans have many diseases and features which are particular to certain locations on the body and certain tissues, be it blood, brain, skin, or lung.
So to answer the question of whether a protein is produced in a context relevant to a phenotype, we not only need gene expression information, but *tissue-specific* gene expression information: is this gene ever expressed in the heart?

For a typical (human) next-generation sequencing transcriptomics experiment, data is collected for over 20,000 genes, but generally far fewer samples, and very few replicates of a certain kind of sample (e.g. tissue). 
For context, the largest experiment in the Ensembl Gene Expression Atlas (GxA) is the Genotype-Tissue Expression (GTEx) Project with 18736 samples.
It is currently too expensive for one experiment to measure enough samples to give us a comprehensive understanding of how genes can behave.
So, when it comes to gene expression, we have “big data” because we are measuring so many genes, but in any one experiment we don't collect enough to have a deep understanding of how these genes behave in different contexts.

## The Approach
### Combining data sets
Combining expression data from many different experiments has the potential to create a data set containing a more representative view of gene expression. 
This has already been done for two experiments{cite}`Wang2018-rz`. 

### Batch effects
[//]: # (TODO: Check if batch effects are mentioned previously)
Combining gene expression data sets, however, is not trivial: a major problem is their well known susceptibility to batch effects (differences in measurements due to technical artefacts of sequencing batch) {cite}`Leek2010-yw`. 
When combining and comparing gene expression data from two (or more) experiments, it's not obvious how much of our signal comes from real biological differences in transcription, and how much comes from unwanted variation associated with the batch it was sequenced in, resulting from unknown variation during the process of sequencing for example the date, time, or location of sequencing{cite}`Irizarry2005-ie`, or the technician doing the work

To complicate matters, some batch effects may be due to factors that might be expected to genuinely influence expression of genes, such as temperature, time of year, humidity, diet, individual, age, etc.
Covariates such as these are often unrecorded and/or not reported, so it is not easy to distinguish these from those due to protocol differences, such as reagents, personnel doing the sequencing, hardware, processing pipeline, etc. 
As such the problem of batch effects is closely related to the problem of recording sample metadata. 

Batch effects can often confound and obscure the biological differences of interest between samples (e.g. tumour versus healthy tissue). 
At best, batch effects add random variation to expression measurements, which obscure signals. 
Often they can also add systematic differences that can lead to incorrect biological conclusions{cite}`Leek2010-yw`. 
They are a problem for analysing the output of an individual experiment where there are multiple sequencing batches, but pose a particular problem in combining data from different experiments, as there is almost certainly more variations between analysis pipelines.
 
### Batch effect correction
Batch effects may affect only specific subsets of genes, and may affect different genes in different ways{cite}`Leek2010-yw`. This means that {ref}`normalisation<rna-normalisation>` (e.g. TPM, FKPM) will not account for batch.
However, when it is known, date of sequence processing is often used as a surrogate for batch, enabling researchers to check for, and then remove, batch effects if necessary. 

Principal components analysis is often used to visually inspect experimental results for batch effects; when biologically alike samples cluster together rather than those from like-batches, batch effects are often ignored. 
In order to do this, we must also have enough meaningful information recorded per sample, access to data in raw count format, and mapping between the data that is given and similar samples in other datasets, as well as computational problems (data storage, optimisation of running operations on many or large files, etc). 

#### Combat
[//]: # (TODO: Explain ComBat here)


#### Using tissue metadata to aid in batch correction
[//]: # (TODO: Make sure I have mentioned transcriptome: do it in an aside if I haven't already)

Cell type is one of the better understood influences on gene expression. 
We know that the same DNA is in every cell, and yet the morphology and function of each cell is determined by its cell type, due to its gene expression. 
So, we can expect largely similar patterns of gene expression in similar cell types.
This means that it can be used to aid in checking the results of batch correction.

[//]: # (TODO: ADd in image, cite and cross-ref)
Figure 17:  Images of smooth muscle tissue from the stomach wall (left) and lung tissue (right), examples of homogeneous and heterogeneous tissue types respectively, taken from the Human Tissue Atlas website(The Human Protein Atlas ).

Tissues can be made up of various cell types. 
Some tissue types (e.g. smooth muscle) are quite homogeneous, comprising of predominantly one cell type and/or lacking structural features. 
Other tissues (e.g. lung) are heterogeneous, consisting of multiple cell types and features. Figure 17 shows the different structure of two example tissue types. 
The bronchioles of the lung alone consist of six different cell types (basal cells, neuroendocrine cells, ciliated cells, serous cells, Clara cells and goblet cells), while smooth muscle tissue consists almost exclusively of tightly packed smooth muscle cells. 
The varying proportions of constituent cell types in heterogeneous tissues can influence tissue function.

## Approach
There is general agreement that integrating -omics datasets is one of the primary challenges to overcome if we wish to harness the full information contained within them{cite}`Gomez-Cabrero2014-gk`. 

Experiments are chosen such that it is possible to apply batch effect removal techniques to ensure that these batch effects are minimised.

The resulting data set would be useful beyond the specific context of the Snowflake phenotype predictor, but in many contexts where we hope to understand gene function: for example variant prioritisation, or as input to machine learning solutions.
Having more repeated measurements, and more variation in samples would allow researchers to apply additional statistical techniques, and ask additional questions. 

Tissue-specific data set information can be used to check if genes are expressed in a given cell/tissue, which may indicate the gene function, to identify housekeeping genes, and to build models of gene regulatory networks. 

