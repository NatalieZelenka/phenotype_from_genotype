# Data
[//]: # (TODO: Write)

## Gene expression data
I chose the FANTOM5 data (at the time the latest data output of the {ref}`FANTOM consortium<fantom-consortium>`) as the input gene expression data for `filip`, for the following reasons:
- The data set has a good coverage of different tissue types, meaning that `filip` should be able to turn this into a good coverage of predictions.
- The data set uses Capped Analysis Gene Expression (CAGE) technology, meaning that it has information per transcript (i.e. per protein, rather than per gene).
- The data set has an ontology of samples, which is already linked to Uberon tissue terms and CL cell terms, making the mapping process much easier.

```{margin} The FANTOM Consortium
:name: fantom-consortium
The Functional ANnoTation Of the MAmmalian genome (FANTOM) consortium was established as the human genome project was nearing completion when researchers had a parts list of human biology, but few of the functions of these parts (genes) were known. The consortium has run a range of large scale collaborative projects in five rounds to further this goal. The first FANTOM project used only the mouse genome, but later versions also included human. 
```

## Validation: CAFA data

## CAFA2 - During Development
During development, I tested `filip` by comparing DcGO only and `filip` + DcGO on data from the 2nd round of the CAFA competition: CAFA2.

## CAFA3 
I entered DcGO only, and `filip` + DcGO into the CAFA3 competition in order to test `filip` on a new dataset, and have the validation independently reproduced by an unaffilated researcher.