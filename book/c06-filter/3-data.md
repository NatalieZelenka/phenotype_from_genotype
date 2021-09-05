---
jupytext:
  formats: md:myst
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

(filter-data)=
# Data

This section describes the {ref}`gene expression data<fantom5-expression-data>` used for creating and validating Filip, including it's provenance as well as any necessary data-cleaning.

I also describe the {ref}`benchmarking data<cafa2-training-set>` I used to develop Filip.

In addition to this, Filip requires the input of a protein function or phenotype prediction method, but this (and the data required for this) is described in {ref}`filter-methods`.

(fantom5-expression-data)=
##  Expression data: FANTOM5

[//]: # (TODO: Check where I say sample, but mean measurement, ie. where I am talking about the columns of the CAGE data FF accessions are the same for technical replicates)
[//]: # (TODO: Write: Data given as TPM per CAGE peak - CAGE peaks map to multiple genes when the CAGE peak overlaps multiple genes, also CAGE peaks that map to the same protein, could map to different sets of genes because CAGE peaks map to different genes: don't map via CAGE peaks because you lose information) 

The Filip method requires expression data to inform whether or not predictions should be filtered out.
The FANTOM5 data set was chosen for this purpose.

My reasoning for choosing FANTOM5 data as the input gene expression data to test Filip was:
- The data set has a good coverage of different tissue types, which I hoped would be helpful in Filip having a good coverage of predictions.
- The data set has an ontology of samples, which is already linked to Uberon tissue terms terms, making the mapping process much easier.
- For the purpose of Filip (getting measure of whether a cell is meaningfully expressed in a tissue of interest), choosing bulk RNA-Seq over scRNA-Seq makes sense, as it is a measure of many more cells.

I chose the version of the FANTOM5 data that:
- had been reprocessed using the hg38 reference genome (the original FANTOM5 data was processed using hg19){cite}`Abugessaisa2017-fc`.
- contained annotated information about the samples, as this information could be used to aid in mapping.
- available in {ref}`TPM<rna-normalisation>` format.

(fantom-files)=
### Data files and acquisition
[//]: # (TODO: Signpost that I don't use the FANTOM OBO yet)
[//]: # (TODO: double-check that I don't say anything about transcript expression)
[//]: # (TODO: Check how I format human sample information file, maybe italicise it and make sure that the capitalisation lines up)

```{margin} FANTOM5 Accession numbers
:name: fantom-accession
Each FANTOM *sample* has an accession number of the form `FF:#####-#####`. These numbers are used in all three of the FANTOM5 data files.
Note: some samples have repeat measurements per sample.
```

I downloaded the following files from the FANTOM website:
- the [FANTOM5 CAGE peaks expression data](http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/extra/CAGE_peaks_expression/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt.gz) containing expression in counts per CAGE peak, and mappings to transcript id (ensembl ENST id), HGNC id and entrez gene ID. The long sample labels in this file are also a source of metadata (including {ref}`sample identifiers (FANTOM accession numbers)<fantom-accession>`).
- FANTOM's [human sample information file](https://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/basic/HumanSamples2.0.sdrf.xlsx) containing text descriptions about sample, for example FANTOM accession numbers, tissue, age, sex, disease, etc, which is necessary for data cleaning.
- the [FANTOM5 ontology](https://fantom.gsc.riken.jp/5/datafiles/latest/extra/Ontology/ff-phase2-170801.obo.txt) containing an obo file mapping between FANTOM accession numbers, Uberon and cell ontology (CL) terms.

```{code-cell} ipython3
:tags: [remove-cell]

%load_ext autoreload
%autoreload 2

from myst_nb import glue
```

(fantom-cleaning)=
### Initial FANTOM5 data cleaning: sample info file

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import helper_c05.fantom_sample_clean as fsc

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

(fantom-sample-categories)=
**Sample categories**

[//]: # (TODO: Add HeLa image)

```{margin} HeLa cell line
The FANTOM5 experiment contains HeLa cell lines samples (e.g. sample `FF:10815-111B5`).

HeLa is short for Henrietta Lacks, the woman whose cells were the source of this first immortal cell line.
Henrietta was a black woman who lived in Baltimore, Maryland.
Her cells were taken without consent during a hospital biopsy for an aggressive cervical cancer, which she died from at age 31 in 1951. 

Companies continue to profit from the sale of these lines of cells, since such cell lines have several practical advantages over primary cells, notably their immortality, low variability (compared to primary cells, which vary depending on cell donor characteristics such as age and sex), and easiness to keep alive (without the need for e.g. additional nutrients). 

Some companies have recently begun to pay reparations for this injustice{cite}`Witze2020-vr`.
```

(primary-cell-tissue)=
__Restriction to  primary cell and tissue samples__:

The human FANTOM5 sample information file contains four categories of samples (in the `Characteristics [Category]` field): 
- __time courses__: RNA extracted from samples being measured over time as cells change types during cell development and differentiation ({glue:}`time-courses-num-samps` samples), e.g. {glue:}`time-courses-ex-id` - *{glue:text}`time-courses-ex-desc`*.
- __primary cells__: RNA extracted from cultures of cells recently isolated from tissues, before undergoing proliferation with nutrients specific to the cell type ({glue:}`primary-cells-num-samps` samples), e.g. {glue:}`primary-cells-ex-id` - *{glue:text}`primary-cells-ex-desc`*.
- __cell lines__: RNA extracted from immortal cell lines (which unlike primary cells) can keep undergoing division indefinitely ({glue:text}`cell-lines-num-samps` samples)<!-- TODO: add examples e.g. {glue:}`cell-line-ex-id` - *{glue:text}`cell-line-ex-desc`*-->.
- __tissues__: RNA extracted from post-mortem tissues, which may be pooled or individual donors ({glue:}`tissues-num-samps` samples), e.g. {glue:}`tissues-ex-id` - *{glue:text}`tissues-ex-desc`*.
- __fractionations__: RNA extracted from parts of cells (fractionations) ({glue:}`fractionations-and-perturbations-num-samps` samples), e.g. {glue:}`fractionations-and-perturbations-ex-id` - {glue:}`fractionations-and-perturbations-ex-desc`.

I restricted the data set to only *tissues* and *primary cells*, as these represent the closest approximations to *in vivo* biology.
Immortal cell lines are often expressed differently than their primary counterparts{cite}`Pastor2010-hk,Kaur2012-en`, and time courses and fractionations do not represent any particular tissue.

[//]: # (TODO: discuss difference between tissue and primary cell samples here)

__Sample Type__:

As mentioned, tissues can come from a pool, or individual donor. 
This information can be found in the `Charateristics [description]` field.
I combined this information with information from the `Characteristics [Category]` field to create an additional `Sample Type` field that describes whether a sample is a `tissue - pool`, `tissue - donor` or `primary cells` sample.

**Technical and biological replicates:**


```{margin} Technical and biological replicates
:name: tech-biol-replicates
Usually *technical replicates* refer to repeated measures of the same sample, while *biological replicates* refer to separate samples which have been treated in the same way (e.g. different donors){cite}`Bell2016-dm`.

In FANTOM, the "biol_rep" and "donor" label are both used to denote biological replicates.
```

The {ref}`FANTOM accession numbers<fantom-accession>` are per sample, not per measurement. 
Samples for which there are repeat measurements (technical replicates) will show up multiple times in the expression file. 
FANTOM technical and biological replicates are indicated in long labels of the annotated expression FANTOM file, by the inclusion of “tech_rep” or “biol_rep” in the long sample labels e.g. `tpm.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20tech_rep1.CNhs10855.11227-116C3.hg38.nobarcode`. 
These were used to create additional fields for the human samples table.

Note: there is an error in the original transcript expression file for one of these identifiers (`tpm.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20rep2.CNhs11062.11227-116C3.hg38.nobarcode`) such that it is missing the “tech” part of the the replicate label. 
There is a hard-coded fix for this accession when I read in the input file and the FANTOM data curation team was informed.

After restricting the data set to *primary cell* and *tissue* type samples, there are {glue:}`num_bio_rep_samples` remaining samples which have biological replicates (between 2 and 3 replicates each), and {glue:}`num_tech_rep_samples` sets of samples with technological replicates (2 replicates each).

**Age and age range:** 


The age of the sample source donor(s) is available through two fields in the human sample information file: `Characteristics [Developmental stage]`, and `Characteristics [Age]`.
These fields contain description-like text, which are somewhat inconsistent, for example, “3 year old child”, “3 years old child”, “25 year old”, “76” and “76 years old adult” all feature in the same column, amongst other errors. 
These were standardised into a new field (`Age (years)`).
This field does not seek to include multiple ages (i.e. when the sample comes from a pool of donors).
There is a complementary (i.e. no overlap) field (`Age range (years)`), which contains age ranges for the {glue:}`age_ranged` samples that contain multiple ages.
In both columns, some samples contain fetal samples, in which caset age (range) is given as a negative decimal (converted to years before birth).

There file also contained some discrepancies between ages and developmental stages in the FANTOM human samples file.
For example, sample `FF:10027-101D9` is labelled as *thymus, adult, pool1* in the *Description* field, but as *0.5,0.5,0.83 years old infant* in the *Developmental Stage* field. 
Sample `FF:10209-103G2` had an age of ‘M’ and a sex of ‘28’. 
I reported both these discrepencies: and the latter has since been fixed in the FANTOM file, and for the former, I hardcode the age to `NaN`.

**Sex:**

The `Characteristics [Sex]` field contains information about the sex of the sample source donor(s). 
Similarly to age, due to the consortium nature of FANTOM5, the entries of this field are not consistently labelled.
They undergo data cleaning into 4 categories: male, female, mixed (pool with both male and female samples), and unlabelled.

**Disease and tissue mapping:**


The disease status of samples (e.g. healthy/non-healthy) is not straight-forwardly labelled in the human sample file, so requires some basic text-mining (and cross-referencing with ontology terms).
Similarly, there is a `Characteristics[Tissue]` field in the human samples file containing some manually mapped tissue types, but as I point out with an example in {ref}`the exploratory data analysis<eda-sample-tissues>`, these do not contain ideal mappings for Filip. 

The continued data processing of these components is described in {ref}`the methdology section <filter-methods>`, after the introduction of `uberon-py` (the package developed to do this).

<!--
[//]: # (TODO: Add link to FANTOM exp download)

```{admonition} FANTOM5 cleaned experimental design file
:name: cleaned-fantom-exp
The cleaned FANTOM5 experimental design file (which has undergone the cleaning mentioned in this section, and in {ref}`the methodology section<filter-methods>`) is available [here](link). 
```
-->

(fantom-cleaning-expression)=
### Initial FANTOM5 data cleaning: expression file

```{code-cell} ipython3
:tags: [hide-input, remove-output]

from helper_c05 import fantom_tpm_clean as tpm_clean

# Create list of allowed primary + tissue samples to prevent reading in whole tpm file:
long_ids_to_keep, long_ids_to_new_ff = fsc.long_ids_to_restricted_samples(samples_info, expression_header)
dtypes = tpm_clean.get_dtypes(expression_header)
tpm_file = '../c08-combining/data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_tpm_ann.osc.txt'
cage_tpm = tpm_clean.read_and_clean_tpm(tpm_file, long_ids_to_keep, long_ids_to_new_ff, dtypes)
protein_tpm = tpm_clean.get_protein_tpm(cage_tpm)
```

```{code-cell} ipython3
:tags: [remove-input, remove-output]

fsc.save_sample_cleaned(samples_info, file_path='data/cleaned_pre_input/samples_info.csv')
tpm_clean.save_long_ids(long_ids_to_new_ff, file_path = 'data/cleaned_pre_input/ff_accessions_to_keep.txt')
tpm_clean.save_protein_tpm(protein_tpm, file_path='data/cleaned_pre_input/protein_tpm.csv')
```

The tidied and restricted sample data, is combined with the FANTOM5 CAGE peaks expression data file and processed to create a protein-centric expression file.
The CAGE peaks have already been cleaned by FANTOM (labeled as "fair") meaning that CAGE peaks do not overlap.

**CAGE peaks with associated proteins:**


The CAGE peaks represent all kinds of mRNA transcripts, not only those which map to protein-coding gene, for example "RNA genes" representing pseduogenes or long non-coding RNAs.
The FANTOM file provides mappings to Uniprot IDs (`uniprot_id`), and these are used to discard the CAGE peaks that do not map to protein-coding genes: this takes us from {glue:}`total_F5_peaks` to  {glue:}`has_protein_F5_peaks` rows (CAGE peaks).

**CAGE peaks mapped to one gene only:**

[//]: # (TODO: Do I want to do this? What about overlapping genes?)
[//]: # (TODO: cross-ref discrepencies between gene ID databases)
[//]: # (TODO: Plotly Gannt for CAGE peaks overlapping with multiple transcripts/genes)
CAGE peaks are mapped to genes based on overlap with the gene, so it is not always clear which gene a CAGE peak maps to.
For simplicity, and to remove the potential of wrongly mapped genes being used in Filip, protein-coding CAGE peaks (those which are mapped to at least one `uniprot_id` by FANTOM) but that map to multiple genes are removed.
These can be found by looking at either the `hgnc_id` or `entrezgene_id` gene identifier columns.
The choice of gene ID matters, since there are discrepancies between gene ID databases: in this case, choosing `hgnc_id` finds all those CAGE peaks found by using `entrezgene_id`, and more, so these are removed.
This represents a total of {glue:}`total_gene_id_duplicates` CAGE peaks that map to multiple genes according to the given identifiers.

**Proteins that map to multiple genes:** 

For Filip, the expression was calculated per protein (since it is protein function predictions that it is filtering), rather than per CAGE peak (summing the TPMs of all CAGE peaks mapped to a protein to get the total for that protein) as in the original data, or as is often presented per gene.
This gave {glue:}`protein_expression_total` rows of "protein expression" data.

Of these, there were then {glue:}`rows_left_multiple_genes` rows of data (corresponding to {glue:}`proteins_multiple_genes` proteins) for which each protein maps to multiple genes.
This happens when different genes are translated to make identical protein products, for example the [H4 human histone protein](https://www.uniprot.org/uniprot/P62805) is encoded by 14 different genes at different loci, across three different chromosomes.
It used to be the case that Uniprot would map these genes to the same Uniprot ID, but more recently different Uniprot IDs are used to capture where the proteins came from.
These small number of rows were also removed for simplicity.

<!--It would probably make sense to keep these multiple gene proteins and sum over them because they are expressed lots around the geneome, so it would make sense to continue to count them. The small number and the fact that they are widely expressed means it isn't likely to be important though-->

(fantom-filter-eda)=
### Exploratory Data Analysis

**Samples:**

After {ref}`restricting the samples to those which are primary cells or tissues<fantom-sample-categories>`, there were {glue:}`fantom-primary-tissue-samples` remaining samples.

```{code-cell} ipython3
:tags: [hide-input]

from helper_c05 import fantom_sample_eda as f_eda
sex_donut, tissues_samples, nan_age_count, collaborators_providers = f_eda.create_plot_dfs(samples_info)
fig = f_eda.create_plotly_plots(samples_info, sex_donut, tissues_samples, nan_age_count, collaborators_providers)
fig.show('notebook')
```

```{figure} ../images/blank.png
---
name: fantom-eda
---
(a) sex: a donut plot showing the sex labels of samples. 
(b) collaborators and providers: a stacked histogram showing the {glue:}`num_collaborators` most common collaborators, and {glue:}`num_providers` most common providers. 
(c) age: a histogram of age of sample donors (this does not include the {glue:}`age_ranged` samples which have age ranges due to pooled donors of various ages). 
(d) tissues and sample types: a histogram showing the {glue:}`num_common_tissues` most common tissues, spread across the different types of samples (primary cells, tissue donors, and tissue pools).
```

<!-- ../images/blank.png This is a workaround to put a 1x1px blank image after an interactive image so that it appears to have a figure label -->

__Sample metadata:__ 
Looking at the FANTOM5 data (see {numref}`fantom-eda`), overall we see that there the samples are very varied, across ages, sex, sample providers, and collaborators, although (d) shows that the majority of samples are *primary cell* samples, and very few are *tissue - pool* samples.
Secondly, we can see that after careful cleaning, some metadata is missing, i.e. 38.4% of samples have unknown sex (a), most collaborators did not label the sample provider (b), and most samples do not have a labelled age (c).

(eda-sample-tissues)=
__Sample Tissues:__ 
In {numref}`fantom-eda` subplot (d), we can also note some interesting things about the tissue types provided by the Fantom Human Samples file. {glue:}`anatomical-system` primary cell samples are labeled *ANATOMICAL SYSTEM*. If we look closer at these samples, we can see that it is theoretically possible to map some of these samples to tissues (see {numref}`anatomical-system-table`). 

[//]: # (TODO: cross-ref to where discussed in methodology, and vice versa) 

(fantom-tissues-how-general)=
There is also the question of how general or specific the human sample categories are. There are {glue:}`blood-samples` samples which are mapped to *blood* ({numref}`anatomical-system-table` (d)), but when we come to map the FANTOM5 tissues to phenotypes, this may be too broad a category. Similarly, there are {glue:}`tissues-less-three` with less than three samples each (not pictured) that may be too narrow to map to phenotypes, and a more accurate picture of that phenotype would come from taking a more general tissue.

```{code-cell} ipython3
:tags: [hide-input]

anatomical_system_samples = f_eda.anat_system_tbl(samples_info, chosen_samples = [2, 10, 15, 20])
```

```{glue:figure} anatomical-system-sample-table
:figwidth: 800px
:name: anatomical-system-table

An example of four *ANANTOMICAL SYSTEM* tissues, with tissue-specific cells, indicating that they could be mapped to tissues. For example sample `FF:11922-125H5` is a gingival fibroblast, which are one of the main constituent cells of gum tissue.
```

[//]: # (TODO: Cross ref to uberon-py)
[//]: # (TODO: Cross ref to use of uberon-py for removal of disease samples)

We can also see in {numref}`anatomical-system-table` that this data set, though having undergone some data cleaning, still contains disease samples (e.g. "aggressive periodontitis"). 


**Protein-centric TPM:**


```{code-cell} ipython3
:tags: [hide-input]

from helper_c05 import fantom_tpm_eda as fte
fig = fte.create_distribution_plot(samples_info, protein_tpm)
fig.show('notebook')
```

```{figure} ../images/blank.png
---
name: fantom-protein-distribution
---
(a) box-plots showing the distribution of mean (TPM+1) values (note: logarithmic x axis) for the top {glue:}`num-tissues-fpd` most common tissue and primary cell samples in the FANTOM5 human data.
(b) density-plots showing the distribution of mean (TPM+1) values for the top {glue:}`num-tissues-fpd` most common tissue and primary cell samples in the FANTOM5 human data on log-log axes.
```

<!-- ../images/blank.png This is a workaround to put a 1x1px blank image after an interactive image so that it appears to have a figure label -->

As expected, {numref}`fantom-protein-distribution` shows similar distributions of expression per tissue since the data is TPM normalised ({ref}`since TPM normalises samples by sample library size to account for sequencing depth <rna-normalisation>`), with the characteristic long tail.

(cell-tissue-phen-map-data)=
## Cell, tissue, and phenotype mapping data
[//]: # (TODO: Cross ref to methodology)

I also used the following datasets to aid in mapping to a common set of identifiers:
- the [uberon extended ontology OBO file](http://purl.obolibrary.org/obo/uberon/ext.obo) from [the uberon website](http://uberon.github.io/downloads.html) to assist in mapping cells and tissues.

[//]: # (TODO: Describe mapping data here, e.g. biomart/uniprot)

+++

(cafa2-training-set)=
## "Training" set: CAFA2

During development, I tested Filip by comparing DcGO only and Filip-plus-DcGO on data from the 2nd round of the CAFA competition: CAFA2. 
I chose to use the CAFA2 data because rather than a larger set of annotations (such as those available from SwissProt-KB or GOA) because it provided a way of validating on unknown targets.
I.e. if I made predictions with DcgO using the version of GO from the time the challenge was launched, and I use the groundtruth data provided by CAFA2, then I could compare my results with those in the CAFA2 competition and I could look at my results on unknown targets.
Although Filip was not literally "trained" on this data in a machine-learning sense (it doesn't have any formalised parameters), I had access to the "groundtruth" data as I was developing CAFA2.

This was the most recent round of CAFA for which there were "groundtruth" data available at the time of development.

### Data files and acquisition

The data consisted of:
- {ref}`CAFA2 targets<cafa2-targets>`: a list of proteins which the CAFA2 competition was soliciting predictions for.
- {ref}`CAFA2 ground truth data<cafa-benchmark>`: experimentally validated associations between proteins and GO terms, divided by category.

Both of which could be found within the CAFA2 paper{cite}`Jiang2016-rz`'s [Supplementary Material](https://figshare.com/articles/dataset/Supplementary_Data_for_CAFA2/2059944).

(cafa2-targets)=
**CAFA2 targets**: 
CAFA2 provided targets from species across the tree of life: bacteria (10 species), archaea (7 species), and eukaryotes (10 species).
Since tissue-specific gene expression data (which Filip requires) is not available for all species, I only used the human targets (in `data/CAFA2-targets/eukarya/sp_species.9606.tfa`). 

[//]: # (TODO: Move explain FASTA at/before PQI, due to X content)

```{margin} FASTA format
:name: fasta
FASTA is a text-based file format for proteins, where each letter represents an amino acid (except X, which represents any amino acid).
```

The `sp_species.9606.tfa` file is a {ref}`FASTA<fasta>` file containing information about `20257` proteins, each with a CAFA2 identifier (e.g. `T96060000001`), Uniprot Entry Name (the mnemonic identifier for the protein, e.g. [`1433B_HUMAN`](https://www.uniprot.org/uniprot/P31946)), and the amino acid sequence, as in the following excerpt:

```
>T96060000001 1433B_HUMAN
MTMDKSELVQKAKLAEQAERYDDMAAAMKAVTEQGHELSNEERNLLSVAYKNVVGARRSS
WRVISSIEQKTERNEKKQQMGKEYREKIEAELQDICNDVLELLDKYLIPNATQPESKVFY
LKMKGDYFRYLSEVASGDNKQTTVSNSQQAYQEAFEISKKEMQPTHPIRLGLALNFSVFY
YEILNSPEKACSLAKTAFDEAIAELDTLNEESYKDSTLIMQLLRDNLTLWTSENQGDEGD
AGEGEN
```

[//]: # (TODO: move note to secion where I use this data so I can explain that)
[//]: # (NOTE: doesn't matter if it's the right build hg38 - not relevant - we only use the mnemonic id)

(cafa-benchmark)=
**CAFA2 benchmark**: 
The CAGA2 benchmark data was available in the `/data/benchmark` directory of the CAFA2 Supplementary Data. 
It includes:
- **Lists** of different types of targets for which there is groundtruth data (in `/data/benchmark/lists`): each line of these files is a CAFA2 protein identifier (e.g. `T96060015767`). The lists are separated into different files according to species, source phenotype ontology (e.g. `HP`, `GO`), and protein {ref}`type<no-limited-knowledge>` (type1 = No Knowledge, type2 = Limited Knowledge). There are `7` files for human.
- **Groundtruth** associations (in `/data/benchmark/groundtruth`): tab-separated CAFA protein identifiers and phenotype ontology terms, e.g. `T96060000002    HP:0000348`), organised into `8` separate files by source phenotype ontology, and whether the proteins are experimentally annotated to the exact term, or whether an association can be inferred due to a {ref}`ontology relationship<ont-relationships>`.
