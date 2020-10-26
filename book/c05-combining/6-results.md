---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

## Results
<!--TODO: Write-->

### Simulated data
Box-plots (figure {numref}`box-plot-sim`) shows that the simulated data has similar distributions to the true data, and PCA (figure {numref}`pca-sim`) reveals that batch effects are visible in the simulated data, as they are in the real data.

```{code-cell} ipython3
---
render:
  figure:
    caption: Box-plots showing distributions of the real (left) and simulated (right)
      data.
    name: box-plot-sim
  image:
    width: 200px
---
# Code for box-plots showing distributions of the real (left) and simulated (right) data.
```

```{code-cell} ipython3
---
render:
  figure:
    caption: PCA plot showing colour by experiment and tissue group.
    name: pca-sim
  image:
    width: 200px
---
# Code for PCA plot showing colour by experiment and tissue group. 
```


The simulated data does not simulate the mean expression that we would expect for a given tissue type or experiment, so the labels in {numref}`pca-sim` instead indicate the model design rather than the expression, i.e. there are the same number of GTEx-labelled simulated samples, which have the same breakdown of tissues as those in our final combined data set.

#### ComBat on simulated data
The obvious next step is to test batch effect removal such as ComBat on the simulated dataset. 

### Dataset
[//]: # (TODO: REWRITE!)
The combined dataset represents 122 healthy tissues (all of which map to Uberon terms), over almost 20,000 samples, all which have consistent labelled sample information (age, development stage, sex). This information can now be used to increase coverage of the FilP filter of protein function predictions. 

While a great deal of careful work has clearly been spent on making the datasets used in this analysis available and useful to researchers such as myself, there were still many barriers to their use in this circumstance. This ranged from mislabelled samples, to missing information, to having to seek data about the same experiment from multiple different sources. In particular, I think it’s important that key information that we know affects gene expression such as age, developmental stage, and sex are made available with the dataset and preferably in a format which is easy to compare across experiments. It is reassuring that the data issues that were discovered had clear pathways for reporting, and that some of them have already resulted in changes to the files used.

The problem of batch effects for this dataset has not yet been overcome. This means that the dataset can not yet be used for the purpose of improving measurements from baseline experiments (e.g. housekeeping genes or baseline tissue-specific gene expression).

However, by overcoming the data cleaning and standardisation necessary to have all datasets in the same format with the same sample metadata, the dataset can be used for analyses where batch and other sample metadata is used as covariates (e.g. differential expression of tissues).  In its current iteration, it is also suitable for use in FilP, where the dataset only needs to distinguish between presence/absence.

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```
