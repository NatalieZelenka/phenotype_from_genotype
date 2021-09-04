---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.9.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(batch-correction-section)=
# Batch correction

## Pre-batch-corrected data
[//]: # (TODO: Add batch before graph - high priority)
Visual inspection of the PCA plot in {numref}`combine-pca-before` shows that data clusters by experiment more strongly than by tissue group, meaning that batch correction is necessary to compare across experiment samples.

```{code-cell} ipython3
:tags: [hide-input]

# Code to create combine-pca-before
```

```{figure} ../images/combine-pca-before.png
name: combine-pca-before
PCA plots without batch correction coloured by experiment (left) and tissue group (right). 
This PCA was carried out on a subset of 1000 randomly selected genes, after quantile normalisation and filtering of absent genes.
```

+++

## Correcting batch with ComBat
The batch effects that can be seen in {numref}`combine-pca-before` were corrected using {ref}`ComBat<combat-description>` {cite}`Johnson2007-zh`.

### Experimental design
[//]: # (TODO: table showing unbalanced experimental design over 11 tissue groups, + 4 experiments - lower priority)

```{code-cell} ipython3
:tags: [hide-input]

# code to create experimental design table (tissue groups by experiments?)
```

## Post batch-correction
[//]: # (TODO: post-PCA batch correction - high priority)

```{figure} ../images/combine-pca-after.png
name: combine-pca-after
PCA plots with batch correction coloured by experiment (left) and tissue group (right). 
This PCA was carried out on a subset of 1000 randomly selected genes, after quantile normalisation and filtering of absent genes.
```

Visual inspection of the PCA plots in {numref}`combine-pca-after` shows that ComBat has been successful in removing batch effects: samples no longer cluster by experiment, but by tissue group.

```{code-cell} ipython3
:tags: [hide-input]

# Code to create combine-pca-after
```
