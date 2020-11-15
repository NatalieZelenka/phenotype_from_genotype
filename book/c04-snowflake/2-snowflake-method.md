---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

## Snowflake Method

### Overview

+++

```{figure} ../images/snowflake-overview.png
---
height: 220px
name: snowflake-overview
---
Flowchart showing an overview of the phenotype predictor. Scores are generated per allele using SUPERFAMILY, FATHMM and dcGO for both the input genotype(s), and the background genotypes. These data points are then combined into a matrix, which is then clustered..
```

+++

{numref}`snowflake-overview` shows how the phenotype predictor is run. One or more genotypes (in 23andme, or VCF format) are needed as input. Each genotype will be compared against all others, including (optionally) a diverse background set from the 2500 genomes project{cite}`Consortium2015-ci`. 

1. For each phenotype $i$, a list of SNPS is generated such that the SNPs are associated with the phenotype (according to DcGO), and the SNPs are present in the input individuals.
2. The input SNPS are given deleterious scores (using FATHMM), and this us used to construct an $N_{i}\times M$ matrix of scores is created based on the individual’s alleles for each of these SNPs, (where $N$=number of SNPs and $M$=number of individuals).
3. Individuals of interest are clustered by SNP, alongside a diverse background of other people
4. A score is calculated per person per phenotype, designed to calculate how much of an outlier the person is according to their SNPs for a given phenotype.

Further detail on these steps is provided below:

<!--TODO: Check in detail how the following tools are described in the background section and reference back to them.-->

#### SNPs are mapped to phenotype terms using DcGO
DcGO{cite}`Fang2013-ms` is used to map combinations of protein domains to their associated phenotype terms, using a false discovery rate cut-off of $10^{-3}$ or less. SNPs are therefore mapped to phenotype terms by whether they fall in a gene whose protein contains domains or combinations of domains that are statistically associated with a phenotype. In order to do this, DcGO makes use of SUPERFAMILY{cite}`Gough2001-ct` domain assignments, and a variety of ontology annotations (GO{cite}`Ashburner2000-cr`, MPO{cite}`Smith2005-uh`, HP{cite}`Robinson2010-ga`, DOID{cite}`Schriml2012-dz` and others).

Using DcGO means that phenotypes are only mapped to protein if the link is statistically significant due to the protein’s contingent domains. This leaves out some known protein-phenotype links, where the function may be due to disorder for example rather than protein domain structure. Known phenotype-associated variants are therefore added back in using dbSNP{cite}`Sherry2001-nm`.

#### SNPs are given deleteriousness scores using FATHMM
The phenotype predictor uses the unweighted FATHMM scores{cite}`Shihab2013-pk` to get scores per SNP for the likelihood of it causing a deleterious mutation. This is based on conservation of protein domains across all life, according to data from SUPERFAMILY{cite}`Gough2001-ct` and Pfam{cite}`Bateman2002-bz`. 

This method gives SNPs the same base FATHMM score for being deleterious, no matter which phenotype we are predicting them for. It is therefore the combination of SNPs per phenotype, and their rarity in the population that determines the phenotype prediction score.

#### Comparison to a background via clustering,
Individuals are compared to all others through clustering. This usually includes comparing each individual to the genetically diverse background of the 2500 genomes project{cite}`Consortium2015-ci`.

Clustering is the task of grouping objects into a number of groups (clusters) so that items in the same cluster are similar to each other by some measure. There are many clustering algorithms, but most are unsupervised learning algorithms which iterate while looking to minimise dissimilarity in the same cluster. A number of options were implemented for the predictor, but for the time being at least, OPTICS is used as a default.

#### Phenotype score
The OPTICS clustering assigns each individual to a cluster (or labels them as an outlier). Depending on the phenotype term, the cluster is expected to either correspond to a haplogroup or a phenotype. In cases where the cluster refers to a haplogroup, we are interested in the outliers of both clusters, i.e. the local outlier-ness. In cases where the cluster is the phenotype, we are interested in the outlying cluster, i.e. the global outlier-ness. 

A local score, $L_{ij}$ can be defined as the average Euclidean distance from an individual to the centre of it’s cluster, or for individuals that are identified as outliers by OPTICS, 2 multiplied by the distance to the centre of the nearest cluster.

A global score $G_{ij}$ can be defined as the distance of the cluster to the rest of the cohort.

