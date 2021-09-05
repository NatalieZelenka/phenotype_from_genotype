---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.9.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(alspac-data)=
# Data


[//]: # (TODO: Move this to the ALSPAC chapter)
[//]: # (TODO: Further describe the value of the dataset and what it is generally used for)

## ALSPAC




[//]: # (TODO: link ethics approval docs (put on OSF?)

<!--Although the ALSPAC data set is large, it is not very diverse, therefore the 1000 genomes project (Phase 1) genomes were used as a background set.-->

## Genotypes
Of the 14,000+ families in the ALSPAC cohort, 8365 unrelated children of European ancestry were genotyped by 23andMe and passed quality control. 
The participants were genotyped using the 23andme v2 chip, which measures ~550,000 SNPS.

[//]: # (TODO: Fix cross-ref)
[//]: # (TODO: Optional for thesis: Link to reproducible versions of scripts that do this: form_alspac_vcf, form_alspac_consequence)

These 23andMe files use build 36 of the human reference genome, so a build 36 version of the `.vcf` and `.Consequence` files for ALSPAC were made first (created with the `snowflake create_input` command described in {numref}`snowflake-create-input`), before lifting them over to the build 37 versions which were used for input to the `Snowflake`. 


<!--
**Lift-over procedure**
Lifting over VCF files between {ref}`different-builds` was done using the UCSC LiftOver tool.
[//]: # (TODO: Here?? EDA: Number of variants overlap with 1000G)
-->

## Phenotypes

[//]: # (TODO: explain that using the catalogue - and link - ALSPAC phenotypes matching the DcGO phenotypes were chosen for the highest scoring things on a the prototype version. Maybe explain that due to the sensitivity of this to other things, they were not the highest ranking things any more)
[//]: # (TODO: Mapping phenotypes to ALSPAC measurements. Write - was done by hand using the ALSPAC catalogue)


[//]: # (TODO: Rewrite paragraph below:)
The majority of the top-predicted phenotype terms (Ataxia, Abnormal Fat Cell Morphology, Abnormal Fetal Development) did not map cleanly to ALSPAC phenotypes, and those that did (e.g. Intellectual Disability) had many missing values, or did not overlap with the genotyped individuals.

[//]: # (TODO: Cite lack of diversity)

[//]: # (TODO: EDA table: list of phenotypes with missing data)
