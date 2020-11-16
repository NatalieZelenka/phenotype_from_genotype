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

## Snowflake input data
[//]: # (TODO: Have I already explained VCF format? Link or explain here. Cite. Cite the version of the format we use. Explain that there are different versions.)
`Snowflake` requires:
     - genetic data as input, in VCF format. 
     - conservation scores per SNP.
     
This section describes the sources and pipelines for creating input files.

+++

### Data sources

+++

#### ALSPAC
[//]: # (TODO: Further describe the value of the dataset and what it is generally used for)
The Avon Longitudinal Study of Parents and Children, ALSPAC{cite}`Golding2001-oj` (a.k.a. the children of the 90s) is a cohort of over 14,000 families from the Avon area. A wealth of phenotype information has also been collected from these families, through a series of voluntary surveys and clinics.

Due to the private nature of the data, we were granted access to the genotype data first, then allowed to request a small number of high-scoring phenotypes after running the predictor.
[//]: # (TODO: link ethics approval docs (put on OSF?)

Although the ALSPAC dataset is large, it is not very diverse, therefore the 1000 genomes project (Phase 1) genomes were used as a background set.

##### Genotypes
[//]: # (TODO: Write)
[//]: # (TODO: Cross-ref to description of VCF creation in previous section)
Of the 14,000+ families in the ALSPAC cohort, 8365 of the children were genotyped by 23andMe and passed quality control. The participants were genotyped using the 23andme v2 chip, which measures ~550,000 SNPS.

+++

##### Phenotypes
[//]: # (TODO: explain that using the catalogue - and link - ALSPAC phenotypes matching the DcGO phenotypes were chosen for the highest scoring things on a the prototype version. Maybe explain that due to the sensitivity of this to other things, they were not the highest ranking things any more).

[//]: # (TODO: Rewrite paragraph below:)
The majority of the top-predicted phenotype terms (Ataxia, Abnormal Fat Cell Morphology, Abnormal Fetal Development) did not map cleanly to ALSPAC phenotypes, and those that did (e.g. Intellectual Disability) had many missing values, or did not overlap with the genotyped individuals.

[//]: # (TODO: EDA Graph: What phenotypes do we have?)
[//]: # (TODO: EDA Graph: Phenotype missing data)

[//]: # (TODO: Cite lack of diversity).

+++

### Athletes
[//]: # (TODO: Write)

+++

### CAGI
[//]: # (TODO: Write)

+++

### Data Pipelines

+++



+++

#### Pipeline for creating VCF files from 23andMe data
The CAGI, Athletes, and ALSPAC datasets were all genotyped using 23andMe, so the following applies to all of these datasets.

##### 23andMe chips
[//]: # (TODO: Write and cite)
Since launch, 23andMe have used a number of different illumina chips for their genotyping service. These chips capture information for different SNPs.

##### Ambiguous Flips
[//]: # (TODO: Explain ambigious flips a bit better)
The majority of input data to the predictor is 23andMe data. In testing the predictor with the 2500G background and a cohort of 23andMe genomes, it became clear that for many phenotypes, the background was forming a separate cluster to the cohort. This led to the realisation that there are 23andMe calls which had the opposite ratio of wild type:mutant than the 2500 genomes. Some further reading revealed this to be a known problem{cite}`Church2005-zv`, which may be due to ambiguous flips{cite}`Sand2007-ed`. 

[//]: # (TODO: Finish writing this sentence:)
Implausible distributions of SNPs in the input cohort (given the background) are therefore discarded. i.e if the input cohort doesn't match the background. (all one way and the rest all the other).

+++

#### ALSPAC

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was ALSPAC data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for ALSPAC. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Phenotypes
[//]: # (TODO: Mapping phenotypes to ALSPAC measurements. Write - was done by hand using the ALSPAC catalogue)

+++

#### CAGI
[//]: # (TODO: Possibly delete this section)

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was CAGI data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for CAGI. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Mapping phenotypes to CAGI measurements
[//]: # (TODO: Write)

+++

#### Athletes
[//]: # (TODO: Possibly delete this section)

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was CAGI data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for CAGI. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Mapping phenotypes to CAGI measurements
[//]: # (TODO: Write)

+++

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```
