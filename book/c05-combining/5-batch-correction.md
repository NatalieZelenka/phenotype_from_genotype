---
jupytext:
  formats: ipynb, md:myst
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

# Batch correction
[//]: # (TODO: Batch corrected results here)
[//]: # (TODO: Cross-ref to ComBat description <combat-description>)

## Pre-batch-corrected data
Visual inspection of {numref}`combine-pca-before` shows that data appears to cluster by experiment more strongly than by tissue group, meaning that batch correction is necessary to compare across experiment samples.

```{code-cell} ipython3
---
render:
  figure:
    caption: PCA plots without batch correction coloured by experiment (left) and
      tissue group (right). This PCA was carried out on a subset of 1000 randomly
      selected genes, after quantile normalisation and filtering of absent genes.
    name: combine-pca-before
  image:
    width: 200px
---
# Code to create combine-pca-before
```

