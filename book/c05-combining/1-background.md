# Background
[//]: # (TODO: Make sure I have already mentioned "omics" - or put it in a margin)

There is general agreement that integrating omics datasets is one of the primary challenges to overcome if we wish to harness the full information contained within them{cite}`Gomez-Cabrero2014-gk`. 
Combining gene expression data sets is a challenge in terms of data management, statistics, and harmonisation of meta-data for interoperability.
The latter is crucial for downstream use as we'll see in {ref}`the next Chapter<c06-filter>`. 

## Motivation: linking Genotype and phenotype
As we explored in {ref}`Chapter 2<c02-biology-bg>`, there is a complex web of interactions between proteins and other molecular machinery that lead to phenotype. 

[//]: # (TODO: Check: Have I mentioned pathways before?)
The {ref}``inconclusive results of the `Snowflake`<snowflake-results>`` led me to pursue an answer to a much smaller piece of the genotype-to-phenotype puzzle. 
As mentioned in {ref}`the previous Chapter's discussion<dcgo-expression-problem>`, it could be possible that some predictions of a protein's phenotype are incorrect because the protein is not produced, even though they do have a structure that means that they could be involved in the pathway if they were present.
To understand if this is the case, we need to know as a minimum if a gene is *ever* expressed a relevant context. 
This would rule out, for example, proteins that are predicted to be associated with eye health, but are only ever produced in the developing limbs.

[//]: # (TODO: Cross-ref to descriptions of other phenotype prediction and variant prioritisation methods)
And if we could apply this approach to `Snowflake`, then we could also apply it to other phenotype prediction and variant prioritisation methods.
Furthermore, having access to a (combined) data set with more repeated measurements, and more variation in samples would allow researchers to apply additional statistical techniques, and ask additional questions, by increasing the statistical power. 
For example, tissue-specific data sets are often used to identify housekeeping genes, and to build models of gene regulatory networks. 

## Tissue-specific gene expression data
[//]: # (TODO: Check: Have I mentioned EMBL before? Don't have to write long name)

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

[//]: # (TODO: Preliminary work: show basic coverage of one data set - for gene expression only: over UBERON. Note: coverage can be improved by mapping phenotypes: tissues as well as increasing gene expression data)

## Challenges in combining data sets
Combining expression data from many different experiments has the potential to create a data set containing a more representative view of gene expression. 
This has already been done for two experiments{cite}`Wang2018-rz`. 

### Harmonising meta-data
[//]: # (TODO: Link to earlier explanation of ontologies)
Data about samples was recorded at different levels of specificity.
This was a particular challenge for tissue where some samples are simply labelled "brain", while others are labelled "medulla oblongata", and yet others are identified by cell type.
Harmonising this cell and tissue meta-data was one of the challenges of combining this data set, which was done using the Uberon cross-species anatomy ontology{cite}`Mungall2012-nc`, and the Cell Ontology{cite}`Malladi2015-iq` (CL), which is integrated with Uberon. 
Samples were primarily assigned Uberon term identifiers by searching for matching text between sample information files and CL or Uberon term names or descriptions.
Where existing terms did not turn up a match, samples were assigned an Uberon term by hand.
Then using the Uberon ontology, tissues could be understood in relation to each other, being mapped to tissues and more general tissue groups.

### Batch effects
[//]: # (TODO: Check if batch effects are mentioned previously)
Combining gene expression data sets, however, is not trivial: a major problem is their well known susceptibility to batch effects (differences in measurements due to technical artefacts of sequencing batch){cite}`Leek2010-yw`. 
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

There are a number of batch correction analyses which attempt to remove batch effects from RNA-seq data, for example ComBat{cite}`Johnson2007-zh` and Surrogate Variable Analysis (SVA){cite}`Leek2007-ba`
Batch correction can be very useful for understanding baseline gene expression, but can lead to inflated p-values for downstream analysis (notably for differential gene expression, using ComBat{cite}`Johnson2007-zh`), where a more sensible approach is to include batch as a confounder for statistical tests. 

(combat-description)=
#### ComBat
[//]: # (TODO: Explain need for "balanced experimental design")
ComBat{cite}`Johnson2007-zh` is a popular batch effect removal procedure, which was first developed for use with microarray data, but continues to be a popular choice for RNA-seq data. 
Generally, it is a well-trusted method for both of these types of gene expression data{cite}`Chen2011-ke`, although there is some evidence that it may “over-correct” batches for some RNA-seq data{cite}`Liu2016-wa`.

ComBat is an Empirical Bayes method, meaning that the prior distribution is estimated from the data. 
It is designed to “borrow/share information” between genes in order to get a better estimate of batch effects, and assumes that batch effects affect many genes in similar ways.

#### PCA to visualise batch effect removal
Principal Components Analysis (PCA) is often used to visually inspect experimental results for batch effects; when biologically alike samples cluster together rather than those from like-batches, batch effects are often ignored. 
In order to do this, we must also have enough meaningful information recorded per sample, access to data in raw count format, and mapping between the data that is given and similar samples in other datasets, as well as computational problems (data storage, optimisation of running operations on many or large files, etc). 

[//]: # (TODO: Make sure I have mentioned transcriptome: do it in an aside if I haven't already)
Cell type is one of the better understood influences on gene expression. 
We know that the same DNA is in every cell, and yet the morphology and function of each cell is determined by its cell type, due to its gene expression. 
We can expect largely similar patterns of gene expression in similar cell types, which means that when we know cell type of samples, this information can be used to aid in visually checking the results of batch correction using PCA.
