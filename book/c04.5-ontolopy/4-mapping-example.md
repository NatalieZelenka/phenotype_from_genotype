(ontolopy-mapping-example)=
# Example use: mapping samples to phenotypes via tissues
[//]: # (TODO: Write intro to examples)
[//]: # (TODO: Rename examples)

## Creating sample-to-tissue mappings
[//]: # (TODO: Open as ipynb and bring over mapping bits and pieces from c05-filter)


(tissue-group-mapping)=
### Re-grouping samples based on tissues
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

## Creating tissue-to-phenotype mappings

## Creating sample-tissue-to-potential-phenotype mappings

## Harmonisation of gene expression data
[//]: # (TODO: Show a snippet of code and output)
[//]: # (TODO: Write to explain the difference between this and the rest, i.e. that it's extra useful to use the SAME specific tissue names)

{numref}`c05.3-data-wrangling` shows an example of how this package can be used to create a sample to tissue mapping for four different gene expression data sets.

A similar methodology can be used to map your samples to other concepts, for example:
- dividing your samples into those cell types that can differentiate (turn into other cell types, i.e. pluripotent, stem and precursor cells), and those that can't. 
- dividing your samples into those that are mapped to certain classes of diseases (e.g. heart disease, cancer) and those that aren't.