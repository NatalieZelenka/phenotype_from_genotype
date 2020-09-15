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

## Data wrangling and the `uberon-py` package

[//]: # (TODO: cross-ref appendix or move appendix info here)
[//]: # (TODO: Migrate from actual notebook to here to make this thesis damn reproducible!)

In order to combine the four chosen datasets, substantial data wrangling was necessary. The details of these processes (obtaining, checking, and mapping identifiers, excluding irrelevant data, etcetera), are described in this section. Further details are provided in the appendix.

The steps required to obtain consistently formatted and labelled data can be described as follows:
1. Obtaining the raw expression per gene for healthy human tissues
    A. Obtaining data
    B. (Where required) Mapping from transcript to gene
    C. (Where required) Filtering out disease samples
    D. (Where required) Filtering out non-human samples
2. Mapping from sample name to UBERON tissue
3. Aggregating metadata

[//]: # (TODO Add/create reproducible figure version of F18)
Figure 18 gives an overview of the of the data wrangling pipeline. Additional steps 1A, 1B, and 1C were only necessary for the FANTOM dataset.

+++

**1A\. Obtaining raw expression per gene for healthy human tissues**

[//]: # (TODO: Check how raw the data was and if it's sensible to refer to it that way)
Raw data was obtained, where possible via the ExpressionAtlas R package[107], which gives gene expression counts identified by ENSG IDs, metadata (containing pipeline, filtering, mapping and quantification information), and details of experimental design (containing for example organism part name, individual demographics, and replicate information, depending on the experiment). 

Raw counts for the HPA, GTeX and HDBR experiments were available through the ExpressionAtlas R package[107]. For the FANTOM dataset, raw counts were not available through the ExpressionAtlas R package[107]. In this case, raw counts for transcript expression were downloaded directly [from the FANTOM website](http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/extra/CAGE_peaks_expression/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt.gz). 

The downloaded FANTOM5 file has already undergone some quality control by FANTOM, it is limited to peaks which meet a “robust” threshold (>10 read counts and 1TPM for at least one sample). 

+++


**1B\. Mapping from transcript to gene** 

This step was only required for the FANTOM dataset.
[//]: # (TODO: sentence about why FANTOM is per transcript - CAGE)
[//]: # (TODO: cite biomart)

FANTOM provides mappings to gene IDs based on proximity of genes to peaks according to Ensembl. Gene expression was then calculated by summing over transcripts mapped to genes. The transcripts were already mapped to HGNC gene identifiers in the downloaded FANTOM file and [Ensembl’s Biomart](https://www.ensembl.org/biomart) was used to obtain a mapping from HGNC gene identifiers to ENSG gene identifiers, in order to match the gene expression atlas format. 

Any transcripts which mapped to multiple genes were discarded, as were any HGNC ids which did not map to ENSG ids.

+++


**1C\. Filtering out disease samples**

**GTEx**

Although GTEx contained clinical data, no disease-related phenotypes were removed from the data set, since the `disease` column contains only values of “normal” and the only clinical variables (as described in the `clinical_variables` column) in the dataset were sun exposure or lack thereof for skin tissues. I judged these to be within the normal range of environments that we would expect skin to be subjected to.

**FANTOM**
The FANTOM sample ontology was used to remove samples which are models for diseases. Samples which are disease models are identified using the `is_model_for` relationship and these relationships are propagated to the children terms based on the `is_a` relationship. For example, `FF:11558-120D1` (Fibroblast - skin spinal muscular atrophy, donor2) would be removed from the set of samples, since:
`FF:11558-120D1` (Fibroblast - skin spinal muscular atrophy, donor2) `is_a FF:0000251` (human fibroblast - skin spinal muscular atrophy sample) `is_model_for DOID:12377` (spinal muscular atrophy).

+++

**1D\. Filtering out non-human samples**

The GTEx, HDBR, and HPA experiments contained only human samples. 

**FANTOM**
The FANTOM5 data set also contains non-human (mouse) samples. The FANTOM sample ontology (which was downloaded [from here](http://fantom.gsc.riken.jp/5/datafiles/latest/extra/Ontology/ff-phase2-170801.obo.txt)) was used to look-up which FANTOM samples are human samples, i.e. have an `is_a` relationship to the term `FF:0000210` (human sample) directly or indirectly. 

+++

**2\. Mapping to UBERON**

**FANTOM**
FANTOM also contains time courses of cell differentiation (cells changing from one type to another) as well measures of perturbed cells. Since these samples do not have a well-defined locality in the body given by cell or tissue type, they were not used in the combined dataset. Such samples were filtered out using the human sample information spreadsheet.
