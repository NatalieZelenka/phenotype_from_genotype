(snowlflake-intro)=
# Introduction
The Snowflake algorithm is primarily a phenotype prediction method: it takes data about individuals DNA as input and outputs predictions about which phenotypes each individual has. 
These predictions are based on how unusual an individual is for variants relating to each phenotype, and are made across a breadth of phenotypes and for missense variants across the protein-coding genome. 
It does this by combining existing predictions of variant deleteriousness from FATHMM{cite}`Shihab2013-pk` and association of protein domains to phenotypes from DcGO{cite}`Fang2013-ms`, and finding unusual combinations of these variants through clustering individuals against a diverse background cohort and looking for outliers.
The phenotype prediction implicitly contains protein function predictions, due to {ref}`the relationship between protein function and phenotype<phenotype-protein-prediction-link>`, and these are the key output of Snowflake.
As a protein function predictor, Snowflake seeks rare combinations of SNPs which may influence a phenotype.
In other words, Snowflake looks for the mechanisms behind complex traits, which are currently not well understood, but are thought to cause many human diseases. 

(snowflake-intro-motivation)=
## Motivation
[//]: # (TODO: Cite odyssey of diagnosis and >50% undiagnosed)
In {numref}`chapter %s<c02-biology-bg>`, we discussed the theoretical mechanism from which phenotype arises from genotype.
In summary: differences in DNA cause differences in cell functionality, which interact with the cell environment to create differences in overall phenotype. 

As {ref}`previously mentioned<which-phenotypes>`, many recognised phenotypes are medical disorders or their symptoms. 
Currently to achieve diagnoses for genetic illnesses, specific genes are often sequenced one at a time, since looking at whole genomes would be too time consuming for clinical staff. 
Patients seeking diagnoses for rare genetic diseases describe the process as an "Odyssey", more than half undiagnosed at any given time.
If whole genome (or genotype) based phenotype prediction was possible, only one sample and test would be needed to get a much fuller picture of a person's health, and we would be able to reduce the long and tiring process of obtaining diagnoses for rare genetic diseases.
Applied to the plant and animal kingdom, phenotype prediction could also be beneficial in veterinary science and agriculture.

[//]: # (TODO: Dicuss complex traits, missing/hidden heritability)
The discovery of underlying mechanisms for complex traits remains a particular challenge.

(snowflake-related-work)=
## Related work

(phenotype-predictors-variant-prioritisation)=
### Phenotype predictors and variant prioritisation
Biology databases are home curated, open data that cover genomes across the tree of life, as well as cross-species ontologies of biological processes, diseases, and anatomical entities. 
There are a number of recent phenotype prediction methods that have had some success in using these resources for either variant prioritisation or use as a clinical diagnostic tool.

There are a class of "knowledge-based" methods, which use knowledge from databases of experimental results (known associations between genes and phenotypes) as the basis for these predictions, for example Phen-Gen{cite}`Javed2014-mr`, dcGO{cite}`Fang2013-ms`, PhenoDigm{cite}`Smedley2013-oe`, and PHIVE{cite}`Robinson2014-kg`.
The better performing methods in this class, use associations between model organisms and orthologous genes, to leverage the wealth of information that is collected from these model organism experiments.

There are also "functional" methods, like FATHMM{cite}`Shihab2013-pk` and CADD{cite}`Kircher2014-zf`, which instead use information about how the molecules and their function may change with different nucleotide or amino acid substitutions, as well as conservation metrics to prioritise variants.
These tools rank variants for deleteriousness, but do not link them to specific phenotypes.

Most successful methods of any kind now combine multiple sources of information, some combine both functional and knowledge-based sources.
This approach is used within Exomiser{cite}`Smedley2015-ql`, which combines PHIVE with many other sources of information such as protein-protein interactions, cross-species phenotype associations, and variant frequency using a black-box classifier.
Phenolyzer{cite}`Yang2015-dq` and Genomiser{cite}`Smedley2016-os` also take similar approaches of combining many different sources of data.

[//]: # (TODO: Cross-ref to CAFA)
The aim of these models is mostly to prioritise variants associated with diseases, and they are bench-marked by their ability to identify known variants.
Lists of known variants may be purpose-curated from the literature according to specific evidence, or may come from some subset of annotation databases (which in some cases the algorithm may have used as input data).
Each phenotype predictor often targets a specific use case (e.g. non-coding variants), and in combination with the varying validation methods used, it is difficult to compare the accuracy of all of these models directly.
For this reason, the CAFA competition is very useful in getting a more objective view of the capabilities of these kinds of tools.

[//]: # (TODO: BRIEF SUMMARY OF %S IN CAFA)  

Similar approaches have been used as clinical diagnostic tools. 
PhenIX (Phenotypic Interpretation of eXomes){cite}`Zemojtel2014-vd` is a version of PHIVE which is restricted to the "human disease-causing genome" (genes known to cause disease) to make it more suitable for clinical use in diagnosis of rare genetic diseases. 
It also includes semantic similarity information between inputted symptoms and Human Phenotype Ontology terms, using the Phenomizer{cite}`Kohler2009-sq` algorithms. 
For PhenIX the measure of success is that it enabled skilled clinicians to find diagnoses for 11 out of 40 (28%) patients with rare genetic diseases, who were not able to be diagnosed through other means.

[//]: # (TODO: Check which CAGI things are published)
While these examples are the most similar published work to Snowflake, they are all tested as variant prioritisation tools rather than phenotype predictors.

(clustering-outlier-genetics)=
### Clustering and outlier-detection in genetics
[//]: # (TODO: Have I explained clustering anywhere? Should I explain that in some detail here?)

```{margin} Haplotypes and haplogroups
:name: haplotypes

Haplotypes are groups of alleles that are inherited together from a single parent.
In humans, Y-chromosomes and mitochondrial DNA (mtDNA) are often analysed for haplotypes to understand ancestry within species since these are passed from parents to children without recombination (only mothers pass on mtDNA, and only fathers pass on Y chromosomes).

Haplogroups are groups of haplotypes, representing major branching points in the within-species phylogenetic tree.
```

Clustering algorithms, particularly hierarchical methods, are commonly used in genetics for:
 1. finding evolutionary relationships between DNA samples, for example, in reconstructing phylogenetic trees and mapping {ref}`haplotypes<haplotypes>` within populations{cite}`Paschou2007-wn`.
 2. finding functional relationships between genes based on gene expression data{cite}`Eisen1998-fd,Ressom2008-pb`.

For applications in group (1), individuals are generally separated into clusters based on their DNA variants, whereas for (2) samples are separated into clusters based on their gene expression.

[//]: # (TODO: write - the use of clustering methods in phenotype prediction is rare, maybe even novel, cite CAGI)
 
Clustering methods are only very rarely used to cluster individuals in phenotype prediction or variant prioritisation tasks.
In one case, clustering individuals based on a combination of genotype and phenotype information has been applied to identify subtypes within emphysema{cite}`Cho2010-eo` (a lung disease).

(curse-of-dimensionality-section)=
### Overcoming the curse of dimensionality through dimensionality reduction and feature selection

[//]: # (TODO: Figure below not rendering)

```{figure} ../images/curse-of-dimensionality.png
---
height: 220px
name: curse-of-dimensionality
---
As the number of dimensions increase from 1 dimension on the left to 3 on the right, the number of points needed to cover the space increases exponentially. This means that for a fixed number of points (individuals), increasing the number of dimensions (SNPs) that we cluster on decreases the density of our space exponentially, making it exponentially harder to identify clusters. 
```

The "curse of dimensionality" is a phrase coined by Richard E Bellman, during his work on dynamic programming{cite}`Bellman1957-dc`, but has since proved relevant in many different mathematical and data-driven fields. 
While it's used colloquially as a catch-all complaint about high-dimensional data, the "curse" specifically refers to the sparsity of data that occurs exponentially with an increase in dimensions. 
This leads to various problems in different fields{cite}`Zimek2012-fg` including general difficulty in reaching statistical significance and reduced usefulness of clustering, distance, and outlier metrics.
This can easily be a problem in genetics since we have tens of thousands of genes, and hundreds of thousands of variants as dimensions that we may want to cluster over.

As {numref}`curse-of-dimensionality` illustrates, increasing the number of dimensions that we cluster over makes it exponentially harder for us to identify clusters in the data given a fixed number of individuals in our cohort. 
In extreme cases, all samples or individuals look equally distant from each other in the sparse, high-dimensional space.

The curse of dimensionality can be partially reduced by choosing a clustering or outlier detection method which is more robust to the number of dimensions. 
However, these still have limits, and in order to overcome these, it is necessary to reduce the number of dimensions in some way, this process is called feature selection.
This can be done through careful curation of important features, through variance cut-offs, or by dimensional reduction methods like Prinipal Component Analysis (PCA) or Multi-dimensional Scaling (MDS) which project the data into a different coordinate system and then discard some of the newly calculated dimensions.

<!--
### Summary
[//]: # (TODO: Big up themes of multi-omics, comibing different sources of data)
-->
