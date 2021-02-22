# Methods
[//]: # (TODO: Overview here?)
[//]: # (TODO: Code here)
[//]: # (TODO: Links to packages, etc)

+++

## Expression cut-off
[//]: # (TODO: Expression cut-off)

`filip` filters out predictions which are not expressed in the tissue relating to the prediction. Deciding whether a gene is or isn’t expressed in a tissue is not trivial with gene expression data, since it can be noisy. 
Therefore a cut-off must be chosen.  
This cut-off was chosen for TPM-normalised data was chosen as this best allows for comparing between different samples. 
The cut-off was chosen by plotting the distribution of TPM expression and choosing a value below which there appeared to be little noise (10 TPM).

+++

### Mapping multi-species phenotype terms to tissue

```{margin} Stop words
:name: stop-words
Stop words are words that are filtered out before processing text using Natural Language Processing (NLP) methods.
These are usually very common words (e.g. “and”, ”the”), or word which are meaningless in the context of the analysis. 
```

The extended Uberon ontology is first interrogated for any existing relation to the term in the ontology using `uberon-py`. 

Failing this, text-mining is used to assist in mapping based on phenotype term names:
- First {ref}`stop words<stop-words>` are removed, using the base list in the Natural Language Toolkit (`nltk`) Python Package{cite}`Bird2006-xu`, and a small number of manually curated phenotypic stopwords (e.g. “phenotype”, “abnormality”).
- Then, an exact match between an UBERON term’s name or synonyms and phenotype term’s name is searched for. 
- If such a match does not exist, individual words from the phenotype term name or synonyms are then searched for exactly, such that the HP term “abnormality of the head and neck” would be mapped to UBERON’s “head” and “neck” terms (but never “neck of radius”). 
- In cases where multiple terms are found, a common parent would be searched for, in the case of this example, “craniocervical region”. 
- Failing that, a similarity measure is used to search a list of related words. This finds important words in the document using {ref}`TF-IDF<tf-idf>`, and then creates a similarity measure based on co-occurance, e.g. “mental” and “brain” have high similarity since they often appear in the same document  (documents are term descriptions).
- This list was then used to aid in manually mapping to relevant phenotype terms where one existed. 

```{margin} TF-IDF
:name: tf-idf
Term Frequency, Inverse Document Frequency is a common and basic measure in NLP which attempts to measure how representative a term (word) is of a document. 
It is defined by {math}`tfidf=tf(t,d) \cdot idf(t,D) = (f_{t,d}) \cdot (\frac{N}{abs{d \in D : t \in d}) ` where {math}`f_{t,d}` is the frequency of a term {math}`t` in a document {math}`d`, {math}`N` is the number of documents, and {math}`{abs{d \in D : t \in d}` is the number of documents containing the term.
```

+++


```{code-cell} ipython3

```
## Validation

### CAFA Validation 
This confidence score allows for a range of possible sets of predictions, depending on the threshold parameter {math}`\tau`. 
Precision (the proportion of selected items that are relevant), and recall (the proportion of relevant items that are selected) are defined as:

{math}`precision = p = \frac{t_p}{t_p + f_p}`
{math}`recall = r = \frac{t_p}{t_p + f_n}`

Precision-recall curves are generally used to validate a predictors performance, but the {math}`F_1` measure combines these into a single measure of performance:

{math}`F_1 =2/ \frac{precision \cdot recall}{precision + recall}`

Since the precision and recall will be different for any {math}`\tau`, the {math}`F_{max}` score is the maximum possible {math{`F_1`} for any value of $\tau$.

[//]: # (TODO: explain the below a little more: how many measures does that make? 2 x2 = 4?)
CAFA validation can either be term-centric or protein-centric. For each option, submissions are assessed per species and for wholly unknown and partially known genes separately.

### Limitations of validation method
There is no penalty for making a broad guess, or reward for making a precise one. This is one of the reasons that the naive method does so well: for example it is not penalised for guessing that the root term of the GO BPO ontology Biological Process is related to every gene. 

Due to the nature of the validation set, it’s possible that the best-scoring CAFA methods simply predict which associations are likely to be discovered soon (i.e. associations to genes people are currently studying).

### Implementation
To create the input to DcGO, I used:
- BioPython{cite}`Cock2009-py`'s `Bio.SeqIO` interface for reading CAFA FASTA files.
- SUPERFAMILY{cite}`Gough2001-ct` [domain assignments for Homo Sapiens](https://supfam.mrc-lmb.cam.ac.uk/SUPERFAMILY/cgi-bin/save.cgi?var=ht;type=ass).
- UniprotKB{cite}`Pundir2016-vv`'s [mapping tool](https://www.uniprot.org/uploadlists/) to create a mapping between the UniprotKB id's provided by CAFA and the ENSP ID's used by SUPERFAMILY. 

Then, to create the DcGO only entry, I used the `DcGOR` library{cite}`Fang2014-hx` (the `dcAlgoPredictMain` function).