The global-local score is designed to balance these sources of interest. It sums the two scores, adjusting the weighting by a cluster size correction factor, $\mu_{\gamma}$:
$$score_{ij}=L_{ij}+\mu_{\gamma} \cdot G_{ij}$$

Such that: $\mu_{\gamma}=\frac{exp(\gamma \frac{n-n_j}{n})-1}{exp(\gamma)-1}$ where $\gamma$ is a parameter representing how strongly we wish to penalise large clusters, $n$ is the over all number of individuals and $n_j$ is the number of individuals in a cluster.

+++

### Features added to the predictor
As mentioned, the phenotype predictor was already prototyped when I began working on it. However, considerable time was spent developing, bug-fixing, and extending this prototype. Here, I describe my contributions to this.

#### Different running modes
The original version of the phenotype predictor could only be ran one individual compared to a background set at a time. In order to allow for a wider range of inputs (which will be necessary to validate the predictor), support for a wider range of genotype formats and running modes was developed, e.g.:
* Can be run with one person against a background
* Can be run with multiple people (VCF) against the background
* Can be run with or without the background set if there are enough people in the input set.
* Support for different 23andMe genotype file formats (from different chips).

As the predictor was developed to perform in different running modes, it became clear that it would be necessary to streamline the algorithm. This included parallelisation (possible due to the independence of different phenotype terms), and various data storage and algorithmic adjustments.

Implementing these running modes and increases in efficiency was a collaborative effort between myself, Jan, and Ben.

#### Adding SNP-phenotype associations from dbSNP 
As mentioned in the overview, using DcGO as the only SNP-phenotype mapping leaves out some known associations that are not due to protein domain structure. Adding dbSNP{cite}`Sherry2001-nm` associations to the predictor was one of my contributions to this software. 

#### Dealing with missing calls 
Genotyping SNP arrays often contain missing calls, where the call can not be accurately determined. This is an obstacle to the phenotype predictor if left unchecked as it can appear that an individual has a very unusual call when it is really just unknown. Sincce most people have a call, the missing call is unusual, and this is flagged.

The most sensible solution to this problem is to assign the most common call for the individual’s cluster (i.e. combination of SNPs). This prevents a new cluster being formed or an individual appearing to be more unusual than they are. However, there is a downside to this approach when there are many missing calls. Adding all missing calls to a cluster that was only slightly more common than the alternatives can lead to the new cluster containing the missing data dwarfing the others. To fix this, SNPs with many missing calls were discarded. This implementation of missing calls was one of my personal contributions.

Alternatives such as assigning the most common call for that SNP only, or assigning an average score for that SNP dimension by carrying out a “normalised cut”{cite}`Poland2006-gd` are untenable since they can create the same problem we are trying to overcome: the appearance of an individual having an unusual combination of calls.

#### Confidence score per phenotype
The phenotype predictor outputs a score for each person for each phenotype. Our confidence in these scores depends on the distribution of scores, as well as the scale of them. A distribution of scores with distinct groups of individuals is generally preferable, since most phenotypes that we are interested in are categorical or it is at least more useful to highlight phenotypes that can be predicted this way (i.e. if there are 100 groups with varying risk of a disease, that would be less useful than knowing there are 2 groups with high/low risk). 

I developed a simple method of prioritising predictions according to these requirements. A confidence score is achieved by plotting the ranked raw score and measuring the minimum area between a straight line resting on this line (resting on the two points furthest from y=x) and the line itself, as illustrated in {numref}`shaded-score`. Since this measure takes into account the size of the raw scores, these confidence scores  compared across phenotypes.

{numref}`ranked-scores` shows an example of an interesting and uninteresting distribution. These distributions mostly depend on the number, population frequency, and FATHMM score of the SNPs associated with the phenotype term. 

```{code-cell} ipython3
# Code for: An illustration of how the confidence score is calculated (shaded area).  - `shaded-score`
```

```{code-cell} ipython3
# Code for: Ranked scores for `DOID:1324` - the disease ontology term Lung Cancer (left) and HP:0008518 - the human phenotype ontology term for Absent/underdeveloped sacral bone (right). These represent an interesting and uninteresting distribution of scores, respectively.  - `ranked-scores`
```

### Outputs of the predictor

[//]: # (TODO: Write)


---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```
