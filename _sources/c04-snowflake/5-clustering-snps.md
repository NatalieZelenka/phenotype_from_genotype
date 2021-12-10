---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.9.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(clustering-snps)=
# Considerations for Clustering SNPs
[//]: # (TODO: Write this section)
[//]: # (TODO: Intrinsin dimensionality)
In this section, I discuss the implementation of clustering and outlier detection methodologies for SNPs.

Snowflake is essentially a method for finding unusual combinations of SNPs, within sets of SNPs associated with a phenotype.
Since there will be many rare combinations of SNPs just through randomness, the deleteriousness score (via FATHMM) decides which rare combinations are of interest.

[//]: # (TODO: Cross-ref to overview)
The clustering takes place per phenotype, with the distinct phenotypes and the SNPs associated with them are chosen according to dcGO. 
This therefore determines how many dimensions (SNPs) we are clustering on for any given phenotype

[//]: # (TODO: Explain that the data is sparse, only 3 options, but that even binary data can be clustered)

<!--
Put this back in if I can get to it
## Cases to test

While `snowflake` was created to find complex traits (featuring combinations of SNPs), we would also like it to work for single SNPs.
Data is simulated for the following cases, representing the diversity of phenotypes that `snowflake` should predict phenotypes for:
- 1 dominant (high-scoring) SNP with a rare allele
- 2 dominant SNPs with a rare combination of alleles
- 3 dominant SNPs with a rare combination of alleles
- 5 dominant SNPs with a rare combination of alleles
- 10 dominant SNPs with a rare combination of alleles
-->

(combinations-of-snps)=
## Combinations of SNPs

[//]: # (TODO: Maths not displaying on PDF)
[//]: # (TODO: Check how fathmm works, is it across all superkingdoms?)

[//]: # (TODO: tie in this section with the curse of dimensionality part)
Given $N$ SNPs of interest, there are $3^N$ different options for individual's combinations of calls for biallelic SNPS, since there are three different options for each SNP `WW` wild-wild homozygous, `MW`/`WM` heterozygous, or `MM` mutant-mutant heterozygous.
<!--{numref}`snp-combo-table` shows this for 2 SNPs.-->
For our purposes, heterozygous SNPs are considered the same whether they are mutant-wild `MW` or wild-mutant `WM`, since we assume they would create the same balance of proteins in a cell.

<!--
```{list-table} Table showing all possible combinations of calls for two biallelic SNPs where M denotes mutant type and W denotes wild type.
:header-rows: 1
:name: snp-combo-table

* - count
  - SNP 1
  - SNP 2
* - 1
  - `WW`
  - `WW`
* - 2
  - `WW`
  - `WM`
* - 3
  - `WW`
  - `MM`
* - 4
  - `WM`
  - `WW`
* - 5
  - `WM`
  - `WM`  
* - 6
  - `WM`
  - `MM`
* - 7
  - `MM`
  - `WW`
* - 8
  - `MM`
  - `WM`  
* - 9
  - `MM`
  - `MM`
````
-->

(linkage-disequilibrium)=
```{admonition} Linkage Disequilibrium
:class: note
Linkage disequilibrium is the measure of how much more often alleles are found together than would be expected if they were randomly distributed.
SNPs are not independent, and we wouldn't expect alleles to be randomly distributed for many reasons, for example because:
- SNPs are inherited together through genetic linkage, due to being on the same gene or nearby genes from one another.
- we would expect combinations of SNPs to reflect the structure of the population, e.g. individuals who are geographically close to one another are more likely to have similar genetics.
- particular combinations of SNPs may be fatal or otherwise prevent people from passing them on.
```

The combinations of SNPs are not distributed randomly based only on the frequency of each SNP independently, this is what's known in population genetics as {ref}`linkage disequilibrium<linkage-disequilibrium>`.
<!--
Given any 2 or 3 random SNPs, much of the combinatorial space is empty, as {numref}`empty-combinatorial-space` shows.

[//]: # (TODO: Make empty-combinatorial-space image, possibly also show a table showing where this data comes from - actually shows empty space - explain that it does also show there are random combinations - like these things aren't zero, they're just rarer than you would expect)

[//]: # (TODO: Calculate mean and sd of mm/mw/ww)

[//]: # (TODO: Explain that heterozygous SNPs can also be disease-causing and that sometimes we will be looking to score highly just homozygous people and sometimes homo and heterozygous people. Give examples from SNPedia. Maybe move this to overview?)

```{code-cell} ipython3
import allel

vcf = allel.read_vcf('data/alspac_hg19_allSNPs_header.vcf', fields=['variants/*', 'samples', 'calldata/GT'])

# TODO: Allel isn't workig to read in vcf... do it like I did before and remove allel from requirements
```

## Simulating SNP data
In order to test how well the clustering methods worked, I simulated data with a rare combination of mid-high scoring SNPs, representing the ideal candidates for detection by `snowflake`.

[//]: # (TODO: add detail of generation of genotypes, step 1)

1. Randomly generate genotypes for 300 SNPs and 2500 individuals.
2. Randomly generate SNP deleteriousness scores for 300 SNPs.
3. For 10 high-scoring SNPs, ensure that all individuals have exist in subpopulations.

```{code-cell} ipython3
import numpy as np

num_individuals = 1000

num_important_snps = [1, 2, 3, 5, 10]  # med-high score AND rare *combination*
num_snps_iter = range(2,100) # snps involved with phenotype

# TODO: first try with only important snps high scoring, then try with some unimportant snps (not rare) high scoring
# TODO: Simulating the data is difficult because of the combinatoric nature of the snps. Test for whether similar combinatorics are happening, for 2 medium-scoring snps within a phenotype.

def simulate_data(num_important_snps, num_snps, num_with_phenotype):
    """Simulate SNP data"""
    with_phenotype = np.random.randint(1,num_individuals, num_with_phenotype)
    snps_causing_phenotype = np.random.randint(1, num_snps, num_important_snps)
    
    # Simulate deleteriousness scores per snp... 
    # TODO: Simulate deleteriousness scores separately outside simulate_data
    deleteriousness_scores = [np.random.random() for i in num_snps]  # TODO: draw from actual distribution of scores 
    # TODO: Also increase the deleteriousness for some other common snps
    for i in snps_causing_phenotype:
        deleteriousness_scores[i] *= 5 
    
    # Simulate rarity of calls per snp, normally distributed percentage in biggest category
    # TODO: check distribution % homozygous, more common hetero, less common hetero
    rarity = []
    for i in range(num_snps):
        homo = np.random.normal(proportion_homozygous_mean, proportion_homozygous_sd)
        hetero_common = np.random.normal(proportion_homozygous_mean, proportion_homozygous_sd)
        # three options MM, MW (same as WM), and WW.
        
    # TODO: run it through the actual snowflake create_distance_matrix
    data = np.zeroes(num_snps, num_individuals)
    for i in range(num_snps):
        # TODO implement for different distance metrics
        
    
        
    return data
```

```{code-cell} ipython3
import numpy as np
import scipy.stats as stats

num_individuals = 2500

print(np.random.randint(1,num_individuals, 5))
```

```{code-cell} ipython3
num_snps = 10

# TODO: See if normally distributed is the best distribution for this
# TODO: Make this into a `simulate_genotypes` function.
# TODO: Might want to do this for less common rather than more common.
# TODO: Probably just want to do this once, not inside the simulate_data function

def simulate_genotypes(num_snps, num_individuals, homo_mean=0.7, homo_sd=0.5, hetc_mean=0, hetc_sd=0.001):
    """
    homo_mean: mean proportion of homozygous calls
    homo_sd: standard deviation of homozygous calls
    hetc_mean: mean proportion of most common heterozygous calls
    hetc_sd: standard deviation of most common heterozygous calls
    """
    lower, upper = 0, 1  # bounds

    homo = stats.truncnorm((lower - homo_mean)/homo_sd, (upper - homo_mean)/homo_sd, homo_mean, homo_sd).rvs(num_snps)
    hetero_common = stats.truncnorm((lower - hetc_mean)/hetc_sd, (upper - hetc_mean)/hetc_sd, hetc_mean, hetc_sd).rvs(num_snps)

    # Fix invalid proportions (add up to greater than 100%)
    invalid = homo + hetero_common > 1
    while sum(invalid) != 0:
        # Make replacements
        homo_r = stats.truncnorm((lower - homo_mean)/homo_sd, (upper - homo_mean)/homo_sd, homo_mean, homo_sd).rvs(sum(invalid))
        hetero_common_r = stats.truncnorm((lower - hetc_mean)/hetc_sd, (upper - hetc_mean)/hetc_sd, hetc_mean, hetc_sd).rvs(sum(invalid))

        # For every valid replacement, replace:
        r = 0  # replacement_count
        for i, valid in enumerate(homo_r + hetero_common_r < 1):
            if valid:
                homo[np.where(invalid==True)[0][r]] = homo_r[i]
                hetero_common[np.where(invalid==True)[0][r]] = hetero_common_r[i]
                r+=1
        assert(sum(homo + hetero_common > 1) <= sum(invalid))
        invalid = homo + hetero_common > 1    

    rarity = np.zeros((num_snps, 3))
    for i in range(num_snps):
        rarity[i] = [
            int(np.round(num_individuals*homo[i])), 
            int(np.round(num_individuals*hetero_common[i])), 
            int(np.round(num_individuals*(1 - homo[i] - hetero_common[i])))
        ]
    rarity = rarity.astype(int)
    print(rarity)
    return None
    
simulate_genotypes(1000, num_individuals)
[//]: # (TODO: Turn into np array like we have internally when we read in the VCF)
```

```{code-cell} ipython3
[//]: # (TODO: OPTIONAL: Number of call combinations seen per random pairs/trios of SNPs - different for SNPs in the same pathway/phenotype/similar domains?)
```

### The specificity of phenotypes
[//]: # (TODO: Write: show example of a DcGO "phenotype" with a weird combinations of phenotype terms.)

+++
-->

(clustering-methodology)=
## Choice of clustering methodology

```{figure} ../images/clustering_snps.png
---
height: 220px
name: non-spherical
---
A drawing indicating how the combinations of SNPs we might expect to cause disease would represent a non spherical relationship between SNPs. 
```

+++

```{figure} ../images/clustering_comparison.png
---
height: 220px
name: clustering-comparison
---
Comparison illustrating differences between the implemented clustering methods. Image adapted from sklearn documentation{cite}`noauthor_undated-nc`.
```

The original implementation of the phenotype predictor used k-means clustering{cite}`Le_Cam1967-ku`. 
This wasn’t suitable for the predictor, since we expect combinations of SNPs to form non-spherical shapes (see {numref}`non-spherical`), and k-means cannot achieve this (see {numref}`clustering-comparison`).

+++

Spectral clustering, DBSCAN (Density-Based Spatial Clustering of Applications with Noise), IDOS, OPTICS and LOF (Local Outlier Factor) were also implemented. 
This involved automation of parameter selection, to enable clustering to be performed automatically on thousands of phenotype terms. 
These methods have theoretical pros and cons with respect to the predictor. 
For example, OPTICS and DBSCAN do not need the number of clusters as an input, but instead require the minimum number of points required to form a cluster and a radius from each point to consider as part of a cluster, which has more meaning in this context. 
They also automatically output outliers to clusters, which will affect the resulting phenotype score, potentially in unseen ways - particularly as it is difficult to visualise high-dimensional data. OPTICS is the default setting, as in addition to not requiring a number of clusters, it can identify clusters of differing densities (a quality that DBSCAN lacks - as can be seen in the second row of {numref}`clustering-comparison`). 
A final informed choice between these options requires a large benchmarking set.

[//]: # (TODO: Comparison of kmeans, spectral, dbscan, optics and LOF for 2 phenotypes, e.g. using CAGI PGP)
[//]: # (TODO: Discuss how choice of k in kmeans and spectral, or choice of other hyperparameters effects the final score - which clustering methods are more/less sensitive)

+++

(distance-metric)=
### Choice of distance metric
The phenotype predictor’s original distance metric was non-linear, such that the homozygous calls were further from each other than the distance via the heterozygous call, as shown in {numref}`non-linear-metric`.
 Non-linear distance metrics mean that it is not possible to create a location matrix rather than a distance matrix. 
 This is required for some types of clustering.

[//]: # (TODO: Give examples - PCA - of known phenotypes for different distance metrics, e.g. one with small number of SNPs and one with more SNPs, e.g. maybe just 2-3 SNPs and maybe 30 with dimensionality reduction)
[//]: # (TODO: Sensitivity due to different distance metrics, on two known CAGI phenotypes)

+++

A linear distance metric which also captured the increased likelihood of homozygous alleles to be disease-causing ({numref}`linear-metric`) was developed to enable this, and to better represent the biology. 
In this version, the popularity of an allele decides which homozygous call the heterozygous call is more functionally similar to.

+++

```{figure} ../images/nonlinear_metric.png
---
width: 220px
name: non-linear-metric
---
Original non-linear distance metric. 
$MM$ denotes homozygous mutant alleles, $WW$ denotes homozygous wild type alleles, and $MW$ denotes heterozygous alleles. 
The FATHMM score for the SNP $f$, defines the distance between the wild type and mutant alleles.
```

+++

```{figure} ../images/linear_metric.png
---
width: 220px
name: linear-metric
---
Linear distance metrics. $MM$ denotes homozygous mutant alleles, $WW$ denotes homozygous wild type alleles, and $MW$ denotes heterozygous alleles, and $N$ represents the number of people with that allele call. The FATHMM score for the SNP $f$, defines the distance between the wild type and mutant alleles. 
```

+++


+++

<!--
### Input individuals
[//]: # (TODO: Sensitivity of clustering score to background cohort)
-->
+++ 

<!--
### Overcoming the curse of dimensionality in Snowflake
-->
<!--
#### Dimensionality reduction
[//]: # (TODO: When is dimensionality reduction appropriate? Correlation between SNPs, cooccurance of snps, FATHMM scores, Too many SNPs for a phenotype.)

#### Sensitivity of number of SNPs on final score
[//]: # (TODO: Show the effect of number of SNPs per phenotypes on the sensitivity of the final score to the FATHMM score. Choose a phenotype with many snps and randomly sample various numbers of them and see the how sensitive the results are.)

#### Sensitivity of particular SNPs on final score
[//]: # (TODO: Randomly delete SNPs and see how this effects the final score)
[//]: # (TODO: See how number of SNPs and randomly deleting them interacts)
[//]: # (TODO: Explain meaningfulness, show DcGO prediction, where SNP is in a gene which is not expressed in the tissue)
-->

[//]: # (TODO: Add making predictions back into TOC)