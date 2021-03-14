<!-- #region -->

# Data

[//]: # (TODO: explain overall types of data and how they will fit together for `filip` with cross references to each part of this page, Expression, samples info, obo, etc )

##  Expression data: FANTOM5

[//]: # (TODO: Check where I say sample, but mean measurement, ie. where I am talking about the columns of the CAGE data FF accessions are the same for technical replicates)
[//]: # (TODO: Mention CAGE - ?relevant because mapping to proteins..)
[//]: # (TODO: Data given as TPM per CAGE peak - CAGE peaks map to multiple genes when the CAGE peak overlaps multiple genes, also CAGE peaks that map to the same protein, could map to different sets of genes because CAGE peaks map to different genes: don't map via CAGE peaks because you lose information) 

`filip` requires expression data to inform whether or not predictions should be filtered out. The FANTOM5 data set was chosen for this purpose (at the time this was the latest data output of the {ref}`FANTOM consortium<fantom-consortium>`).

FANTOM5 represents one of the most comprehensive collections of expression data, in this case transcript expression. 
It contains a combination of human, mouse, health, and disease data, as well as time courses and cell perturbations.

```{margin} The FANTOM Consortium
:name: fantom-consortium
The Functional ANnoTation Of the MAmmalian genome (FANTOM) consortium was established as the human genome project was nearing completion when researchers had a parts list of human biology, but few of the functions of these parts (genes) were known. The consortium has run a range of large scale collaborative projects in five rounds to further this goal. The first FANTOM project used only the mouse genome, but later versions also included human. 
```

[//]: # (TODO: What does the data contain, how many samples, etc)

### Reasoning

I chose the FANTOM5 data as the input gene expression data for `filip`, for the following reasons:
- The data set has a good coverage of different tissue types, meaning that `filip` should be able to turn this into a good coverage of predictions.
- The data set has an ontology of samples, which is already linked to Uberon tissue terms and CL cell terms, making the mapping process much easier.

I chose the version of the FANTOM5 data that:
- had been reprocessed using the hg38 reference genome (the original FANTOM5 data was processed using hg19).
- contained annotated information about the samples, as this information could be used to aid in mapping
- available in TPM format

[//]: # (TODO: Aside about TPM/link to before)


### Data files and acquisition
[//]: # (TODO: Signpost that I don't use the FANTOM OBO yet)

I downloaded the following files from the FANTOM website:
- the [FANTOM5 CAGE peaks expression data](http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/extra/CAGE_peaks_expression/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt.gz) containing expression in counts per transcript, and mappings to HGNC id and entrez gene ID. The long sample labels in this file are also a source of metadata.
- the [FANTOM5 ontology](https://fantom.gsc.riken.jp/5/datafiles/latest/extra/Ontology/ff-phase2-170801.obo.txt) containing an obo file mapping between FANTOM sample IDs, Uberon and cell ontology (CL) terms.
- FANTOM's [human sample information file](https://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/basic/HumanSamples2.0.sdrf.xlsx) containing text descriptions about sample, for example tissue, age, sex, disease, etc, which is necessary for data cleaning.

[//]: # (TODO: Where do I first explain sample accession numbers?)
[//]: # (TODO: if time, update so that data aquisition code is here/above)
[//]: # (TODO: Explain FANTOM Accession numbers here)
<!-- #endregion -->

```python
%load_ext autoreload
%autoreload 2

# TODO: Add cell metadata to prevent output + hide
```

```python
import helper_c05.fantom_sample_clean as fsc
# TODO: Add cell metadata to prevent output + make code dropdown

# read in CAGE header and samples info files:
expression_header = fsc.read_CAGE_header()
samples_info = fsc.read_samples_info()

# calculate replicates information:
rep_info = fsc.get_tech_bio_reps(expression_header, samples_info)

# clean samples info files:
samples_info = fsc.restrict_samples(samples_info)
samples_info = fsc.update_sample_info_labels(samples_info, rep_info)
samples_info = fsc.clean_samples_info(samples_info, rep_info)
```

<!-- #region -->
### Initial FANTOM5 data cleaning: sample info file

(fantom-sample-categories)=
#### Sample categories
[//]: # (TODO: Add HeLa image)

```{margin} HeLa cell line
The FANTOM5 experiment contains HeLa cell lines samples (e.g. sample `FF:10815-111B5`).

HeLa is short for Henrietta Lacks, the woman whose cells were the source of this first immortal cell line.
Henrietta was a black woman who lived in Baltimore, Maryland.
Her cells were taken without consent during a hospital biopsy for an aggressive cervical cancer, which she died from at age 31 in 1951. 

Companies continue to profit from the sale of these lines of cells, since such cell lines have several practical advantages over primary cells, notably their immortality, low variability (compared to primary cells, which vary depending on cell donor characteristics such as age and sex), and easiness to keep alive (without the need for e.g. additional nutrients). 
```

The human FANTOM5 sample information file contains four categories of samples (in the `Characteristics [Category]` field): 
- __time courses__: RNA extraced from samples being measured over time as cells change types during cell development and differentiation ({glue:}`time-course-num-samps` samples), e.g. {glue:}`time-course-ex-id` - {glue:}`time-course-ex-desc`.
- __primary cells__: RNA extracted from cultures of cells recently isolated from tissues, before undergoing proliferation with nutrients specific to the cell type ({glue:}`primary-num-samps` samples), e.g. {glue:}`primary-ex-id` - {glue:}`primary-ex-desc`.
- __cell lines__: RNA extracted from immortal cell lines (which unlike primary cells) can keep undergoing division indefinitely ({glue:}`cell-line-num-samps` samples), e.g. {glue:}`cell-line-ex-id` - {glue:}`cell-line-ex-desc`.
- __tissues__: RNA extracted from post-mortem tissues, which may be pooled or individual donors ({glue:}`tissue-num-samps` samples), e.g. {glue:}`tissue-ex-id` - {glue:}`tissue-ex-desc`.
- __fractionations__: RNA extracted from parts of cells (fractionations) ({glue:}`frac-per-num-samps` samples), e.g. {glue:}`frac-per-ex-id` - {glue:}`frac-per-ex-desc`.

I restricted the data set to only **tissues** and **primary cells**, as these represent the closest approximations to *in vivo* biology.
Immortal cell lines are often expressed differently than their primary counterparts{cite}`Pastor2010-hk,Kaur2012-en`, and time courses and fractionations and perturbations do not represent any particular tissue.

[//]: # (TODO: discuss difference between tissue and primary cell samples here)

__Sample Type__:
As mentioned tissues can come from a pool, or individual donor. This information can be found in the `Charateristics [description]` field.
[//]: # (TODO: Write about tissue pool versus tissue donor here)


#### Technical and biological replicates
[//]: # (TODO: Rewrite)
[//]: # (TODO: Add glues of how many are left in/explanations of why)
[//]: # (TODO: Aside for difference between biological and technilogical replicates)
[//]: # (TODO: Cross-ref to where I explain FANTOM accession numbers)

Note that the FANTOM accession numbers are per sample, not per measurement, so there are some columns of the expression file which correspond to the same accession number. 
These represent technical replicates. 
FANTOM technical and biological replicates are indicated in long labels of the annotated expression FANTOM file, by the inclusion of “tech_rep” or “biol_rep” in the long sample labels e.g. `tpm.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20tech_rep1.CNhs10855.11227-116C3.hg38.nobarcode`. 
These were used to create additional fields for the human samples table.

Note: there is an error in the original transcript expression file for one of these identifiers (`tpm.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20rep2.CNhs11062.11227-116C3.hg38.nobarcode`) such that it is missing the “tech” part of the the replicate label. 
There is a hard-coded fix when I read in the input file and the FANTOM data curation team was informed.

After restricting the dataset to *primary cell* and *tissue* type samples, there are {glue:}`num_bio_rep_samples` remaning samples which have biological replicates, and {glue:}`num_tech_rep_samples` sets of samples with technological replicates (2 replicates each).
<!-- #endregion -->

#### Age and age range
[//]: # (TODO: Check how I format human sample information file, maybe italicise it and make sure that the capitalisation lines up)

The age of the sample source donor(s) is available through two fields in the human sample information file: `Characteristics [Developmental stage]`, and `Characteristics [Age]`.
These fields contain description-like text, which are somewhat inconsistent, for example, “3 year old child”, “3 years old child”, “25 year old”, “76” and “76 years old adult” all feature in the same column, amongst other errors. 
These were standardised into a new field (`Age (years)`).
This field does not seek to include multiple ages (i.e. when the sample comes from a pool of donors).
There is a complementary (i.e. no overlap) field (`Age range (years)`), which contains age ranges for the {glue:}`age_diranged` samples that contain multiple ages.
In both columns, some samples contain fetal samples, in which caset age (range) is given as a negative decimal (converted to years before birth).

There file also contained some discrepancies between ages and developmental stages in the FANTOM human samples file.
For example, sample `FF:10027-101D9` is labelled as *thymus, adult, pool1* in the *Description* field, but as *0.5,0.5,0.83 years old infant* in the *Developmental Stage* field. 
Sample `FF:10209-103G2` had an age of ‘M’ and a sex of ‘28’. 
I reported both these discrepencies: and the latter has since been fixed in the FANTOM file, and for the former, I hardcode the age to `NaN`.

#### Sex
The `Characteristics [Sex]` field contains information about the sex of the sample source donor(s). 
Similarly to age, due to the consortium nature of FANTOM5, the entries of this field are not consistently labelled.
They undergo data cleaning into 4 categories: male, female, mixed (pool with both male and female samples), and unlabelled.

#### Disease and tissue mapping
The disease status of samples (e.g. healthy/non-healthy) is not straight-forwardly labelled in the human sample file, so requires some basic text-mining (and cross-referencing with ontology terms).
Similarly, there is a `Characteristics[Tissue]` field in the human samples file containing some manually mapped tissue types, but as I point out with an example in {ref}`the exploratory data analysis<eda-sample-tissues>`, these do not contain ideal mappings for `filip`. 

The continued data processing of these components is described in {ref}`the methdology section <filter-methods>`, after the introduction of `uberon-py` (the package developed to do this).

[//]: # (TODO: Add link to FANTOM exp download)

```{admonition, note} FANTOM5 cleaned experimental design file
:class: dropdown
:name: cleaned-fantom-exp
The cleaned FANTOM5 experimental design file (which has undergone the cleaning mentioned in this section, and in {ref}`the methodology section<filter-methods>`) is available [here](link). 
```

```python
# TODO: Create list of allowed primary + tissue samples (in sample_header)

```

```python
from helper_c05 import fantom_tpm_clean as tpm_clean

tpm_file = '../c06-combining/data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_tpm_ann.osc.txt'
cage_tpm = tpm_clean.read_and_clean_tpm(tpm_file)
cage_tpm
```

```python
protein_tpm = tpm_clean.get_protein_tpm(cage_tpm)
protein_tpm
```

### Initial FANTOM5 data cleaning: expression file
[//]: # (TODO: Choose output of these code cells: make some invisible, show some data snippets)
[//]: # (TODO: mention the file we're talking about and restriction to existing samples)
[//]: # (TODO: Structure section... first explain that/why want protein-centric expression... etc)

#### CAGE peaks with associated proteins
[//]: # (TODO: Check what type of uniprot ID these are)
The CAGE peaks represent all kinds of transcripts, not only those which map to protein-coding genes. 
The FANTOM file provides mappings to Uniprot IDs (`uniprot_id`), and these are used to discard the CAGE peaks that do not map to protein-coding genes: this takes us from {glue:}`total_F5_peaks` to  {glue:}`has_protein_F5_peaks` rows (CAGE peaks).

#### CAGE peaks mapped to one gene only
[//]: # (TODO: Do I want to do this? What about overlapping genes?)
[//]: # (TODO: cross-ref discrepencies between gene ID databases)
CAGE peaks are mapped to genes based on overlap with the gene, so it is not always clear which gene a CAGE peak maps to.
For simplicity, and to remove the potential of wrongly mapped genes being used in `filip`, protein-coding CAGE peaks (those which are mapped to at least one `uniprot_id` by FANTOM) that map to multiple genes are removed.
These can be found by looking at either the `hgnc_id` or `entrezgene_id` gene identifier columns.
The choice of gene ID matters, since there are discrepencies between gene ID databases: in this case, choosing `hgnc_id` finds all those CAGE peaks found by using `entrezgene_id`, and more, so these are removed.
This represents a total of {glue:}`total_gene_id_duplicates` CAGE peaks that map to multiple genes according to the given identifers.

#### Proteins that map to multiple genes
For `filip`, the expression was calculated per protein (since it is protein function predictions that it is filtering), rather than per CAGE peak (summing the TPMs of all CAGE peaks mapped to a protein to get the total for that protein) as in the original data, or as is often presented per gene.
This gave {glue:}`protein_expression_total` rows of "protein expression" data.

Of these, there were then {glue:}`rows_left_multiple_genes` rows of data (corresponding to {glue:}`proteins_multiple_genes` proteins) for which each protein maps to multiple genes.
This happens when different genes are translated to make identical protein products, for example the [H4 human histone protein](https://www.uniprot.org/uniprot/P62805) is encoded by 14 different genes at different loci, across three different chromosomes.
It used to be the case that Uniprot would map these genes to the same Uniprot ID, but more recently different Uniprot IDs are used to capture where the proteins came from.
These rows were also removed.



### Exploratory Data Analysis

#### Samples
[//]: # (TODO: Number of samples, biological and technical replicates)

After {ref}`restricting the samples to those which are primary cells or tissues<fantom-sample-categories>`, there were {glue:}`fantom-primary-tissue-samples` remaining samples. 


```python
from helper_c05 import fantom_sample_eda as f_eda
sex_donut, tissues_samples, nan_age_count, collaborators_providers = f_eda.create_plot_dfs(samples_info)
fig = f_eda.create_plotly_plots(samples_info, sex_donut, tissues_samples, nan_age_count, collaborators_providers)
fig
```

```python
anatomical_system_samples = f_eda.anat_system_tbl(samples_info, chosen_samples = [2, 10, 15, 20])
anatomical_system_samples
```

```{figure} ../../images/fantom_eda.png
:name: fantom-eda
width: 1000px
---
(a) sex: a donut plot showing the sex labels of samples, (b) collaborators and providers: a stacked histogram showing the {glue:}`num_collaborators` most common collaborators, and {glue:}`num_providers` most common providers. (c) age: a histogram of age of sample donors (this does not include the {glue:}`age_ranged` samples which have age ranges due to pooled donors of various ages). (d) tissues and sample types: a histogram showing the {glue:}`num_common_tissues` most common tissues, spread across the different types of samples (primary cells, tissue donors, and tissue pools).
```

__Sample metadata:__ 
Looking at the FANTOM5 data (see {numref}`fantom-eda`), overall we see that there the samples are very varied, across ages, sex, sample providers, and collaborators, although (d) shows that the majority of samples are *primary cell* samples, and very few are *tissue - pool* samples.
Secondly, we can see that after careful cleaning, some metadata is missing, i.e. 38.4% of samples have unknown sex (a), most collaborators did not label the sample provider (b), and most samples do not have a labelled age (c).

(eda-sample-tissues)=
__Sample Tissues:__ 
In {numref}`fantom-eda` subplot (d), we can also note some interesting things about the tissue types provided by the Fantom Human Samples file. {glue:}`anatomical-system` primary cell samples are labeled *ANATOMICAL SYSTEM*. If we look closer at these samples, we can see that it is theoretically possible to map some of these samples to tissues (see {numref}`anatomical-system-sample-table`). 

[//]: # (TODO: cross-ref to where discussed in methodology, and vice versa) 
(fantom-tissues-how-general)=
There is also the question of how general or specific the human sample categories are. There are {glue:}`blood-samples` samples which are mapped to "blood" ({numref}`tbl:anatomical-system` (d)), but when we come to map the FANTOM5 tissues to phenotypes, this may be too broad a category. Similarly, there are {glue:}`tissues-less-three` with less than three samples each (unpictured) that may be too narrow to map to phenotypes, and a more accurate picture of that phenotype would come from taking a more general tissue.

```{glue:figure} anatomical-system-sample-table
:figwidth: 300px
:name: "tbl:anatomical-system"

An example of four *ANANTOMICAL SYSTEM* tissues, with tissue-specific cells, indicating that they could be mapped to tissues. For example sample `FF:11922-125H5` is a gingival fibroblast, which are one of the main constituent cells of gum tissue.
```

[//]: # (TODO: Cross ref to uberon-py)
[//]: # (TODO: Cross ref to use of uberon-py for removal of disease samples)

We can also see in {numref}`tbl:anatomical-system` that this dataset, though having undergone some data cleaning, still contains disease samples (e.g. "aggressive periodontitis"). 


#### Protein-centric TPM

[//]: # (TODO: Number of CAGE peaks, transcripts, proteins, genes)
[//]: # (TODO: Expression distribution)


```python
display(transcript_tpm[transcript_tpm['uniprot_id'].str.contains('B2R4R0', na=False)])
```

```python
# TODO: Plotly Gannt for CAGE peaks overlapping with multiple transcripts/genes (check association with transcript to check whether it's multiple transcripts or just muktiple genes with same TSS)
```

## Supplementary mapping data
[//]: # (TODO: Cross ref to methodology)

I also used the following datasets to aid in mapping to a common set of identifiers:
- the [uberon extended ontology OBO file](http://purl.obolibrary.org/obo/uberon/ext.obo) from [the uberon website](uberon.github.io/downloads.html) to assist in mapping cells and tissues.

[//]: # (TODO: Describe mapping data here, e.g. biomart/uniprot)


## Test set: CAFA2

### What?
During development, I tested `filip` by comparing DcGO only and `filip` + DcGO on data from the 2nd round of the CAFA competition: CAFA2. 
This was the most recent round of CAFA for which there were "groundtruth" data available at the time of development.
The data consisted of CAFA2 targets and the CAFA2 ground truth data.

**CAFA2 targets**: 

[//]: # (TODO: describe data format)
[//]: # (TODO: check it's the right build hg38)

**CAFA2 groundtruth**: 

[//]: # (TODO: describe data format)

### Why?
[//]: # (TODO: Cite swissprot KB and GOA)

I chose to use the CAFA2 data because rather than a larger set of annotations (such as those available from SwissProt-KB or GOA) because it provided a way of validating on unknown targets.
I.e. if I made predictions with DcgO using the version of GO from the time the challenge was launched, and I use the groundtruth data provided by CAFA2, then I could compare my results with those in the CAFA2 competition and I could look at my results on unknown targets.

### How?
[//]: # (TODO: describe data acquisition)

+++

## Test set: CAFA3 
After initial development, I entered DcGO only, and `filip` plus DcGO into the CAFA3 competition in order to test `filip` on a new dataset.

This meant that I did not download the CAFA3 groundtruth, as this analysis was done by the CAFA3 team, but only the CAFA3 targets.

**CAFA3 targets**: 

[//]: # (TODO: describe data format)
