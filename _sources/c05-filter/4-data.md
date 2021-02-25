# Data
[//]: # (TODO: Write)

## Gene expression data

### What?

`filip` requires gene expression data to inform whether or not predictions should be filtered out. The FANTOM5 data set was chosen for this purpose (at the time this was the latest data output of the {ref}`FANTOM consortium<fantom-consortium>`).

FANTOM5 represents one of the most comprehensive collections of gene expression data. 
It contains a combination of human, mouse, health, and disease data, as well as time courses and cell perturbations.

```{margin} The FANTOM Consortium
:name: fantom-consortium
The Functional ANnoTation Of the MAmmalian genome (FANTOM) consortium was established as the human genome project was nearing completion when researchers had a parts list of human biology, but few of the functions of these parts (genes) were known. The consortium has run a range of large scale collaborative projects in five rounds to further this goal. The first FANTOM project used only the mouse genome, but later versions also included human. 
```

[//]: # (TODO: What does the data contain, how many samples, etc)

### Why?

I chose the FANTOM5 data as the input gene expression data for `filip`, for the following reasons:
- The data set has a good coverage of different tissue types, meaning that `filip` should be able to turn this into a good coverage of predictions.
- The data set uses Capped Analysis Gene Expression (CAGE) technology, meaning that it has information per transcript (i.e. per protein, rather than per gene).
- The data set has an ontology of samples, which is already linked to Uberon tissue terms and CL cell terms, making the mapping process much easier.

### How? Data Acquisition

[//]: # (TODO: How did I get the data?)

## Validation: CAFA data

## CAFA2 - During Development

### What?
During development, I tested `filip` by comparing DcGO only and `filip` + DcGO on data from the 2nd round of the CAFA competition: CAFA2. 
This was the most recent round of CAFA for which there were "groundtruth" data available at the time of development.
The data consisted of CAFA2 targets and the CAFA2 ground truth data.

**CAFA2 targets**: 

[//]: # (TODO: describe data format)

**CAFA2 groundtruth**: 

[//]: # (TODO: describe data format)

### Why?
[//]: # (TODO: Cite swissprot KB and GOA)

I chose to use the CAFA2 data because rather than a larger set of annotations (such as those available from SwissProt-KB or GOA) because it provided a way of validating on unknown targets.
I.e. if I made predictions with DcgO using the version of GO from the time the challenge was launched, and I use the groundtruth data provided by CAFA2, then I could compare my results with those in the CAFA2 competition and I could look at my results on unknown targets.

### How?
[//]: # (TODO: describe data acquisition)

## CAFA3 
After initial development, I entered DcGO only, and `filip` plus DcGO into the CAFA3 competition in order to test `filip` on a new dataset.

This meant that I did not download the CAFA3 groundtruth, as this analysis was done by the CAFA3 team, but only the CAFA3 targets.

**CAFA3 targets**: 

[//]: # (TODO: describe data format)


