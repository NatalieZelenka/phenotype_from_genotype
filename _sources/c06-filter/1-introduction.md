# Introduction
[//]: # (TODO: Release mapping data separately)

As we explored in {numref}`chapter %s<c02-biology-bg>`, there is a complex web of interactions between proteins and other molecular machinery that lead to phenotype.
Our {ref}`current understanding of how phenotype arises from genotype<model-genotype-phenotype-summary>` tells us that knowing what proteins *can* be produced isn't necessarily enough of a clue to tell us about phenotype.
Liver cells and heart cells have the same DNA, but it's how that DNA is used (what genes are expressed in the cell) that leads to the difference between those cell types. 
Since larger scale phenotypes will follow from cellular differences, we expect gene expression data to be a useful measure for phenotype prediction.

This is backed-up by data: disease-associated genes are generally over-expressed in the tissue they cause symptoms in, with the exception of cancer-associated genes{cite}`Lage2008-gq,Winter2004-rr`. 
This can and has already been leveraged effectively as part of some gene and variant prioritisation methods {cite}`Rackham2015-jp,Antanaviciute2015-ke`.

## Motivation: improving phenotype and protein function prediction
The {ref}`inconclusive results of the snowflake predictor<snowflake-results>` led me to focus my efforts on finding answer to a much smaller piece of the genotype-to-phenotype puzzle. 
As mentioned in {ref}`the previous chapter's discussion<dcgo-expression-problem>`, some predictions of a protein's phenotype are incorrect because the protein is not produced, even though they do have a structure that means that they could be involved in the pathway if they were present.
To understand if this is the case, we need to know as a minimum if a gene is *ever* expressed a relevant context. 
This would rule out, for example, proteins that are predicted to be associated with eye health, but are only ever produced in the developing limbs.

<!--
As previously mentioned, there are many genes/proteins for which we have sequence information, but not functional information. 
There is a community of researchers who seek to overcome this problem by developing computational methods that predict protein function from sequence, structure, or additional information.
Accurate protein function prediction would give the practical benefit of discovering the function of many proteins without having to carry out hundreds of thousands of expensive and time-consuming wet lab experiments to test non-existent functions. 
Such knowledge could be used to identify genes or proteins for future treatments. 
An accurate model might also be able to give us an insight into the mechanisms behind such functions, giving further insight into how an effective therapy might be designed.
-->

Machine learning methods are currently the most successful class of protein function predictors. 
While this is promising for answering one aspect of the problem (“what are the functions of a given protein?”), they do not always attempt to answer how or why. 
Structural or sequence methods that estimate protein function based on for example conservation or structure counter this problem, but they are currently less accurate: one of the reasons for this might be the lack of inclusion of cell context.
Few of these methods include tissue-specific gene expression information (such data was completely missing in the first and second {ref}`CAFA competitions<CAFA>`).
Filtering out predictions where genes are never expressed in a relevant tissue may help in protein function prediction, just as in phenotype prediction.

<!--
## Related work
TODO: Write: tissue-specific expression in phenotype prediction, transcirptional noise and the idea of genes being "on" or "off"
-->

## When are transcripts "expressed"?

The idea behind Filip is that some proteins are predicted to affect phenotypes that they are unable to affect, because the environment in the tissue or cell means that the protein isn't around to perform it's function (or fail to). 
And, we have a measure of gene expression, for which many proteins have `0` counts (and therefore `0` TPM) in many tissues, so we *could* apply the filter to this cut-off. 
But is it meaningful to do so?

[//]: # (TODO: Image showing gene expression as stochastic, e.g. mRNAs and ribosomes running into eachother/ribosomes running into some promoters before others)

Like all chemical reactions, transcription is a stochastic process; there is an element of randomness; to describe if a transcription event will happen at a specific moment you have to use statistics.
Genetically identical organisms with the same environment have different measured gene expression patterns{cite}`Raj2008-jy` and the same can be said for single cells from the same organism{cite}`Kim2015-mc`.
The reason that it's hard to predict with precision whether a given protein will be transcribed at a given moment is that it depends on the concentration of different molecules in the cell and the energy of the system. 
Transcription events which have a very low probability of occuring will happen sometimes and we will measure this. 
If we sequenced the transcriptome in infinite depth, we might expect all transcripts to be expressed at some level.


[//]: # (TODO: check that I mentioned counts in sequencing technology section)
[//]: # (TODO: Cite gene expression known phenotypes)

```{margin} Transcriptional noise
:name: transcriptional-noise
Transcriptional noise is variation in rates of transcription due to the implicit stochasticity of the reaction process. The implication is that many transcripts with low counts do not play a big role and cells are known to have mechanisms to protect themselves from this noise{cite}`Raj2008-jy,Eling2019-hn`. Since is difficult to distinguish between meaningful and non-meaningful and expression, in differential expression analyses it is common to remove low count transcripts{cite}`Anders2013-zh,Love2021-jf`. 
Similar noise occurs in the process of translation (translational noise).
```

[//]: # (TODO: Cross-ref batch effects, or put in an aside here)

When we look at expression data for a sample, it will just be a snapshot of the transcription in that sample, and one that isn't necessarily representative of what's happening all the time.
Very low count values in a sample are extremely common, and these are usually considered to be difficult to distinguish from {ref}`transcriptional-noise`: low levels of transcription with little effect are often randomly happening in the cell. 
In addition to the biological stochasticity (which could possibly create phenotypic differences), RNA-Seq is sensitive to technical experimental artefacts (batch effects) due to differences in RNA extraction and library preparation{ref}`Conesa2016-gq`.
In both cases, it is low counts where this is most difficult to correct for
So, it isn't necessarily meaningful to take all genes expressed above `0` TPM as a sensible cut-off for whether a gene counts as "expressed" or not in a tissue: when I dichotomise proteins as "expressed" or "not expressed", I am using this as a convenient shorthand for "meaningfully expressed" or "not meaningfully expressed".

We also know that proteins that do cause phenotypes are likely to be highly expressed in tissues related to the phenotype, so we definitely want to keep protein-phenotype predictions where proteins are produced at high levels in the tissue of interest, but when do TPM levels become low enough that we would want to exclude them?