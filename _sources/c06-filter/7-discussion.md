(filip-discussion)=
# Discussion and Future work
[//]: # (TODO: rewrite - this is out of date. Discuss the ever-changing GO ontology anotations and other issues relating to validation)

However incrementally, Filip met its goal of increasing the precision of DcGO predictions: Filip was correct in 99.973% of it's predictions, showing that this could be a useful approach if coverage can be increased.
In addition, 100% of wrongly filtered out (true) predictions, appear to be explainable due to the sample condition of the gene expression data (development-related phenotypes, with a lack of development age tissue-specific samples).

The results show that including gene expression information does improve results of a structure-based predictor, and that this improvement is extremely unlikely to be due to chance.
The overall improvement is very slight, but this could be be improved by a more comprehensive coverage of gene expression data for tissues, and/or by an improved mapping of tissues to ontology terms.

(filip-coverage)=
## Coverage
We have seen that Filip was successful for 99.973% of it's "choices", but that the number of decisions it could make were not enough to usefully boost the performance of the predictor it was tested on.
This reveals that the limited success of Filip on the CAFA data is due to it's poor mapping coverage. 

Although the FANTOM5 data set has a excellent coverage of tissue types and number of samples, the filter is nonetheless limited to the tissues it contains. 
This low coverage of tissues limits the number of predictions that Filip can filter out, and as we saw in the results, this is the major bottleneck for it's performance.
However, by {ref}`combining baseline gene expression sets from multiple sources<c05-combining>`, the coverage of tissues and therefore phenotype terms might be improved. 

In addition, although proteins, tissues and protein functions may be present in multiple species, Filip only currently measures if a gene is expressed in the human tissue of interest.
This further reduces the coverage of CAFA predictions that Filip could be tested on.

In addition to the influence of the input gene expression data set, the poor coverage is also limited by the quality of the mapping, which is reliant on the input metadata and ontologies.
In this initial test of Filip, I did not include mappings via Cell Ontology terms. 
Including Cell Ontology terms can increase the coverage (see {numref}`cl-increases-coverage`).

(practicalities-improving-coverage)=
### Practical difficulties in finding and creating alternative input data
In theory, Filip could be used with any other RNA-Seq data set with a wide range of tissues. 
In practice, however, finding a data set with the appropriate spread of tissues and cell samples (and furthermore, detailed metadata about these samples) is difficult.

The Ontolopy package ({ref}`next chapter<c06-ontolopy>`) does make mapping samples to Uberon tissues possible, even when only names or descriptions of the tissues are present. 

(filtered-out)=
## Wrongly filtered out tissues
100% of wrongly filtered out tissues were "development" terms. 
This could mean that time is another way in which cell context should be considered, for example we shouldn't filter out predictions for development phenotypes if we only have adult/not-fetal tissues, and perhaps vice versa.
Should we include developing tissue samples as evidence that a gene is expressed in a tissue type if the phenotype manifests after development?
This is another question for which it would be necessary to increase the coverage of the GE data set(s) used by Filip to answer.

(filip-future-work)=
## Future work
There is some additional work that needs to be done with Filip to get it to the stage of being ready for publication.
This primarily includes testing on more protein function prediction methods, and software engineering work necessary to release it as a resource for others to use in future CAFA competitions or similar (e.g as a public Python package/command line tool).
The mappings between phenotype terms and tissues should also be made available at this time, so that other people can easily interrogate these for individual genes.

I plan to do this work in time for the next CAFA challenge (CAFA5), by which time I would like to improve the coverage using the mapping improvements made in the rest of this thesis, specifically those made by including the cell ontology (in addition to Uberon - explained in the next chapter, and using the {ref}`combined tissue-specific gene expression data set<c05-combining>`.
I would also like to enter CAFA5 using the naive predictor plus Filip, to test Filip's potential as a standalone predictor.

(filip-speed)=
### Speed
For usability, it would speed up the process of running Filip on new predictors considerably to pre-calculate the tissue-phenotype pairs. Currently, this process is done within Filip, which makes it somewhat slow.

(filip-protein-abundance)=
### Protein abundance
As noted earlier, gene expression data is a measure of mRNA abundance, not protein abundance, and it is not especially well correlated with it. 
Furthermore, when it is available, protein abundance data outperforms mRNA data for predicting gene function{cite}`Buccitelli2020-ei`. 
By choosing a sensible cut-off for gene expression, we do discard some of the transcriptional noise which characterises some of the difference between mRNA and protein abundance, which is good.
Still, Filip would almost certainly throw away more false positive predictions if the mRNAs that are destined for degradation weren't present in the input data.

There are some attempts to predict protein abundance from mRNA abundance{cite}`Terai2020-lv`. 
It would be interesting to investigate if these predictors can improve the performance of Filip.
