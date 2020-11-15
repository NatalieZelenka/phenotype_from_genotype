---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

## Genetic input data
[//]: # (TODO: Have I already explained VCF format? Link or explain here. Cite. Cite the version of the format we use. Explain that there are different versions.)
Snowflake requires genetic data as input. For use in the predictor, the data are recorded in VCF format.

+++

### 2500 genomes
The 2500 genomes data is used as the default "background cohort" for Snowflake. The background cohort is included in order to diversify the sample of individuals (and therefore mutations), so that clustering can be meaningful. 
[//]: # (TODO: Write about the diversity/limitations of the 2500 genomes project).
[//]: # (TODO: Write about the impact of the fact that the 2500 genomes project is whole genome sequencing, while the rest is mostly genotype data).

#### Data acquisition
[//]: # (TODO: Write)

#### Data pipeline
[//]: # (TODO: Write)

#### Exploratory data analysis
[//]: # (TODO: Write)

+++

### 23andMe data
The CAGI, Athletes, and ALSPAC datasets were all genotyped using 23andMe, so the following applies to all of these datasets.

#### Ambiguous Flips
[//]: # (TODO: Explain ambigious flips a bit better)
The majority of input data to the predictor is 23andMe data. In testing the predictor with the 2500G background and a cohort of 23andMe genomes, it became clear that for many phenotypes, the background was forming a separate cluster to the cohort. This led to the realisation that there are 23andMe calls which had the opposite ratio of wild type:mutant than the 2500 genomes. Some further reading revealed this to be a known problem{cite}`Church2005-zv`, which may be due to ambiguous flips{cite}`Sand2007-ed`. 

[//]: # (TODO: Finish writing this sentence)
Implausible distributions of SNPs in the input cohort (given the background) are therefore discarded. i.e if the input cohort doesn't match the background. (all one way and the rest all the other).

#### 23andMe chips
[//]: # (TODO: Write and cite)
Since launch, 23andMe have used a number of different illumina chips for their genotyping service. These chips record different SNPs. 

+++

### ALSPAC
[//]: # (TODO: Further describe the value of the dataset and what it is generally used for)
The Avon Longitudinal Study of Parents and Children, ALSPAC{cite}`Golding2001-oj` (a.k.a. the children of the 90s) is a cohort of over 14,000 families from the Avon area. Of these, 8365 of the children were genotyped by 23andMe and passed quality control. A wealth of phenotype information has also been collected from these families, through a series of voluntary surveys and clinics.

+++

#### Experiment design
Due to the private nature of the data, we were granted access to the genotype data first, then allowed to request a small number of high-scoring phenotypes after running the predictor.

[//]: # (TODO: link ethics approval docs (put on OSF?)
[//]: # (TODO: explain that using the catalogue - and link - ALSPAC phenotypes matching the DcGO phenotypes were chosen for the highest scoring things on a the prototype version. Maybe explain that due to the sensitivity of this to other things, they were not the highest ranking things any more).
We had ethics approval to run the anonymised genotype information for the ALSPAC cohort in the phenotype predictor, and then to request phenotype information for the top-scoring phenotypes. The phenotype predictor was run on this cohort. Unfortunately the majority of the top-predicted phenotype terms (Ataxia, Abnormal Fat Cell Morphology, Abnormal Fetal Development) did not map cleanly to ALSPAC phenotypes, and those that did (e.g. Intellectual Disability) had many missing values, or did not overlap with the genotyped individuals.

[//]: # (TODO: Cite lack of diversity).
Although the ALSPAC dataset is large, it is not very diverse, therefore the 2500 genomes project genomes were used as a background set. 

+++

#### Data format
[//]: # (TODO: Write)
**Genotype data format**

**Phenotype data format**

+++

#### Data pipeline
[//]: # (TODO: Write)

**Missing values**

**Mapping DcGO phenotypes to ALSPAC measurements**

+++

#### Exploratory Data Analysis
**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for ALSPAC. Known phenotypes included, dotted lines showing max scores for any SNP.)

+++

### Athletes
[//]: # (TODO: Write)

+++

### CAGI
[//]: # (TODO: Write)

+++

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```
