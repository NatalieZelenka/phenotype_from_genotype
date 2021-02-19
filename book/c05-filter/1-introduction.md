## Introduction
[//]: # (TODO: Add cross-ref)
[//]: # (TODO: Release mapping data separately)
[//]: # (TODO: Rewrite - make relevant to Snowflake)

## CAFA

As previously mentioned, there are many genes/proteins for which we have sequence information, but not functional information. 
This is due to the low cost in sequencing experiments in comparison to the expense of knock-out or other function-determining experiments, and the inequality of studied proteins/genes. 

There is a community of researchers who seek to overcome this problem by developing computational methods that predict protein function from sequence, structure, or additional information (e.g. via the CAFA competitions{cite}`Zhou2019-jk,Jiang2016-rz,Radivojac2013-wh`). 
If successful, this would give the practical benefit of discovering the function of many proteins without having to carry out hundreds of thousands of expensive and time-consuming wet lab experiments. 
Such knowledge could be used to identify genes or proteins for future treatments. An accurate model might also be able to give us an insight into the mechanisms behind such functions, giving further insight into how an effective therapy might be designed.

Machine learning methods are currently the most successful class of protein function predictors. While this is promising for answering one aspect of the problem (“what are the functions of a given protein?”), they do not always attempt to answer how or why. 

Structural or sequence methods that estimate protein function based on for example conservation or structure counter this problem. 
However, they are generally less accurate. 
One reason for this might be that they can predict that a protein affects a phenotype in a context that it would never encounter. 
For example, that a protein which is only ever transcribed in skin cells is associated with lung cancer. 
Such predictions are at odds with our understanding of how proteins function, and gene expression data could be used to filter out such predictions. 

Disease-associated genes are generally over-expressed in the tissue they cause symptoms in, with the exception of cancer-associated genes{cite}`Lage2008-gq,Winter2004-rr`. 
This can and has already been leveraged effectively as part of gene and variant prioritisation methods {cite}`Rackham2015-jp,Antanaviciute2015-ke`.
 Despite this, tissue-specific gene expression data was completely missing from entries to CAFA1 or CAFA2.

For this reason, I developed a filter to be used on top of any protein function prediction method (FilP), which removes predictions where the protein is not transcribed in the tissue that the phenotype relates to. 

### Critical Assessment of Functional Annotation
Critical Assessment of Functional Annotation (CAFA) is an international community-wide competition for the prediction of protein function. 
It has been running approximately every 2-3 years since 2013. CAFA aims both to stimulate research in the field of protein function prediction, and to measure progress in the field.

#### Challenge
Each CAFA challenge begins by the organisers releasing a large number of target sequences about which participants must make predictions. 
Participants can use any additional data they see fit to make predictions, which must be triples containing a sequence ID, ontology term ID (e.g. a GO/HP identifier), and a confidence score between 0 and 1. 
A score of 1 indicates a very confidence predictor, while a score of 0 is equivalent to not returning the prediction. Each team may submit up to three models, the best of which is ranked.

#### CAFA Validation 
This confidence score allows for a range of possible sets of predictions, depending on the threshold parameter $\tau$. 
Precision (the proportion of selected items that are relevant), and recall (the proportion of relevant items that are selected) are defined as:

$$$ precision = p = \frac{t_p}{t_p + f_p} $$$
$$$ recall = r = \frac{t_p}{t_p + f_n} $$$

Precision-recall curves are generally used to validate a predictors performance, but the $F_1$ measure gives a one-number overview of the performance:

$$$F_1 =2/ \frac{precision \cdot recall}{precision + recall}$$$

Since the precision and recall will be different for any $\tau$, the $F_{max}$ score is the maximum possible $F_1$ for any value of $\tau$.

[//]: # (TODO: explain the below a little more: how many measures does that make? 2 x2 = 4?)
CAFA validation can either be term-centric or protein-centric. For each option, submissions are assessed per species and for wholly unknown and partially known genes separately.

##### Limitations of validation method
There is no penalty for making a broad guess, or reward for making a precise one. This is one of the reasons that the naive method does so well: for example it is not penalised for guessing that the root term of the GO BPO ontology Biological Process is related to every gene. 

Due to the nature of the validation set, it’s possible that the best-scoring CAFA methods simply predict which associations are likely to be discovered soon (i.e. associations to genes people are currently studying).

#### Past CAFAs
In 2014, the CAFA2 experiment began: 100,8216 target sequences from 27 different species were released to participants. In addition to the GO Biological Process and Molecular Function ontologies used in CAFA1, predictions were also requested for the Human Phenotype Ontology and GO Cellular Component ontology. 

### Overview

```{figure} ../images/filp-overview.png
---
height: 220px
name: filp-overview
---
A flow chart showing how FilP works.
```

The filter is a simple rule-based model. Such models have not been very successful, as is the case for most models. This work is simply meant to show that including tissue-specific information can improve the results of protein function prediction, suggesting that it should be included in future ensemble predictors.

Such a tool could be used on top of any protein function predictor, but would provide the most value for predictors that rely on structural or sequence similarity
