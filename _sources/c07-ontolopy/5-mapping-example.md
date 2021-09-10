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

<!-- TODO: Give `sample_to_tissue_mapping` and `mapped_by_tissue_name` more similar names -->
<!-- TODO: Check that I've put propagate up and down the right way around -->

This section presents a more sizable example of using Ontolopy, the task it was developed for: mapping from samples to tissue-related phenotypes.
This is a substantial challenge, in part because it requires:
1. Mapping over many different types of ontology terms (`FF`, `UBERON`, `CL`, `GO`).
2. Using more {ref}`complex<has-part-part-of>` relations such as `part_of`.
3. Mapping from text as well as using the mapping from ontology, which then requires combining the two mappings into an overall mapping and investigating any disagreements between mappings.

This task can be generally divided into the following parts:
1. Creating sample (`FF`) to tissue (`UBERON`) {ref}`mapping<1-sample-to-tissue>`, including looking at {ref}`disagreements<FANTOM5-inconsistencies-example>` between mappings.
2. Tissue (`UBERON`) to phenotype (`GO` Biological Process - GOBP) {ref}`mapping<2-tissue-to-phenotype>`.
3. Combining the above, to create the final sample (`FF`) to tissue-related phenotype (`GO`) {ref}`mapping<3-sample-tissue>`.

We are using the same input data as described in {ref}`the previous section<ontolopy-example-inputs>` for this example.

(1-sample-to-tissue)=
## Creating sample-to-tissue mappings

To create the mapping between FANTOM sample ID (`FF:XXXXX-XXXXX`) and tissue (`UBERON:XXXXXX`), we use the `Uberon` class.
The `Uberon` class has three useful functions for creating this mapping:
1. `sample_map_by_ont`: creates a mapping via ontology.
2. `sample_map_by_name`: creates a mapping via sample or tissue names.
3. `get_overall_tissue_mappings`: combines the two mappings to create a more comprehensive overall mapping.

(map-load-prefilter)=
### Load data and pre-filter
In order to do this, I load the input FANTOM5 ontology and sample information files.
These are the same files that I explained {ref}`in the previous section<ontolopy-example-inputs>`.

```{code-cell} ipython3
:tags: [remove-cell]

%load_ext autoreload
%autoreload 2
```

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import ontolopy as opy
import pandas as pd 
from myst_nb import glue
import time
import numpy as np
import logging
import plotly.graph_objects as go_
from plotly.subplots import make_subplots

notebook_start = time.time()

# Read in files:
# -------------
fantom_obo_file = '../c08-combining/data/experiments/fantom/ff-phase2-170801.obo.txt'
fantom_samples_info_file = '../c08-combining/data/experiments/fantom/fantom_humanSamples2.0.csv'
uberon_obo_file = '../c08-combining/data/uberon_ext_210321.obo' 

# Uberon OBO:
uberon_obo = opy.load_obo(
    file_loc=uberon_obo_file, 
    ont_ids=['GO', 'UBERON','CL','FMA'], 
)

