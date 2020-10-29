## Discussion
It is disappointing that the phenotype predictor does not produce statistically significant results. However, the phenotype predictor may yet be useful for revealing candidate SNPs for certain kinds of diseases, and when a suitable data set becomes available (e.g. through the growing number of publicly available genotypes on platforms such as OpenSNP{cite}`Greshake2014-mp`), this method will still be ready to be tested. An alternative validation would be experimentally testing a prediction (e.g. with knockouts) of a phenotype with a highly interesting distribution of scores.

Despite much development effort, there remain some idiosyncrasies to the predictor. For example, DcGO can map multiple terms to the same set of SNPs. This can sometimes be a diverse group of phenotypes which do not tend to co-occur in individuals and when this occurs, it is likely that we cannot make a good prediction. A semantic similarity measure, such as GOGO{cite}`Zhao2018-rw` or Wang’s method{cite}`Wang2007-yc` could be used to check this, and update the confidence score accordingly.

There are also clearly many aspects of the molecular biology mentioned in chapter 1 that are not represented in the model used by the phenotype predictor. For example, nonsense mutations, regulatory networks, the environment of the cell (e.g. tissue-specific gene expression). Updating the predictor to include these things could potentially give the predictor enough power to be validated on existing data sets. For example, non-coding variants could be included by extending DcGO annotations to SNPs in linkage disequilibrium, and using the non-coding version of FATHMM (FATHMM-XF{cite}`Rogers2018-rc`).

In investigating some of the ALSPAC phenotype predictions, I identified that some of the predicted dcGO relations between proteins and ontology terms may not be expressed in the tissue of interest. Improving dcGO or FATHMM may be a good route for improving the predictor, and this is the focus of the next Chapter.

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```
