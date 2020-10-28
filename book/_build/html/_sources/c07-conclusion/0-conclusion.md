(c07-conclusion)=
## Conclusion
[//]: # (TODO: Rewrite: tell the truth)
Because of the broad range of projects in this thesis (and the speed at which new methods and datasets become available in this field), there are a number of avenues for future work. 

The continued development of the phenotype predictor is something that continues to interest me. In particular, I would love to include tissue-specific gene expression information, and tissue-specific gene networks to see if this enables the predictor to make more accurate predictions for the benchmark data that is currently available. However, I feel that this should be on hold until a sensitivity/multiverse analysis of the components of the predictor (FATHMM and DcGO) can be carried out, and until annotations that are used to benchmark such a tool can be of an assured level of reliability.

My immediate next steps will be to make the combined gene expression dataset more usable, to finish the current iteration of the MAPS project, and to carry out a multiverse analysis for calculating gene-enrichment.

After that, I think that testing the limits of ComBat for combining unbalanced datasets and comparing that to batch effect removal using MNN is a promising avenue for further research.

These activities will help to lay further groundwork for combining different data sets in order to facilitate predicting and explaining how function and phenotype arise from genotype.

### Closing remarks

My work has shown that bringing baseline gene expression data into protein function predictions will (with current data) slightly increase the accuracy of those predictions. The value of this work has also been the development of methods for combining datasets, as well as the errors and unexpected data features that this has uncovered.  

In my attempts to make explanative genome-wide predictions about protein function, I have continuously bumped up against the limits of what is possible with the data that we currently have. This thesis describes some of these current limits are and highlighted areas where our fantastic collaborative open resources in computational biology could be improved to allow them to be used for big-picture biology. In particular it has shown the instability of gene enrichment measurements to annotation libraries.

Accurate protein function and phenotype prediction (particularly without leaning on “black-box” methods like deep learning) may be out of reach for now. However, progress is being made at a blistering speed in computational, biological and meta-research. Computational biology is a field that has had open data for much longer than others; it is well-placed to rise to the challenge of curating high quality research data. 

When some of these pieces move into place, I hope that the prediction-related methods, tools and datasets that I have made available will be a useful resource for future researchers (including myself!). Until then, I hope to spend my time contributing to the discussion about reproducibility and data provenance in computational biology in order to hurry that day along. 

