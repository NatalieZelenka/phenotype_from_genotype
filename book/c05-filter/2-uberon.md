(uberon-py)=
# The `uberon-py` package
[//]: # (TODO: Make Uberon-py a website and link to it)
[//]: # (TODO: Make a Zenodo for uberon-py and reference it here)
[//]: # (TODO: Explain Research Software Engineering approach)
[//]: # (TODO: Signpost this section)
[//]: # (TODO: make sure I am consistent about uberon-py/uberon_py)
[//]: # (TODO: Write roadmap/future work for this section, e.g. make the example public)
[//]: # (TODO: Link to documentation)

[//]: # (TODO: Rewrite intro)

The biggest challenge in creating `filip` was to create a high-coverage mapping between phenotype and gene expression sample name. 

This was done by:
1. Mapping between phenotype term (GO, HP, or DO term) and related tissue (Uberon term) or cell type (CL term).
2. Mapping between expression sample name/description (text) or sample ontology term and tissue (Uberon term) or cell type (CL term).
3. Matching on the tissue or cell type.

As this was quite an involved process, I created a small Open Source Python Package -  `uberon-py`, which is [available to install via the Python Package Index]([https://pypi.org/project/uberon-py/]), with code [available on GitHub](https://github.com/NatalieThurlby/uberon-py).
This section describes the general functionality/methodology of `uberon-py`, and you can see exactly how `uberon-py` was used to do the mapping for `filip` in {ref}`filter-methods`.

## Methodology
[//]: # (TODO: Figure 14:)
<!--
Figure 14: A diagram illustrating parts of the UBERON and GO ontologies, with a fictional example of an UBERON-GO relationship. In this example, Regulation of lung development would be related to Left lung, but not to Bronchiole (as regulation of lung development could refer to a regulation of a different part of the lung).
-->

[//]: # (TODO: Write explain how mapping works: what is prioritised, etc)

## Functionality
[//]: # (TODO: List what can be downloaded)
[//]: # (TODO: Merge files)
[//]: # (TODO: Allow adding updating merged ontology in Python as you find issues, and output additions to a separate obo file)

While there are existing packages which allow users (and particularly creators) of ontologies to load and query them, `uberon-py` is designed specifically to map samples to terms using these ontologies.
It makes use of familiar Python objects (native dictionaries and Pandas data frames), to make downstream analysis or extending the use case easier.

This package allows users to use Python to:
1. **Download useful Uberon ontology files** a selection of Uberon ontology `.obo` files.
2. **Load `.obo` ontology files**, either your own, separately downloaded, or those obtained in (1).
3. **Automatically merge `.obo` ontology files**: Add additional information into the Uberon `.obo` file.
3. **{ref}`Mapping via name<mapping-by-name>`:** Map from sample-to-tissue via informal tissue names given in experimental design information (e.g. “eye stalk”) to an Uberon term (`UBERON:0010326`, Optic Pedicel).
4. **{ref}`Mapping via ontology term<mapping-by-term>`:** Map from CL cell types (e.g. `CL:0000235`, Macrophage), sample ontology term to Uberon tissues (e.g. `UBERON:0002405`, Immune system). Or from sample ontology terms (like FANTOM terms, such as `FF:10048-101G3`, *Smooth Muscle, Adult, Pool1*) to Uberon terms (`UBERON:0001135`, Smooth Muscle Tissue). Returns relationships between source term and Uberon term.
5. **Create sample-to-tissue mappings** based on (3) and (4)
6. **{ref}`Find disagreements in mappings<disagreement-finding>`** based on (3) and (4), which my indicate errors in sample metadata or ontologies.

The less self-explanatory aspects of this functionality are explained below:

[//]: # (TODO: Explain merge here)

(mapping-by-name)=
**Mapping by name:**

Informal tissue names are mapped Uberon term identifiers by checking for exact name matches to Uberon term names and their synonyms in the extended Uberon ontology.

(mapping-by-term)=
**Mapping by term: regular mapping**
[//]: # (TODO: Cite cell ontology)

A mapping between a provided term (e.g. a FANTOM sample identifier or CL identifier) associated with a sample and an Uberon term is created by:
* Finding all relationships of interest (e.g. `is_a`, `related_to`, `part_of`, `derives_from`, `intersection_of`, `union_of`) to any other sample, cell or Uberon term (i.e. all *parents* of our term of interest).
* Propagate any relationships found using the same list of relationships, until either an Uberon term is found, or no new relationships are found, or you reach the root terms of the ontology. 

In this way, some mappings can be made via the cell ontology, which cannot be made through Uberon alone, for example: Macrophage - monocyte derived, donor3 `is_a` Human macrophage sample `derives_from` Macrophage `is_a` Monocyte `is_a` Leukocyte `part_of` Immune System, e.g. this sample is related to the immune system.

[//]: # (TODO: Write about collapsing relationships)

[//]: # (TODO: Add example code for child-mapping melanocyte.)
(child-mapping)=
**Mapping by term: child mapping**
Some samples may be pools of cell types that may come from more than one anatomical location.
In this case, there will be no regular mapping, since no parent terms will have a mapping to a tissue. 
In this case, we can look at tissue mappings (in the usual way, described above), for all of the children of our parent term of interest.
I call this mode "child mapping" and it is off by default.

So, for example *melanocytes* are are melanin-producing cells found in many different places in the body (skin, hair, heart), and therefore they (nor any of their parents map to a specific Uberon term).
If we choose {python}`child_mapping=TRUE`, then for this term, we will get a list of all Uberon terms that cells of this type can come from.
This mode isn't currently used in the context of `filip`.

(disagreement-finding)=
**Using disagreements between mappings to improve biological ontologies and sample mappings:**

As described, the `uberon_py` package has two methods of mapping to tissues. 
Where both can be ran, disagreements between these mappings can be checked. 
When these two methods disagree, logical inconsistencies in either the mappings or the ontologies is revealed. 
See the {ref}`example<FANTOM5-inconsistencies-example>` of how this worked for the FANTOM5 data set.

## Example usage
[//]: # (TODO: Add CL + variuous citations)
The Uberon ontology connects many different ontologies and dictionaries, including many anatomy ontologies for different species (mouse, xenopus, fly, zebrafish) and specific structures (Neuroscience Information Framework (NIF) Gross Anatomy, Edinburgh Human Developmental Anatomy), as well as phenotype ontologies (Mammalian Phenotype Ontology, Gene Ontology){cite}`Mungall2012-nc`.
As such it is used by a wide variety of researchers.

### Example 1: Harmonisation of gene expression data
[//]: # (TODO: Show a snippet of code and output)

{numref}`c05.3-data-wrangling` shows an example of how this package can be used to create a sample to tissue mapping for four different gene expression data sets.

A similar methodology can be used to map your samples to other concepts, for exampple:
- dividing your samples into those cell types that can differentiate (turn into other cell types, i.e. pluripotent, stem and precursor cells), and those that can't. 
- dividing your samples into those that are mapped to certain classes of diseases (e.g. heart disease, cancer) and those that aren't.

(tissue-group-mapping)=
### Example 2: Re-grouping samples based on tissues
[//]: # (TODO: Update data locations)
Either using existing Uberon mappings, or after mapping to Uberon samples (as in example 1), samples can be grouped by more general Uberon terms representing groups of tissues.

[//]: # (TODO: Make code more usable: relations needs to have some functions for getting mapping, shouldn't be doing weird string stuff)

````{admonition} Code mapping samples to more general groups
:class: dropdown

```python
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

````


(FANTOM5-inconsistencies-example)=
### Example 3: finding inconsistencies in the FANTOM5 data
[//]: # (TODO: Add a table here of all the inconsistencies: medium priority)
For the FANTOM5 data, disagreements between these mappings revealed problems in the biological ontologies and experiment metadata that were provided to the package in order to create the mappings. 
These could then be fed back to the maintainers of these ontologies and datasets in order to improve/correct them. 

Disagreements between the tissue-sample mappings created through the (FANTOM, CL and Uberon) ontologies and those created using human annotation illuminates what may be a lack of specificity, incompleteness in, or disagreement between FANTOM, CL, or Uberon annotations, either in creating ontologies or annotating tissues to samples. 
The process of mapping FANTOM to Uberon tissues found twenty-two such disagreements, of which FANTOM, Uberon, and CL where appropriate have been informed via GitHub issues, some of which have already sparked changes in the ontologies. 

Three different types of example are described below, to give an idea of how multiple mappings may be used to improve annotation.

#### Missing Uberon or CL annotation
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

## Benchmarking 
[//]: # (TODO: speed - compare from combining)
[//]: # (TODO: coverage - compare from combining)

## Limitations
### Ontologies don't always capture the directionality of relationships that we are interested in
Ontology structures are directed and acyclic, and we depend on the directionality of the relationships in order to infer new relationships from these graphs. 
These are very well thought out, but very general, so they don't always simply suit our use case. 

In terms of mapping tissues, this was noticeable in terms of the `develops_from` relationship.
For example `CL:0008002` *skeletal muscle fiber* `develops_from` `CL:0000515` *skeletal muscle myoblast*. 
The acylic nature of ontologies, means that if `develops_from` is captured per term, then `develops_into` isn't.
If we look for parent terms only, we will not find that *skeletal muscle myoblast* develops into skeletal muscle fiber, and therefore we will not find that it develops into a part of *skeletal muscle tissue* (`UBERON:0001134`). 
But, currently, we would need to write a specific script if we wanted to capture these kinds of relationships. 
This would likely need more complex logic than simply turning on `child-mapping=TRUE`, because for example, we might only want to capture `develops_into` relationships where the cell of interest is a single-fate stem cell or a pre-cursor cell, so that we don't end up with too much broad and meaningless mapping, or for example we might only be interested in cell types that are found in adults.

In order to do something like this, we would need to have something more like a query language (e.g. SPARQL) for interacting with the ontology, which is beyond this scope of this package.

### Only maps to one tissue
[//]: # (TODO: Write)
When mapping by ontology or name, multiple mappings can be retrieved, but when finding an overall mapping, only one (per method) is chosen. 

### Software engineering best practices
This package was developed before I discovered most best practices for package development, e.g. test coverage, continuous integration, or detailed documentation. 
I think this kind of software development would be necessary in order for this package to gain wider usage, as I explain in {ref}`filip-future-work`. 
