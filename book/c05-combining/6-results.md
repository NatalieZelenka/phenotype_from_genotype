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
[//]: # (TODO: Write)
[//]: # (TODO: EDA of the combined data set)
[//]: # (TODO: Move simulated data to A. Creation of simulated data and B. Batch effects)

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

### Dat aset
[//]: # (TODO: REWRITE: Maybe this should be in dicussion/limitations mostly)
[//]: # (TODO: Have the data set available for download somewhere)

The combined data set represents 122 healthy tissues (all of which map to Uberon terms), over almost 20,000 samples, all which have consistent labelled sample information (age, development stage, sex). 
This information can now be used to increase coverage of the FilP filter of protein function predictions. 



The problem of batch effects for this dataset has not yet been overcome. This means that the dataset can not yet be used for the purpose of improving measurements from baseline experiments (e.g. housekeeping genes or baseline tissue-specific gene expression).

[//]: # (TODO: Rewrite: and sigpost to FilP rather than refer to it because I haven't mentioned it yet.)
However, by overcoming the data cleaning and standardisation necessary to have all datasets in the same format with the same sample metadata, the dataset can be used for analyses where batch and other sample metadata is used as covariates (e.g. differential expression of tissues).  
In its current iteration, it is also suitable for use in FilP, where the data set only needs to distinguish between presence and absence.

[//]: # (TODO: double-check for any mention of FilP in this chapter)

