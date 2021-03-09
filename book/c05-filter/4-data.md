<!-- #region -->

# Data

##  Expression data

### FANTOM5 data

[//]: # (TODO: Mention CAGE - ?relevant because mapping to proteins..)
[//]: # (TODO: Data given as TPM per CAGE peak - CAGE peaks map to multiple genes when the CAGE peak overlaps multiple genes, also CAGE peaks that map to the same protein, could map to different sets of genes because CAGE peaks map to different genes: don't map via CAGE peaks because you lose information) 

`filip` requires expression data to inform whether or not predictions should be filtered out. The FANTOM5 data set was chosen for this purpose (at the time this was the latest data output of the {ref}`FANTOM consortium<fantom-consortium>`).

FANTOM5 represents one of the most comprehensive collections of expression data, in this case transcript rather than gene expression. 
It contains a combination of human, mouse, health, and disease data, as well as time courses and cell perturbations.

```{margin} The FANTOM Consortium
:name: fantom-consortium
The Functional ANnoTation Of the MAmmalian genome (FANTOM) consortium was established as the human genome project was nearing completion when researchers had a parts list of human biology, but few of the functions of these parts (genes) were known. The consortium has run a range of large scale collaborative projects in five rounds to further this goal. The first FANTOM project used only the mouse genome, but later versions also included human. 
```

[//]: # (TODO: What does the data contain, how many samples, etc)

#### Reasoning

I chose the FANTOM5 data as the input gene expression data for `filip`, for the following reasons:
- The data set has a good coverage of different tissue types, meaning that `filip` should be able to turn this into a good coverage of predictions.
- The data set has an ontology of samples, which is already linked to Uberon tissue terms and CL cell terms, making the mapping process much easier.

I chose the version of the FANTOM5 data that:
- had been reprocessed using the hg38 reference genome (the original FANTOM5 data was processed using hg19).
- contained annotated information about the samples, as this information could be used to aid in mapping
- was in TPM format

[//]: # (TODO: Aside about TPM/link to before)

### Additional mapping data

I also used the following datasets to aid in mapping to a common set of identifiers:
- the [uberon extended ontology OBO file](http://purl.obolibrary.org/obo/uberon/ext.obo) from [the uberon website](uberon.github.io/downloads.html) to assist in mapping cells and tissues.

[//]: # (TODO: Describe mapping data here, e.g. biomart/uniprot)


### Data Acquisition

I downloaded the following files from the FANTOM website:
- the [FANTOM5 CAGE peaks expression data](http://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/extra/CAGE_peaks_expression/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt.gz) containing expression in counts per transcript, and mappings to HGNC id and entrez gene ID.
- the [FANTOM5 ontology](https://fantom.gsc.riken.jp/5/datafiles/latest/extra/Ontology/ff-phase2-170801.obo.txt) containing an obo file mapping between FANTOM sample IDs, Uberon and cell ontology (CL) terms.
- FANTOM's [human sample information file](https://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/basic/HumanSamples2.0.sdrf.xlsx) containing text descriptions about sample, for example tissue, age, sex, disease, etc, which is necessary for data cleaning.

[//]: # (TODO: if time, update so that data aquisition code is here)
<!-- #endregion -->

### Data Cleaning
In order to clean the FANTOM data for use in `filip`, transcripts that didn't match to proteins were removed, and the following samples were removed:
- Disease samples
- Non tissue-specific samples
- Non human samples


### Exploratory Data Analysis

[//]: # (TODO: Number of transcripts, proteins, genes)
[//]: # (TODO: Number of samples, biological and technical replicates)
[//]: # (TODO: Expression distribution)

#### TPM

```python
import pandas as pd
from myst_nb import glue

transcript_tpm = pd.read_csv('../c06-combining/data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_tpm_ann.osc.txt', delimiter='\t', comment='#', dtype={'entrezgene_id': object})
transcript_tpm.drop([0], axis='index', inplace=True)
transcript_tpm.set_index('00Annotation', inplace=True)

sep_in_col = ' '  # In the transcript expression file, genes and proteins ids with multiple values in a column are separated by a space.

n_peaks = transcript_tpm.shape[0] # Total number of CAGE peaks in FANTOM5 data set
glue("total_F5_peaks", n_peaks)

transcript_tpm.dropna(axis=0, subset=['uniprot_id'], inplace=True)
n_peaks_protein = transcript_tpm.shape[0]  # Number of peaks which are protein-coding (as mapped by FANTOM)
glue("has_protein_F5_peaks", n_peaks_protein)

transcript_tpm['uniprot_list'] = transcript_tpm['uniprot_id'].str.split(sep_in_col)  
transcript_tpm.head()
```

[//]: # (TODO: Check what type of uniprot ID these are)
[//]: # (TODO: Choose output of these code cells: make some invisible, show some data snippets)

The CAGE peaks represent all kinds of transcripts, not only those which map to protein-coding genes. 
The FANTOM file provides mappings to Uniprot IDs (`uniprot_id`), and these are used to discard the CAGE peaks that do not map to protein-coding genes: this takes us from {glue:}`total_F5_peaks` to  {glue:}`has_protein_F5_peaks` rows.

```python
# How many CAGE peaks map to multiple HGNC id genes?
hgnc_id_duplicates = transcript_tpm[transcript_tpm['hgnc_id'].str.contains(' ', na=False)].shape[0]
print(f"There are {hgnc_id_duplicates} CAGE peaks that map to multiple HGNC ids (genes)")
glue("hgnc_id_duplicates", hgnc_id_duplicates)

entrezgene_id_duplicates = transcript_tpm[transcript_tpm['entrezgene_id'].str.contains(' ', na=False)].shape[0]
print(f"There are {entrezgene_id_duplicates} CAGE peaks that map to multiple Entrezgene ids")
glue("entrezgene_id_duplicates", entrezgene_id_duplicates)

total_gene_id_duplicates = transcript_tpm[(transcript_tpm['hgnc_id'].str.contains(' ', na=False) | transcript_tpm['entrezgene_id'].str.contains(' ', na=False))].shape[0]
print(f"There are {total_gene_id_duplicates} CAGE peaks that map to multiple genes (HGNC or entrezgene IDs)")
glue("total_gene_id_duplicates", total_gene_id_duplicates)

# Remove gene duplicates per CAGE TSS (due to overlapping CAGE TSS)
transcript_tpm = transcript_tpm[~(transcript_tpm['hgnc_id'].str.contains(' ', na=False) | transcript_tpm['entrezgene_id'].str.contains(' ', na=False))]

n_peaks_single_gene = transcript_tpm.shape[0]  # Number of peaks which are protein-coding (as mapped by FANTOM)
glue("single_gene_F5_peaks", n_peaks_single_gene)
```

CAGE peaks are mapped to genes based on overlap with the gene, so it is not always clear which gene a CAGE peak maps to.
Protein-coding CAGE peaks (map to at least one `uniprot_id`), that map to multiple genes are removed for simplicity. 
These can be found by looking at either the `hgnc_id` or `entrezgene_id` gene identifier columns: the mapping to `hgnc_id` contains all those found in `entrezgene_id`, so these are removed.
This represents a total of {glue:}`total_gene_id_duplicates` CAGE peaks that map to multiple genes according to the given identifers.

```python
# Create expression by protein (uniprot ID), rather than by transcript
protein_tpm = transcript_tpm.explode('uniprot_list').groupby(['uniprot_list', 'entrezgene_id', 'hgnc_id']).sum()
protein_tpm.reset_index(level=['hgnc_id', 'entrezgene_id'], inplace=True)
protein_tpm.rename_axis(index='uniprot_id')
# Every protein ID should have at least one gene ID
assert(protein_tpm[protein_tpm['entrezgene_id'].isna()].shape[0]==0) 
assert(protein_tpm[protein_tpm['hgnc_id'].isna()].shape[0]==0)

glue("protein_expression_total", protein_tpm.shape[0])
protein_tpm.head()
```

```python
rows_left_multiple_genes = protein_tpm[protein_tpm.index.duplicated(keep=False)].shape[0]
print(f"Number of remaining rows that map to multiple genes: {rows_left_multiple_genes}")
glue("rows_left_multiple_genes", rows_left_multiple_genes)

proteins_multiple_genes = len(protein_tpm[protein_tpm.index.duplicated(keep=False)].index.unique())
print(f"Number of proteins that map to multiple genes: {proteins_multiple_genes}")
glue("proteins_multiple_genes", proteins_multiple_genes)

protein_tpm[protein_tpm.index.duplicated(keep=False)].head()

protein_tpm = protein_tpm[~protein_tpm.index.duplicated(keep=False)]
assert(protein_tpm.shape[0]==len(protein_tpm.index.unique()))
glue("unique_proteins", protein_tpm.shape[0])
```

For `filip`, the expression was calculated per protein (since it is protein function predictions that it is filtering), rather than per CAGE peak (summing the TPMs of all CAGE peaks mapped to a protein to get the total for that protein) as in the original data, or as is often presented per gene.
This gave {glue:}`protein_expression_total` rows of "protein expression" data.

Of these, however, there were {glue:}`rows_left_multiple_genes` rows of data (corresponding to {glue:}`proteins_multiple_genes` proteins) for which the proteins map to multiple genes.
This happens when different genes are translated to make identical protein products.
It used to be the case that Uniprot would map these genes to the same Uniprot ID, but more recently different Uniprot IDs are used to capture where the proteins came from.
These rows were also removed.

```python
display(transcript_tpm[transcript_tpm['uniprot_id'].str.contains('B2R4R0', na=False)])
```

```python
# CAGE PEAKS ARE TOO SMALL TO SEE ON A STATIC PLOT, WOULD NEED AN INTERACTIVE PLOT.

# from Bio.SeqFeature import SeqFeature, FeatureLocation
# from Bio.Graphics import GenomeDiagram
# from IPython.core.display import Image

# gdd = GenomeDiagram.Diagram('Test Diagram')
# gdt_features = gdd.new_track(1, name="CAGE Peaks", greytrack=True)
# gds_features = gdt_features.new_set()

# #Add three features to show the strand options,
# p13_HIST1H4B = SeqFeature(FeatureLocation(26027058,26027076))
# gds_features.add_feature(p13_HIST1H4B, name="p13@HIST1H4B", label=True)

# p12_HIST1H4B = SeqFeature(FeatureLocation(26027093, 26027119))
# gds_features.add_feature(p12_HIST1H4B, name="p12@HIST1H4B", label=True)

# p12_HIST1H4B = SeqFeature(FeatureLocation(26189331, 26189346))
# gds_features.add_feature(p12_HIST1H4B, name="p3@HIST1H4D", label=True)

# p12_HIST1H4B = SeqFeature(FeatureLocation(26285754, 26285769))
# gds_features.add_feature(p12_HIST1H4B, name="p4@HIST1H4H", label=True)

# p12_HIST1H4B = SeqFeature(FeatureLocation(27841151, 27841161))
# gds_features.add_feature(p12_HIST1H4B, name="p12@HIST1H4L", label=True)

# gdd.draw(format='linear', fragments=1,
#          start=25900000, end=28100000)
# gdd.write("GD_labels_default.png", "png")
# Image("GD_labels_default.png")

```

```python
# DNA FEATURES VIEWER IS NOT YET READY TO USE.

# from bokeh.plotting import figure, show

# from dna_features_viewer import GraphicFeature, GraphicRecord
# features=[
#     GraphicFeature(start=0, end=20, strand=+1, color="#ffd700",
#                    label="Small feature"),
#     GraphicFeature(start=20, end=500, strand=+1, color="#ffcccc",
#                    label="Gene 1 with a very long name"),
#     GraphicFeature(start=400, end=700, strand=-1, color="#cffccc",
#                    label="Gene 2"),
#     GraphicFeature(start=600, end=900, strand=+1, color="#ccccff",
#                    label="Gene 3")
# ]
# record = GraphicRecord(sequence_length=1000, features=features)
# p = record.plot_with_bokeh(figure_width=5)
# show(p)
```

#### Counts

```python
# # DON'T WANT COUNTS

# import pandas as pd
# from myst_nb import glue

# transcript_counts = pd.read_csv('../c06-combining/data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt', delimiter='\t', comment='#', dtype={'entrezgene_id': object})
# transcript_counts.drop([0], axis='index', inplace=True)
# transcript_counts.set_index('00Annotation', inplace=True)

# # In the transcript expression file, genes and proteins ids with multiple values per transcript are separated by a space.
# sep_in_col = ' '

# n_transcripts = transcript_counts.shape[0] # Total number of transcripts in FANTOM5 data set
# glue("total_F5_transcripts", n_transcripts)

# transcript_counts.dropna(axis=0, subset=['uniprot_id'], inplace=True)
# n_transcripts_protein = transcript_counts.shape[0]  # Number of transcripts which are protein-coding (as mapped by FANTOM)
# glue("has_protein_F5_transcripts", n_transcripts_protein)

# # Create expression by protein (uniprot ID), rather than by transcript
# transcript_counts['uniprot_id'] = transcript_counts['uniprot_id'].str.split(sep_in_col)  
# protein_counts = transcript_counts.explode('uniprot_id').groupby(['uniprot_id', 'entrezgene_id', 'hgnc_id']).mean()
# protein_counts.reset_index(level=['hgnc_id', 'entrezgene_id'], inplace=True)

# # Every protein ID should have at least one gene ID
# assert(protein_counts[protein_counts['entrezgene_id'].isna()].shape[0]==0) 
# assert(protein_counts[protein_counts['hgnc_id'].isna()].shape[0]==0)

# print(f"Number of rows that map to multiple genes: {protein_counts[protein_counts.index.duplicated(keep=False)].shape[0]}")
# print(f"Number of proteins that map to multiple genes: {protein_counts[protein_counts.index.duplicated(keep='first')].shape[0]}")

# display(protein_counts[protein_counts.index.duplicated(keep=False)])
# display(protein_counts.loc['A0A024QZ90'])  # example duplicate

# # Ideally, if we're doing a protein centric, thing, then we would like to average over the two protein averages (this should be done AFTER conversion to TPM).
# # Or if we're doing a gene centric thing, then obviously we'd do it gene centric.

# protein_counts['hgnc_id'] = protein_counts['hgnc_id'].str.split(' ')
# protein_counts['entrezgene_id'] = protein_counts['entrezgene_id'].str.split(' ')
# hgnc_counts = protein_counts.explode('hgnc_id')
# entrez_counts = protein_counts.explode('entrezgene_id')
# print('hgnc',len(hgnc_counts['hgnc_id'].unique()))
# print('entrezgene_id',len(entrez_counts['entrezgene_id'].unique()))

# print(f"Rows with multiple hgnc IDs, but only one entrezID: {protein_counts[protein_counts['hgnc_id'].str.contains(' ', na=False) & ~protein_counts['entrezgene_id'].str.contains(' ', na=False)].shape[0]}") # two or more hgncids and only one entrez id

# print(f"Rows with multiple entrez IDs, but only one hgnc ID: {protein_counts[protein_counts['entrezgene_id'].str.contains(' ', na=False) & ~protein_counts['hgnc_id'].str.contains(' ', na=False)].shape[0]}") # two or more entrez ids and only one hgnc id

# print(transcript_counts[transcript_counts['hgnc_id'].str.contains('HGNC:17992',na=False)]['entrezgene_id'].unique())

# print('hgnc',len(protein_counts['hgnc_id'].unique()))
# print('entrezgene_id',len(protein_counts['entrezgene_id'].unique()))
```

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
