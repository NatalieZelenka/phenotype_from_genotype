# Introduction

## Motivation
To recap, I created `Ontolopy` in order to create a high-coverage mapping between tissues and gene expression samples, which I hoped would aid in phenotype and protein function prediction.

## Mapping samples to tissues
There are many gene expression data sets, and the reporting for tissue metadata is not at all standardised between them.
This is true even within databases of gene expression data where great care has been taken to harmonise the metadata such as the Gene Expression Atlas.
If tissue type is recorded at all, it is usually manually given a label tissue using a name (e.g. "blood", "kidney"), or perhaps as part of the sample name ("blood adult donor1"). 
In other cases, cell type might be recorded instead (e.g. "leukocyte", "cardiac fibroblast").
In other circumstances still, the samples might be annotated to existing ontologies, and some even have their own ontologies of samples (such as FANTOM5).

Names like *blood* can be useful, but if you'd like to compare across samples, then it's helpful to have a controlled vocabulary such as ontology terms.
There is a wealth of information about tissues and cells in existing ontologies, particularly Uberon, the cross-species anatomy ontology, and the Cell Ontology. 
For example, Uberon contains information about synonyms for different anatomical entities: the *pituitary stalk* is also known as the *infundibular stem* which is part of the brain that connects to the *hypothalamus*. 


### The power of ontologies

### Uberon

## Why OBO files?

## Other available tools
### GOAtools
### Protege
- for `.owl` files


(ontolopy-purpose)=
## Purpose

```{figure} ../images/ontolopy_logo.png
---
height: 220px
name: ontolopy-logo
---

```
```

[//]: # (TODO: delete backticks)

`Ontolopy` takes `.obo` files and:
 1. makes them into an intuitive Python object (which subclasses a Python `dict` (dictionary object), meaning that you can do everything with it that you can do with this very popular and useful data type.
 2. provides a set of tools for doing some useful manipulations and queries to these objects, which are particular to ontologies.

