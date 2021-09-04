# Results 

## Validation of prototype `filip`

### CAFA 2
[//]: # (TODO: Explain how I calculated it differently - based on only the types of things I was trying to do, which is why it's a bigger number)

**{math}`F_{max}` Improvement:** 

```{list-table} CAFA2 data f-max results for DcGO and filip
:header-rows: 1
:name: cafa2-results

* - {math}`F_{max}` DcGO
  - {math}`F_{max}` DcGO + `filip`
* - 0.408
  - 0.409
```

During development, I validated `filip` using the original DcGO CAFA2 submission, using the CAFA2 targets.
The {math}`F_{max}` score was calculated for human BPO, combining both *No Knowledge* and *Limited Knowledge* targets. 
{numref}`cafa2-results` shows that `filip` provides a small benefit to the {math}`F_{max}` score. 
``
**Bootstrapping:** 

```{figure} ../images/filip_bootstrap.png
---
height: 300px
name: filip-bootstrap
---
This bootstrapping histogram shows the distribution of the number of correct predictions found when deleting a random selection of DcGO predictions (the same number as are discarded by the filter). The dotted lines shows the number of correct predictions found by the filter. The low p-value ({math}`9.99 \times 10^{-5}`) shows the low probability of the filter performing at least as well as it has (in terms of the number of correct predictions) by random chance.
```

The small improvement is due to `filip` filtering out 85,637 GOBP human protein predictions, only 23 of which were true according to the CAFA2 ground truth, meaning that 99.973% of filip's predictions (on what to filter in or out) were correct.

[//]: # (TODO: Explain that the majority of predictions are false, since e.g. DcGO predicts up to 5% of the space of all possible predictions is true - with varying confidence)

To ensure that this is a better success rate than we would expect by chance, I performed a bootstrapping test by taking out random sets of 85,637 predictions from the DcGO set and measuring the number of true positives remaining in the set. 
This was repeated 100,000 times to create {numref}`filip-bootstrap`, and calculate the p-value {math}`p < 0.001`, meaning that the filter performed far better than chance.

**Relationship between incorrect terms:** 

```{figure} ../images/revigo_filip_wrong_cafa2.png
---
height: 300px
name: filip-go-wrong
---
A grouping/summary of the incorrectly excluded predictions. Larger circles represent terms which are parents to more of the input terms.
```

I also looked to see whether there was any relationship between the 23 incorrectly removed predictions. 
Interestingly, all of these incorrectly filtered out predictions were for GOBP terms which were related to development (e.g. tissue development, anatomical structure development, epithelium development, organ morphogenesis). 
{numref}`filip-go-wrong` shows a summarises the incorrectly mapped GO terms, created using ReviGO{cite}`Supek2011-ii`. 
The fact that the incorrectly filtered out terms are all related to development implies there may be due to a bias in the developing tissues in the FANTOM5 data-set used by `filip`.

### CAFA 3 
[//]: # (TODO: Explain validation in more detail)
The same kind of improvement is seen by the independently calculated CAFA3 results (validated by the CAFA3 team).
I entered two models into CAFA3: DcGO only and DcGO plus `filip`, for Human and for Gene Ontology Biological Process terms only. 

In all categories, `filip` improved DcGO by 0.02 {math}`F_{max}` (see {numref}`cafa3-results`. 
This was not enough to be a competitive model (ranked between 33 and 38 out of 67 for this category).
Despite this, this result does show that the improvement was reproduced in another data set, carried out by other researchers.
 
[//]: # (TODO: Change labels to more sensible, e.g. type1 == -un-known, check)
[//]: # (NOTE: Type1 = no knowledge, type2 = limited knowledge, Mode1 = Full Assessement, Mode2 = Partial Assessment)

```{list-table} CAFA3 f-max results for DcGO and filip
:header-rows: 1
:name: cafa3-results

* - Type
  - Mode
  - {math}`F_{max}` DcGO
  - {math}`F_{max}` DcGO + `filip`
* - No Knowledge
  - Partial Assessment
  - 0.326
  - 0.328
* - No Knowledge
  - Full Assessment
  - 0.326
  - 0.328
* - Limited Knowledge
  - Partial Assessment
  - 0.503
  - 0.505
* - Limited Knowledge
  - Full Assessment
  - 0.503
  - 0.505
```

<!--

## Coverage

We have seen that `filip` was successful for 99.973% of it's "choices", but that the number of decisions it could make were not enough to usefully boost the performance of the predictor it was tested on.
This reveals that the limited success of `filip` on the CAFA data is due to it's poor mapping coverage. 

### Using `uberon-py`

### Overall
-->