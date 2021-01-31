# Discussion

## Combining omics data sets is an opportunity to improve existing resources
While a great deal of careful work has clearly been spent on making the datasets used in this analysis available and useful to researchers such as myself, there were still many barriers to their use in this circumstance. 
This ranged from mislabelled samples, to missing information, to having to seek data about the same experiment from multiple different sources. 
In particular, I think it’s important that key information that we know affects gene expression such as age, developmental stage, and sex are made available with the data set and preferably in a format which is easy to compare across experiments. 
It is reassuring that the data issues that were discovered had clear pathways for reporting, and that some of them have already resulted in changes to the files used.

## Batch effect clearly exist but are hard to estimate
[//]: # (TODO: Write: need more metadata, and a more standardised way of presenting it)
[//]: # (TODO: Write: difficult to measure batch effect. Can't be sure if it is over-estimated)

The problem of batch effects for this data set has not yet been overcome.
This means that the data set can not yet be used for the purpose of improving measurements from baseline experiments (e.g. housekeeping genes or baseline tissue-specific gene expression).

However, by overcoming the data cleaning and standardisation necessary to have all datasets in the same format with the same sample metadata, the data can be used for analyses where batch and other sample metadata is used as covariates (e.g. differential expression of tissues).  
In its current iteration, it is also suitable for use in FilP, where the data set only needs to distinguish between presence and absence.
