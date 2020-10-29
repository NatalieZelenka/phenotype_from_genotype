## Introduction

A huge question in biology is how does phenotype arise from genotype. Efforts to disentangle these relationships generally take a reductionist approach, looking closely at one particular gene or phenotype.

We are fortunate in biology to have good quality, curated, open datasets that cover genomes across the tree of life, as well as cross-species ontologies of biological processes, diseases, and anatomical entities (to name just a few). These resources are only possible because of the international community who contribute to them, and the talented bio-curators who curate them.

In this chapter, I present some extensive exploratory work which was carried out in developing the Snowflake phenotype prediction method. This method combines conservation and variant effect scores using FATHMM{cite}`Shihab2013-pk`, inference about function of protein domains using DcGO{cite}`Fang2013-ms`, and human genetic variation data from the 2500 genomes project{cite}`Consortium2015-ci` to predict phenotypes of individuals based on their combinations of missense SNPs. 

The aim of the phenotype predictor is to reveal individuals with unusual combinations of deleterious SNPs associated with a phenotype. This may not be expected to provide a very accurate prediction, as it will only work for missense SNPs in coding regions of globular proteins. However, the advantage over other methods (e.g. GWAS) is that the role of the involved SNPs is explained.

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```