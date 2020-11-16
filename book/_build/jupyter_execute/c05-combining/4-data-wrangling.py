## Data Wrangling
Before the data sets could be combined, substantial data wrangling was necessary. The details of these processes; obtaining, checking, mapping identifiers, excluding irrelevant data, etc, are described in this section.

### Overview
The steps required to obtain consistently formatted and labelled data can be described as follows:
1. Obtaining the raw expression per gene for healthy human tissues
 - a. Obtaining data
 - b. (Where required) Mapping from transcript to gene
 - c. (Where required) Filtering out disease samples
 - d. (Where required) Filtering out non-human samples
2. Mapping from sample name to UBERON tissue
3. Aggregating metadata

# fig.align: center
# fig.cap: Funnel plot showing the data cleaning pipeline for FANTOM transcripts/genes
#   (left) and samples (right), along with the number which remained after each stage
#   of data cleaning.
# name: combining-data-pipeline
# Code here for creating data wrangling pipeline image. Steps should be labelled matching 1A, 1B, etc.

{numref}`combining-data-pipeline` shows an overview of the data wrangling pipeline. Additional steps 1A, 1B, and 1C were only necessary for the FANTOM dataset.

**1A\. Obtaining raw expression per gene for healthy human tissues**

As mentioned in {ref}`data-aquisition`, for the HPA, GTeX and HDBR experiments, count data were available through the *ExpressionAtlas* R package{cite}`Keays2018-pg`, while this was not the case for the FANTOM dataset, which was downloaded directly. 

**1B\. Mapping from transcript to gene** 

This step was only required for the FANTOM dataset.

