(alspac-intro)=
# Introduction

(alspac-motivation)=
## Motivation
[//]: # (TODO: Write - to test Snowflake)
In order to test Snowflake, I needed a data set that had a wealth of phenotype and genotype information.

(alspac-study)=
## The ALSPAC cohort study
The Avon Longitudinal Study of Parents and Children, ALSPAC{cite}`Golding2001-oj` is a cohort of over 14,000 families from the Avon area with children born in 1991-1992. 
It is also known as "the Children of the 90s" study.
Many of these families continue to be part of the study to this day, including some of their own children through an extension of the project: children of the children of the 90s (COCO90s).

A wealth of phenotype information (over 80,000 variables) has been collected from these families over the years, through a series of voluntary surveys and clinics, including genotyping of over 9000 children using 23andMe.

[//]: # (TODO: Explain the contents of the ALSPAC catalogue)
ALSPAC's phenotype information, while extensive, is not mapped to phenotype terms in ontologies. 
All data held by ALSPAC can be searched for in the [ALSPAC variable catalogue](http://www.bristol.ac.uk/alspac/researchers/our-data/), after which it can then requested per variable or data type. 
At the time of writing, the cohort is around 30 years old, meaning that there is little information about phenotypes that manifest later in life, for example Alzheimer's or heart disease.
Many phenotype terms may not have any measurements, and there may be many variables associated with some others.

(alspac-exp-design)=
## Experiment Design
Due to the identifiable nature of the data, our ethics application did not allow us to access many different phenotypes to perform a cross-phenotype validation of the predictor. 
Instead, we were granted access to the genotype data only first, then allowed to request a small number of phenotypes of interest after running Snowflake.

[//]: # (TODO: ALSPAC could be run for ALSPAC only since there is no ethnic diversity within the ALSPAC genotypes - it was specifically restricted to europeans - https://academic.oup.com/ije/article/47/4/1207/5001767)

(choosing-phenotypes)=
### Choosing phenotypes of interest
I created a shortlist of phenotypes of interest by first restricting the set of scores to phenotypes for which Snowflake makes a prediction within the ALSPAC cohort, then ordering this list by the {ref}`phenotype confidence score<phenotype-score>`, to ensure that Snowflake could give confident predictions for phenotypes that were requested.
I then mapped these to ALSPAC phenotypes by searching the ALSPAC variable catalogue.

