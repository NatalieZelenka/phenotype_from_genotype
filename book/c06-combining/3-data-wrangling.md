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

(c05.3-data-wrangling)=
# Data Wrangling

[//]: # (TODO: Cross-ref to Uberon section)

Before the data sets could be combined, substantial data wrangling was necessary. The details of these processes - obtaining, checking, mapping identifiers, and excluding irrelevant data - are described in this section. 
A Python package (`uberon_py`) was developed and used to do much of this mapping. 
It's functionality is described in {numref}`uberon-py`. 

The steps required to obtain consistently formatted and labelled data can be described as follows:
- Obtaining the raw expression per gene for healthy human tissues
   - Data acquisition
   - (Where required) Mapping from transcript to gene
   - (Where required) Filtering out disease samples
   - (Where required) Filtering out non-human samples
- Mapping from sample name to UBERON tissue using {ref}`uberon-py<uberon-py>`.
- Aggregating metadata

+++

````{admonition} FANTOM5 data pipeline code
:class: dropdown

This code makes use of the [fantom.py helper script](../helper_c05/fantom.py).

```python

# General:
import pandas as pd
import numpy as np
import sys
import time
import os
from uberon_py import obo # my package

# My helper functions:
from helper_c05 import fantom

#load ontologies
fantom_obo_file = 'data/experiments/fantom/ff-phase2-170801.obo.txt'
uberon_obo_file = 'data/uberonext_obo.txt'
fantom_obo_root_terms = ['FF:0000001','EFO:0000001']

fantom_obo = obo.Obo(fantom_obo_file, ['FF','CL','UBERON'], fantom_obo_root_terms)
uberon_obo = obo.Obo(uberon_obo_file, ['UBERON','CL'], fantom_obo_root_terms)

#load and process fantom counts data 
fantom_count_file_loc = 'data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt'
ensg_mapping_loc = 'data/experiments/fantom/biomart_ensg_hgnc.txt'
samples_info_file = 'data/experiments/fantom/fantom_humanSamples2.0.csv'
fantom_counts = fantom.Fantom(fantom_count_file_loc,
                              ensg_mapping_loc, 
                              fantom_obo, 
                              uberon_obo, 
                              samples_info_file)

fantom_counts.gene_expression.to_csv('data/experiments/fantom/fantom_gene_expression.tsv', sep='\t')

pd.DataFrame(fantom_counts.funnel_plot_samples.items(), columns=['Sample Data Stage', 'Number of samples']).to_csv('data/experiments/fantom/funnel_plot_samples.tsv', index=False, sep='\t')

pd.DataFrame(fantom_counts.funnel_plot_transcripts.items(), columns=['Transcript Data Stage', 'Number of transcripts']).to_csv('data/experiments/fantom/funnel_plot_transcripts.tsv', index=False, sep='\t')
```

````

+++

## Obtaining raw expression per gene for healthy human tissues

### Data Acquisition
As mentioned in {ref}`data-aquisition`, for the HPA, GTeX and HDBR experiments, count data were available through the *ExpressionAtlas* R package{cite}`Keays2018-pg`, and the FANTOM dataset was downloaded directly. 

### Mapping from transcript to gene

This step was only required for the FANTOM dataset.

FANTOM provides mappings to gene IDs based on proximity of genes to peaks according to Ensembl. Gene expression was then calculated by summing over transcripts mapped to genes. The transcripts were already mapped to HGNC gene identifiers in the downloaded FANTOM file and [Ensembl’s Biomart](https://www.ensembl.org/biomart) was used to obtain a [mapping from HGNC gene identifiers to ENSG gene identifiers](data/experiments/fantom/data/experiments/fantom/biomart_ensg_hgnc.txt), in order to match the gene expression atlas format. 

Any transcripts which mapped to multiple genes were discarded, as were any HGNC ids which did not map to ENSG ids.

### Filtering out disease samples

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

+++

## Mapping to UBERON

Mapping from samples to Uberon tissue required the development of a small Python package `uberon-py`, which is described in detail in {ref}`the next section<uberon-py>`. To create input to this package, informal tissue names (e.g. blood, kidney) were taken from the experimental design files (or the human sample information file for FANTOM) to create a map of samples to informal tissue names.
For FANTOM, the FANTOM ontology could also be used to create a more fine-grained mapping of samples to tissues based on FANTOM sample identifiers and/or cell type (CL) identifiers.

**HPA**
The HPA samples were mapped using exact matches to Uberon names. 
Three types of sample did not have exact matches: *transformed skin fibroblast*, *suprapubic skin*, and *ebv-transformed lymphocyte*. 
I manually mapped *suprapubic skin* to `UBERON:0001415` *Skin of pelvis*, and excluded the other two (corresponding to excluding 869 samples). 

**HDBR**
For HDBR, tissue names from the “organism part’ column of the column data file were matched to Uberon names and synonyms from the Uberon extended ontology. The 96 unmatched terms corresponding to mixed brain tissues and brain fragments were defaulted to the more general Uberon Brain term. 

**FANTOM**
Since an experimental design file could not be obtained for FANTOM via GxA, additional sample information was obtained via the FANTOM5 website, namely the [human sample information file](https://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/basic/HumanSamples2.0.sdrf.xlsx) and the FANTOM5 ontology.

FANTOM also contains time courses of cell differentiation (cells changing from one type to another) as well measures of perturbed cells. 
Since these samples do not have a well-defined locality in the body given by cell or tissue type, they were not used in the combined dataset. 
Such samples were filtered out using the human sample information file.

Since the FANTOM data had both an ontology file and the human sample information file, both were used to map to Uberon.
The disagreements between the two mappings revealed some inconsistencies with the data set: these are described in {ref}`the next section<FANTOM5-inconsistencies-example>`, as they demonstrate a potential use case for the `uberon-py` package.

```{code-cell} ipython3
:tags: [hide-input]

from plotly import graph_objects as go
from plotly.subplots import make_subplots

# from myst_nb import glue
import textwrap
import pandas as pd

funnel_plot_transcripts = pd.read_csv('data/experiments/fantom/funnel_plot_transcripts.tsv', sep='\t', index_col=0, header=0)
funnel_plot_samples = pd.read_csv('data/experiments/fantom/funnel_plot_samples.tsv', sep='\t', index_col=0, header=0)

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.3)


transcript_y = ["<br>".join(textwrap.wrap(x, 15)) for x in list(funnel_plot_transcripts.index)]
fig.add_trace(
    go.Funnel(name='Transcripts', 
              y=transcript_y,
              x=list(funnel_plot_transcripts['Number of transcripts'])),
    row=1,
    col=1
)

sample_y = ["<br>".join(textwrap.wrap(x, 27)) for x in list(funnel_plot_samples.index)]
fig.add_trace(
    go.Funnel(name='Samples', 
              y=sample_y,
              x=list(funnel_plot_samples['Number'])),
    row=1,
    col=2
)

fig.update_layout(showlegend=False,
                  autosize=False,
                  width=800,
                  height=400,
                  margin=dict(
                      l=50,
                      r=50,
                      b=50,
                      t=50,
                      pad=2
                  )
)

fig.write_image('../images/fantom_funnel.png')
fig.write_html('../images/fantom_funnel.html')

# glue('transcript-funnel', fig, display=False)
```

```{figure} ../images/fantom_funnel.html
:name: "fantom-funnel-interactive"

Funnel plot showing the data cleaning pipeline for FANTOM transcripts/genes (left) and samples (right), along with the number which remained after each stage of data cleaning.
```

The amount of data that flows through the processing pipeline for the FANTOM5 dataset can be seen in {numref}`fantom-funnel-interactive`.

## Aggregating Metadata
To create consistent metadata for the samples (e.g. age, developmental stage, replicate status, etc), information was extracted from multiple sources (including GxA and additional data from each experiment), and sometimes manually curated or corrected. 

**HPA, HBDR, and GTEx:**
Metadata about the experiments was collected from multiple sources, primarily the column data files accessed via ExpressionAtlas. 
This metadata was used to describe the the experimental design for ComBat. 
The metadata collected includes (where available), sample identifier, individual identifier, age (exact), age (range), developmental stage, tissue type (as Uberon term), sex, experiment, biological replicate identifier and technical replicate identifier. 

Both age variables are given in years and may include negative values (e.g. for a developing fetus). 
The age (range) variable contains uneven ranges, since this allows there to be an age-related factor that is compatible across the experiments. 
These values had to be converted to common units, since they were incompatible between experiments, and age-related terms were missing in GxA for GTEx and HPA. 
For GTEx it was possible to acquire this information via [its own website](https://storage.googleapis.com/gtex_analysis_v7/annotations/GTEx_v7_Annotations_SubjectPhenotypesDS.txt).

**FANTOM:**
FANTOM metadata collection was mostly taken from the human sample information file. 
There were discrepancies between ages and developmental stages in the FANTOM human samples file, for example, sample `FF:10027-101D9` is labelled as *thymus, adult, pool1* in the *Description* field, but as *0.5,0.5,0.83 years old infant* in the *Developmental Stage* field, and sample `FF:10209-103G2` has an age of ‘M’ and a sex of ‘28’. 
There were also numerous typographical inconsistencies, for example, “3 year old child”, “3 years old child”, “25 year old”, “76” and “76 years old adult” all feature in the same column, amongst other errors. 
For this reason, creating a cleaned experimental design file was laborious, but the resulting file has been sent to the FANTOM data curators so that they might make it officially available.

FANTOM technical and biological replicates are indicated in the annotated gene expression FANTOM file, by the inclusion of “tech_rep” or “biol_rep” in the long sample labels e.g. `counts.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20tech_rep1.CNhs10855.11227-116C3.hg38.nobarcode`. 
These were used to create the experimental design file. 

Note: there is an error in the original transcript expression file for one of these identifiers (`counts.Dendritic%20Cells%20-%20monocyte%20immature%20derived%2c%20donor1%2c%20rep2.CNhs11062.11227-116C3.hg38.nobarcode`) such that it is missing the “tech” part of the the replicate label. 
This was manually changed in my copy of the input file and the FANTOM data curation team was informed.

```{code-cell} ipython3
:tags: [hide-input]

# CREATE EXP DESIGN FILES: FANTOM
```

````{admonition} Code to harmonise meta-data for GxA data sets
:class: dropdown

```python

# CREAT EXP DESIGN FILES: GXA
import pandas as pd
import numpy as np
from uberon_py import obo 
from helper_c05 import clean
from myst_nb import glue

uberon_obo_file = 'data/uberonext_obo.txt'
uberon_obo = obo.Obo(uberon_obo_file,['UBERON','CL'])

#HPA E-MTAB-2836
col_data_hpa_file = 'data/experiments/hpa/E-MTAB-2836_colData.tsv'
col_data_hpa = pd.read_csv(col_data_hpa_file,delimiter='\t', quotechar ='"')
col_data_hpa[col_data_hpa=='  '] = None  # make empty elements None

tissue_map_hpa = uberon_obo.map_tissue_name_to_uberon(col_data_hpa, 'organism_part')
assert(len(tissue_map_hpa[tissue_map_hpa.UBERON.isna()]['name matched on'].unique()) == 0)

# Make HPA experimental file:
lines = []
for index, row in col_data_hpa.iterrows():
    lines.append([
        index,
        'HPA',
        np.nan, #HPA doesn't have individual IDs
        np.nan, #HPA doesn't have individual age
        np.nan, #HPA doesn't have age ranges
        row['developmental_stage'],
        clean.clean_sex(row['sex']),
        clean.clean_tissue(tissue_map_hpa.loc[index,'UBERON']),
        'tissues - donor',
        clean.clean_techrep(row['technical_replicate_group'],'HPA'),
        np.nan, #HPA doesn't have Bio Reps or individual, so can't even try to calc
    ])
hpa_experimental_design = pd.DataFrame(lines,columns = experimental_design_columns)
hpa_experimental_design.set_index('Sample ID',inplace=True)
hpa_experimental_design.to_csv('data/experiments/hpa/hpa_experimental_design.csv')

# GTEx
col_data_gtex_file = 'data/experiments/gtex/E-MTAB-5214_colData.tsv'
col_data_gtex = pd.read_csv(col_data_gtex_file,delimiter=',', quotechar ='"')
col_data_gtex = col_data_gtex.rename(columns = {'Unnamed: 0':'Sample ID'})
col_data_gtex.set_index('Sample ID',inplace=True)

col_data_gtex[col_data_gtex=='  '] = None  #make empty elements None
assert(set(col_data_gtex.disease.unique()) == set(['normal']))
assert(set(col_data_gtex.clinical_information.unique()) == set([None,'not sun exposed', 'sun exposed']))

tissue_map_gtex = uberon_obo.map_tissue_name_to_uberon(col_data_gtex,'organism_part')
#Manually map the GTEx names that don't automatically map
manual_mapping_gtex = {
    'transformed skin fibroblast': None, #Alternative: ? 'UBERON:0002097',#skin of body
    'ebv-transformed lymphocyte': None,  #Alternative: ? 'UBERON:0000178', #blood
    'suprapubic skin': 'UBERON:0001415', #Alternative: ? 'UBERON:0002097',#skin of body
}

for index, row in tissue_map_gtex.iterrows():
    if row['UBERON'] == None:
        uberon_term = manual_mapping_gtex[row['name matched on']]
        tissue_map_gtex.loc[index,'UBERON'] = uberon_term
        
num_excluded_samples = tissue_map_gtex[tissue_map_gtex.UBERON.isna()].shape[0]  # excluded because transformed cell 
glue("Number of excluded GTEx samples", num_excluded_samples)
samples_to_exclude = list(tissue_map_gtex[tissue_map_gtex.UBERON.isna()].index)

#Use additional file to add age information
gtex_additional_info = pd.read_csv('data/experiments/gtex/GTEx_v7_Annotations_SubjectPhenotypesDS.txt',sep='\t')
gtex_additional_info = gtex_additional_info.rename(columns={'SUBJID':'individual','AGE':'age_range'})

col_data_gtex = col_data_gtex.merge(gtex_additional_info[['age_range','individual']],on='individual',how="left").set_index(col_data_gtex.index)

# Make gtex experimental file:
lines = []
for index, row in col_data_gtex.iterrows():
    lines.append([
        index,
        'GTEx',
        row['individual'],
        np.nan,#GTEx doesn't have individual age
        row['age_range'],
        'adult',
        clean_sex(row['sex']),
        clean_tissue(tissue_map_gtex.loc[index,'UBERON']),
        'tissues - donor',
        clean_techrep(row['technical_replicate_group'],'GTEx'),
        np.nan, #TODO: Try to calculate bio reps based on same individual + tissue, but different tech rep?
    ])
gtex_experimental_design = pd.DataFrame(lines,columns = experimental_design_columns)
gtex_experimental_design.set_index('Sample ID',inplace=True)
gtex_experimental_design.to_csv('data/experiments/gtex/gtex_experimental_design.csv')

# HDBR
col_data_hdbr_file = 'data/experiments/hdbr/E-MTAB-4840_colData.tsv'
col_data_hdbr = pd.read_csv(col_data_hdbr_file, delimiter='\t')

# tissue mapping:
tissue_map_hdbr = uberon_obo.map_tissue_name_to_uberon(col_data_hdbr,'organism_part')
for index in tissue_map_hdbr[tissue_map_hdbr.UBERON.isna()]['name matched on'].index:
    tissue_map_hdbr.loc[index,'UBERON'] = 'UBERON:0000955' # Brain
assert(tissue_map_hdbr[tissue_map_hdbr.UBERON.isna()].shape[0]==0)

# clean age and sex metadata:
col_data_hdbr['age'] = col_data_hdbr['developmental_stage'].map(clean.MapHDBR.age)
col_data_hdbr['sex'] = col_data_hdbr['karyotype'].map(clean.MapHDBR.sex)

# Make experimental file:
lines = []
for index, row in col_data_hdbr.iterrows():
    lines.append([
        index,
        'HDBR',
        'HDBR-'+str(row['individual']),
        row['age'],
        np.nan,#HDBR doesn't have age ranges
        'fetus',
        row['sex'],
        clean_tissue(tissue_map_hdbr.loc[index,'UBERON']),
        'tissues - donor',
        np.nan, # TODO:? Calculate based on "block"
        np.nan, # TODO:? Define from individual and tissue IDs different "block"
    ])
hdbr_experimental_design = pd.DataFrame(lines,columns = experimental_design_columns)
hdbr_experimental_design.set_index('Sample ID',inplace=True)
hdbr_experimental_design.to_csv('data/experiments/hdbr/hdbr_experimental_design.csv')
```

````

+++

```{admonition} Code: combine experimental design
:class: dropdown

```python
import pandas as pd
from myst_nb import glue

# read in experimental design files:
hdbr_experimental_design=pd.read_csv(
    'data/experiments/hdbr/hdbr_experimental_design.csv', 
    index_col='Sample ID')
fantom_experimental_design=pd.read_csv(
    'data/experiments/fantom/fantom_experimental_design.csv', 
    index_col='Sample ID')
hpa_experimental_design=pd.read_csv(
    'data/experiments/hpa/hpa_experimental_design.csv', 
    index_col='Sample ID')
gtex_experimental_design=pd.read_csv(
    'data/experiments/gtex/gtex_experimental_design.csv', 
    index_col='Sample ID')

# combine:
combined_design =  pd.concat([hdbr_experimental_design, fantom_experimental_design, hpa_experimental_design, gtex_experimental_design])

# drop non-tissue-specific:
combined_design.dropna(subset =['Tissue (UBERON)'], inplace=True)
assert(combined_design[combined_design['Tissue (UBERON)'].isna()].shape[0] == 0)

# save
combined_design.to_csv('data/combined/combined_experimental_design.csv')
```

````

```{code-cell} ipython3
:tags: [hide-input]

# # load combined_design + add tissue groups info and save/print.

# # glue
# glue('number of samples in combined data set', combined_design.shape[0])
# glue('number of Uberon tissue types in combined data set', combined_design['Tissue (UBERON)'].unique().shape[0])
# glue('number of individuals in combined data set', combined_design['Individual ID'].unique().shape[0]-1)

# print('sex breakdown (of samples):\n',combined_design['Sex'].value_counts())
# print('sample type breakdown:\n',combined_design['Sample Type'].value_counts())
# print('experiment breakdown:\n',combined_design['Experiment'].value_counts())
```

### Tissue groups
While the data is in general mapped to the most specific Uberon terms possible, eleven broader tissue groups (for example brain, digestive system, connective tissue) were identified by hand.
Individual tissues were mapped to these groups using `uberon-py`'s `Relations()` function - the code doing this is shown in the {ref}`the second example of uberon-py usage<tissue-group-mapping>` in the next section.

```{code-cell} ipython3
# Code that adds tissue groups to the combined-design file
```
