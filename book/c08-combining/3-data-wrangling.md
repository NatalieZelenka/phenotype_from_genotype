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

Before the data sets could be combined, substantial data wrangling was necessary. 
The details of these processes - obtaining, checking, mapping identifiers, and excluding irrelevant data - are described in this section. 
Ontolopy was developed and used to do much of this mapping, and parts of the wrangling mentioned here form examples in the {ref}`Ontolopy chapter<c06-ontolopy>`.

The steps required to obtain consistently formatted and labelled data can be described as follows:
- Obtaining the raw expression per gene for healthy human tissues
   - Data acquisition
   - (Where required) Mapping from transcript to gene
   - (Where required) Filtering out disease samples
   - (Where required) Filtering out non-human samples
- Mapping from sample name to UBERON tissue using {ref}`Ontolopy<c06-ontolopy>`.
- Mapping from UBERON tissues to tissue groups using Ontolopy.
- Aggregating metadata

+++

(rawgeneexpression)=
## Obtaining raw expression per gene for healthy human tissues

As mentioned in {ref}`data-acquisition`, for the HPA, GTeX and HDBR experiments, count data were available through the *ExpressionAtlas* R package{cite}`Keays2018-pg`, and the FANTOM dataset was downloaded directly. 

(transcriptgenemapping)=
### Mapping from transcript to gene

This step was only required for the FANTOM dataset.

