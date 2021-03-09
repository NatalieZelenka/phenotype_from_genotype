# Discussion
[//]: # (TODO: rewrite - this is out of date. Discuss the ever-changing GO ontology anotations and other issues relating to validation)

## Limitations
### Reliance on FANTOM 5
Although the FANTOM5 data set has a good coverage of tissue types and number of samples, the filter is nonetheless limited to the tissues it contains. 
It is also limited by the coverage and accuracy of the mapping from phenotype to tissue.

Similarly, although proteins, tissues and protein functions may be present in multiple species, FilP only uses human data, so the filter only measures if a gene is expressed in the human tissue of interest. 
This means that where there are differences in expression between species, FilP will be incorrect if it is run on non-human data (not recommended).
 Reliance on FANTOM
 
FilP’s low coverage of tissues (due to its reliance on the FANTOM dataset) limits the number of predictions that can be filtered out. 
However, by combining baseline gene expression sets from multiple sources (the focus of the next chapter), this coverage of tissues (and therefore phenotype terms) may be improved. 

[//]: # (TODO: Explain that mapping is difficult - so the approach is limited by the expression data set)

### Coverage

## Wrong-ly filtered out tissues

## Summary
However incrementally, `filip` met its goals in increasing the precision of DcGO predictions: `filip` was correct in 99.973% of it's predictions, showing that this could be a useful approach if coverage can be increased.
In addition, 100% of wrongly filtered out (true) predictions, appear to be explainable due to the sample condition of the gene expression data.

The results show that including gene expression information does improve results of a structure-based predictor, and that this improvement is extremely unlikely to be due to chance.
The overall improvement is very slight, but this could be be improved by a more comprehensive coverage of gene expression data for tissues, and/or by an improved mapping of tissues to ontology terms.
