# Discussion
[//]: # (TODO: rewrite - this is out of date. Discuss the ever-changing GO ontology anotations and other issues relating to validation)

## Limitations

### Reliance of prototype on FANTOM 5
Although the FANTOM5 data set has a excellent coverage of tissue types and number of samples, the filter is nonetheless limited to the tissues it contains. 
This low coverage of tissues limits the number of predictions that `filip` can filter out, and as we saw in the results, this is the major bottleneck for it's performance.
However, by combining baseline gene expression sets from multiple sources (the focus of {ref}`the next chapter<c05-combining>`), the coverage of tissues therefore phenotype terms might be improved. 

In addition, although proteins, tissues and protein functions may be present in multiple species, `filip` only uses human data, so the filter only measures if a gene is expressed in the human tissue of interest, making it only suitable for this class of predictions.

### Practical difficulties in finding and creating alternative input data
In theory, `filip` could be used with any other RNA-Seq data set with a wide range of tissues. 
In practice, finding a data set with the appropriate spread of tissues and cell samples (and furthermore, detailed metadata about these samples) is difficult.

However, the `uberon-py` package does provide make mapping samples to Uberon tissues much easier, even when only names or descriptions of the tissues are present. 

### mRNA abundance, not protein abundance
As {ref}`noted earlier<>`, gene expression data is a measure of mRNA abundance, not protein abundance, and it is not especially well correlated with it. 
Furthermore, when it is available, protein abundance data outperforms mRNA data for predicting gene function{cite}`Buccitelli2020-ei`. 
By choosing a sensible cut-off for gene expression, we do discard some of the transcriptional noise which characterises some of the difference between mRNA and protein abundance, which is good.
Still, `filip` would almost certainly throw away more false positive predictions if the mRNAs that are destined for degradation weren't present in the input data.

### Coverage
[//]: # (TODO: Write)
In addition to the influence of the input gene expression data set, the poor coverage is also limited by the quality of the mapping, which is reliant on the input metadata and ontologies.

## Wrong-ly filtered out tissues
[//]: # (TODO: Write)

## Summary
However incrementally, `filip` met its goals in increasing the precision of DcGO predictions: `filip` was correct in 99.973% of it's predictions, showing that this could be a useful approach if coverage can be increased.
In addition, 100% of wrongly filtered out (true) predictions, appear to be explainable due to the sample condition of the gene expression data.

The results show that including gene expression information does improve results of a structure-based predictor, and that this improvement is extremely unlikely to be due to chance.
The overall improvement is very slight, but this could be be improved by a more comprehensive coverage of gene expression data for tissues, and/or by an improved mapping of tissues to ontology terms.
