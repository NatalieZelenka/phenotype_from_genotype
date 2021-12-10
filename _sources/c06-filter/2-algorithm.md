(filter-algorithm)=
# Algorithm

In order to overcome the problem of predictors containing erroneous predictions due to a lack of gene expression information, I have created a lightweight tool which allows researchers to filter their phenotype or protein function predictions using tissue-specific gene expression information.
 
````{margin} Naming things
:name: naming-things

> There are only two hard things in Computer Science: cache invalidation and naming things
>
> -- Phil Karlton

Aside from the above joke, there is also evidence in the literature{cite}`Pottegard2014-yc` to suggest that strained acronyms exist across scientific disciplines. 

````
 
Drawing on the noble tradition of scientists {ref}`naming things badly<naming-things>`, I call this Filip as it is for **Fil**ter**i**ng **p**redictions. 

(filter-algo-overview)=
## Overview

{numref}`filip-overview` illustrates Filip's two-step approach, which aims to filter out predictions for proteins which are not created in the tissue of interest (related to the predicted phenotype).
The filter is a simple rule-based tool, which is designed to be used on top of any protein function predictor, but would provide the most value for predictors that rely on structural or sequence similarity.

```{figure} ../images/filip.png
---
name: filip-overview
width: 300px
---
An illustration showing how Filip works. 
It's a two-step process where protein-phenotype predictions are expected as input. 
In step 1,*preprocessing*, proteins are mapped to genes, and phenotypes are mapped to tissues. 
In step 2, *filtering*, Filip filters out any predictions where for which the gene is not expressed in the tissue.
```

[//]: # (TODO: cross-ref to previous mention of FANTOM5, or include as margin comment)
[//]: # (TODO: Cite FANTOM5)
[//]: # (TODO: cross-ref to UBERON, and make sure it is included in ontology section)
[//]: # (TODO: cross-ref next section)
[//]: # (TODO: cross-ref to Ontolopy section)

(filter-inputs)=
## Inputs
Three types of input are needed for Filip: 
1. Protein function predictions 
2. Normalised gene expression data.
3. A map from gene expression samples to Uberon tissues. 

(input-predictions)=
### Protein function predictions
Protein function predictions must be links between Protein identifiers and phenotype terms from GOBP, HP, MP or DOID ontologies. 
This is the standard for CAFA competitions.

(input-ge)=
### Gene expression file
If Filip was a filter coffee machine, the gene expression (GE) file would be the (reusable) filter: it is the part that determines what can and cannot pass through the  filter and it can be used with any kind of input predictions (coffee). 
Once we have the GE file, it can be reused for any different protein function predictor, as long as it predicts phenotype terms related to the samples in our GE file.

The user must also determine a cut-off: the minimum gene expression level to count as "expressed". 
The higher the cut-off the more genes will count as unexpressed, and therefore more predictions will be filtered from the original list.

(input-sample-tissue)=
### Sample-tissue map
Some GE datasets will include a sample-to-Uberon map as part of their metadata (e.g. FANTOM5).
For those that don't, the {ref}`ontolopy<c06-ontolopy>` Python package can be used to map between samples tissue names and their Uberon tissue.

(filter-preprocessing)=
## Step 1: Preprocessing
The preprocessing file outputs:
1. A phenotype-to-sample map, which stores a list of column indices in the gene expression file which Filip should use for filtering each phenotype.
2. A protein-to-gene map, which maps between proteins present in the input predictions and genes present in the input GE file.

Mapping between phenotype and sample is the most invovled part of Filip: it relies on Ontolopy ({ref}`next Chapter<c06-ontolopy>`) to create this mapping.

(filter-filtering)=
## Step 2: Filtering
The filtering step takes the orginal inputs, preprocessing outputs, and a GE cutoff as input. 
It outputs a reduced list of predictions that are still valid (are expressed above the cut-off on average across the samples).
