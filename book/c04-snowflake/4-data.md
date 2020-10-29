## Data

### Background cohort (2500 genomes)

### 23andMe data
[//]: # (TODO: Explain ambigious flips a bit better)
The majority of input data to the predictor is 23andMe data. In testing the predictor with the 2500G background and a cohort of 23andMe genomes, it became clear that for many phenotypes, the background was forming a separate cluster to the cohort. This led to the realisation that there are 23andMe calls which had the opposite ratio of wild type:mutant than the 2500 genomes. Some further reading revealed this to be a known problem{cite}`Church2005-zv`, which may be due to ambiguous flips{cite}`Sand2007-ed`.

[//]: # (TODO: Finish writing this sentence)
Implausible distributions of SNPs in the input cohort (given the background) are therefore discarded. i.e if the input cohort doesn't match the background. (all one way and the rest all the other)

### ALSPAC
The Avon Longitudinal Study of Parents and Children, ALSPAC{cite}`Golding2001-oj` (a.k.a. the children of the 90s) is a cohort of over 14,000 families from the Avon area. Of these, 8365 of the children were genotyped by 23andMe and passed quality control. A wealth of phenotype information has also been collected from these families. Since the ALSPAC data set is not very diverse, so the 2500 genomes project genomes were used as a background set. 

We had ethics approval to run the anonymised genotype information for the ALSPAC cohort in the phenotype predictor, and then to request phenotype information for the top-scoring phenotypes. The phenotype predictor was run on this cohort. Unfortunately the majority of the top-predicted phenotype terms (Ataxia, Abnormal Fat Cell Morphology, Abnormal Fetal Development) did not map cleanly to ALSPAC phenotypes, and those that did (e.g. Intellectual Disability) had many missing values, or did not overlap with the genotyped individuals. The resulting phenotype dataset was too small to use for validation (p>0.05). 

### CAGI Data


---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```