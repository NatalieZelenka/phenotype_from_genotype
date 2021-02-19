## Introduction
[//]: # (TODO: Release mapping data separately)

As we explored in {ref}`Chapter 2<c02-biology-bg>`, there is a complex web of interactions between proteins and other molecular machinery that lead to phenotype.
Our {ref}`current understanding of how phenotype arises from genotype<model-genotype-phenotype-summary>` tells us that knowing what proteins *can* be produced isn't necessarily enough of a clue to tell us about phenotype.
Liver cells and heart cells have the same DNA, but it's how that DNA is used (what genes are expressed in the cell) that leads to the difference between those cell types. 
Since larger scale phenotypes will follow from cellular differences, we expect gene expression data to be a useful measure for phenotype prediction.

This is backed-up by data: disease-associated genes are generally over-expressed in the tissue they cause symptoms in, with the exception of cancer-associated genes{cite}`Lage2008-gq,Winter2004-rr`. 
This can and has already been leveraged effectively as part of gene and variant prioritisation methods {cite}`Rackham2015-jp,Antanaviciute2015-ke`.

## Motivation: linking genotype and phenotype
The {ref}``inconclusive results of the snowflake predictor<snowflake-results>`` led me to focus my efforts on finding answer to a much smaller piece of the genotype-to-phenotype puzzle. 
As mentioned in {ref}`the previous Chapter's discussion<dcgo-expression-problem>`, some predictions of a protein's phenotype are incorrect because the protein is not produced, even though they do have a structure that means that they could be involved in the pathway if they were present.
To understand if this is the case, we need to know as a minimum if a gene is *ever* expressed a relevant context. 
This would rule out, for example, proteins that are predicted to be associated with eye health, but are only ever produced in the developing limbs.

[//]: # (TODO: Cross-ref to descriptions of other phenotype prediction and variant prioritisation methods)
And if we could apply this approach to `snowflake`, then we could also apply it to other phenotype prediction and variant prioritisation methods.

## Motivation: protein function prediction
[//]: # (TODO: Cross-ref previously mentioned)
As previously mentioned, there are many genes/proteins for which we have sequence information, but not functional information. 
There is a community of researchers who seek to overcome this problem by developing computational methods that predict protein function from sequence, structure, or additional information.
Accurate protein function prediction would give the practical benefit of discovering the function of many proteins without having to carry out hundreds of thousands of expensive and time-consuming wet lab experiments to test non-existent functions. 
Such knowledge could be used to identify genes or proteins for future treatments. 
An accurate model might also be able to give us an insight into the mechanisms behind such functions, giving further insight into how an effective therapy might be designed.

Machine learning methods are currently the most successful class of protein function predictors. 
While this is promising for answering one aspect of the problem (“what are the functions of a given protein?”), they do not always attempt to answer how or why. 
Structural or sequence methods that estimate protein function based on for example conservation or structure counter this problem, but they are currently less accurate.
Few of these methods include tissue-specific gene expression information (such data was completely missing in the first and second {ref}`CAFA competitions<CAFA>`).
Filtering out predictions where genes are never expressed in a relevant tissue, may help in protein function prediction, just as in phenotype prediction.

(CAFA)=
## CAFA
Critical Assessment of Functional Annotation{cite}`Zhou2019-jk,Jiang2016-rz,Radivojac2013-wh` (CAFA) is an international community-wide competition for the prediction of protein function, which aims both to stimulate research in the field of protein function prediction, and to measure progress in the field.
It has been running approximately every 2-3 years since 2013. 

[//]: # (TODO: Write about CAFA challenges)
The CAFA competitions consist of a number of different challenges.

Each CAFA challenge begins by the organisers releasing a large number of target sequences about which participants must make predictions. 
Participants can use any additional data they see fit to make predictions, which must be triples containing a sequence ID, ontology term ID (e.g. a GO/HP identifier), and a confidence score between 0 and 1. 
A score of 1 indicates a very confidence predictor, while a score of 0 is equivalent to not returning the prediction. Each team may submit up to three models, the best of which is ranked.

### CAFA Validation 
This confidence score allows for a range of possible sets of predictions, depending on the threshold parameter $\tau$. 
Precision (the proportion of selected items that are relevant), and recall (the proportion of relevant items that are selected) are defined as:

$ precision = p = \frac{t_p}{t_p + f_p} $
$ recall = r = \frac{t_p}{t_p + f_n} $

Precision-recall curves are generally used to validate a predictors performance, but the $F_1$ measure gives a one-number overview of the performance:

$F_1 =2/ \frac{precision \cdot recall}{precision + recall}$

Since the precision and recall will be different for any $\tau$, the $F_{max}$ score is the maximum possible $F_1$ for any value of $\tau$.

[//]: # (TODO: explain the below a little more: how many measures does that make? 2 x2 = 4?)
CAFA validation can either be term-centric or protein-centric. For each option, submissions are assessed per species and for wholly unknown and partially known genes separately.

### Limitations of validation method
There is no penalty for making a broad guess, or reward for making a precise one. This is one of the reasons that the naive method does so well: for example it is not penalised for guessing that the root term of the GO BPO ontology Biological Process is related to every gene. 

Due to the nature of the validation set, it’s possible that the best-scoring CAFA methods simply predict which associations are likely to be discovered soon (i.e. associations to genes people are currently studying).

[//]: # (TODO: delete below)

<!--
### Past CAFAs
In 2014, the CAFA2 experiment began: 100,8216 target sequences from 27 different species were released to participants. 
In addition to the GO Biological Process and Molecular Function ontologies used in CAFA1, predictions were also requested for the Human Phenotype Ontology and GO Cellular Component ontology. 
-->

## `filip`
In order to overcome the problem of predictors containing erroneous predictions due to a lack of gene expression information, I have created a lightweight tool which allows researchers to filter their phenotype or protein function predictions using tissue-specific gene expression information.
 
````{margin} Naming things
:name: naming-things

> There are only two hard things in Computer Science: cache invalidation and naming things
>
> -- Phil Karlton

Aside from the above joke (and my anecdotal experience), there is also evidence in the literature{cite}`Pottegard2014-yc` to suggest that strained acronyms exist across scientific disciplines. 

````
 
Drawing on the noble tradition of scientists {ref}`naming things badly<naming-things>`, I call this `filip` as it is for `fil`ter`i`ng `p`redictions. 
{numref}`filip-overview` illustrates filip's two-step approach, which aims to filter out predictions for proteins which are not created in the tissue of interest (related to the predicted phenotype).
The filter is a simple rule-based tool, which is designed to be used on top of any protein function predictor, but would provide the most value for predictors that rely on structural or sequence similarity.

```{figure} ../images/filip.png
---
name: filip-overview
---
An illustration showing how filip works. 
It's a two-step process where protein-phenotype predictions are expected as input. 
In step 1, proteins are mapped to genes, and phenotypes are mapped to tissues. 
In step 2, `filip` filters out any predictions where for which the gene is not expressed in the tissue.
```

