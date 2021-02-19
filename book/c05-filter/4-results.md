## Results

+++

### CAFA3 Results

[//]: # (TODO: Explain validation in more detail)

I entered two models into CAFA3: DcGO only and DcGO plus FilP. Due to time constraints, I only entered CAFA3 with predictions for Human, and for Gene Ontology Biological Process terms. 

In all categories, FilP improved DcGO by 0.02 f-max (Table 1). This was not enough to be a competitive model (ranked between 33 and 38/67 for this category).
 
[//]: # (TODO: Format table 1 and check cross-refs)

Type (known/
unknown) 
Mode (protein/
term)
F-max (DcGO) 
F-max (DcGO + FilP)
type1
mode2
0.326
0.328
type1
mode1
0.326
0.328
type2
mode2
0.503
0.505
type2
mode1
0.503
0.505
Table 1: CAFA3 f-max results for DcGO and FilP.





+++

### Validation
The approach of the filter was validated using the CAFA2 data. In order to do this, the original DcGO CAFA2 submission was run on the CAFA2 targets, and FilP was applied to these DcGO results. 

The F-max score was calculated for human BPO, combining both type 1 and type2. The results (Table 2) show that FilP provides a small benefit to the F-max score. 

[//]: # (TODO: Format table 2 and check cross-refs)

F-max
DcGO only 
F-max
DcGO + FilP
F-max score
0.408
0.409
Table 2: F-max score with and without FilP 

```{code-cell} ipython3
# Figure 15: Graph of GO terms that FilP incorrectly removed from the predictions, made using ReviGO(Supek et al. 2011).
# TODO: Add code that creates this graph.
# TODO: Check cross-refs + figure labels work
```

FilP filtered out 85,637 GOBP human protein predictions, only 23 of which were true according to the CAFA2 ground truth. I
nterestingly, of these incorrectly filtered out predictions contained GO terms which were related to development (Figure 15). 
This may be due to the lack of developing tissues in the dataset used by FilP. 

```{code-cell} ipython3
# Figure 16: Bootstrapping histogram shows the distribution of the number of correct predictions found when deleting a random selection of dcGO predictions (the same number as are discarded by the filter). The dotted lines shows the number of correct predictions found by the filter. The low p-value (9.9910-5) is the probability of the filter performing as well as it has (number of correct predictions) by random chance.
# TODO: Add code that creates this graph.
# TODO: Check cross-refs + figure labels work
```

To check that the improvement due to FilP was not just due to the fact that there are more false positives in dcGO’s prediction than there are true positives, I performed a bootstrapping test by taking out random sets of 85,637 predictions (the number removed by FilP) from the dcGO set and measuring the number of true positives remaining in the set. 
This was repeated 100,000 times to create the histogram in Figure 16.

+++

### Combined data-set results
[//]: # (TODO: Write)
