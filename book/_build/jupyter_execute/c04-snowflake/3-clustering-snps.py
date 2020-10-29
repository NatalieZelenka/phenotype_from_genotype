## Clustering SNPs

[//]: # (TODO: Write this section)

In this section, I implement clustering and outlier detection methodologies for SNPs.

### The curse of dimensionality
The "curse of dimensionality" is a phrase coined by Richard E Bellman, during his work on dynamic programming{cite}`Bellman1957-dc`, but has since proved relevant in many different mathematical and data-driven fields. In addition to it's more colloquial use as a catch-all complaint about high-dimensional data, the "curse" refers to the sparsity of data that occurs exponentially with an increase in dimensions. This leads to various problems in different fields{cite}`Zimek2012-fg` and of which we run into two in this chapter; general difficulty in reaching statistical significance and reduced usefulness of clustering, distance, and outlier metrics.

This problem can be reduced by choosing a clustering/outlier detection method which is more robust to the number of dimensions. It is also helpful to reduce the number of dimensions in some way (feature selection), or to project the data into a different coordinate system (feature projection) and then discard some of the newly calculated coordinates/dimensions.

A range of clustering methods were trialled on the phenotype predictor in an attempt to overcome the curse of dimensionality and increase the phenotype predictor’s accuracy. Jan mostly implemented the Spectral Clustering, while I implemented the other methods.

### Choice of distance metric
The phenotype predictor’s original distance metric was non-linear, such that the homozygous calls were further from each other than the distance via the heterozygous call, as shown in {numref}`non-linear-metric`. Non-linear distance metrics mean that it is not possible to create a location matrix rather than a distance matrix. This is required for some types of clustering.

```{figure} ../images/nonlinear_metric.png
---
height: 220px
name: non-linear-metric
---
Original non-linear distance metric. $MM$ denotes homozygous mutant alleles, $WW$ denotes homozygous wild type alleles, and $MW$ denotes heterozygous alleles. The FATHMM score for the SNP $f$, defines the distance between the wild type and mutant alleles.
```

A linear distance metric which also captured the increased likelihood of homozygous alleles to be disease-causing ({numref}`linear-metric`) was developed to enable this, and to better represent the biology. In this version, the popularity of an allele decides which homozygous call the heterozygous call is more functionally similar to.

```{figure} ../images/linear_metric.png
---
height: 220px
name: linear-metric
---
Linear distance metrics. $MM$ denotes homozygous mutant alleles, $WW$ denotes homozygous wild type alleles, and $MW$ denotes heterozygous alleles, and $N$ represents the number of people with that allele call. The FATHMM score for the SNP $f$, defines the distance between the wild type and mutant alleles. 
```

### Clustering
The original implementation of the phenotype predictor used k-means clustering{cite}`Le_Cam1967-ku`. This wasn’t suitable for the predictor, since we expect combinations of SNPs to form non-spherical shapes (see {numref}`non-spherical`), and k-means cannot achieve this (see {numref}`clustering-comparison`).

```{figure} ../images/clustering_snps.png
---
height: 220px
name: non-spherical
---
A drawing indicating how the combinations of SNPs we might expect to cause disease would represent a non spherical relationship between SNPs. 
```

```{figure} ../images/clustering_comparison.png
---
height: 220px
name: clustering-comparison
---
Comparison illustrating differences between the implemented clustering methods. Image adapted from sklearn documentation{cite}`noauthor_undated-nc`.
```

Spectral clustering, DBSCAN (Density-Based Spatial Clustering of Applications with Noise), OPTICS and LOF (Local Outlier Factor) were also implemented. This involved automation of parameter selection, to enable clustering to be performed automatically on thousands of phenotype terms. These methods have theoretical pros and cons with respect to the predictor. For example, OPTICS and DBSCAN do not need the number of clusters as an input, but instead require the minimum number of points required to form a cluster and a radius from each point to consider as part of a cluster, which has more meaning in this context. They also automatically output outliers to clusters, which will affect the resulting phenotype score, potentially in unseen ways - particularly as it is difficult to visualise high-dimensional data. OPTICS is the default setting, as in addition to not requiring a number of clusters, it can identify clusters of differing densities (a quality that DBSCAN lacks - as can be seen in the second row of {numref}`clustering-comparison`). A final informed choice between these options requires a large benchmarking set.


---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```