## Clustering SNPs

2.2.2.5 Implementation of different clustering and outlier detection methodologies
2.2.2.5.1 The curse of dimensionality
The "curse of dimensionality" is a phrase coined by Richard E Bellman, during his work on dynamic programming[61], but has since proved relevant in many different mathematical and data-driven fields. In addition to it's more colloquial use as a catch-all complaint about high-dimensional data, the "curse" refers to the sparsity of data that occurs exponentially with an increase in dimensions. This leads to various problems in different fields[62] and of which we run into two in this chapter; general difficulty in reaching statistical significance and reduced usefulness of clustering, distance, and outlier metrics.

This problem can be reduced by choosing a clustering/outlier detection method which is more robust to the number of dimensions. It is also helpful to reduce the number of dimensions in some way (feature selection), or to project the data into a different coordinate system (feature projection) and then discard some of the newly calculated coordinates/dimensions.

A range of clustering methods were trialled on the phenotype predictor in an attempt to overcome the curse of dimensionality and increase the phenotype predictor’s accuracy. Jan mostly implemented the Spectral Clustering, while I implemented the other methods.
2.2.2.5.2 Choice of distance metric
The phenotype predictor’s original distance metric was non-linear, such that the homozygous calls were further from each other than the distance via the heterozygous call, as shown in Figure 10. Non-linear distance metrics mean that it is not possible to create a location matrix rather than a distance matrix. This is required for some types of clustering. 

Figure 10: Original non-linear distance metric. MM denotes homozygous mutant alleles, WW denotes homozygous wild type alleles, and MW denotes heterozygous alleles. The FATHMM score for the SNP, f, defines the distance between the wild type and mutant alleles.

A linear distance metric which also captured the increased likelihood of homozygous alleles to be disease-causing (Figure 11) was developed to enable this, and to better represent the biology. In this version, the popularity of an allele decides which homozygous call the heterozygous call is more functionally similar to. 




Figure 11: Linear distance metrics. MM denotes homozygous mutant alleles, WW denotes homozygous wild type alleles, and MW denotes heterozygous alleles, and N represents the number of people with that allele call. The FATHMM score for the SNP, f, defines the distance between the wild type and mutant alleles. 
2.2.2.5.3 Clustering
The original implementation of the phenotype predictor used k-means clustering[63]. This wasn’t suitable for the predictor, since we expect combinations of SNPs to form non-spherical shapes (see Figure 12), and k-means cannot achieve this (see Figure 13).

Figure 12:  A drawing indicating how the combinations of SNPs we might expect to cause disease would represent a non spherical relationship between SNPs. 

Spectral clustering, DBSCAN (Density-Based Spatial Clustering of Applications with Noise) , OPTICS and LOF (Local Outlier Factor) were also implemented. This involved automation of parameter selection, to enable clustering to be performed automatically on thousands of phenotype terms. These methods have theoretical pros and cons with respect to the predictor. For example, OPTICS and DBSCAN do not need the number of clusters as an input, but instead require the minimum number of points required to form a cluster and a radius from each point to consider as part of a cluster, which has more meaning in this context. They also automatically output outliers to clusters, which will affect the resulting phenotype score, potentially in unseen ways - particularly as it is difficult to visualise high-dimensional data. OPTICS is the default setting, as in addition to not requiring a number of clusters, it can identify clusters of differing densities (a quality that DBSCAN lacks - as can be seen in the second row of Figure 13). A final informed choice between these options requires a large benchmarking set.

Figure 12: Comparison illustrating differences between the implemented clustering methods. Image adapted from sklearn documentation[64].

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```