FANTOM provides mappings to gene IDs based on proximity of genes to peaks according to Ensembl. Gene expression was then calculated by summing over transcripts mapped to genes. The transcripts were already mapped to HGNC gene identifiers in the downloaded FANTOM file and [Ensembl’s Biomart](https://www.ensembl.org/biomart) was used to obtain a {download}`mapping from HGNC gene identifiers to ENSG gene identifiers<./data/experiments/fantom/data/experiments/fantom/biomart_ensg_hgnc.txt>`, in order to match the gene expression atlas format. 

Any transcripts which mapped to multiple genes were discarded, as were any HGNC ids which did not map to ENSG ids.

(filteroutdisease)=
### Filtering out disease samples

The HDBR and HPA experiments contained only healthy samples.

**GTEx**
Although GTEx contained clinical data, no disease-related phenotypes were removed from the data set, since the `disease` column contains only values of “normal” and the only clinical variables (as described in the `clinical_variables` column) in the dataset were sun exposure or lack thereof for skin tissues. 
I judged these to be within the normal range of environments that we would expect skin to be subjected to.

**FANTOM**
The FANTOM sample ontology was used to remove samples which are models for diseases. Samples which are disease models are identified using the `is_model_for` relationship and these relationships are propagated to the children terms based on the `is_a` relationship. For example, `FF:11558-120D1` (Fibroblast - skin spinal muscular atrophy, donor2) would be removed from the set of samples, since:
`FF:11558-120D1` (Fibroblast - skin spinal muscular atrophy, donor2) `is_a FF:0000251` (human fibroblast - skin spinal muscular atrophy sample) `is_model_for DOID:12377` (spinal muscular atrophy).

**1D\. Filtering out non-human samples**
The GTEx, HDBR, and HPA experiments contained only human samples. 

**FANTOM**
The FANTOM5 data set also contains non-human (mouse) samples. 
The FANTOM sample ontology (which was downloaded [from here](http://fantom.gsc.riken.jp/5/datafiles/latest/extra/Ontology/ff-phase2-170801.obo.txt)) was used to look-up which FANTOM samples are human samples, i.e. have an `is_a` relationship to the term `FF:0000210` (human sample) directly or indirectly.

+++

(combininguberonmapping)=
## Mapping to UBERON

Mapping from samples to Uberon tissue required the development of a small Python package {ref}`Ontolopy<c06-ontolopy>`. 
To create input to this package, informal tissue names (e.g. blood, kidney) were taken from the experimental design files (or the human sample information file for FANTOM) to create a map of samples to informal tissue names.
For FANTOM, the FANTOM ontology could also be used to create a more fine-grained mapping of samples to tissues based on FANTOM sample identifiers and/or cell type (CL) identifiers.

**HPA**
The HPA samples were mapped using exact matches to Uberon names. 
Three types of sample did not have exact matches: *transformed skin fibroblast*, *suprapubic skin*, and *ebv-transformed lymphocyte*. 
I manually mapped *suprapubic skin* to `UBERON:0001415` *Skin of pelvis*, and excluded the other two (corresponding to excluding 869 samples). 

**HDBR**
For HDBR, tissue names from the “organism part’ column of the column data file were matched to Uberon names and synonyms from the Uberon extended ontology. 
The 96 unmatched terms corresponding to mixed brain tissues and brain fragments were defaulted to the more general Uberon Brain term. 

**FANTOM**
Since an experimental design file could not be obtained for FANTOM via GxA, additional sample information was obtained via the FANTOM5 website, namely the [human sample information file](https://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/basic/HumanSamples2.0.sdrf.xlsx) and the FANTOM5 ontology.

FANTOM also contains time courses of cell differentiation (cells changing from one type to another) as well measures of perturbed cells. 
Since these samples do not have a well-defined locality in the body given by cell or tissue type, they were not used in the combined dataset. 
Such samples were filtered out using the human sample information file.

Since the FANTOM data had both an ontology file and the human sample information file, both were used to map to Uberon.
The disagreements between the two mappings revealed some inconsistencies with the data set: these are described in {ref}`the next section<FANTOM5-inconsistencies-example>`, as they demonstrate a potential use case for Ontolopy.

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

# fig.write_image('../images/fantom_funnel.png')
# fig.write_html('../images/fantom_funnel.html')
fig.show()
# glue('transcript-funnel', fig, display=False)
```

```{figure} ../images/blank.png
:name: "fantom-funnel-interactive"

Funnel plot showing the data cleaning pipeline for FANTOM transcripts/genes (left) and samples (right), along with the number which remained after each stage of data cleaning.
```

The amount of data that flows through the processing pipeline for the FANTOM5 dataset can be seen in {numref}`fantom-funnel-interactive`.

(aggregatingmetadata)=
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
The metadata aggregation for the FANTOM dataset is described in detail in {numref}`ontolopy-mapping-example`.

+++

(tissue-groups)=
### Tissue groups
While the data is in general mapped to the most specific Uberon terms possible, 10 broader tissue groups (e.g. "brain", "connective tissue") were identified by hand and the individual samples were mapped to these groups using Ontolopy's `Relations()` function.
This level of specificity is useful for comparing between experiments, since many experiments describe some tissues more specifically than others.
For example, there are many FANTOM5 tissues labelled "brain", but many HDBR experiments are labelled as more specific parts of the brain.

+++

(experimental-design)=
## Final Experimental Design

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import pandas as pd 
from myst_nb import glue

design_file = 'data/design.csv'
design = pd.read_csv(design_file, sep=',' ,index_col=0,
                     usecols=['Sample ID','Experiment','Tissue (UBERON)'])

tissue_groups_df = pd.read_csv('data/tissues_groups.csv', index_col=0)

design['Group name'] = design['Tissue (UBERON)'].map(tissue_groups_df['Group name'])

tissue_groups = list(design['Group name'].dropna().unique())
mod = pd.DataFrame(index = design.index)
for tissue_group in tissue_groups:
    # Note: zeros correspond to a normal fold change of 1 (as mod contains logfold changes)
    mod[tissue_group] = (design['Group name']==tissue_group).astype('int')

overall_design = mod.copy()
overall_design['Experiment'] = design['Experiment']
overall_design = overall_design.groupby('Experiment').sum()
overall_design['Samples per experiment'] = overall_design.sum(axis=1)
overall_design.loc['Total'] = overall_design.sum(axis=0)

percentage = overall_design.sum(axis=0)/float(overall_design.loc['Total', 'Samples per experiment'])
tissue_groups_to_discard = percentage.index[percentage<0.01]
overall_design.drop(columns=tissue_groups_to_discard, inplace=True)
mod.drop(columns=tissue_groups_to_discard, inplace=True)
tissue_groups.remove(tissue_groups_to_discard)

glue('design-balance', overall_design)
glue('mod-head', mod.head())

mod.to_csv('data/simulated/group_mod.csv')
```

```{glue:figure} design-balance
:name: design-balance-tbl

A table showing the number of samples in each category, by tissue group and experiment. Note that the design is not balanced: there are some categories that do not overlap at all. 
```

{ref}`design-balance-tbl` shows the experimental design of the combined data set. 
Since it is not balanced, it is not likely to be suitable for batch-correction algorithms such as ComBat or ComBat-Seq.