uberon_obo_tissue_only = opy.load_obo(
    file_loc=uberon_obo_file, 
    ont_ids=['GO', 'UBERON','FMA'], 
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

(bigexamplemapbyont)=
### Mapping by ontology
The `sample_map_by_ont` function is a wrapper function which calls `relations.Relations`, and excludes too-general Uberon tissues such as anatomical structure, tissue, anatomical system, embryo, and multi fate stem cell.
We use a merged sample (FANTOM) and tissue (Uberon) ontology as input.

The inclusion of the Cell Ontology (which is included in the Uberon OBO file) is important to retrieve a mapping for as many samples as possible. 
{numref}`cl-increases-coverage` shows how the inclusion of CL terms in the input ontology significantly changes the mapping coverage.

[//]: # (TODO: Mention in filip chapter that originally I didn't include via CL in filip, maybe tell the story a bit better here... Like present just with Uberon, then with CL)

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Find mappings:
# -------------

total = len(samples_info.index.unique())

def get_mapped(mapping):
    mapped = mapping[~mapping['to'].isna()]
    unmapped = mapping[mapping['to'].isna()]
    return mapped, unmapped

# Uberon tissue only (no CL cells)
start = time.time()
merged_tissue_only = opy.uberon_from_obo(uberon_obo_tissue_only.merge(fantom_obo_no_cl))
sample_to_tissue_mapping_tissue_only = merged_tissue_only.sample_map_by_ont(samples_info.index)
mapped_nocl, unmapped_nocl = get_mapped(sample_to_tissue_mapping_tissue_only)
glue("mapped-uberon-no-cl",f"{len(mapped_nocl)} ({100*len(mapped_nocl)/float(total):.2f}%)", False)
glue("unmapped-uberon-no-cl",f"{len(unmapped_nocl)} ({100*len(unmapped_nocl)/float(total):.2f}%)", False)
glue("time-uberon-no-cl", f"{time.time()-start:.2f} seconds", False)

# Uberon tissue and CL cells 
start = time.time()
merged = opy.uberon_from_obo(uberon_obo.merge(fantom_obo))
sample_to_tissue_mapping = merged.sample_map_by_ont(samples_info.index)
mapped_cl, unmapped_cl = get_mapped(sample_to_tissue_mapping)
glue("mapped-uberon-cl",f"{len(mapped_cl.index.unique())} ({100*len(mapped_cl.index.unique())/float(total):.2f}%)", False)
glue("unmapped-uberon-cl",f"{len(unmapped_cl.index.unique())} ({100*len(unmapped_cl.index.unique())/float(total):.2f}%)", False)
glue("time-uberon-cl", f"{time.time()-start:.2f} seconds", False)
```

```{list-table} Table comparing the difference in coverage (mappable samples) for different mapping techniques.
:header-rows: 1
:name: cl-increases-coverage

* - Mapping name
  - Number (and percentage) of all mapped samples 
  - Number (and percentage) of all unmapped samples
  - Run time
* - By ontology: using Uberon tissues only
  - {glue:text}`mapped-uberon-no-cl`
  - {glue:text}`unmapped-uberon-no-cl`
  - {glue:text}`time-uberon-no-cl`
* - By ontology: using Uberon tissues and CL cells
  - {glue:text}`mapped-uberon-cl`
  - {glue:text}`unmapped-uberon-cl`
  - {glue:text}`time-uberon-cl`
* - By name: using tissue column
  - {glue:text}`mapped-name`
  - {glue:text}`unmapped-name`
  - {glue:text}`time-name`
* - Combined: combining by name and by ontology including CL
  - {glue:text}`mapped-overall`
  - {glue:text}`unmapped-overall`
  - **N/A**
```

{numref}`cl-increases-coverage` also shows that mapping via ontology alone (with CL terms used), has a fairly good coverage.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Show some examples of things that aren't matched that should be (not mappable by ontology alone), e.g. caudate nucleus
tissue_col = 'Characteristics[Tissue]'

expect_to_map = samples_info[samples_info.index.isin(unmapped_cl.index) & ( (~samples_info[tissue_col].isna()) & ~samples_info[tissue_col].isin(['ANATOMICAL SYSTEM', 'UNDEFINED_TISSUE_TYPE', 'unclassifiable']))]
not_expect_map = samples_info[samples_info.index.isin(unmapped_cl.index) & (samples_info[tissue_col].isna() | samples_info[tissue_col].isin(['ANATOMICAL SYSTEM', 'UNDEFINED_TISSUE_TYPE', 'unclassifiable']))]

glue("not_expect_map", len(not_expect_map), False)
glue("expect_map", len(expect_to_map), False)
glue("num_expect_map_tissues", len(expect_to_map[tissue_col].unique()), False)

def list_to_text(lst):
    text = ', '.join(lst)
    return text[:text.rindex(', ') + 1] + ' and' + text[text.rindex(', ')+1:]

glue("tissues_list", list_to_text(expect_to_map[tissue_col].unique()))

chosen_examples = ['FF:10379-105H1',  # caudate nucleus
                   'FF:10422-106C8',  # blood (lymphoma)
                   'FF:10558-107I9', # osteoblast
                   'FF:11794-124C3', # t-cell
                  ]
cell_col = 'Characteristics [Cell type]'
desc_col = 'Charateristics [description]'
expect_to_map_table = expect_to_map.loc[chosen_examples][[desc_col, tissue_col, cell_col]]
glue("expect-to-map-table", expect_to_map_table, False)
```

(expect-to-map)=
The unmapped samples do contain some samples that we wouldn't expect to be able to map to tissue (defined as those that do not have a tissue provided in the samples information file, or that are labelled as `unclassifiable`, `UNDEFINED_TISSUE_TYPE`, or `ANATOMICAL SYSTEM`): these account for {glue:text}`not_expect_map` of the {glue:text}`unmapped-uberon-cl` unmapped samples.
This, however, leaves {glue:text}`expect_map` samples which we would expect to map, spread across {glue:text}`num_expect_map_tissues` tissues ({glue:text}`tissues_list`).

```{glue:figure} expect-to-map-table
:figwidth: 800px
:name: expect-to-map-examples

Four FANTOM5 samples that we would expect to be able to map using Ontolopy based on the information in the samples information file (selected columns shown here), but that do not map using Ontolopy with the FANTOM5 ontology.
```

{numref}`expect-to-map-examples` show four examples of such samples.
The existence of such tissues, means that mapping via name as well as by ontology could prove useful.

+++

(bigexamplemapbyname)=
### Mapping by name

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# map by name
uberon_obo_tissue_only = opy.uberon_from_obo(uberon_obo_tissue_only)

start = time.time()
mapped_by_tissue_name = uberon_obo_tissue_only.sample_map_by_name(samples_info[tissue_col], xref='FMA')
mapped_name, unmapped_name = get_mapped(mapped_by_tissue_name)

glue("time-name", f"{time.time()-start:.2f} seconds", False)
glue("mapped-name", f"{len(mapped_name.index.unique())} ({100*len(mapped_name.index.unique())/float(total):.2f}%)", False)
glue("unmapped-name", f"{len(unmapped_name.index.unique())} ({100*len(unmapped_name.index.unique())/float(total):.2f}%)", False)
```

The `Uberon.sample_map_by_name` function simply looks up the strings provided (in this case those from the `Characteristics[Tissue]` column of the sample information file) and checks if any Uberon terms in the provided ontology has a matching name or synonym. 
The term name is preferred over synonyms, and where there are no exactly matching term names, but there are multiple possible synonyms (e.g. *bladder* is a synonym for *urinary bladder* and *bladder organ*), we decide by whether either of the terms are linked to the Foundational Model of Anatomy (FMA) ontology, as this is a human-specific ontology by using the `xref='FMA'` option.
Since we are only looking for Uberon terms, it doesn't make any difference whether we use the "tissue only" or "including CL" versions of the Uberon ontology that we read in earlier, aside from a negligible difference in run time).

```{code-cell} ipython3
:tags: [remove-input, remove-output]

# Create and glue table showing examples of mappings
imprecise = samples_info.loc[mapped_name.index.intersection(mapped_cl.index)][[desc_col, tissue_col]]
imprecise.index.rename("FF ID", inplace=True)
imprecise['Mapped by ontology'] = [merged[x]['name'] for x in mapped_cl.loc[imprecise.index]['to']]
imprecise['Mapped by name'] = [merged[x]['name'] for x in mapped_name.loc[imprecise.index]['to']]
imprecise = imprecise[imprecise['Mapped by name'] != imprecise['Mapped by ontology']]
illustrative_samples = ['FF:10040-101F4',  # frontal cortex more precise than frontal lobe
                        'FF:10055-101H1',  # embryonic uterus more precise than uterus 
                        'FF:10075-102A3',  # lower lobe of right lung more precise than lung
]

examples_rows = imprecise[imprecise['Mapped by ontology']!=imprecise['Mapped by name']].loc[illustrative_samples]
glue("example-imprecise-table", examples_rows, False)
```

```{glue:figure} example-imprecise-table
:name: example-imprecise
:figwidth: 800px

Comparisons of sample mappings by ontology (inlcluding CL) and by name (by tissue column of samples information file), illustrating the tendency of by-name mappings to be less precise.
```

As {numref}`cl-increases-coverage` shows, mapping by name function is quite slow, taking {glue:text}`time-name`. 
The mappings coverage is {glue:text}`mapped-name`.

This measure doesn't show that the mapping is constrained to be less precise than the mapping via ontology - of course this is particular to the data as it depends on how the tissues were labelled. 
In this case, FANTOM5 labelled the tissues fairly broadly, so we see examples like `FF:10075-102A3` (*lung, right lower lobe*) and `FF:14331-155F2` (*Fibroblast - Aortic Adventitial*) in {numref}`example-imprecise` - this is particularly common when the samples are cell types.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Examples of things that would be unmappable by text alone "Anatomical system"
tissue_col = 'Characteristics[Tissue]'

anatomical_system = samples_info.loc[samples_info[samples_info[tissue_col]=='ANATOMICAL SYSTEM'].index.intersection(mapped_cl.index)][[desc_col, tissue_col]]

anatomical_system['Mapped by ontology'] = [merged[x]['name'] for x in mapped_cl.loc[anatomical_system.index]['to']]
anatomical_system['Mapped by name'] = [merged[x]['name'] for x in mapped_by_tissue_name.loc[anatomical_system.index]['to']]

illustrative_samples = ['FF:11966-126D4', 
                        'FF:11941-126A6', 
                        'FF:11937-126A2', 
                        'FF:11936-126A1', 
                        'FF:11930-125I4', 
                        'FF:11927-125I1']

examples_rows = anatomical_system.loc[illustrative_samples]
glue("anatomical-system-examples-table", examples_rows, False)
```

In addition, there are samples that are not usefully mapped at all (or completely missing a mapping) using the by-name approach, that we can get by-ontology.
One subset of these is the tissues which are labelled "ANATOMICAL SYSTEM": these map to the Uberon term *anatomical system*, but this is too general to be useful.
{numref}`anatomical-system` shows how these terms can be mapped to more localised terms 

This also shows the one limitation of mapping by ontology, in that we might expect that samples such as `FF:11936-126A1` to be mapped to the more specific (and useful) `UBERON:0001997` *olfactory epithelium*. 
This is not the case since there is a "missing" annotation between `CL:0002167` *olfactory epithelial cell* and *olfactory epithelium*, since the definition of olfactory epithelial cell is [still under discussion and development](https://github.com/obophenotype/cell-ontology/issues/167).

```{glue:figure} anatomical-system-examples-table
:figwidth: 800px
:name: anatomical-system

An example of *ANATOMICAL SYSTEM* tissue samples, with tissue-specific cells, which are unmapped by-name, but have useful by-ontology mappings.
```

[//]: # (TODO: Mention in discussion that it would be easier to build in preference per tissue type)
(immune-system-mappings)=
There are also some benefits to the name based mapping.
A quirk of the ontology-based mapping is that many cell types are identified as having being part of the *immune system*, however, this isn't a well-defined locality.
It's possible for samples from different physical locations (e.g. liver, blood) to map to the *immune system* term. 
For the FANTOM5 data at least, the names better describe locations that these samples came from.

+++

(bigexamplecombiningmappings)=
### Combining mappings

To get the best of both mappings, we need to combine them using the `Uberon.get_overall_tissue_mappings` function.
This function creates both an overall mapping and a list of disagreements.
Where only one mapping covers a term, it is trivial to do this (the overall mapping uses the present mapping, and there are no disagreements).
When both mappings are present and one term is an ancestor of another, we say there is no disagreement and choose the more specific mapping e.g. if mapping by ontology gives us *photoreceptor array*, but mapping by name gives us *eye*, then because *photoreceptor array* is `part_of` *eye* and *eye* `is_a` *sense organ*, we would use the overall mapping by ontology since *photoreceptor array* is the more specific term.
When both mappings are present and there is no relationship between them, this is when we say there is a disagreement, and we can choose which mapping we give precedence to, by default it is the ontology mapping.

Before we create the overall mapping, we will remove the *immune system* by-ontology mappings, for the reasons {ref}`discussed above<immune-system-mappings>`.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Remove immune system mappings
immune_system = 'UBERON:0002405'
for ff in sample_to_tissue_mapping[(sample_to_tissue_mapping['to'] == immune_system) & sample_to_tissue_mapping.index.isin(mapped_by_tissue_name[~mapped_by_tissue_name['to'].isna()].index)].index:
    sample_to_tissue_mapping.loc[ff] = [np.nan, np.nan, np.nan]

# Combine mappings
overall, disagreements = merged.get_overall_tissue_mappings(
    map_by_ont=sample_to_tissue_mapping, 
    map_by_name=mapped_by_tissue_name,
    rel = ['is_a', 'part_of', 'continuous_with', 'has_potential_to_develop_into', 'develops_into']
)

unmapped_overall = overall[overall['mapped_by'].isna()]
mapped_overall = overall[~overall['mapped_by'].isna()]
glue('overall-unique-tissues', len(overall['overall'].unique()), False)

# Add overall to table
def format_mapped(mapped, total):
    return f"{len(mapped)} ({100*len(mapped)/float(total):.2f}%)"

glue("mapped-overall", format_mapped(mapped_overall, total), False)
glue("unmapped-overall", format_mapped(unmapped_overall, total), False)
```

(primary-cell-tissues-ontolopy)=
{ref}`The FANTOM5 data contains different categories of samples<primary-cell-tissue>` including tissues, time courses, immortal cell lines, fractionations and purturbations and primary cells. 
Some of these categories might not map in the way that we might want them to because although they might be a cell type that is usually localised to a tissue, they are unusual since they represent unusual in-between developing tissues (e.g. stem cells) or cancerous immortal cell lines.
This is likely to have led to uncertainties in the sample ontology file, so by restricting to primary cell and tissue samples, we might get a more accurate picture of the percentage of mappabble samples that Ontolopy can reach.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Glue all values for the primary cell and tissues version of the table `coverage-tissue-primary-cell`
def primary_and_tissues(mapped, unmapped, samples_info, name_string):
    """Removes non primary cell and tissue samples from the `mapped` and `unmapped` samples."""
    category_col = 'Characteristics [Category]'
    categories = ['primary cells', 'tissues']
        
    category_samples = samples_info[samples_info[category_col].isin(categories)].index
    total = len(category_samples)
    
    new_mapped = mapped[mapped.index.isin(category_samples)]
    new_unmapped = unmapped[unmapped.index.isin(category_samples)]
    
    glue(f"{name_string}_mapped_pt", format_mapped(new_mapped, total), False)
    glue(f"{name_string}_unmapped_pt", format_mapped(new_unmapped, total), False)

    return new_mapped, new_unmapped

mapped_nocl_pt, unmapped_nocl_pt = primary_and_tissues(mapped_nocl, unmapped_nocl, samples_info, 'nocl')
mapped_cl_pt, unmapped_cl_pt = primary_and_tissues(mapped_cl, unmapped_cl, samples_info, 'cl')
mapped_name_pt, unmapped_name_pt = primary_and_tissues(mapped_name, unmapped_name, samples_info, 'name')
mapped_overall_pt, unmapped_overall_pt = primary_and_tissues(mapped_overall, unmapped_overall, samples_info, 'overall')
```

```{list-table} Table showing the difference in coverage for different mappings, when restricting the samples to tissue and primary cell samples.
:header-rows: 1
:name: coverage-tissue-primary-cell

* - Mapping name
  - Number (and percentage) of primary cell and tissue mapped samples 
  - Number (and percentage) of primary cell and tissue  unmapped samples
* - By ontology: using Uberon tissues only
  - {glue:text}`nocl_mapped_pt`
  - {glue:text}`nocl_unmapped_pt`
* - By ontology: using Uberon tissues and CL cells
  - {glue:text}`cl_mapped_pt`
  - {glue:text}`cl_unmapped_pt`
* - By name: using tissue column
  - {glue:text}`name_mapped_pt`
  - {glue:text}`name_unmapped_pt`
* - Overall mapping (combining by-ontology with CL, and by-name mappings)
  - {glue:text}`overall_mapped_pt`
  - {glue:text}`overall_unmapped_pt`
```

```{code-cell} ipython3
:tags: [hide-input, remove-output]

sex_col = 'Characteristics [Sex]'
age_col = 'Characteristics [Age]'
remaining_unmapped = samples_info.loc[unmapped_overall_pt.index][[desc_col, sex_col, age_col, tissue_col]]
glue("unmapped-table", remaining_unmapped, False)
```

{numref}`coverage-tissue-primary-cell` shows that the missing mapping seen in {numref}`cl-increases-coverage` can be explained by the presence of sample types such as developing tissues and immortal cell lines (models for diseases), i.e. not healthy adult tissues. 
Again there was a benefit in combining mappings. 
The only remaining unmapped tissues were all *unclassifiable* reference RNA samples (from different providers) - shown in {numref}`unmapped-samples`, from mixed donors and cell types: this is reassuring as we would hope that these would not be mapped to a tissue.

```{glue:figure} unmapped-table
:figwidth: 800px
:name: unmapped-samples

Table showing the three remaining samples which could not be mapped to an Uberon tissue using Ontolopy. All three are  reference RNA samples.
```

```{code-cell} ipython3

```

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Create disagreements table
category_col = 'Characteristics [Category]'
categories = ['primary cells', 'tissues']

category_samples = samples_info[samples_info[category_col].isin(categories)].index

disagreements_pt = disagreements[disagreements.index.isin(category_samples)]
disagreements_pt.loc[:,'by name text'] = pd.Series([merged[x]['name'] for x in disagreements_pt['by_name']], disagreements_pt.index)
disagreements_pt.loc[:,'by ont text'] = pd.Series([merged[x]['name'] for x in disagreements_pt['by_ont']], disagreements_pt.index)

disagreements_table = disagreements_pt.drop_duplicates(subset=['by name text','by ont text'])[['by name text', 'by ont text']]
disagreements_table.loc[:,'description'] = pd.Series(samples_info[desc_col].loc[disagreements_table.index], index=disagreements_table.index)

glue('number-disagreements', len(disagreements_pt), False)
glue('number-types-disagreements', len(disagreements_table), False)
disagreements_table = disagreements_table[['description','by name text', 'by ont text']]
glue('disagreements-table', disagreements_table, False)
```

(FANTOM5-inconsistencies-example)=
### Finding inconsistencies 
By comparing the results of both ontology and text based searches, Ontolopy can find inconsistencies between the two representations which sign post to issues with samples data and how it is presented, or in the ontologies that it is linked to (in this case Uberon and CL): I give an example of each type.
I found this approach very useful, as it allowed me to feed back my discoveries to the maintainers of these ontologies and datasets in order to improve them, and has resulted in improvements to several of these resources. 

There were two main ways in which inconsistencies were found:
1. Through looking at samples which are not mapped by one method or another.
2. By looking at the disagreements output which compares the mapping that Ontolopy finds using one file and method (text in sample information file), to that it finds using the other (terms in sample ontology file).

For the FANTOM5 data, disagreements between these mappings revealed problems in the biological ontologies and experiment metadata that were provided to the package in order to create the mappings. 

Disagreements between the tissue-sample mappings created through the (FANTOM and extended Uberon) ontologies and those created using human annotation illuminates what may be a lack of specificity, incompleteness in, or disagreement between FANTOM, CL, or Uberon annotations, either in creating ontologies or annotating tissues to samples. 
The process of mapping FANTOM to Uberon tissues found twenty-two such disagreements, of which FANTOM, Uberon, and CL where appropriate have been informed via GitHub issues, some of which have already sparked changes in the ontologies. 

Four different types of example are described below, to give an idea of how multiple mappings may be used to improve annotation.

A full list of disagreements can be seen in {numref}`disagreements-examples`. 
There were {glue:text}`number-types-disagreements` disagreements/inconsistencies found using Ontolopy.
These disagreements can effect multiple (replicate) samples, for a total of {glue:text}`number-disagreements` samples.

```{glue:figure} disagreements-table
:figwidth: 800px
:name: disagreements-examples

Table showing all types of disagreements found using Ontolopy, with example samples.
```

#### Finding samples that are missing annotations to tissues
When we look at the samples that we would {ref}`expect to map<expect-to-map>` by ontology, but that don't, after filtering for tissues and primary cells only, we see that there are just two types of samples: 
1. One sample `FF:10379-105H1` which is missing `is_a: FF:0010164 ! human caudate nucleus - adult donor sample` in the FANTOM5 ontology file  
2. 21 T-cell samples, all of which appear not to have been fully classified (i.e. contain the following line in the ontology file `comment: Changed from previous label. TODO: full classification`). I could map all of them to the term for *T-cell*, whereas someone with more knowledge of T-cells could more accurately map these samples to more specific cell types.

I can use Ontolopy to add these mappings to the merged ontology to improve the by ontology mapping if I needed to: this would help me to find additional mappings, for example, to *immune system* as well as *blood*.

#### Missing Uberon or CL annotation
**Example: Missing annotation `Bronchus part_of some Lung`**

One type of problem that can be revealed is a missing link in an ontology.

An example of this that was found using the FANTOM data set was that there was no formal relation in the Uberon ontology between *Bronchus* and *Lung*, despite the fact that the description text for *Bronchus* says “the upper conducting airways of the lung”.

This was found because the sample `FF:11511-119G8` (*Bronchial Epithelial Cell, donor1*) is mapped by name to `UBERON:0002048` *Lung*, but by ontology to `UBERON:0002185` *Bronchus*. 
This was flagged as inconsistent because there are no relations in the Uberon ontology between these terms.

Similar missing annotations were discovered between *Aorta* and *Artery*, *Hair follicle* and *Dermal papilla*, and *Skeletal muscle myoblast* and *Skeletal muscle fiber*, and *Trophoblast* and *Placenta*.

#### Mislabelled sample
Sometimes samples are simply mislabelled, this can happen in any file type.

**Example: `FF:11590-120G6` should be labelled _Alveolar Epithelial Cells_ not _Renal Glomerular Endothelial Cells_**

The FANTOM sample ontology file contains two samples named Renal Glomerular Endothelial Cells, donor2: `FF:11590-120G6` and `FF:11594-120H1`. 
One of these is a mislabelled sample, and it is actually an Alveolar Epithelial Cell sample.
The mistake is only for the name in the FANTOM ontology file, but not the tissue annotation.

**Example: `FF:11842-124H6` should be labelled *ovary* not *bone marrow* in the samples information file**
The tissue column of the samples information file lists sample `FF:11842-124H6` as a bone marrow sample, despite being an ovarian cancer sample.

#### Imprecise annotation to tissue
__Example: *Nucleus pulpopus* as *Spinal cord*__

Several FANTOM5 tissues are labelled by name colloquially, rather than precisely. 
For example, both *Nucleus pulpopus* and *Vertebra* are labelled *Spinal cord* (although the spinal cord itself is considered disjoint from these entities by definition, and in the Uberon ontology).
It’s for this reason that the ontology mapping is preferred over the labelled sample name in creating the overall FANTOM sample-to-tissue mapping.

__Example2: `FF:11423-118G1 is_a` *dermal melanocyte*__

Sometimes the text in the samples information file can help us to reach better mappings in the sample ontology file. 
For example sample `FF:11423-118G1` (and five other similar samples) are mapped to `CL:0000148` (*melanocyte*), which is a cell that can come from many different parts of the body (skin, heart, eyes, etc), so Ontolopy can only map this term to several tissues (some of which this cell will not have come from) and only if the {ref}`child mapping<child-mapping>` functionality is used.
However, since the sample was labelled as coming from the "skin", it's clear that this sample would have been better annotated to `CL:0002482` (*dermal melanocyte*).

+++ {"tags": ["remove-input", "remove-output"]}

<!--
(tissue-group-mapping)=
### Re-grouping samples based on tissues
[//]: # (TODO: Check this renders)

Samples can be grouped by more general Uberon terms representing groups of tissues.
This {ref}`can be useful<>` when comparing to experiments that use more general tissue meta data.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Re-grouping samples by tissue "groups"

# groups = ['brain','cardiovascular system', 'respiratory system','digestive system','skeletal system','skin of body', 'reproductive system','muscle tissue','renal system','central nervous system','connective tissue']
# groups_UBERON = []
# for group in groups:
#     for u_id in obo.ont.keys():
#         if obo.ont[u_id]['name'] == group:
#             groups_UBERON.append(u_id)
# group_name_map = dict(zip(groups_UBERON, groups))

# relations = obo.get_relations(['is_a','part_of'],tissues['UBERON'],groups_UBERON,obo.ont).relations
# groups = []
# for uberon, row in relations.iterrows():
#     try:
#         group = row[0].split('_')[-1]
#     except:
#         group = None
#     groups.append(group)
# relations['Group'] = pd.Series(groups,index=relations.index)
# relations['Group name'] = relations['Group'].map(group_name_map)
# relations['Name'] = relations.index.map(name_map)
# relations=relations.rename(columns={0:'Relation string'})
# relations.to_csv('../data/mappings/tissues_groups.csv')
```
-->

(mappingstatistics)=
### Mapping overview
Using Ontolopy we can get a coverage of all samples that we would expect to map to a localised tissue (defining this as primary cell and tissue samples excluding reference RNA). 
These mappings correspond to {glue:text}`overall-unique-tissues` unique tissues.

(2-tissue-to-phenotype)=
## Creating tissue-to-phenotype mappings

[//]: # (TODO: Make sure they are biological_process not cellular_component)

```{margin} by-ontology mapping
:name: phenotype-by-name
Here we are only using an ontology based mapping, but if we had information in the samples information file about phenotype (e.g. disease), we could also use this to do an additional name based mapping if we wanted to.
```

The approach to the creation of the tissue-to-phenotype mappings is different to that we just took for sample-to-tissue mappings in that we are only doing a {ref}`by-ontology mapping<phenotype-by-name>`, rather than also mapping by-name and then comparing.
However, it is also a more complex example of a by-ontology mapping since we are asking more than one question to the ontology and adding them together.
For all these questions, we start with the {glue:text}`overall-unique-tissues` tissues that we are interested in finding mappings for as source terms, and we use `opy.Relations`'s `mode='all'` option to find *all* of the Gene Ontology `targets=['GO']` terms that are related to them.

We are interested broadly in tissues where a phenotype can take place, so this could be something on the level of proteins (*calcium signalling*), cells (*cell motility*), or tissue (*protein secretion*). 
This will effect what settings (particularly `allowed_relations`) we use when we make calls to `Relations`. 

Only Gene Ontology *Biological Process* terms are related to phenotypes.
The quickest way to retrieve only these is to ask for all `GO` terms and then filter them afterwards.
After loading the [GO basic ontology](http://geneontology.org/docs/download-ontology/#go_basic), we can easily retrieve a list of *Biological Process* terms.

```{code-cell} ipython3
:tags: [hide-input, remove_output]

go_obo_file = '../c08-combining/data/go-basic.obo' 
go_obo = opy.load_obo(
    file_loc=go_obo_file, 
    ont_ids=['GO', 'UBERON','CL','FMA'], 
)

biological_processes = [x for x in go_obo.terms if ('biological_process' in go_obo[x]['namespace'])]
```

(partofprop)=
### Propagating relationships up the tree using `part_of`

Our first example of looking for relations between tissues and phenotypes will include the `part_of` relation.
Since ontologies are often represented by DAGs, relationships are usually generally in one direction. 
While there is also the `has_part` relationship that we will look at {ref}`shortly<has-part>`, `part_of` is preferred  in the Uberon ontology with almost 10 times as many instances (15,486 compared to 1,703).

We first combine the GO ontology with the uberon ontology, which will simply help us to be able to look up the names of the GO terms to present the output in a more accessible format.
This doesn't make a difference to the number of mappings, only to the `relation_text` field of the output (which will contain names instead of GO term IDs if available).

We then use the `opy.Relations` class with `mode='all'`, and `allowed_relations` including `is_a`, `part_of` (as mentioned), and some relationships which typically define relationships between tissues and phenotypes `is_model_for`, `capable_of`, `capable_of_part_of`, and the `GO` relation which is defined by Ontology to capture references to `GO` terms within definitions.
This retrieves the mappings in {glue:text}`time-tissue-up`. 

The `Relations` class returns a dataframe with the same format whether you use the default `mode` (finding `any` mapping that looks like the `targets`) or the `all` mode; both are indexed by source terms.
For `all` mode, however, there can be multiple mappings for each source term, so the dataframe contains lists of mappings.
This dataframe isn't too easy on the eyes (or analysis), so Ontolopy also has a helpful method called `format_all` which reformats the `Relations` output dataframe when the `all` mode is used into an easier-to-work-with multi-indexed dataframe.
Example output of this can be seen in {numref}`phenotype-mapping-example-table`.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Merge GO obo:
go_uberon = uberon_obo.merge(go_obo)

# Retrieve tissue-phenotype mapping:
start = time.time()
source_tissues = overall['overall'].unique()[1:]
relations = ['GO', 'is_a', 'is_model_for', 'part_of', 'capable_of', 'capable_of_part_of']
phenotype_mapping = opy.Relations(
    allowed_relations=relations, 
    ont=go_uberon, 
    sources=source_tissues, 
    targets=['GO'], 
    mode='all'
)
glue("time-tissue-up", f"{(time.time()-start):.2f} seconds", True)

# Create formatted version (easy to work with):
formatted_phenotype_mapping = phenotype_mapping.format_all(ont=go_uberon, targets=['GO'])
formatted_phenotype_mapping.index.set_names(['Tissue', 'Phenotype'], inplace=True)
formatted_phenotype_mapping = formatted_phenotype_mapping[formatted_phenotype_mapping.index.get_level_values('Phenotype').isin(biological_processes)]

# Create table view
chosen_rows = [('UBERON:0001255', 'GO:0048731'), # urinary bladder
               ('UBERON:0001255', 'GO:0007275'),
               ('UBERON:0001255', 'GO:0048856'),
               ('UBERON:0001255', 'GO:0032502'),
               ('UBERON:0001255', 'GO:0008015'),
               ('UBERON:0000955', 'GO:0050890'), # brain
               ('UBERON:0000955', 'GO:0048856'),
               ('UBERON:0000955', 'GO:0007275'),
               ('UBERON:0000955', 'GO:0021551')]
phenotype_mapping_table = formatted_phenotype_mapping[['relation_text']].loc[chosen_rows]
pd.set_option("display.max_colwidth", 600)
glue('phenotype-mapping-table', phenotype_mapping_table)
pd.reset_option("display.max_colwidth")
```

```{glue:figure} phenotype-mapping-table
:figwidth: 800px
:name: phenotype-mapping-example-table

Table showing a view of the output of `Relations.format_all` for the tissue-to-phenotype mapping.
```

As {numref}`phenotype-mapping-example-table` shows, mappings contain a mixture of mappings to specific GO terms like *brain* and *cognition*, and very general phenotype terms, like *urinary bladder* and *anatomical structure development*.

[//]: # (TODO: Bug reading in alt_id GO_0061039, GO_0008585, put in Ontolopy GH)

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Calculate number of mapped GO terms:
go_counts = pd.DataFrame(formatted_phenotype_mapping.index.get_level_values(1).value_counts())
go_counts.columns = ['Frequency']
name = []
for go in go_counts.index:
    try:
        name.append(go_uberon[go]['name'])
    except KeyError:
        name.append(None)
go_counts.loc[:, 'name'] = pd.Series(name, go_counts.index)
go_counts_table = go_counts.head(20)
glue("go-counts-table", go_counts_table)

to_remove = go_counts_table.iloc[:9]['name'].to_list() + ['cellular process']

glue("num-go-to-remove", len(to_remove))
glue("lst-go-to-remove", list_to_text(to_remove))
glue("num-go-mapped", len(go_counts))
```

As we've seen in other example use cases, it's possible to use the `exclude` option when retreiving the mapping, to exclude any terms that you might wish to avoid, for example very general terms if you have a list of these.
Since we didn't know this, we found the 20 most frequently mapped GO terms (seen in {numref}`go-counts-top20`), out of {glue:text}`num-go-mapped` mapped overall.
From this list {glue:text}`num-go-to-remove` tissues to remove were then manually identified: {glue:text}`lst-go-to-remove`.

```{glue:figure} go-counts-table
:figwidth: 800px
:name: go-counts-top20

Table showing the frequency that phenotype (`GO`) terms are mapped to the provided tissue terms, for the top 20 GO terms.
```

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Calculate number of mappings per UBERON term
def mapping_to_tissue_counts(df):
    """
    Input formatted df
    """
    counts = df.groupby(level=['Tissue']).size()
    counts = pd.DataFrame(counts, columns = ['Number mapped phenotypes'])
    
    # Add zeros to counts
    unmapped_tissue_phenotype = []
    for tissue in source_tissues:
        if not tissue in counts.index:
            counts.loc[tissue] = [0]
            unmapped_tissue_phenotype.append(tissue)
            
    return counts, unmapped_tissue_phenotype

counts, unmapped_tissue_phenotype = mapping_to_tissue_counts(formatted_phenotype_mapping)

glue("unmapped-tissue-up", len(unmapped_tissue_phenotype))
glue("lst-unmapped-tissue-phenotype", list_to_text([merged[tissue]['name'] for tissue in unmapped_tissue_phenotype]))

# remove to_remove and then recalculate:
to_remove_ids = list(go_counts_table.iloc[:9].index) + ['GO:0009987']
formatted_phenotype_mapping_filtered = formatted_phenotype_mapping.drop(to_remove_ids, level='Phenotype')
counts_less, unmapped_tissue_phenotype_less = mapping_to_tissue_counts(formatted_phenotype_mapping_filtered)

num_mapped_up = len(formatted_phenotype_mapping_filtered.index.get_level_values("Tissue").unique())
glue("mapped-tissue-up", f"{num_mapped_up} ({100*num_mapped_up/float(len(source_tissues)):.2f}%)")
# glue("mapped-tissue-up", len(formatted_phenotype_mapping_filtered.index.get_level_values("Tissue").unique()))
glue("num-unique-phen-up",  len(formatted_phenotype_mapping_filtered.index.get_level_values("Phenotype").unique()))

glue("num-unmapped-tissue-phenotype-num", len(unmapped_tissue_phenotype_less))
glue("lst-unmapped-tissue-phenotype-lst", list_to_text([merged[tissue]['name'] for tissue in unmapped_tissue_phenotype_less]))
```

{numref}`mapped-phenotypes-per-tissue` (b) shows us that after removing very general terms, the majority of terms have 1-20 phenotypes mapped to them. 

A small number have more, and a small number have no mappings. 
There are {glue:text}`num-unmapped-tissue-phenotype-num` terms in (b) which do not have a mapping except for the very general terms.
These terms are: {glue:text}`lst-unmapped-tissue-phenotype-lst`.
Clearly there are phenotypes that affect these tissues (with the exception of the obsolete term), so the lack of mapping here may represent missing relationships or terms within the gene ontology.
An important one for our data set is *blood* (since we have many such tissue samples): there are GO phenotype terms relating to *blood* such as *blood circulation* and *blood coagulation*, so why don't we get mappings to these terms?

(has-part)=
### Propagating "down" the tree: `has_part`
The problem above happens because the annotation to these phenotype terms is not carried out at the level of tissue (*blood*) but at the level of cell type (*blood cell*).
In order to retrieve these terms, instead of propagating up the tree (to more general terms) we need to look down the tree (to more specific terms).

```{margin} has_part and part_of
:name: has-part-part-of
Ontological relations have strict definitions which help allow us to reason based on these relations, for example by `A has_part B`, we mean that A always has B as a part, while `B part_of A` means that whenever B exists it is part of A.

This means that `has_part` and `part_of` are not inverses{cite}`Smith2005-ug`, i.e. if `A part_of B`, that does not necessarily mean that `B has_part A`.
For example, wherever human ovaries exist, they are `part_of` humans, but whever humans exist, they don't necessarily `has_part` human ovaries. 

There are also other terms which denote similar relations, such as `composed_primarily_of`.
```

One way is to use `Relations` including relations in `allowed_relations` that denote having something as a part: `has_part` and `composed_primarily_of`.
From here onwards, I'll use `has_part` as a shorthand for both of these terms.
It doesn't make sense to run `Relations` with both `has_part` and `part_of`, since by running both up and down the tree, it could lead to technically true, but uninteresting and potentially misleading mappings.
A simple fictional example of this would be mapping *little toe* and *big toe nail* by finding the relation *little toe **part of** toes **has part** big toe **has part** big toe nail*.

(has-part-thoughts)=
Including phenotypes that are only relevant for part of the tissue makes sense for tissue samples like *blood* where we have all parts of the blood in our sample (e.g. the sample will certainly contain *blood cell*s and *plasma*). 
However, they may make less sense for a tissue sample like *heart*, where we don't know if the sample came from the *right ventricle* or the *left ventricle* and there may be phenotype terms which are specific to a part of the anatomy we didn't sample from.
With this in mind, our choices are: 
1. don't include `has_part` relations, and miss phenotype mappings that are made at the level of constituent parts
2. include `has_part` relations, but be aware that some samples may map to phenotypes that they are not capable of if the sample-to-tissue mapping is not specific enough.

In our case, option (2) is preferable, particularly because the FANTOM5 dataset contains many blood samples, and otherwise we would be missing phenotype mappings entirely for these samples.
Running this is otherwise very similar.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Retrieve tissue-phenotype mapping (propagating down using "has_part"):
# TODO: Add test to Ontolopy checking that the order of checking the new terms doesn't matter - add issue
start = time.time()
relations = ['GO', 'is_a', 'is_model_for', 'has_part', 'capable_of', 'capable_of_part_of', 'channel_for', 'composed_primarily_of']
phenotype_mapping_down = opy.Relations(
    allowed_relations=relations, 
    ont=go_uberon, 
    sources=source_tissues, 
    targets=['GO'], 
    mode='all'
)
glue("time-tissue-down-1", f"{(time.time()-start):.2f} seconds", True)

# Format and calculate counts of phenotypes per tissue:
formatted_phenotype_mapping_down = phenotype_mapping_down.format_all(ont=go_uberon, targets=['GO'])
formatted_phenotype_mapping_down.index.set_names(['Tissue', 'Phenotype'], inplace=True)
formatted_phenotype_mapping_down = formatted_phenotype_mapping_down[formatted_phenotype_mapping_down.index.get_level_values('Phenotype').isin(biological_processes)]
formatted_phenotype_mapping_down_filtered = formatted_phenotype_mapping_down.drop(list(set(to_remove_ids) & set(formatted_phenotype_mapping_down.index.get_level_values('Phenotype'))), level='Phenotype')

glue("num-unique-phen-down-1", len(formatted_phenotype_mapping_down_filtered.index.get_level_values('Phenotype').unique()))
num_mapped_down1 = len(formatted_phenotype_mapping_down_filtered.index.get_level_values("Tissue").unique())
glue("mapped-tissue-down-1", f"{num_mapped_down1} ({100*num_mapped_down1/float(len(source_tissues)):.2f}%)")

counts_down1, _ = mapping_to_tissue_counts(formatted_phenotype_mapping_down)
counts_down1_less, unmapped_down1_less = mapping_to_tissue_counts(formatted_phenotype_mapping_down_filtered)

# Combine to find as yet unmapped 
yet_unmapped_down1 = list(set(unmapped_tissue_phenotype_less) & set(unmapped_down1_less))
glue("unmapped-tissue-down-1", len(yet_unmapped_down1))
glue("lst-unmapped-updown-less", list_to_text([merged[x]['name'] for x in yet_unmapped_down1]))

```

In {numref}`tissue-mapping-comparison`, which compares the number of mapped tissues and phenotypes for different tissue-to-phenotype mapping methods, we can see that this method maps more phenotypes, but for less tissues.

[//]: # (TODO: Check unmapped-updown-less - missing number)

Although less tissues have been mapped overall, we can tell they do capture previously unmapped tissues since the overall number of unmapped tissues (after removal of too-general terms) reduces from {glue:text}`num-unmapped-tissue-phenotype-num` with propagating up only to {glue:text}`unmapped-tissue-down-1` which aren't mapped by either method.
While propagating down therefore improves the overall mapping coverage, looking at the tissues which remain unmapped gives us a clue as to what further improvements we can make.

The terms which remain unmapped are {glue:text}`lst-unmapped-updown-less`. 
The give-away term is *skin of body*, since looking at subfigure `(d)` in {numref}`mapped-phenotypes-per-tissue`, by hovering over the top most well-mapped tissue we can see that it is *stratum basale of epidermis*, which is part of the *epidermis* which is in turn part of the *skin of body*. 
The reason skin of body doesn't have a mapping is because while the *epidermis* is `part_of` the *skin of body*, the *skin of body* does not have the `has_part` relation to *epidermis*.

(can-have-human-part-define)=
### Propagating down the tree: inverse of `part_of`

In addition to the `has_part` approach, we could use the inverse of the `part_of` relations, however the {ref}`definitions of these terms<has-part-part-of>` mean that the inverse of `part_of` means something like *can have part*.
This would mean that in addition to the risk of potentially including mapping to more specific parts of the body that weren't in our sample (as we {ref}`discussed<has-part-thoughts>` for the `has_part` approach), we might sometimes include mappings to tissues that were not even present in the species or gender from which the sample came.
The species problem is the much more pressing concern since Uberon is a multi-species ontology containing many non-human-specific terms and therefore we could end up mapping human samples to terms like `GO:0035844` *cloaca development*.

One solution to this in Ontolopy is to define relations that look something like `A can_have_human_part B` from the information in the ontology files, by using the inverse of `part_of` relations only where there is an external reference (`xref`) to the FMA human anatomy ontology.
We need to do this semi-manually as Ontolopy does not currently contain tools for automatically defining new relations. 
Once we've created this new relationship, we can ask for relations including it in the same query as `has_part`.
One downside of this approach is that relations found using this kind of self-defined relation will not be able to use the simple reasoning that Ontolopy is capable of (i.e. collapsing relations by using definitions like `is_a`$\cdot$`part_of` == `part_of`, since such equivalences are not defined).

```{admonition} Sex-specific phenotype mappings
:name: sex-specific-mappings
We could also create a relation like `A can_have_part_in_female B` (and an analagous term for male) when `B part_of A` and `B part_of UBERON:0003100` *female organism*.
We could then cross-reference the sex of our samples from the sample information file to ensure that we don't create mappings between e.g. male-only samples and ovaries.
This isn't done here, since it will only effect a very small number of mappings (given that many of the samples are mixed/unknown sexes, that there are only a small number of sexual dimorphic tissues, and that these are generally mapped at the level of specific sexes already), and wouldn't illustrate a different aspect of using Ontolopy.
Such mappings, if they exist, are simply not included. 
If they are excluded, it means that we simply do not map non sex-specific tissues like *gonad* to either testes or ovary-related phenotypes, so we might be missing such mappings.
```

We could also do the same for {ref}`sex-specific tissue-phenotype mappings<sex-specific-mappings>`, should we want to. 
This could be useful, depending on the experiment data in question and the resulting sample-tissue mappings we'd previously attained.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Create new ontology term 'can_have_human_part' as inverse of 'part_of' with 'xref'=='FMA':
for term in go_uberon.terms:
    if term.split(':')[0] == 'UBERON':
        try:
            parts_of = go_uberon[term]['part_of']
        except KeyError:
            parts_of = []
            
        try:
            xrefs = go_uberon[term]['xref']
        except:
            xrefs = []
        
        if not any([xref.startswith('FMA') for xref in xrefs]):  # not human, e.g. cloaca
            continue
        
        for part in parts_of:
            if part.split(':')[0] == 'UBERON':
                try:
                    go_uberon[part]['can_have_human_part'].add(term)
                except:
                    go_uberon[part]['can_have_human_part'] = {term}

# Create mapping:
start = time.time()
phenotype_mapping_down2 = opy.Relations(
    allowed_relations=relations+['can_have_human_part'], 
    ont=go_uberon, 
    sources=source_tissues, 
    targets=['GO'], 
    mode='all'
)
glue("time-tissue-down-2", f"{(time.time()-start):.2f} seconds", True)

# Format:
formatted_phenotype_mapping_down2 = phenotype_mapping_down2.format_all(ont=go_uberon, targets=['GO'])
formatted_phenotype_mapping_down2.index.set_names(['Tissue', 'Phenotype'], inplace=True)
formatted_phenotype_mapping_down2 = formatted_phenotype_mapping_down2[formatted_phenotype_mapping_down2.index.get_level_values('Phenotype').isin(biological_processes)]
formatted_phenotype_mapping_down2_filtered = formatted_phenotype_mapping_down2.drop(list(set(to_remove_ids) & set(formatted_phenotype_mapping_down2.index.get_level_values('Phenotype'))), level='Phenotype')
num_mapped_down2 = len(formatted_phenotype_mapping_down2_filtered.index.get_level_values("Tissue").unique())
glue("mapped-tissue-down-2", f"{num_mapped_down2} ({100*num_mapped_down2/float(len(source_tissues)):.2f}%)")
glue("num-unique-phen-down-2", len(formatted_phenotype_mapping_down2_filtered.index.get_level_values('Phenotype').unique()))

# Calculate counts:
counts_down2, _ = mapping_to_tissue_counts(formatted_phenotype_mapping_down2)
counts_down2_less, unmapped_down2_less = mapping_to_tissue_counts(formatted_phenotype_mapping_down2_filtered)

yet_unmapped_down2 = list(set(unmapped_tissue_phenotype_less).intersection(set(unmapped_down1_less), set(unmapped_down2_less)))
glue("unmapped-tissue-down-2", len(yet_unmapped_down2))
glue("lst-unmapped-updown2-less", list_to_text([merged[x]['name'] for x in yet_unmapped_down2]))

assert(len(set(formatted_phenotype_mapping_down.index) - set(formatted_phenotype_mapping_down2.index))==0)

# Create examples of new relations table
examples = [2, 9, 19, 45, 59, 105]
new_samples = list(set(formatted_phenotype_mapping_down2_filtered.index)-set(formatted_phenotype_mapping_down_filtered.index))
glue('new-down2', len(new_samples))
pd.set_option("display.max_colwidth", 600)
table_down2_examples = formatted_phenotype_mapping_down2_filtered.loc[[new_samples[i] for i in examples]][['relation_text']]
glue('table-down2-examples', table_down2_examples)
pd.reset_option("display.max_colwidth")
```

[//]: # (TODO: Explain more in both categories, and less unmapped)
This resulting mapping contains {glue:text}`new-down2` additional tissue-phenotype mappings (not found in either the `has_part` or the `part_of` approach).
Some examples of these additional tissue-phenotype mappings that were found using this `can_have_human_part` approach are given in {numref}`tbl-down2-examples`.
Overall, this mapping covers {glue:text}`mapped-tissue-down-2` tissues and {glue:text}`num-unique-phen-down-2` phenotypes.

The yet unmapped tissues (by any method) are now: {glue:text}`lst-unmapped-updown2-less`.
While this list still contains tissues that we would expect to map to GOBP phenotypes, the lack of these terms in our searches now means that they are simply missing annotations. 
For example we have no mapping for *adipose tissue* despite the fact that GOBP terms exists for *adipose tissue development* and *fat cell proliferation*, but there is no cross-ontology mapping of these term in the current version of the ontology, so there is no way Ontolopy could pick them up.

```{glue:figure} table-down2-examples
:figwidth: 800px
:name: tbl-down2-examples

An example of six of the {glue:text}`new-down2` additional Uberon-GOBP mappings found using `can_have_human_part`. 
```

(combiningexample2)=
### Combining previous mappings

To create the final tissue-phenotype mapping, we combine the propagating up (`part_of`) mapping with the {ref}`larger<can-have-contains>` propagating down (`can_have_human_part`) mapping, by simply appending the new lines of the DataFrame.

```{admonition} 'can_have_human_part' query completely contains 'has_part' query.
:name: can-have-contains
Because the `allowed_relations` for the  mappings of the `can_have_human_part` query completely contain those for the `has_part` query, so do the found relations.
This means that we only need to combine the `part_of` and `can_have_human_part` mappings to get the most complete set.
```

As we can see in {numref}`tissue-mapping-comparison`, the overall combined mapping covers {glue:text}`mapped-tissue-combined` of the Uberon tissues searched for and maps to {glue:text}`num-unique-phen-combined` unique GOBP tissues. 
Since this is greater than any other individual mapping, we can see that it is necessary to combine different mapping types to get high (>90%) coverage of tissues.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# COMBINING:
# Add new mappings:
new_mappings =  set(formatted_phenotype_mapping.index) - set(formatted_phenotype_mapping_down2.index)
up_down_phenotype_mapping_formatted = formatted_phenotype_mapping_down2.copy()
for i in new_mappings:
    up_down_phenotype_mapping_formatted = up_down_phenotype_mapping_formatted.append(formatted_phenotype_mapping.loc[i])

# filter:
up_down_phenotype_mapping_filtered = up_down_phenotype_mapping_formatted.drop(list(set(to_remove_ids) & set(up_down_phenotype_mapping_formatted.index.get_level_values('Phenotype'))), level='Phenotype')
                               
# counts per phenotype:
counts_updown, _ = mapping_to_tissue_counts(up_down_phenotype_mapping_formatted)        
counts_updown_less, unmapped_updown_less = mapping_to_tissue_counts(up_down_phenotype_mapping_filtered)

# calc stats:
glue("num-unique-phen-combined", len(up_down_phenotype_mapping_filtered.index.get_level_values('Phenotype').unique()))
num_mapped_combined = len(up_down_phenotype_mapping_filtered.index.get_level_values('Tissue').unique())
glue("mapped-tissue-combined", f"{num_mapped_combined} ({100*num_mapped_combined/float(len(source_tissues)):.2f}%)")
```

```{code-cell} ipython3
:tags: [hide-input]

# Create bar charts:
fig = make_subplots(rows=4, cols=2,
                    subplot_titles=(
                        "(a) all phenotype terms,<br>propagating up `part_of`", 
                        "(b) general phenotypes removed,<br>propagating up `part_of`",
                        "(c) all phenotype terms,<br>propagating down `has_part`",
                        "(d) general phenotypes removed,<br>propagating down `has_part`",
                        "(e) all phenotype terms,<br>propagating down<br>`can_have_human_part`",
                        "(f) general phenotypes removed,<br>propagating down<br>`can_have_human_part`",
                        "(g) all phenotype terms,<br>propagating both up and down",
                        "(h) general phenotypes removed,<br>propagating both up and down"
                    ),
                    shared_yaxes=True,
                   horizontal_spacing=0.05,
                   )

# ROW 1: (a) all phenotype terms propagating up
fig.add_trace(
    go_.Bar(y=counts.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index], 
           name='all, up',
           marker_color = 'slateblue',
           ),
    row=1, col=1
)
# ROW 1 (b) general phenotypes removed propagating up
fig.add_trace(
    go_.Bar(y=counts_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index],
           name='filtered, up',
           marker_color = 'darkslateblue',
           ),
    row=1, col=2
)
# ROW 2: (c) all phenotype terms propagating down: has_part
fig.add_trace(
    go_.Bar(y=counts_down1.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts_down1.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index],
           name='all, down: has_part',
           marker_color = 'lightsalmon',
           ),
    row=2, col=1
)
# ROW 2: (d) general phenotypes removed propagating down
fig.add_trace(
    go_.Bar(y=counts_down1_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts_down1_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index],
           name='filtered, down: has_part',
           marker_color = 'tomato',
           ),
    row=2, col=2
)    

# ROW 3: (e) all phenotype terms, down can_have_human_part
fig.add_trace(
    go_.Bar(y=counts_down2.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts_down2.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index],
           name='all, down: can_have_human_part',
           marker_color = 'orchid',
           ),
    row=3, col=1
)    
# ROW 3: (f) general phenotypes removed, down can_have_human_part
fig.add_trace(
    go_.Bar(y=counts_down2_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts_down2_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index],
           name='filtered, down: can_have_human_part',
           marker_color = 'darkorchid',
           ),
    row=3, col=2
)    

# ROW 4: (g) all phenotype terms, propagating both up and down
fig.add_trace(
    go_.Bar(y=counts_updown.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts_updown.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index],
           name='all, both up and down',
           marker_color = 'palevioletred',
           ),
    row=4, col=1
)    
# ROW 4: (h) general phenotypes removed, propagating both up and down
fig.add_trace(
    go_.Bar(y=counts_updown_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'], 
           x=[f"{merged[x]['name']}, {x}" for x in counts_updown_less.sort_values(by='Number mapped phenotypes')['Number mapped phenotypes'].index],
           name='filtered, both up and down',
           marker_color = 'mediumvioletred',
           ),
    row=4, col=2
)    

fig.update_layout(showlegend=False, width=800, height=600)
fig.update_yaxes(range=[0,150], tickvals=list(range(0,151,25)))
fig.update_yaxes(title_text='Number<br>phenotypes<br>mapped to', col=1)
fig.update_annotations(font_size=12)  # subplot titles are annotations in plotly

fig.update_xaxes(showticklabels=False)
fig.update_xaxes(title_text='Tissue term', row=4)
fig.show('notebook')
```

[//]: # (TODO: Link to website - and say that images can be scrolled over to see each tissue - figure showing up weird)

```{figure} ../images/blank.png
---
name: mapped-phenotypes-per-tissue
---
Bar charts showing the number of tissue-phenotype mappings (number of phenotypes mapped to each tissue - roll mouse over to see tissue names) for (a) all phenotype terms propagating down, (b) general phenotypes removed propagating down, (c) all phenotype terms propagating up, (d) general phenotypes removed propagating down, (e) all phenotype terms propagating both up and down, and (f) general phenotypes removed propagating both up and down. 

```

<!-- ../images/blank.png This is a workaround to put a 1x1px blank image after an interactive image so that it appears to have a figure label -->

There are {glue:text}`unmapped-tissue-down-2` unmapped tissues (which map to zero phenotypes), and all other tissues map to between 2 and 131 phenotype terms, (as we can see in figure {numref}`mapped-phenotypes-per-tissue`).
The number of mappings varies smoothly in this range with more general tissues and organs broadly appearing to have higher numbers of mappings than very specific tissues.
We can also see in {numref}`mapped-phenotypes-per-tissue` that the `can_have_human_part` mapping makes up the majority of the mappings in the final combined mapping.

```{list-table} Table comparing the difference in coverage (mappable tissues), phenotypes, time taken, and unmapped tissues for different mapping techniques.
:header-rows: 1
:name: tissue-mapping-comparison

* - Mapping name
  - Tissue coverage: number (percent) tissues mapped (this mapping only)
  - Number of unique phenotype mapped to (by this mapping only)
  - Number tissues remaining unmapped (by this or any previous mapping)
  - Time to retrieve mapping
* - Propagating up 
  - {glue:text}`mapped-tissue-up`
  - {glue:text}`num-unique-phen-up`
  - {glue:text}`unmapped-tissue-up`
  - {glue:text}`time-tissue-up`
* - Propagating down using `has_part`
  - {glue:text}`mapped-tissue-down-1`
  - {glue:text}`num-unique-phen-down-1`
  - {glue:text}`unmapped-tissue-down-1`
  - {glue:text}`time-tissue-down-1`
* - Propagating down using `can_have_human_part`
  - {glue:text}`mapped-tissue-down-2`
  - {glue:text}`num-unique-phen-down-2`
  - {glue:text}`unmapped-tissue-down-2`
  - {glue:text}`time-tissue-down-2`
* - Combined (all of the above)
  - {glue:text}`mapped-tissue-combined`
  - {glue:text}`num-unique-phen-combined`
  - **N/A** 
  - **N/A**
```

(3-sample-tissue)=
## Creating sample-to-tissue-phenotype mappings
Once we have both the sample-to-tissue and tissue-to-phenotype mappings, we can combine them to get the sample-to-tissue-phenotype mappings: mappings between samples and phenotypes that occur in the tissue type of that sample. 
There isn't a built-in Ontolopy function to do this, but since Ontolopy objects are built on top of Pandas DataFrames, they are fairly easy to work with.

Since we chose to map primary cell and tissue samples only, there are many samples which are not mapped.
Null mappings are included in the output, and where mapping by name is used, it is recorded as a `mapped_by_name_to` relationship in the relation path, e.g. `FF:11453-119A4.mapped_by_name_to~UBERON:0002048.is_a~UBERON:0000171.capable_of~GO:0007585` or in text *__Bronchial Epithelial Cell, donor4__ mapped by name to __lung__ is a __respiration organ__ capable of __respiratory gaseous exchange by respiratory system__*.
Since relation strings can now contain FANTOM5, CL, UBERON and GO terms, I first merge the GO ontology into the merged FANTOM5 and Uberon ontologies, so that the names of all terms can be found for the relation text.

[//]: # (TODO: Put the overall mapping table available for download on the OSF, and link)

```{code-cell} ipython3
:tags: [hide-input, remove-output]

mapped_by_name_relation = 'mapped_by_name_to'

# merge ontology
merged = merged.merge(go_obo)

sample_to_tissue = {}
for sample, row_i in overall.iterrows():
    if not pd.isna(row_i['overall']):
        tissue = row_i['overall']
    else: # no mapping from sample to tissue
        tissue = np.nan
        phenotype = np.nan
        sample_to_tissue[(sample, tissue, phenotype)] = [np.nan, np.nan]
        continue
        
    try:
        mappings = up_down_phenotype_mapping_filtered.xs(tissue, level ='Tissue')
        for phenotype, row_j in mappings.iterrows():
            if row_i['mapped_by'] in ['ontology', 'both (same)']:
                relation_path = sample_to_tissue_mapping.loc[sample, 'relation_path'].replace(tissue, row_j['relation_path'])          
            elif row_i['mapped_by'] == 'name':
                relation_path = f"{sample}.{mapped_by_name_relation}~{tissue}".replace(tissue, row_j['relation_path'])
            else:
                logging.warning(f"{row_i['mapped_by']} has unexpected format")
                continue
            sample_to_tissue[(sample, tissue, phenotype)] = [relation_path, 
                                                             opy.relation_path_to_text(relation_path, merged)]
    except KeyError:
        # Save phenotype as NaN if no phenotype mapping:
        sample_to_tissue[(sample, tissue, np.nan)] = [sample_to_tissue_mapping.loc[sample, 'relation_path'], 
                                                      opy.relation_path_to_text(sample_to_tissue_mapping.loc[sample, 'relation_path'], merged)]
        

# Save out overall mapping:
sample_to_tissue_df = pd.DataFrame.from_dict(sample_to_tissue,
                                      orient='index',
                                      columns=['relation_path', 'relation_text'])
sample_to_tissue_df.index = pd.MultiIndex.from_tuples(sample_to_tissue_df.index, names=["sample", "tissue", "phenotype"])
mapping_file_path = '../c06-filter/data/created/fantom-go-mapping.csv'
sample_to_tissue_df.to_csv(mapping_file_path, sep = '\t')
display(sample_to_tissue_df.head(20))
```

```{code-cell} ipython3
:tags: [remove-cell]

# Examples for mapped_by_name_to (don't want to glue because formatting too annoying)
print(sample_to_tissue_df.loc[('FF:11453-119A4','UBERON:0002048','GO:0007585'),'relation_text'])
sample_to_tissue_df.loc[('FF:11453-119A4','UBERON:0002048','GO:0007585'),'relation_path']
```

(opyexamplefinalmapping)=
### Final mapping

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# Glue final mapping statistics:
glue('sample-phen-rows', len(sample_to_tissue_df))
glue('total-sample-phen', len(sample_to_tissue_df.index.dropna()))

df = sample_to_tissue_df.reset_index()

glue('sample-phen-coverage-cat', f"{100*len(df[~df['phenotype'].isna() & df['sample'].isin(category_samples)]['sample'].unique())/float(len(df[df['sample'].isin(category_samples)]['sample'].unique())):.2f}%")
glue('sample-phen-coverage-all', f"{100*len(df[~df['phenotype'].isna()]['sample'].unique())/float(len(df['sample'].unique())):.2f}%")

glue('sample-tissue-nan', len(df[~df['tissue'].isna() & df['phenotype'].isna()]))
glue('total-sample-nan', len(df[df['tissue'].isna()]))

glue('notebook-time-mapping-example', f"{time.time()-notebook_start:.0f} seconds")

# Why are samples unmapped? 
# Count number of rows per unique tissue without phenotype mapping.
rows = []
for uberon in df[df['phenotype'].isna()]['tissue'].unique():
    if type(uberon) == float:
        if np.isnan(uberon):
            num = len(df[df['phenotype'].isna() & df['tissue'].isna()])
            row = ['NaN', 'Unmapped to phenotype', num]
    else:
        num = len(df[df['phenotype'].isna() & (df['tissue'] == uberon)])
        row = [uberon, merged[uberon]['name'], num]
    rows.append(row)

unmapped_why = pd.DataFrame(rows, columns = ['Uberon ID', 'Uberon Name', 'Number samples mapped to phenotype']);
unmapped_why.set_index('Uberon ID', inplace=True)
glue("unmapped-why", unmapped_why)
```

There are {glue:text}`sample-phen-rows` rows of the sample-to-tissue mapping DataFrame in total. 
This includes some `NaN` values, so it contains {glue:text}`total-sample-phen` mappings from sample to phenotype; equivalent to a sample coverage of {glue:text}`sample-phen-coverage-cat` of filtered (*tissue* and *primary cell*) samples or {glue:text}`sample-phen-coverage-all` of all samples.
It also includes an additional {glue:text}`sample-tissue-nan` mappings from sample to tissue (but not to phenotype), and {glue:text}`total-sample-nan` samples with no mapping to tissue or phenotype.
{numref}`table-unmapped-why` shows why almost 10% of samples are unmapped in more detail: many samples map to the same unmapped tissues, particiularly adipose tissue, epithelium, or connective tissue.

```{glue:figure} unmapped-why
:figwidth: 800px
:name: table-unmapped-why

Table showing how many samples are mapped to each unmappable tissue, showing why the coverage of samples isn't higher.
```

[//]: # (TODO: Change phrasing if I end up running on GH Actions)

With Ontolopy, this complex task is relatively quick: it took {glue:text}`notebook-time-mapping-example` to run this whole notebook on a laptop without any parallelisation.
Also recall that this section is merely an example of an application of Ontolopy: this same process could be done for other datasets that provide an ontology and/or a sample information file.
