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

(ontolopy-mapping-example)=
# Example use: mapping samples to tissue-related phenotypes

This section presents a more sizable example of using Ontolopy, the task it was developed for: mapping from samples to tissue-related phenotypes.
This is a substantial challenge because it requires:
1. Mapping over many different types of ontology terms (`FF`, `UBERON`, `CL`, `GO`).
2. Using more complex relations such as `part_of`.
3. Mapping from text as well as using the mapping from ontology, which then requires combining the two mappings into an overall mapping and investigating any disagreements between mappings.

[//]: # (TODO: Check structure and ref)

This task can be divided into the followig parts, creating the following mappings:
1. Sample (`FF`) to tissue (`UBERON`), including looking at disagreements between mappings.
2. Tissue (`UBERON`) to phenotype (`GO`)
3. Sample (`FF`) to tissue-related phenotype (`GO`).

We are using the same input data as described in {ref}`the previous section<ontolopy-example-inputs>`.

## Creating sample-to-tissue mappings
[//]: # (TODO: Open as ipynb and bring over mapping bits and pieces from c05-filter)

To create the mapping between FANTOM sample ID (`FF:XXXXX-XXXXX`) and tissue (`UBERON:XXXXXX`), we use the `Uberon` class.
We get the mapping by calling the `sample_map_by_ont` function, which calls `Relations`, and excludes too-general tissues such as anatomical structure, tissue, anatomical system, embryo, and multi fate stem cell.
We use a merged sample (FANTOM) and tissue (ontology) as input.

The inclusion of the Cell Ontology is important to retrieve a mapping for as many samples as possible. 
Table {numref}`cl-increases-coverage` shows how the inclusion of CL terms in the input ontology significantly changes the mapping coverage.

[//]: # (TODO: Mention in filip chapter that originally I didn't include via CL in filip, maybe tell the story a bit better here... Like present just with Uberon, then with CL)

```{code-cell} ipython3
%load_ext autoreload
%autoreload 2
```

```{code-cell} ipython3
:tags: [remove-cell]

import ontolopy as opy
import pandas as pd 
from myst_nb import glue
import time

# Read in files:
# -------------
fantom_obo_file = '../c06-combining/data/experiments/fantom/ff-phase2-170801.obo.txt'
fantom_samples_info_file = '../c06-combining/data/experiments/fantom/fantom_humanSamples2.0.csv'
uberon_obo_file = '../c06-combining/data/uberon_ext_210321.obo' 

# Uberon OBO:
uberon_obo = opy.load_obo(
    file_loc=uberon_obo_file, 
    ont_ids=['GO', 'UBERON','CL'], 
)

uberon_obo_tissue_only = opy.load_obo(
    file_loc=uberon_obo_file, 
    ont_ids=['GO', 'UBERON'], 
)

# FANTOM OBO:
fantom_obo = opy.load_obo(
    file_loc=fantom_obo_file, 
    ont_ids=['CL', 'FF', 'GO', 'UBERON', 'DOID'],
)

fantom_obo_no_cl = opy.load_obo(
    file_loc=fantom_obo_file, 
    ont_ids=['FF', 'GO', 'UBERON', 'DOID'],
)

# FANTOM Samples Info file:
samples_info = pd.read_csv(fantom_samples_info_file, index_col=1)
```

```{code-cell} ipython3
# Find mappings:
# -------------

total = len(sample_to_tissue_mapping.index.unique())

def get_num_mapped(mapping):
    sample_to_tissue_mapping.dropna(subset=['to'])
    mapped = len(mapping[~mapping['to'].isna()].index.unique())
    unmapped = len(mapping[mapping['to'].isna()].index.unique())
    return mapped, unmapped

# Uberon tissue only (no CL cells)
start = time.time()
merged_tissue_only = opy.uberon_from_obo(uberon_obo_tissue_only.merge(fantom_obo_no_cl))
sample_to_tissue_mapping_tissue_only = merged_tissue_only.sample_map_by_ont(samples_info.index)
mapped, unmapped = get_num_mapped(sample_to_tissue_mapping_tissue_only)
glue("mapped-uberon-no-cl",f"{mapped} ({100*mapped/float(total):.2f}%)")
glue("unmapped-uberon-no-cl",f"{unmapped} ({100*unmapped/float(total):.2f}%)", False)
glue("time-uberon-no-cl", f"{time.time()-start:.2f} seconds", False)

# Uberon tissue and CL cells
start = time.time()
merged = opy.uberon_from_obo(uberon_obo.merge(fantom_obo))
sample_to_tissue_mapping = merged.sample_map_by_ont(samples_info.index)
mapped, unmapped = get_num_mapped(sample_to_tissue_mapping)
glue("mapped-uberon-cl",f"{mapped} ({100*mapped/float(total):.2f}%)")
glue("unmapped-uberon-cl",f"{unmapped} ({100*unmapped/float(total):.2f}%)", False)
glue("time-uberon-cl", f"{time.time()-start:.2f} seconds", False)
```

```{list-table} Table showing the difference in covereage if including mappings found via CL terms.
:header-rows: 1
:name: cl-increases-coverage

* - Name
  - Number (and percentage) of mapped samples 
  - Number (and percentage) of unmapped samples
  - Run time
* - Using Uberon tissues only
  - {glue:text}`mapped-uberon-no-cl`
  - {glue:text}`unmapped-uberon-no-cl`
  - {glue:text)`time-uberon-no-cl`
* - Using Uberon tissues and CL cells
  - {glue:text}`mapped-uberon-cl`
  - {glue:text}`unmapped-uberon-cl`
  - {glue:text)`time-uberon-cl`
```

[//]: # (TODO: Create mapping and look at the the unmappable things so that I can add in the T-cells)

```{code-cell} ipython3
unmapped = sample_to_tissue_mapping[sample_to_tissue_mapping['to'].isna()].index.unique()
fantom_samples_info.loc[unmapped]
```

```{code-cell} ipython3
category_col = 'Characteristics [Category]'
fantom_samples_info[fantom_samples_info[category_col].isin(['time courses', 'fractionations and perturbations'])]
```

```{code-cell} ipython3
tissue_col = 'Characteristics[Tissue]'
samples_info[tissue_col].unique()
unclassifiables = samples_info[samples_info[tissue_col]=='ANATOMICAL SYSTEM']
for unclassifiable in unclassifiables.index:
    print(merged[unclassifiable]['name'], merged[tissue_relations.loc[unclassifiable]['to']]['name'])
```

```{code-cell} ipython3
desc_col = 'Charateristics [description]'
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

(FANTOM5-inconsistencies-example)=
### Finding inconsistencies 
By comparing the results of both ontology and text based searches, Ontolopy can find inconsistencies between the two representations which sign post to issues with samples data and how it is presented, or in the ontologies that it is linked to (in this case Uberon and CL): I give an example of each type.
I found this approach very useful, as it allowed me to feed back my discoveries to the maintainers of these ontologies and datasets in order to improve them, and has resulted in improvements to several of these resources. 

There were two main ways in which inconsistencies were found:
1. Through looking samples which are not mapped by one method or another.
2. By comparing the mapping that Ontolopy finds using one file and method (text in sample information file), to that it finds using the other (terms in sample ontology file).

[//]: # (TODO: Add a table here of all the inconsistencies: medium priority)
For the FANTOM5 data, disagreements between these mappings revealed problems in the biological ontologies and experiment metadata that were provided to the package in order to create the mappings. 

Disagreements between the tissue-sample mappings created through the (FANTOM and extended Uberon) ontologies and those created using human annotation illuminates what may be a lack of specificity, incompleteness in, or disagreement between FANTOM, CL, or Uberon annotations, either in creating ontologies or annotating tissues to samples. 
The process of mapping FANTOM to Uberon tissues found twenty-two such disagreements, of which FANTOM, Uberon, and CL where appropriate have been informed via GitHub issues, some of which have already sparked changes in the ontologies. 

Four different types of example are described below, to give an idea of how multiple mappings may be used to improve annotation.

### Finding samples that are missing annotations to tissues
[//]: # (TODO: output list of fantom terms to annotate to c+ t-cell)

### Missing Uberon or CL annotation
**Example: `Bronchus part_of some Lung`**

One type of problem that can be revealed is a missing link in an ontology.

An example of this that was found using the FANTOM data set was that there was no formal relationin the Uberon ontology between *Bronchus* and *Lung*, despite the fact that the description text for Bronchus says “the upper conducting airways of the lung”.

This was found because the sample `FF:11511-119G8` (Bronchial Epithelial Cell, donor1) is mapped by name to `UBERON:0002048` Lung, but by ontology to `UBERON:0002185` Bronchus. 
This was flagged as inconsistent because there are no relation in the Uberon ontology between these terms.

Similar missing annotations were discovered between *Aorta* and *Artery*, *Hair follicle* and *Dermal papilla*, and *Skeletal muscle myoblast* and *Skeletal muscle fiber*.

#### Mislabelled sample
**Example: `FF:11590-120G6` should be labelled _Alveolar Epithelial Cells_ not _Renal Glomerular Endothelial Cells_**

Sometimes samples are simply mislabelled.
In this case the mistake was revealed by testing the agreement between annotations because the mistake is only for the name, but not tissue annotation.

[//]: # (TODO: Link to other person who found this on researchgate/wherever)
The FANTOM sample ontology contains two samples named Renal Glomerular Endothelial Cells, donor2: `FF:11590-120G6` and `FF:11594-120H1`. 
One of these is a mislabelled sample, and it is actually an Alveolar Epithelial Cell sample.

#### Imprecise annotation to tissue
[//]: # (TODO: should prefer more precise mapping whichever way around it is? Or not... Need to think.)
There are two types of disagreements that arise from imprecise annotation: those that cause a disagreement between mappings, and those that can be resolved automatically by choosing the more precise term, but still reveal a better possible mapping.

__Example: *Nucleus pulpopus* as *Spinal cord*__
Several FANTOM tissues are labelled by name colloquially, rather than precisely. 
For example, both *Nucleus pulpopus* and *Vertebra* are labelled *Spinal cord* (although the spinal cord itself is considered disjoint from these entities by definition, and in the Uberon ontology).
It’s for this reason that the ontology mapping is preferred over the labelled sample name in creating the overall FANTOM sample-to-tissue mapping.

__Example2: `FF:11423-118G1 is_a` *dermal melanocyte*__
Sometimes the text in the samples information file can help us to reach better mappings in the sample ontology file. 
For example sample `FF:11423-118G1` (and five other similar samples) are mapped to `CL:0000148` (*melanocyte*), which is a cell that can come from many different parts of the body (skin, heart, eyes, etc), so `uberon-py` can only map this tissue to several tissues (some of which this cell will not have come from) if the {ref}`child mapping<child-mapping>` functionality used.
However, since the sample was labelled as coming from the "skin", it's clear that this sample would have been better annotated to `CL:0002482` (*dermal melanocyte*).

+++

(tissue-group-mapping)=
### Re-grouping samples based on tissues
[//]: # (TODO: Update data locations)
Either using existing Uberon mappings, or after mapping to Uberon samples (as in example 1), samples can be grouped by more general Uberon terms representing groups of tissues.

[//]: # (TODO: Make code more usable: relations needs to have some functions for getting mapping, shouldn't be doing weird string stuff)

```{code-cell} ipython3
# FIXME:
import pandas as pd
from uberon_py import obo

tissues=pd.read_csv('data/mappings/tissue_list.csv',names=['UBERON'])
obo = obo.Obo('data/uberonext_obo.txt',['UBERON'])

names = []
name_map = {}
for tissue in tissues['UBERON']:
    name = obo.ont[tissue]['name']
    names.append(name)
    name_map[tissue] = name
tissues['Name'] = pd.Series(names)
tissues.head()
tissues.to_csv('data/mappings/tissues.csv',index=False)

groups = ['brain','cardiovascular system', 'respiratory system','digestive system','skeletal system','skin of body', 'reproductive system','muscle tissue','renal system','central nervous system','connective tissue']
groups_UBERON = []
for group in groups:
    for u_id in obo.ont.keys():
        if obo.ont[u_id]['name'] == group:
            groups_UBERON.append(u_id)
group_name_map = dict(zip(groups_UBERON, groups))

relations = obo.get_relations(['is_a','part_of'],tissues['UBERON'],groups_UBERON,obo.ont).relations
groups = []
for uberon, row in relations.iterrows():
    try:
        group = row[0].split('_')[-1]
    except:
        group = None
    groups.append(group)
relations['Group'] = pd.Series(groups,index=relations.index)
relations['Group name'] = relations['Group'].map(group_name_map)
relations['Name'] = relations.index.map(name_map)
relations=relations.rename(columns={0:'Relation string'})
relations.to_csv('../data/mappings/tissues_groups.csv')
```

## Creating tissue-to-phenotype mappings

## Creating sample-tissue-to-potential-phenotype mappings

[//]: # (TODO: Save out so that I can read in later)

## Harmonisation of gene expression data
[//]: # (TODO: move this to discussion - like to explain that I have tried this on more than one data set)
[//]: # (TODO: Show a snippet of code and output)
[//]: # (TODO: Write to explain the difference between this and the rest, i.e. that it's extra useful to use the SAME specific tissue names)

{numref}`c05.3-data-wrangling` shows an example of how this package can be used to create a sample to tissue mapping for four different gene expression data sets.
