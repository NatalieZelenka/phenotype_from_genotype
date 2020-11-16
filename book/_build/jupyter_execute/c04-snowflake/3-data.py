## Snowflake input data
[//]: # (TODO: Have I already explained VCF format? Link or explain here. Cite. Cite the version of the format we use. Explain that there are different versions.)
`Snowflake` requires:
     - genetic data as input, in VCF format. 
     - conservation scores per SNP.
     
This section describes the sources and pipelines for creating input files.

### Data sources

#### Background data sets: The 1000 Genomes Project
[//]: # (TODO: cross-ref to overview)
As described in the overview, `Snowflake` requires a genetic "background" data set, so that meaningful clustering can take place. Snowflake has the functionality to be run with any background data set, but few datasets are available that contain genetic data from a wide range of populations.

[//]: # (TODO: cross ref to whole genome sequencing)
The 1000 Genomes project{cite}`Consortium2015-ci,1000_Genomes_Project_Consortium2012-ek` ran from 2008 to 2015, with the aim of comprehensively mapping human genetic variation across diverse populations. The project sequenced whole genomes, and released data in two main phases:
- Phase 1: 37.9 million variants, in 1092 individuals, across 14 populations
- Phase 3: 84.4 million, in 2504 individuals, across 26 populations

Data from the 1000 Genomes project are always used for the background cohort to `Snowflake` in this thesis, with data from the 1000 Genomes project Phase 3{cite}`Consortium2015-ci` used as a default, and earlier experiments using data from Phase 1{cite}`1000_Genomes_Project_Consortium2012-ek`. 

For both phases of the 1000 Genomes project, data are provided as VCF files for each Chromosome. Both data sets are available through the [International Genome Sequencing Resource](https://www.internationalgenome.org/data){cite}`Fairley2020-hp` (IGSR); phase 1 VCFs can be downloaded [here](ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase1/analysis_results/integrated_call_sets/), and phase 3 VCFs can be downloaded [here](ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/).

### ALSPAC
[//]: # (TODO: Further describe the value of the dataset and what it is generally used for)
The Avon Longitudinal Study of Parents and Children, ALSPAC{cite}`Golding2001-oj` (a.k.a. the children of the 90s) is a cohort of over 14,000 families from the Avon area. Of these, 8365 of the children were genotyped by 23andMe and passed quality control. The participants were genotyped using the 23andme v2 chip, which measures ~550,000 SNPS. A wealth of phenotype information has also been collected from these families, through a series of voluntary surveys and clinics.

#### Phenotypes
Due to the private nature of the data, we were granted access to the genotype data first, then allowed to request a small number of high-scoring phenotypes after running the predictor.

[//]: # (TODO: link ethics approval docs (put on OSF?)

[//]: # (TODO: explain that using the catalogue - and link - ALSPAC phenotypes matching the DcGO phenotypes were chosen for the highest scoring things on a the prototype version. Maybe explain that due to the sensitivity of this to other things, they were not the highest ranking things any more).

[//]: # (TODO: Rewrite paragraph below:)
We had ethics approval to run the anonymised genotype information for the ALSPAC cohort in the phenotype predictor, and then to request phenotype information for the top-scoring phenotypes. The phenotype predictor was run on this cohort. Unfortunately the majority of the top-predicted phenotype terms (Ataxia, Abnormal Fat Cell Morphology, Abnormal Fetal Development) did not map cleanly to ALSPAC phenotypes, and those that did (e.g. Intellectual Disability) had many missing values, or did not overlap with the genotyped individuals.

[//]: # (TODO: EDA Graph: Phenotype missing data)

[//]: # (TODO: Cite lack of diversity).
Although the ALSPAC dataset is large, it is not very diverse, therefore the 1000 genomes project (Phase 1) genomes were used as a background set.

#### Original data format
[//]: # (TODO: Write)
**Genotype data format**

**Phenotype data format**

### Athletes
[//]: # (TODO: Write)

### CAGI
[//]: # (TODO: Write)

### Data Pipelines

#### Pipeline for creating background cohort inputs
For any given run of `Snowflake`, we are only interested in variants where:
- there is overlap between the background cohort, the predictive cohort
- AND we have conservation information so that we can score the deleteriousnss of the variant.

[//]: # (TODO: Come up with a name for the none-background genetic data set and use it consistently)
We first create base versions of the `Snowflake` background cohort input files, and then create slimmed versions of the background set (with only the overlapping variants for each input/predictive dataset) for each input run.

For the base versions of the background cohort, we create:
- A `.Consequence` file containing conservation scores per SNP
- A VCF file containing the genetic data for the background set that overlaps with the information in the `.Consequence` file.

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

#### Pipeline for creating VCF files from 23andMe data
The CAGI, Athletes, and ALSPAC datasets were all genotyped using 23andMe, so the following applies to all of these datasets.

##### 23andMe chips
[//]: # (TODO: Write and cite)
Since launch, 23andMe have used a number of different illumina chips for their genotyping service. These chips capture information for different SNPs.

##### Ambiguous Flips
[//]: # (TODO: Explain ambigious flips a bit better)
The majority of input data to the predictor is 23andMe data. In testing the predictor with the 2500G background and a cohort of 23andMe genomes, it became clear that for many phenotypes, the background was forming a separate cluster to the cohort. This led to the realisation that there are 23andMe calls which had the opposite ratio of wild type:mutant than the 2500 genomes. Some further reading revealed this to be a known problem{cite}`Church2005-zv`, which may be due to ambiguous flips{cite}`Sand2007-ed`. 

[//]: # (TODO: Finish writing this sentence:)
Implausible distributions of SNPs in the input cohort (given the background) are therefore discarded. i.e if the input cohort doesn't match the background. (all one way and the rest all the other).

#### ALSPAC

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was ALSPAC data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for ALSPAC. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Phenotypes
[//]: # (TODO: Mapping phenotypes to ALSPAC measurements. Write - was done by hand using the ALSPAC catalogue)

#### CAGI
[//]: # (TODO: Possibly delete this section)

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was CAGI data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for CAGI. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Mapping phenotypes to CAGI measurements
[//]: # (TODO: Write)

#### Athletes
[//]: # (TODO: Possibly delete this section)

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was CAGI data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for CAGI. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Mapping phenotypes to CAGI measurements
[//]: # (TODO: Write)

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```