FANTOM provides mappings to gene IDs based on proximity of genes to peaks according to Ensembl. Gene expression was then calculated by summing over transcripts mapped to genes. The transcripts were already mapped to HGNC gene identifiers in the downloaded FANTOM file and [Ensembl’s Biomart](https://www.ensembl.org/biomart) was used to obtain a mapping from HGNC gene identifiers to ENSG gene identifiers, in order to match the gene expression atlas format. 

Any transcripts which mapped to multiple genes were discarded, as were any HGNC ids which did not map to ENSG ids.

**1C\. Filtering out disease samples**

The HDBR and HPA experiments contained only healthy samples.

**GTEx**
Although GTEx contained clinical data, no disease-related phenotypes were removed from the data set, since the `disease` column contains only values of “normal” and the only clinical variables (as described in the `clinical_variables` column) in the dataset were sun exposure or lack thereof for skin tissues. I judged these to be within the normal range of environments that we would expect skin to be subjected to.

**FANTOM**
The FANTOM sample ontology was used to remove samples which are models for diseases. Samples which are disease models are identified using the `is_model_for` relationship and these relationships are propagated to the children terms based on the `is_a` relationship. For example, `FF:11558-120D1` (Fibroblast - skin spinal muscular atrophy, donor2) would be removed from the set of samples, since:
`FF:11558-120D1` (Fibroblast - skin spinal muscular atrophy, donor2) `is_a FF:0000251` (human fibroblast - skin spinal muscular atrophy sample) `is_model_for DOID:12377` (spinal muscular atrophy).

**1D\. Filtering out non-human samples**

The GTEx, HDBR, and HPA experiments contained only human samples. 

**FANTOM**
The FANTOM5 data set also contains non-human (mouse) samples. The FANTOM sample ontology (which was downloaded [from here](http://fantom.gsc.riken.jp/5/datafiles/latest/extra/Ontology/ff-phase2-170801.obo.txt)) was used to look-up which FANTOM samples are human samples, i.e. have an `is_a` relationship to the term `FF:0000210` (human sample) directly or indirectly. 

**2\. Mapping to UBERON**

Mapping from samples to Uberon tissue required the development of a small Python package `uberon_py`. To create input to this package, informal tissue names (e.g. blood, kidney) were taken from the experimental design files (or the human sample information file for FANTOM) to create a map of samples to informal tissue names. For FANTOM, the FANTOM ontology could also be used to create a more fine-grained mapping of samples to tissues based on FANTOM sample identifiers and/or cell type (CL) identifiers.

**HPA**
The HPA samples were mapped using exact matches to Uberon names. Three types of sample did not have exact matches: “transformed skin fibroblast”, “suprapubic skin”, and “ebv-transformed lymphocyte”. I manually mapped “suprapubic skin” to UBERON:0001415 Skin of pelvis, and excluded the other two (corresponding to excluding 869 samples). 

**HDBR**
For HDBR, tissue names from the “organism part’ column of the column data file were matched to Uberon names and synonyms from the Uberon extended ontology. The 96 unmatched terms corresponding to mixed brain tissues and brain fragments were defaulted to the more general Uberon Brain term. 

**FANTOM**
Since an experimental design file could not be obtained for FANTOM via GxA, additional sample information was obtained via the FANTOM5 website, namely the human sample information file (HumanSamples2.0.sdrf.xlsx) and the FANTOM5 ontology.

FANTOM also contains time courses of cell differentiation (cells changing from one type to another) as well measures of perturbed cells. Since these samples do not have a well-defined locality in the body given by cell or tissue type, they were not used in the combined dataset. Such samples were filtered out using the human sample information spreadsheet.

**3/. Aggregating Metadata**
To create consistent metadata for the samples (e.g. age, developmental stage, replicate status, etc), information was extracted from multiple sources (including GxA and additional data from each experiment), and sometimes manually curated or corrected. 

Metadata about the experiments was collected from multiple sources, primarily the column data files accessed via ExpressionAtlas. This metadata was used to describe the the experimental design for ComBat. The metadata collected includes, where available, sample identifier, individual identifier, age (exact), age (range), developmental stage, tissue type (Uberon term), sex, experiment, biological replicate identifier and technical replicate identifier. 

Both age variables are given in years and may include negative values (e.g. for a developing fetus). The age (range) variable contains uneven ranges, since this allows there to be an age-related factor that is compatible across the experiments. These values had to be converted to common units manually, since they were incompatible between experiments, and age-related terms were missing in GxA for GTEx and HPA, although for GTEx it was possible to acquire via its own website (at https://storage.googleapis.com/gtex_analysis_v7/annotations/GTEx_v7_Annotations_SubjectPhenotypesDS.txt ).

FANTOM metadata was mostly taken from the human sample information file. There were discrepancies between ages and developmental stages in the FANTOM human samples file, for example, sample `FF:10027-101D9` is labelled as “thymus, adult, pool1” in the Description field, but as “0.5,0.5,0.83 years old infant” in the Developmental Stage field, and sample `FF:10209-103G2` has an age of ‘M’ and a sex of ‘28’. There were also numerous typographical inconsistencies, for example, “3 year old child”, “3 years old child”, “25 year old”, “76” and “76 years old adult” all feature in the same column, amongst other errors. For this reason, creating a cleaned experimental design file was laborious, but the resulting file has been sent to the FANTOM data curators so that they might make it officially available.

FANTOM technical and biological replicates are indicated in the annotated gene expression FANTOM file, by the inclusion of “tech_rep” or “biol_rep” in the long sample labels e.g. `counts.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20tech_rep1.CNhs10855.11227-116C3.hg38.nobarcode`. These were used to create the experimental design file. 

Note: there is an error in the original transcript expression file for one of these identifiers (`counts.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20rep2.CNhs11062.11227-116C3.hg38.nobarcode`) such that it is missing the “tech” part of the the replicate label. This was manually changed in my copy of the input file and the FANTOM data curation team was informed.

##### Tissue Groups
Eleven more general tissue groups (for example brain, digestive system, connective tissue) were identified by hand. Individual tissues were mapped to these groups using the `Relations()` function. 

# fig.align: center
# fig.cap: Funnel plot showing the data cleaning pipeline for FANTOM transcripts/genes
#   (left) and samples (right), along with the number which remained after each stage
#   of data cleaning.
# name: combining-funnel-plot
# Code here for creating data wrangling pipeline image. Steps should be labelled matching 1A, 1B, etc.

{numref}`combining-funnel-plot` shows a funnel plot, showing how the FANTOM5 data was processed to select the final genes and samples present in the combined dataset. 

**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```
