## Methods
[//]: # (TODO: Overview here?)
[//]: # (TODO: Code here)
[//]: # (TODO: Links to packages, etc)

### Choosing an expression cut-off
FilP filters out predictions which are not expressed in the tissue relating to the prediction. Deciding whether a gene is or isn’t expressed in a tissue is not trivial with gene expression data, since it can be noisy. Therefore a cut-off must be chosen.  This cut-off was chosen for TPM-normalised data was chosen as this best allows for comparing between different samples. The cut-off was chosen by plotting the distribution of TPM expression and choosing a value below which there appeared to be little noise (10 TPM).

### Mapping multi-species phenotype terms to tissue
[//]: # (TODO: Figure 14:)
Figure 14: A diagram illustrating parts of the UBERON and GO ontologies, with a fictional example of an UBERON-GO relationship. In this example, Regulation of lung development would be related to Left lung, but not to Bronchiole (as regulation of lung development could refer to a regulation of a different part of the lung).

The extended uberon ontology is first interrogated for any existing relation to the term in the ontology. Failing this, text-mining is used to map based on phenotype term names. After removing regular (nltk) stopwords (e.g. “and”,”the”) and a small number of manually curated phenotypic stopwords (e.g. “phenotype”, “abnormality”), an exact match between an UBERON term’s name or synonyms and phenotype term’s name is searched for. If such a match does not exist, individual words from the phenotype term are then searched for exactly, such that the HP term “abnormality of the head and neck” would be mapped to UBERON’s “head” and “neck” terms (but never “neck of radius”). In cases where multiple terms are found, a common parent would be searched for, in the case of this example, “craniocervical region”. 

Failing that, a TF-IDF based similarity measure is used to search a list of related words (e.g. “mental” and “brain” have high similarity since they often appear together. The similarity measures are based on the term descriptions in both ontologies. There were a small number of outstanding phenotype terms, which were manually mapped to relevant phenotype terms where one existed.

## Limitations
[//]: # (TODO: Rewrite since FANTOM5 is not the data set any more).

Although the FANTOM5 data set has a good coverage of tissue types and number of samples, the filter is nonetheless limited to the tissues it contains. It is also limited by the coverage and accuracy of the mapping from phenotype to tissue.

Similarly, although proteins, tissues and protein functions may be present in multiple species, FilP only uses human data, so the filter only measures if a gene is expressed in the human tissue of interest. This means that where there are differences in expression between species, FilP will be incorrect if it is run on non-human data (not recommended).



---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```