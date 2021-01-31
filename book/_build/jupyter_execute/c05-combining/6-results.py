## Results and outputs
[//]: # (TODO: EDA/summary statistics of the combined data set: high priority)
[//]: # (TODO: How these stats compare to the consistuent data sets: medium priority)

## Combined data set

<!--
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
-->

[//]: # (TODO: Have the data set available for download somewhere - highest priority)
[//]: # (TODO: Rewrite: and signpost to FilP rather than refer to it because I haven't mentioned it yet.)


The combined data set represents 122 healthy tissues (all of which map to Uberon terms), over almost 20,000 samples, all which have consistent labelled sample information (age, development stage, sex). 
This information can now be used to increase coverage of the FilP filter of protein function predictions. 


### Other outputs
In creating the combined data set, I created the {ref}`uberon-py<uberon-py>` Python package, and by combining ontologies and omics data sets, I {ref}`contributed towards improving these resources<FANTOM5-inconsistencies-example>`.