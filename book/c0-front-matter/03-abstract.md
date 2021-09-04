# Abstract

[//]: # (TODO: MAke sure all chapters are noted here, and none are there that don't feature)
[//]: # (TODO: Add a zenodo reference to ontolopy, and cite it)

The title of this thesis describes the ambitious scientific aim running through it: explaining the link between genotype and phenotype through molecular biology data.
In our cells, proteins are constantly being created and are degrading, and are accumulating or interacting to produce the phenotypes that we see at a larger scale: height, levels of enzymes in blood, diseases.
There are hidden molecular explanations for our phenotypes, and our proteins functions.
The versions of the proteins that it is possible for an organism to produce are determined primarily by its protein-coding DNA, while the selection of possible proteins that are actively produced in each cell are determined by the environment of the particular cell at each time.
The data about these molecules and their activity is our trail of breadcrumbs in the search for a molecular explanation for phenotype, and these data exist in computational biology's collection of large databases of community-sourced experimental and computational results.

This thesis explores two main approaches for making and improving explanatory predictions of phenotype and protein function from genotype.
Both predictors seek to leverage the power of the researchers around the world which contribute their results to community databases, and combines these where possible to get a fuller picture of the complex system of interacting molecules.

The first part of this thesis contains all of the necessary background, and contains three chapters.
{numref}`Chapter %s<c01-philosophy>` briefly introduces the philosophy of this thesis.
The biology background chapter ({numref}`chapter %s<c02-biology-bg>`) then presents a detailed overview of the scientific model that links genotype and phenotype. 
It tells the story of how phenotype arises from genotype, and introduces the different biological molecules that are involved. 
It begins at the very basics: what are DNA, RNA, proteins, and phenotypes; how are they related; how do we categorise them?
This background is intended to make this thesis readable to someone without a background in biology, and to explain the overall aims and context of the research in this thesis. 
It does not contain any of my own research. 
The computational biology background chapter ({numref}`chapter %s<c03-compbio-bg>`) follows on from the previous chapter by discussing popular resources in computational biology, their provenance, and the impact of this on the field. 
In this chapter, I also present my contributions to collaborative projects: the Proteome Quality Index paper{cite}`Zaucha2015-ez`, and the 2014 SUPERFAMILY update paper{cite}`Oates2015-li`

In the second part, I present the Snowflake phenotype predictor, which uses variants conservation scores, prevalence in the population, and protein domain architectures as input to an unsupervised learning method. 
This predictor, the development of which resulted in a patent{cite}`Gough2017-ik`, finds unusual combinations of variants associated with phenotypes, and is designed to create explanatory predictions of complex traits. 
The algorithm itself, and the results of experiments in validating Snowflake are presented in {numref}`chapter %s<c04-snowflake>` and {numref}`chapter %s<c05-alspac>`.

In investigating Snowflake's predictions, it became clear that it was possible for it to include protein-coding SNPs in predictions about phenotypes that exist in tissues in which the protein is never expressed, which brings us to the third and final part of this thesis. 
The Filip protein function prediction filter is discussed in {numref}`chapter %s<c06-filter>`, which uses gene expression data to filter out predictions of proteins which are not expressed in the tissue relating to a given phenotype. 
I discuss attempts to validate `filip`'s predictions, including it's performance in the CAFA3 protein function prediction competition{cite}`Zhou2019-jk`.
In addition, this part presents tools and datasets that were developed through creating Filip: Ontolopy a Python package for querying OBO files in {numref}`chapter %s<c06-ontolopy>`, and a combined data set of gene expression data in {numref}`chapter %s<c05-combining>`. 

