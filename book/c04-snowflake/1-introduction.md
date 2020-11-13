## Introduction

How does phenotype arise from genotype? As explained in the {numref}`c02-biology-bg`, we understand the mechanisms theoretically: differences in DNA cause differences in cell functionality, which interact with the cell environment to create differences in overall phenotype. Efforts to disentangle which genes effect which phenotypes generally take a reductionist approach where we look closely at one particular gene or phenotype. Predicting an individual human phenotype is then based on combinations of mutations that have been discovered through these processes. This chapter describes a radical alternative: predicting human phenotype from genotype directly from data about both the molecular reality of these mutations, together with data about their distributions in the population.

[//]: # (TODO: When are other approaches successful? What are the downsides?)

We are fortunate in biology to have good quality, curated, open datasets that cover genomes across the tree of life, as well as cross-species ontologies of biological processes, diseases, and anatomical entities (to name just a few). These resources are only possible because of the international community who contribute to them, and the talented bio-curators who curate them. The `Snowflake` phenotype prediction method works by identifying individuals who have unusual combinations of deleterious SNPs associated with a phenotype. The phenotype predictor uses only data about missense SNPs in coding regions of globular proteins, so it can only be expected to work well where phenotypes are determined primarily by these kinds of mutations. However, the advantage over other methods (e.g. GWAS) is that the role of the involved SNPs is explained.

The motivation for doing this kind of work is primarily understanding how our bodies work, but there are clear benefits in health if an accurate phenotype prediction method was developed: we would know where to focus our efforts in terms of treating phenotypes which are disease related.

In this chapter, I present work which was carried out in developing the Snowflake phenotype prediction method. This method combines conservation and variant effect scores using FATHMM{cite}`Shihab2013-pk`, inference about function of protein domains using DcGO{cite}`Fang2013-ms`, and human genetic variation data from the 2500 genomes project{cite}`Consortium2015-ci` to predict phenotypes of individuals based on their combinations of missense SNPs. 


My contributions to this software included:
- Adding functionality for running `Snowflake` for different numbers of individuals, including:
    - One person against a background set
    - Multiple people against a background set
    - A cohort without a background set
- Dealing with missing calls 
- Creating a pipeline for creating input files for different genomic data types, e.g.:
    - genotyping formats, including different 23andMe formats (from different chips)
    - VCF format
    - whole genome
- Improvements to memory usage (by sharing memory)
- Developing the outputs, e.g. the output score.

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```