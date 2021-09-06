(combiningintro)=
# Introduction
[//]: # (TODO: Put basically an abstract in this space between title and motivation)
<!--
The included experiments were chosen to minimise differences between data pipelines (which could be a source of data artefacts), to maximise information about different tissues, and to ensure that we have as balanced an "experimental design" as possible (which is important for batch effect removal).

In order to ensure the interoperability of the final combined data set, the meta-data about the experiments is also combined, and mapped to the Uberon tissue ontology, using the Ontolopy package developed for this task, described in {ref}`the previous chapter<c06-ontolopy>`. 
-->

(combmotivation)=
## Motivation

There is general agreement that integrating omics datasets is one of the primary challenges to overcome if we wish to harness the full information contained within them{cite}`Gomez-Cabrero2014-gk`. 
Falling costs and rapid advances in sequencing technologies have resulted in what many have described as a deluge of omics data{cite}`Bell2009-uq`. 
And this includes huge amount of {ref}`gene expression data<rna-measurements>`, as demonstrated by the 3,564 studies and 112,225 assays currently available through the European Molecular Biology Laboratory's (EMBL) Gene Expression Atlas (GxA) website {cite}`Petryszak2016-je`.

Each individual measure of expression is only a snapshot of what a gene can do. 
It only tells us about the transcription of proteins at that one time, in that one sample.
Gene expression can also vary by tissue and cell type, individual organism{cite}`Cortijo2019-wi`, age{cite}`vinuela2018age,Yang2015-mo`, sex{cite}`Reinius2009-ir,Stone2019-fk`, time of day{cite}`Cortijo2019-wi,Schibler2007-jx`, and spatial location within a tissue or culture{cite}`Svensson2018-oa`. 
There are also interactions between these different sources of variation, for example certain genes may only exhibit differential expression based on time of day in certain cell types.
If we want a full understanding of what a gene does, we must understand how it's expressed in a variety of scenarios, for example, in different tissues, from different people, at different times of day, and across many repeats. 

My primary motivation in the creation of this data set was to aid in protein function prediction, since {ref}`as we saw in chapter 4<dcgo-expression-problem>`, when we use structural information to predict function, we don't have enough information about ways in which that structure might be prevented from functioning in certain tissues.
Many phenotypes are naturally linked to certain locations.
Humans have many diseases and features which are particular to certain locations on the body and certain tissues, be it blood, brain, skin, or lung.
So to answer the question of whether a protein is produced in a context relevant to a phenotype, we not only need gene expression information, but *tissue-specific* gene expression information: is this gene ever expressed in the heart?

For our need in mapping tissue-specific gene expression data to phenotypes, preliminary work showed that one gene expression experiment was not sufficient: it would not give us enough coverage of phenotypes to validate an improvement in protein function prediction in CAFA.

For a typical (human) next-generation sequencing transcriptomics experiment, data is collected for over 20,000 genes, but generally far fewer samples, and very few replicates of a certain kind of sample (e.g. tissue). 
For context, the largest experiment in the Ensembl Gene Expression Atlas (GxA) by quite a margin is currently the Genotype-Tissue Expression (GTEx) Project with 18736 samples.
This is simply because it is still too expensive for one experiment to measure enough samples to give us a comprehensive understanding of how genes can behave.
So, when it comes to gene expression, we have “big data” in the sense that the data is large and we need to take care to access and compute on it efficiently (as we are measuring so many genes), but in any one experiment we don't have great coverage of sample types.

[//]: # (TODO: Using only dcGO + ontolopy + FANTOM data, how many terms + proteins can we say something about? Why is that not enough? How many CAGI training set would that tell us about? Preliminary work: show basic coverage of one data set - for gene expression only: over UBERON. Note: coverage can be improved by mapping phenotypes: tissues as well as increasing gene expression data)

Combining expression data from multiple different experiments is perhaps the obvious tonic to this problem, since it has the potential to create a data set containing a more representative view of gene expression.
However, it is not as straightforward as loading in multiple data sets.
There are specific challenges relating to data management, statistics, and harmonisation of meta-data for interoperability.
However it is possible, and has already been done for two experiments{cite}`Wang2018-rz`. 

Although my aim in creating this data set was specifically to improve phenotype and protein function prediction, a larger gene expression data set has further uses outside of this.
Additional repeated measurements, and a larger spread of samples would allow researchers to ask more questions and have a larger statistical power.
For example, one possible use is identification of housekeeping genes, or building models of gene regulatory networks.

(combchallenges)=
## Challenges in combining gene expression data sets
Challenges in combining gene expression data arise from the myriad of possible differences in experimental and analysis protocols between gene expression experiments. 

(harmonisingchallenge)=
### Harmonising meta-data
An important feature of any gene expression data set is the quality of the meta-data, by which I mean everything except the measures of gene expression, particularly including additional information about samples and protocols. 
For example, data about samples can be recorded at different levels of specificity.
This was a particular challenge for tissue type labels where some samples are simply labelled *brain*, while others are labelled *medulla oblongata*, and yet others are identified by cell type.

[//]: # (TODO: Move following paragraph to data wrangling?)
Harmonising this cell and tissue meta-data was the challenges of combining the data sets, which was done using the Uberon cross-species anatomy ontology{cite}`Mungall2012-nc`, and the Cell Ontology{cite}`Malladi2015-iq` (CL), which is integrated with Uberon. 
Samples were primarily assigned Uberon term identifiers by searching for matching text between sample information files and CL or Uberon term names or descriptions.
Where existing terms did not turn up a match, samples were assigned an Uberon term by hand.
Then using the Uberon ontology, tissues could be understood in relation to each other, being mapped to tissues and more general tissue groups.

(batchchallenge)=
### Batch effects
[//]: # (TODO: Check if batch effects are mentioned previously)
Combining gene expression data itself, is also not trivial: a major problem is their well known susceptibility to batch effects (differences in measurements due to technical artefacts of sequencing batch){cite}`Leek2010-yw`. 
When combining and comparing gene expression data from two (or more) experiments, it's not obvious how much of our signal comes from real biological differences in transcription, and how much comes from unwanted variation associated with the batch it was sequenced in.
These "batch effects" result from unknown variation during the process of sequencing for example the date, time, or location of sequencing{cite}`Irizarry2005-ie`, or the technician doing the work.

To complicate matters, some batch effects may be due to factors that might be expected to genuinely influence expression of genes, such as temperature, time of year, humidity, diet, individual, age, etc.
Covariates such as these are often unrecorded and/or not reported, so it is not easy to distinguish these from those due to protocol differences, such as reagents, personnel doing the sequencing, hardware, processing pipeline, etc. 
For this reason, the problem of batch effects is closely related to the problem of recording sample metadata. 

Batch effects can often confound and obscure the biological differences of interest between samples (e.g. tumour versus healthy tissue). 
At best, batch effects add random variation to expression measurements, which obscure signals. 
Often they can also add systematic differences that can lead to incorrect biological conclusions{cite}`Leek2010-yw`. 
They are a problem for analysing the output of an individual experiment where there are multiple sequencing batches, but pose a particular problem in combining data from different experiments, as there is almost certainly more variations between analysis pipelines.
 
(batch-effect-correction)=
**Batch-effect correction:**


Batch effects may affect only specific subsets of genes, and may affect different genes in different ways{cite}`Leek2010-yw`. 
This means that {ref}`normalisation<rna-normalisation>` (e.g. TPM, FKPM) will not account for batch.
However, when it is known, date of sequence processing is often used as a surrogate for batch, enabling researchers to check for, and then remove, batch effects if necessary. 

There are a number of batch correction analyses which attempt to remove batch effects from RNA-seq data, for example ComBat{cite}`Johnson2007-zh` and Surrogate Variable Analysis (SVA){cite}`Leek2007-ba`
Batch correction can be very useful for understanding baseline gene expression, but can lead to inflated p-values for downstream analysis (notably for differential gene expression, using ComBat{cite}`Johnson2007-zh`), where a more sensible approach is to include batch as a confounder for statistical tests. 

(combat-description)=
**ComBat:**


[//]: # (TODO: Explain need for "balanced experimental design")

ComBat{cite}`Johnson2007-zh` is a popular batch effect removal procedure, which was first developed for use with microarray data, but continues to be a popular choice for RNA-seq data. 
Generally, it is a well-trusted method for both of these types of gene expression data{cite}`Chen2011-ke`, although there is some evidence that it may “over-correct” batches for some RNA-seq data{cite}`Liu2016-wa`.

ComBat is an Empirical Bayes method, meaning that the prior distribution is estimated from the data. 
It is designed to “borrow/share information” between genes in order to get a better estimate of batch effects, and assumes that batch effects affect many genes in similar ways.

**PCA to visualise batch effect removal:**

Principal Components Analysis (PCA) is often used to visually inspect experimental results for batch effects; when biologically alike samples cluster together rather than those from like-batches, batch effects are often ignored. 
Cell type is one of the better understood influences on gene expression. 
We know that the same DNA is in every cell, and yet the morphology and function of each cell is determined by its cell type, due to its gene expression. 
We can expect largely similar patterns of gene expression in similar cell types, which means that when we know cell type of samples, this information can be used to aid in visually checking the results of batch correction using PCA.
