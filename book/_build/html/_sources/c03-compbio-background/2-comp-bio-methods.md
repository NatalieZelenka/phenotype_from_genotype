(compbio-methods)=
## How large computational biology datasets are used
[//]: # (TODO: rename title)
[//]: # (TODO: Include?? As the amount of data from high-throughput sequencing experiments has piled up, computational approaches have been ever-more necessary to make sense of the data.)

### Making sense of lists
The output of high throughput sequencing experiments can often be a long list of variants or genes (e.g. the outputs of GWAS studies or differential expression). 

[//]: # (TODO: Check where GO is first mentioned!)
#### Term enrichment
Ontologies are often used to try to make sense of a list of genes that are found to be differentially expressed across different experimental conditions. In the context of GO, a term enrichment analysis can be carried out to see which GO terms are overrepresented (aka enriched) for a given group of genes, thus saying something about the function of the list of genes. 

##### DcGO
The aim of the Domain-centric Gene Ontology (DcGO){cite}`Fang2013-ms,Fang2013-ix` tool is to give insight into uncharacterised or poorly characterised proteins by leveraging information about the content of their constituent protein domains. It annotates domains and combinations of domains (supradomains) to phenotype terms from a variety of ontologies, including the Gene Ontology (GO), Mammalian Phenotype ontology (MP), Disease Ontology (DOID), Zebrafish ontology (ZFA). Domain information comes from SUPERFAMILY, and annotations between (supra)domains and phenotype terms are made below a cut-off of FDR-adjusted statistical associations between the entities. Using phenotypes from a range of species serves to make use of greater numbers of experiments, and therefore increases the number of little-known proteins across species that DcGO can make predictions about.

#### Variant prioritisation
To narrow down a long list of genes or variants to a shorter list of variants or genes which is more likely to be causal, variant prioritisation is used.

##### FATHMM
Functional Analysis through Hidden Markov Models (FATHMM){cite}`Shihab2013-pk` is a tool for predicting the functional effects of protein missense mutations using sequence conservation information (via HMMs), which can be (optionally) weighted by how likely a mutation in a protein/domain would be to lead to disease. Weightings are calculated from the frequency of disease-associated and functionally neutral amino acid substitutions in protein domains from human variation databases (the Human Gene Mutation Database{cite}`Stenson2009-jc` and Uniprot-KB/Swiss-prot{cite}`Pundir2016-ya`).

Consequence files describing whether an amino acid results in a missense, nonsense or synonymous SNP must first be obtained by using Ensembl’s Variant Effect Predictor{cite}`McLaren2016-di` in order to create input to FATHMM. FATHMM then calculates conservation scores which are a measure of the difference in amino acid probabilities for a SNP according to the HMM, i.e. between a wild type amino acid and it’s substitution. A reduction in amino acid probabilities is interpreted as a prediction of deleteriousness, and the larger the reduction the greater the predicted harm. 

---
**Chapter References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```