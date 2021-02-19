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

## `Snowflake` Algorithm
[//]: # (TODO: Describe the purpose of the algorithm here, and the overall user perspective: genetic data in, predictions out)
The purpose of the `Snowflake` algorithm is 

This section describes the `Snowflake` phenotype prediction algorithm that I developed alongside Jan Zaucha, Ben Smithers and Julian Gough. 

[//]: # (TODO: List features I am responsible for here, and link to the sections below where I describe them)
The original idea for the predictor was Julian’s and he created an initial implementation of it in perl. This perl version was initially ported to Python by Ben, and subsequently contributed to heavily by both me and Jan, where we both fixed a number of bugs, and added essential functionality. We then forked the software into two different versions to suit our own research, mine focusing on human phenotype prediction. The project is now being taken forward by the Computational Genomics group at MRC led by Julian.

[//]: # (TODO: Describe the different functionality here and what will be covered in this section here, i.e. what would be different commands, e.g. preparing data for input - 23andMeVCF, preprocessing - i.e. calculating SNPs of interest and creating slimmed in-between versions of files that contain only these SNPs, and predicting)




+++

### `snowflake predict`
[//]: # (TODO: Describe the purpose of this here)
[//]: # (TODO: Explain that the algorithm is pretty massive, so it is a little more subdivided)

#### Overview

+++

```{figure} ../images/snowflake-overview.png
---
height: 220px
name: snowflake-overview
---
Flowchart showing an overview of the phenotype predictor. Scores are generated per allele using SUPERFAMILY, FATHMM and dcGO for both the input genotype(s), and the background genotypes. These data points are then combined into a matrix, which is then clustered..
```

+++

{numref}`snowflake-overview` shows how an overview of how `Snowflake` operates. One or more genotypes (in VCF format) are needed: this is the *input cohort*. Each genotype will be compared against all others, including (optionally) a diverse background set from the 1000 Genomes Project{cite}`Consortium2015-ci`. 

1. For each phenotype $i$, a list of SNPs is generated such that the SNPs are associated with the phenotype (according to DcGO), and the SNPs are present in the input individuals.
2. The input SNPs are given deleterious scores (using FATHMM), and this us used to construct an $N_{i}\times M$ matrix of scores is created based on the individual’s alleles for each of these SNPs, (where $N$=number of SNPs and $M$=number of individuals).
3. Individuals of interest are clustered by SNP, alongside a diverse background of other people
4. A score is calculated per person per phenotype, designed to calculate how much of an outlier the person is according to their SNPs for a given phenotype.

Further detail on these steps is provided below:

[//]: # (TODO: Check in detail how the following tools are described in the background section and reference back to them)

#### SNPs are mapped to phenotype terms using DcGO and dbSNP
DcGO{cite}`Fang2013-ms` is used to map combinations of protein domains to their associated phenotype terms, using a false discovery rate cut-off of $10^{-3}$ or less. SNPs are therefore mapped to phenotype terms by whether they fall in a gene whose protein contains domains or combinations of domains that are statistically associated with a phenotype. In order to do this, DcGO makes use of SUPERFAMILY{cite}`Gough2001-ct` domain assignments, and a variety of ontology annotations (GO{cite}`Ashburner2000-cr`, MPO{cite}`Smith2005-uh`, HP{cite}`Robinson2010-ga`, DOID{cite}`Schriml2012-dz` and others).

Using DcGO means that phenotypes are only mapped to protein if the link is statistically significant due to the protein’s contingent domains. This leaves out some known protein-phenotype links, where the function may be due to disorder for example rather than protein domain structure. Known phenotype-associated variants are therefore added back in using dbSNP{cite}`Sherry2001-nm`.

[//]: # (TODO: How many are left out?)

#### SNPs are given deleteriousness scores using FATHMM
The phenotype predictor uses the unweighted FATHMM scores{cite}`Shihab2013-pk` to get scores per SNP for the likelihood of it causing a deleterious mutation. This is based on conservation of protein domains across all life, according to data from SUPERFAMILY{cite}`Gough2001-ct` and Pfam{cite}`Bateman2002-bz`. 

This method gives SNPs the same base FATHMM score for being deleterious, no matter which phenotype we are predicting them for. It is therefore the combination of SNPs per phenotype, and their rarity in the population that determines the phenotype prediction score.

#### Comparison to a background via clustering
[//]: # (TODO: Rewrite this part - when do we require a background data set and why. What is clustering. Link to the work in the later section comparing clustering methods.)
Individuals are compared to all others through clustering. This usually includes comparing each individual to the genetically diverse background of the 2500 genomes project{cite}`Consortium2015-ci`.

Clustering is the task of grouping objects into a number of groups (clusters) so that items in the same cluster are similar to each other by some measure. There are many clustering algorithms, but most are unsupervised learning algorithms which iterate while looking to minimise dissimilarity in the same cluster. A number of options were implemented for the predictor, but for the time being at least, OPTICS is used as a default.

#### Background data sets: The 1000 Genomes Project
[//]: # (TODO: cross-ref to `snowflake create_background`)
As described in the overview, `Snowflake` requires a genetic "background" data set, so that meaningful clustering can take place. Snowflake has the functionality to be run with any background data set, but few datasets are available that contain genetic data from a wide range of populations.

[//]: # (TODO: cross ref to whole genome sequencing)
The 1000 Genomes project{cite}`Consortium2015-ci,1000_Genomes_Project_Consortium2012-ek` ran from 2008 to 2015, with the aim of comprehensively mapping human genetic variation across diverse populations. The project sequenced whole genomes, and released data in two main phases:
- Phase 1: 37.9 million variants, in 1092 individuals, across 14 populations
- Phase 3: 84.4 million, in 2504 individuals, across 26 populations

Data from the 1000 Genomes project are always used for the background cohort to `Snowflake` in this thesis, with data from the 1000 Genomes project Phase 3{cite}`Consortium2015-ci` used as a default, and earlier experiments using data from Phase 1{cite}`1000_Genomes_Project_Consortium2012-ek`. 

For both phases of the 1000 Genomes project, data are provided as VCF files for each Chromosome. Both data sets are available through the [International Genome Sequencing Resource](https://www.internationalgenome.org/data){cite}`Fairley2020-hp` (IGSR); phase 1 VCFs can be downloaded [here](ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase1/analysis_results/integrated_call_sets/), and phase 3 VCFs can be downloaded [here](ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/).

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
[//]: # (TODO: What about the Y chromosome?)
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

#### Outputs 
[//]: # (TODO: Write about outputs of the predictor)

+++

### `snowflake create_background`
For any given run of `Snowflake`, we are only interested in variants where:
- there is overlap between the background cohort, the predictive cohort
- AND we have conservation information so that we can score the deleteriousnss of the variant.

[//]: # (TODO: Come up with a name for the none-background genetic data set and use it consistently)
We first create base versions of the `Snowflake` background cohort input files, and then create slimmed versions of the background set (with only the overlapping variants for each input/predictive dataset) for each input run.

For the base versions of the background cohort, we create:
- A `.Consequence` file containing conservation scores per SNP
- A VCF file containing the genetic data for the background set that overlaps with the information in the `.Consequence` file.

[//]: # (TODO: Optional for thesis: Upload scripts which do this to `snowflake` repo: `deletesparecomments.py`)

**Step 1: Acquire variant information as a large temporary VCF file**
We first create a large VCF file containing all possible variants.

In order to make the `.Consequence` file it is necessary to have a list of all variants of interest; their locations on the genome, and the possible variants at that location. 

In the case of the 1000 Genomes project, we create a large temporary VCF file by downloading and concatenating the per chromosome VCF files (minus the meta data at the top for all bar the first, which is the same for all files). 

**Step 2: Create `.Consequence` file**
After obtaining the large VCF file, we then:
- trim the VCF file to contain only the necessary columns (first 10) to reduce the amount of memory required in the next step.
- run these variants through the [Variant Effect Predictor](https://www.ensembl.org/info/docs/tools/vep/index.html), using the correct build.
- grep for "missense"
- run `snowflake create-consequence` to get a FATHMM score for each missense variant and create the `.Consequence` file.

**Step 3: Create the base background VCF**
Since the VCF file created in Step 1 is larger than needed by `Snowflake`, we then reduce the temporary VCF file (created in Step 1) to only the proteins in the `.Consequence` file created in Step 2. Other variants will not be used by the predictor, and this substantially reduces the memory needed to run `Snowflake`.

[//]: # (TODO: Write about the diversity/limitations of the 2500 genomes project).
[//]: # (TODO: Write about the impact of the fact that the 2500 genomes project is whole genome sequencing, while the rest is mostly genotype data)
[//]: # (TODO: Put somewhere -after creating the VCF and `.Consequence` files for the input individuals, we create a slimmed version of the background cohort files)

##### 1000 Genome Project background files
[//]: # (TODO: Write)
[//]: # (TODO: Exploratory Data Analysis/Data set stats here)

+++

(snowflake-create-input)=
### `snowflake create_input`

+++

### `snowflake preprocessing`
[//]: # (TODO: Describe the purpose of this here)

#### Inputs

#### Outputs

#### Method

(dcgo)=
##### DcGO
The aim of the Domain-centric Gene Ontology (DcGO){cite}`Fang2013-ms,Fang2013-ix` tool is to give insight into uncharacterised or poorly characterised proteins by leveraging information about the content of their constituent protein domains. 
It annotates domains and combinations of domains (supradomains) to phenotype terms from a variety of ontologies, including the Gene Ontology (GO), Mammalian Phenotype ontology (MP), Disease Ontology (DOID), Zebrafish ontology (ZFA). 
Domain information comes from SUPERFAMILY, and annotations between (supra)domains and phenotype terms are made below a cut-off of FDR-adjusted statistical associations between the entities. 
Using phenotypes from a range of species serves to make use of greater numbers of experiments, and therefore increases the number of little-known proteins across species that DcGO can make predictions about.

(variant-prioritisaton)=
#### Variant prioritisation
To narrow down a long list of genes or variants to a shorter list of variants or genes which is more likely to be causal, variant prioritisation is used.

(fathmm)=
##### FATHMM
Functional Analysis through Hidden Markov Models (FATHMM){cite}`Shihab2013-pk` is a tool for predicting the functional effects of protein missense mutations using sequence conservation information (via HMMs), which can be (optionally) weighted by how likely a mutation in a protein/domain would be to lead to disease. 
Weightings are calculated from the frequency of disease-associated and functionally neutral amino acid substitutions in protein domains from human variation databases (the Human Gene Mutation Database{cite}`Stenson2009-jc` and Uniprot-KB/Swiss-prot{cite}`Pundir2016-ya`).

Consequence files describing whether an amino acid results in a missense, nonsense or synonymous SNP must first be obtained by using Ensembl’s Variant Effect Predictor{cite}`McLaren2016-di` in order to create input to FATHMM. 
FATHMM then calculates conservation scores which are a measure of the difference in amino acid probabilities for a SNP according to the HMM, i.e. between a wild type amino acid and it’s substitution. 
A reduction in amino acid probabilities is interpreted as a prediction of deleteriousness, and the larger the reduction the greater the predicted harm. 



+++
