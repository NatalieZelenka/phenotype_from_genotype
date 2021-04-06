(ontolopy-examples)=
# Example uses

[//]: # (TODO: Add CL + variuous citations)
The Uberon ontology connects many different ontologies and dictionaries, including many anatomy ontologies for different species (mouse, xenopus, fly, zebrafish) and specific structures (Neuroscience Information Framework (NIF) Gross Anatomy, Edinburgh Human Developmental Anatomy), as well as phenotype ontologies (Mammalian Phenotype Ontology, Gene Ontology){cite}`Mungall2012-nc`.
As such it is used by a wide variety of researchers.

## Example 1: Harmonisation of gene expression data
[//]: # (TODO: Show a snippet of code and output)

{numref}`c05.3-data-wrangling` shows an example of how this package can be used to create a sample to tissue mapping for four different gene expression data sets.

A similar methodology can be used to map your samples to other concepts, for example:
- dividing your samples into those cell types that can differentiate (turn into other cell types, i.e. pluripotent, stem and precursor cells), and those that can't. 
- dividing your samples into those that are mapped to certain classes of diseases (e.g. heart disease, cancer) and those that aren't.

(tissue-group-mapping)=
## Example 2: Re-grouping samples based on tissues
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
## Example 3: finding inconsistencies in the FANTOM5 data
[//]: # (TODO: Add a table here of all the inconsistencies: medium priority)
For the FANTOM5 data, disagreements between these mappings revealed problems in the biological ontologies and experiment metadata that were provided to the package in order to create the mappings. 
These could then be fed back to the maintainers of these ontologies and datasets in order to improve/correct them. 

Disagreements between the tissue-sample mappings created through the (FANTOM, CL and Uberon) ontologies and those created using human annotation illuminates what may be a lack of specificity, incompleteness in, or disagreement between FANTOM, CL, or Uberon annotations, either in creating ontologies or annotating tissues to samples. 
The process of mapping FANTOM to Uberon tissues found twenty-two such disagreements, of which FANTOM, Uberon, and CL where appropriate have been informed via GitHub issues, some of which have already sparked changes in the ontologies. 

Three different types of example are described below, to give an idea of how multiple mappings may be used to improve annotation.

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