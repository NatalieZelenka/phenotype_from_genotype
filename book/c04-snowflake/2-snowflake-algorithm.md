---
jupytext:
  formats: ipynb, md:myst
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

(snowflake-algo)=
# `Snowflake` Algorithm
[//]: # (TODO: fix math display in pdf)
This section introduces the Snowflake algorithm, and gives an overview of how it works, as well as a description of it's functionality and which parts of this I contributed to.

(snowflake-approach)=
## Approach
[//]: # (TODO: Cite most successful)
Snowflake belongs to a small number of phenotype prediction methods that aim to predict across many phenotypes and many genotypes.
Although it's designed primarily as a phenotype prediction algorithm, it also implicitly makes protein function predictions.

Snowflake aims to not only create phenotype predictions, but to create explanatory predictions, where the relevant parts of the molecular biology (missense variants falling in protein domains) can be traced back and used to explore the prediction further.
In this sense it contrasts to the black-box approaches that are currently most successful.


<!--
<!--
Snowflake uses outlier detection to find individuals with unusual combinations of variants, but this is primarily a means of discovering the function of combinations of variants.
In finding these variants, Snowflake provides explanations for it's phenotype predictions, which are useful in it's own right as a possible mechanism for the phenotype.
The locations of the variants and the proteins that they are within may then be investigated though other methods (e.g. knock-outs) to investigate whether they could be targets for treatments.
-->

The Snowflake phenotype prediction method works by identifying individuals who have unusual combinations of deleterious missense SNPs associated with a phenotype. 
The phenotype predictor uses only data about missense SNPs in coding regions of globular proteins, so it can only be expected to work well where phenotypes are determined primarily by these kinds of mutations. 

This method combines conservation and variant effect scores using FATHMM{cite}`Shihab2013-pk`, inference about function of protein domains using dcGO{cite}`Fang2013-ms`, and human genetic variation data from the 2500 genomes project{cite}`Consortium2015-ci` to predict phenotypes of individuals based on their combinations of missense SNPs. 

[//]: # (TODO: Write)

<!--
While GWAS looks at each variant individually, `snowflake` groups variants by relation to phenotype: it is capable of finding combinations of SNPs that might be responsible, taking into account the fact that single SNPs do not act alone and biology is full of redundancy. 
However, it does not take into account the structure of the redundancy.
-->
<!--
Move any relevant part of this to the algorithm section:

## Solution
[//]: # (TODO: Write)

The `Snowflake` phenotype prediction method works by identifying individuals who have unusual combinations of deleterious SNPs associated with a phenotype. 
The phenotype predictor uses only data about missense SNPs in coding regions of globular proteins, so it can only be expected to work well where phenotypes are determined primarily by these kinds of mutations. However, the advantage over other methods (e.g. GWAS) is that the role of the involved SNPs is explained.

This method combines conservation and variant effect scores using FATHMM{cite}`Shihab2013-pk`, inference about function of protein domains using dcGO{cite}`Fang2013-ms`, and human genetic variation data from the 2500 genomes project{cite}`Consortium2015-ci` to predict phenotypes of individuals based on their combinations of missense SNPs. 

[//]: # (TODO: Write)

While GWAS looks at each variant individually, `snowflake` groups variants by relation to phenotype: it is capable of finding combinations of SNPs that might be responsible, taking into account the fact that single SNPs do not act alone and biology is full of redundancy. 
However, it does not take into account the structure of the redundancy.

[//]: # (TODO: Take a look at different combinations of SNPs associated with a phenotype and see if they show up in the same genes or genes, different genes in the same pathway, etc)
-->


[//]: # (TODO: Take a look at different combinations of SNPs associated with a phenotype and see if they show up in the same genes or genes, different genes in the same pathway, etc)
[//]: # (TODO: CHECK: When does VEP/fathmm work? The algorithm can be run for organisms from across the phylogenetic tree, as long as the proteins have known sequence, and there are enough sequenced or genotyped individuals to compare against.)

(how-does-it-work)=
## How does it work?
[//]: # (TODO: Check capitalisation or backtick formatting for dcGO, fathmm and SUPERFAMILY)
[//]: # (TODO: Update image to make sure VEP and SUPERFAMILY are in there)
[//]: # (TODO: Change order of steps 1 and 2 in image)

```{figure} ../images/snowflake-overview-new.png
---
width: 250px
name: snowflake-overview
---
Flowchart showing an overview of the phenotype predictor. Scores are generated per allele using SUPERFAMILY, VEP, FATHMM and dcGO for both the input genotype(s), and the background genotypes. These data points are then combined into a matrix, which is then clustered.
```

<!--
The `Snowflake` algorithm predicts phenotype by finding individuals who have unusual combinations of deleterious genetic variants associated with a phenotype. 
-->

{numref}`snowflake-overview` shows how an overview of how Snowflake operates. 
One or more genotypes (in VCF or 23andMe format) are needed: this is the *input cohort*. The algorithm can then be divided into three main steps:
1. Score variants for deleteriousness, using FATHMM and VEP
2. Map variants to phenotype, using dcGO and SUPERFAMILY
3. Cluster individuals per phenotype and extract score, using {abbr}`IDOS (Intrinsic Dimensionality Outlier Score)`. Each genotype will be compared against all others, including (optionally) a diverse background set from the 2500 Genomes Project{cite}`Consortium2015-ci`. 

Further detail on these steps is provided below.

<!--
Each of these steps is modular, meaning that it's possible to use another method (other than `fathmm`) to predict the deleteriousness of variants, to map variants to phenotype, or to cluster individuals and extract the score.
-->

<!--
1. For each phenotype $i$, a list of SNPs is generated such that the SNPs are associated with the phenotype (according to dcGO), and the SNPs are present in the input individuals.
2. The input SNPs are given deleterious scores (using FATHMM), and this us used to construct an $N_{i}\times M$ matrix of scores is created based on the individual’s alleles for each of these SNPs, (where $N$=number of SNPs and $M$=number of individuals).
3. Individuals of interest are clustered by SNP, alongside a diverse background of other people
4. A score is calculated per person per phenotype, designed to calculate how much of an outlier the person is according to their SNPs for a given phenotype.


-->
[//]: # (TODO: Check in detail how the following tools are described in the background section and reference back to them)
[//]: # (TODO: Explain dcGO FDR cut-off)


(dcgo-in-snowflake)=
### SNPs are mapped to phenotype terms using DcGO and dbSNP
DcGO{cite}`Fang2013-ms` is used to map combinations of protein domains to their associated phenotype terms, using a false discovery rate cut-off of $10^{-3}$ or less. 
SNPs are therefore mapped to phenotype terms by whether they fall in a gene whose protein contains domains or combinations of domains that are statistically associated with a phenotype. 
In order to do this, DcGO makes use of SUPERFAMILY{cite}`Gough2001-ct` domain assignments, and a variety of ontology annotations (GO{cite}`Ashburner2000-cr`, MPO{cite}`Smith2005-uh`, HP{cite}`Robinson2010-ga`, DOID{cite}`Schriml2012-dz` and others).

Using DcGO means that phenotypes are only mapped to protein if the link is statistically significant due to the protein’s contingent domains. 
This leaves out some known protein-phenotype links, where the function may be due to disorder for example rather than protein domain structure. 

[//]: # (TODO: Are dbSNP associations added back in? If so, this was my contribution and I should make more of it)
Known phenotype-associated variants are therefore added back in using dbSNP{cite}`Sherry2001-nm`.

[//]: # (TODO: How many are left out?)

(fathmm-in-snowflake)=
### SNPs are given deleteriousness scores using FATHMM
The phenotype predictor uses the unweighted FATHMM scores{cite}`Shihab2013-pk` to get scores per SNP for the likelihood of it causing a deleterious mutation. This is based on conservation of protein domains across all life, according to data from SUPERFAMILY{cite}`Gough2001-ct` and Pfam{cite}`Bateman2002-bz`. 

This method gives SNPs the same base FATHMM score for being deleterious, no matter which phenotype we are predicting them for. 
It is therefore the combination of SNPs per phenotype, and their rarity in the population that determines the phenotype prediction score.

(clustering-step)=
### Comparison to a background via clustering
[//]: # (TODO: Rewrite this part - when do we require a background data set and why. What is clustering. Link to the work in the later section comparing clustering methods.)
Individuals are compared to all others through clustering. This usually includes comparing each individual to the genetically diverse background of the 2500 genomes project{cite}`Consortium2015-ci`.

Clustering is the task of grouping objects into a number of groups (clusters) so that items in the same cluster are similar to each other by some measure. There are many clustering algorithms, but most are unsupervised learning algorithms which iterate while looking to minimise dissimilarity in the same cluster. A number of options were implemented for the predictor, but for the time being at least, OPTICS is used as a default.

(individual-score)=
### Phenotype score
The OPTICS clustering assigns each individual to a cluster (or labels them as an outlier). Depending on the phenotype term, the cluster is expected to either correspond to a haplogroup or a phenotype. 
In cases where the cluster refers to a haplogroup, we are interested in the outliers of all clusters, i.e. the local outlier-ness. 
In cases where the cluster is the phenotype, we are interested in the outlying cluster, i.e. the global outlier-ness. 

A local score, $L_{ij}$ can be defined as the average Euclidean distance from an individual to the centre of it’s cluster, or for individuals that are identified as outliers by OPTICS, 2 multiplied by the distance to the centre of the nearest cluster.

A global score $G_{ij}$ can be defined as the distance of the cluster to the rest of the cohort.

```{margin} TF-IDF
:name: tf-idf
Term Frequency, Inverse Document Frequency is a common and basic measure in NLP which attempts to measure how representative a term (word) is of a document. 
It is defined by {math}`tfidf=tf(t,d) \cdot idf(t,D) = (f_{t,d}) \cdot (\frac{N}{abs{d \in D : t \in d}}) ` where {math}`f_{t,d}` is the frequency of a term {math}`t` in a document {math}`d`, {math}`N` is the number of documents, and {math}```{abs{d \in D : t \in d}``` is the number of documents containing the term.
```

The global-local score is designed to balance these sources of interest. 
It sums the two scores, adjusting the weighting by a cluster size correction factor, $\mu_{\gamma}$:
$score_{ij}=L_{ij}+\mu_{\gamma} \cdot G_{ij}$

Such that: $\mu_{\gamma}=\frac{exp(\gamma \frac{n-n_j}{n})-1}{exp(\gamma)-1}$ where $\gamma$ is a parameter representing how strongly we wish to penalise large clusters, $n$ is the over all number of individuals and $n_j$ is the number of individuals in a cluster.

The global-local score was inspired by the {ref}`tf-idf<tf-idf>` score popular in Natural Language Processing bag-of-word models. 

(snowflake-functionality)=
## Functionality

`Snowflake` is implemented as a {abbr}`CLI (Command Line Interface)` tool, written in Python with the following commands:
- `snowflake create-background`
- `snowflake create-consequence`
- `snowflake preprocessing`
- `snowflake predict`

[//]: # (TODO: Explain inputs)

<!--
Inputs:
- Input genotype(s) in {abbr}`VCF (Variant Call Format)` or 23andMe format
- (Optional) background cohort in {abbr}`VCF (Variant Call Format)` 
-->

The functionality described above all happens within `snowflake predict`, but in order to use `snowflake predict`, there are also three commands which create files needed to run the predictor.

[//]: # (TODO: Describe the different functionality here what each command does and what will be covered in this section here, i.e. what would be different commands, e.g. preparing data for input - 23andMeVCF, preprocessing - i.e. calculating SNPs of interest and creating slimmed in-between versions of files that contain only these SNPs, and predicting)


+++


+++

(snowflake-added-features)=
## Features added to the predictor
As mentioned, the phenotype predictor was already prototyped when I began working on it. 
However, considerable time was spent developing, bug-fixing, and extending this prototype. 
Here, I describe my contributions to this in detail.

(snowflake-running-modes)=
### Different running modes
The original version of the phenotype predictor could only be ran one individual compared to a background set at a time. 
In order to allow for a wider range of inputs (which will be necessary to validate the predictor), support for a wider range of genotype formats and running modes was developed, including:
- Can be run with one person against a background
- Can be run with multiple people (VCF) against the background
- Can be run with or without the background set if there are enough people in the input set.
- Support for different 23andMe genotype file formats (from different chips).

As the predictor was developed to perform in different running modes, it became clear that it would be necessary to streamline the algorithm. 
This included parallelisation (possible due to the independence of different phenotype terms), and various data storage and algorithm adjustments.

Implementing these running modes and increases in efficiency was a collaborative effort between myself, Jan, and Ben.

(snowflake-dbsnp)=
### Adding SNP-phenotype associations from dbSNP 
As mentioned in the overview, using DcGO as the only SNP-phenotype mapping leaves out some known associations that are not due to protein domain structure. 
Adding dbSNP{cite}`Sherry2001-nm` associations to the predictor was one of my contributions to this software. 

(snowflake-missing-calls)=
### Dealing with missing calls 
[//]: # (TODO: What about the Y chromosome?)
Genotyping SNP arrays often contain missing calls, where the call can not be accurately determined. 
This is an obstacle to the phenotype predictor if left unchecked as it can appear that an individual has a very unusual call when it is really just unknown. 
Since most people have a call, the missing call is unusual, and this is flagged.

The most sensible solution to this problem is to assign the most common call for the individual’s cluster (i.e. combination of SNPs). 
This prevents a new cluster being formed or an individual appearing to be more unusual than they are. 
However, there is a downside to this approach when there are many missing calls. 
Adding all missing calls to a cluster that was only slightly more common than the alternatives can lead to the new cluster containing the missing data dwarfing the others. 
To fix this, SNPs with many missing calls were discarded. 

[//]: # (TODO: What is the threshold for "many" missing calls and how many SNPs and therefore phenotypes are affected by this?)

Alternatives such as assigning the most common call for that SNP only, or assigning an average score for that SNP dimension by carrying out a “normalised cut”{cite}`Poland2006-gd` are untenable since they can create the same problem we are trying to overcome: the appearance of an individual having an unusual combination of calls.

(snowflake-dimensionality-reduction)=
### Reducing dimensionality
Some phenotypes have large numbers of SNPs associated with them - too many to assign individuals to clusters.
I added a dimensionality reduction step in the clustering, and tested different clustering methods designed for use on high-dimensional data. 
These changes are explained {ref}`later in this Chapter<curse-of-dimensionality-section>`. 

(phenotype-score)=
### Confidence score per phenotype
The phenotype predictor outputs a score for each person for each phenotype. 
Our confidence in these scores depends on the distribution of scores, as well as the scale of them. 
A distribution of scores with distinct groups of individuals is generally preferable, since most phenotypes that we are interested in are categorical or it is at least more useful to highlight phenotypes that can be predicted this way (i.e. if there are 100 groups with varying risk of a disease, that would be less useful than knowing there are 2 groups with high/low risk). 

[//]: # (TODO: Say why some distributions are more interesting than others)
[//]: # (TODO: should I normalise the distribution score?)

```{figure} ../images/shaded_score.png
---
width: 250px
name: shaded-score
---
An illustration of how the confidence score per phenotype is calculated.
```

I developed a simple method of prioritising predictions according to these requirements. 
A confidence score is achieved by plotting the ranked raw score and measuring the area between a straight line resting on this the most extreme points and the line itself, as illustrated in {numref}`shaded-score`. 
Since this measure takes into account the size of the raw scores, these confidence scores can be compared across phenotypes.

```{figure} ../images/interesting-scores.png
---
width: 500px
name: interesting-scores
---
Ranked scores for `DOID:1324` - the disease ontology term Lung Cancer (left) and HP:0008518 - the human phenotype ontology term for Absent/underdeveloped sacral bone (right). These represent an interesting and uninteresting distribution of scores, respectively.
```

{numref}`interesting-scores` shows an example of an interesting and uninteresting distribution. 
These distributions mostly depend on the number, population frequency, and FATHMM score of the SNPs associated with the phenotype term.


<!--
#### Outputs 
[//]: # (TODO: Write about outputs of the predictor)

+++

### `snowflake create_background`
For any given run of `Snowflake`, we are only interested in variants where:
- there is overlap between the background cohort and the predictive cohort
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

[//]: # (TODO: Write about the diversity/limitations of the 2500 genomes project)
[//]: # (TODO: Write about the impact of the fact that the 2500 genomes project is whole genome sequencing, while the rest is mostly genotype data)
[//]: # (TODO: Put somewhere -after creating the VCF and `.Consequence` files for the input individuals, we create a slimmed version of the background cohort files)


##### 1000 Genome Project background files
[//]: # (TODO: Write)
[//]: # (TODO: Exploratory Data Analysis/Data set stats here)


(snowflake-create-input)=
### `snowflake create_input`


### `snowflake preprocessing`
[//]: # (TODO: Describe the purpose of this here)

#### Inputs

#### Outputs

#### Method





-->