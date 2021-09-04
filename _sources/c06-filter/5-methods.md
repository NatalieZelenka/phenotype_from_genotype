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

(filter-methods)=
# Validation method

In order to fairly test Filip, I entered it in the third {ref}`CAFA<CAFA>` competition, where it could be independently assessed by other researchers.
In CAFA, each researcher can enter up to three methods, so I tested Filip by entering DcGO alone, and DcGO plus Filip, so that I could compare their performances.

<!--
## Creating inputs
There are three main inputs to Filip: 

There are multiple steps that must be carried out in order to create these inputs:
1. {ref}`Create *Protein function predictions*<create-protein-function-predictions>` by running a predictor on the CAFA2 and CAFA3 targets.
2. {ref}`Create the *Background file*<create-background-file>` is created from the expression data and mappings, by:
    A. Mapping {ref}`from gene/transcript expression to protein<gene-to-protein-expression>`.
    B. Mapping from expression samples to phenotype terms using `Ontolopy`. We can break this down into:
        i. Mapping {ref}`from samples to tissue<samples-to-tissue>` (Uberon terms)
        ii. Mapping {ref}`from tissue to phenotype<tissue-to-phenotype>`

-->

(cafa3-test-set)=
## Test set: CAFA3 
After initial development, I entered DcGO only, and `filip` plus DcGO into the CAFA3 competition in order to test `filip` on an unseen dataset.

This meant that I did not download the CAFA3 ground-truth, as this analysis was done by the CAFA3 team, but only the [CAFA3 targets](https://www.biofunctionprediction.org/cafa-targets/CAFA3_targets.tgz), these continue to be available through the CAFA website.

Again, I used only the human targets (file `target.9606.fasta`). 
This is again a FASTA file, with the same format as for CAFA2, this time containing `20197` targets proteins.

## Filip inputs
Two types of input are needed for Filip: 
1. Protein function predictions 
2. Normalised gene expression data.
3. A map from gene expression samples to Uberon tissues. 

I described the gene expression data and metadata for (2) and (3) described in the previous section. 

(create-protein-function-predictions)=
### Creating protein function predictions (DcGO)
I used DcGO as a test since I knew that it's structure-centric prediction method didn't include any gene expression information.

To create the input to DcGO, I used:
- BioPython{cite}`Cock2009-py`'s `Bio.SeqIO` interface for reading CAFA FASTA files.
- SUPERFAMILY{cite}`Gough2001-ct` [domain assignments for Homo Sapiens](https://supfam.mrc-lmb.cam.ac.uk/SUPERFAMILY/cgi-bin/save.cgi?var=ht;type=ass).
- UniprotKB{cite}`Pundir2016-vv`'s [mapping tool](https://www.uniprot.org/uploadlists/) to create a mapping between the UniprotKB id's provided by CAFA and the ENSP ID's used by SUPERFAMILY. 

The script to create the UniprotKB IDs is {download}`available here<scripts/fasta_to_uniprot.py>`, to create the input for DcGO is {download}`here<scripts/make_dcgo_input.py>`.
Then, to create the DcGO-only entry, I used the `DcGOR` library{cite}`Fang2014-hx` (the `dcAlgoPredictMain` function).

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import pandas as pd 
from myst_nb import glue

# TODO: Make drop-down. Glue table.
dcgo_predictions = pd.read_csv('data/created/dcgo_submission.txt', sep='\t', skiprows=4, index_col=0, header=None)
dcgo_predictions.drop('END', inplace=True)
dcgo_predictions.columns = ['phenotype', 'confidence']
dcgo_predictions.index.rename('protein', inplace=True)
glue('dcgo-predictions-view', dcgo_predictions.head())
glue('dcgo-cafa2-predictions', len(dcgo_predictions.index), display=False)
glue('dcgo-cafa2-proteins', len(dcgo_predictions.index.unique()), display=False)
glue('dcgo-cafa2-phenotypes', len(dcgo_predictions.phenotype.unique()), display=False)
```

The DcGO predictions contain only {glue:text}`dcgo-cafa2-predictions` of {glue:text}`dcgo-cafa2-proteins` proteins and {glue:text}`dcgo-cafa2-phenotypes` phenotype terms (all of which are `GO` terms).

+++



+++

<!--

(samples-to-tissue)=
#### Mapping from samples to tissue

```python
# Read in CAFA phenotypes
fantom_obo_file = c08-combining

fantom_obo = opy.load_obo(
    file_loc=fantom_obo_file, 
    ont_ids=['GO', 'CL', 'UBERON', 'FF', 'DOID'], 
)
```

```python
# TODO: glue sizes of ontologies maybe

samples_info_file = 'data/cleaned_pre_input/samples_info.csv'
tissue_col = 'Characteristics[Tissue]'
desc_col = 'Charateristics [description]'

samples_info = pd.read_csv(samples_info_file, sep='\t', comment='#', index_col=0)
```

```python
samples_info['FF'] = 'FF:' + samples_info['Source Name']
names_info = samples_info[['FF',tissue_col]].set_index('FF')
```

```python

```

```python
# Use Ontolopy to read in fantom and uberon and combine.
uberon_obo_file = c08-combining # TODO: maybe want to use old one and compare

uberon_obo = opy.load_obo(
    file_loc=uberon_obo_file, 
    ont_ids=['GO', 'UBERON','CL'], 
)

go_obo_file = 'data/ontologies/go.obo'
go_obo = opy.load_obo(
    file_loc=go_obo_file, 
    ont_ids=['HP', 'GO', 'CL', 'UBERON', 'DOID'], 
)

merged = uberon_obo.merge(new=go_obo)
```

```python
# Create tissues and phenotypes from predictions and input expression data
phenotypes = set(dcgo_predictions.phenotype.unique()) & set(go_obo)
tiessues = overall['overall'].unique()
print(len(phenotypes), len(tissues))
```

```python
output_loc_1B = 'data/cleaned_pre_input/1B-phen-to-tissue.tsv'
from_phen_to_tissue = filip.create_tissue_phenotype_mapping(
    obo=merged, 
    source = tissues,
    target = phenotypes,
    output_file=output_loc_1B,
    relations=['GO', 'is_a', 'is_model_for', 'part_of', 'capable_of'])

# output_loc_1B = 'data/cleaned_pre_input/1B-phen-to-tissue.tsv'
# from_phen_to_tissue = filip.create_tissue_phenotype_mapping(
#     obo=merged, 
#     output_file=output_loc_1B,
#     targets=['GO'], 
#     relations=['GO', 'is_a', 'is_model_for', 'part_of', 'capable_of'])
```

```python
from_phen_to_tissue
```

```python
tissue = merged.terms_from(['UBERON'])
phenotype = merged.terms_from(['GO'])
print(len(tissue), len(phenotype))
```

#### Creating an alternate mapping by searching names



```python
# TODO: put the version without these additions into the ontolopy section: use an example of how to find problems.
unmapped_t_cells = [
    'FF:11784-124B2',
    'FF:11791-124B9',
    'FF:11792-124C1',
    'FF:11793-124C2',
    'FF:11794-124C3', 
    'FF:11795-124C4', 
    'FF:11796-124C5', 
    'FF:11797-124C6', 
    'FF:11798-124C7', 
    'FF:11906-125F7',
    'FF:11907-125F8',
    'FF:11908-125F9', 
    'FF:11909-125G1', 
    'FF:11913-125G5', 
    'FF:11914-125G6', 
    'FF:11915-125G7', 
    'FF:11916-125G8', 
    'FF:11917-125G9', 
    'FF:11918-125H1', 
    'FF:11919-125H2', 
    'FF:11920-125H3',
]

CD4_positive_T_cell_sample = 'FF:0000031'

for t_cell in unmapped_t_cells:
    try:
        merged[t_cell]['is_a'].append(CD4_positive_T_cell_sample)
    except KeyError:
        merged[t_cell]['is_a'] = [CD4_positive_T_cell_sample]
```

```python
# TODO: Check if this is relevant to what I did before
# no_cl = {}
# for key in merged_ont.keys():
#     if key[:2] != 'CL':
#         no_cl[key] = merged_ont[key]
# map_by_ont_no_cl = map_tissue_by_ontology(samples, no_cl)

# # TODO: Create table showing how adding CL increases coverage (and maybe also relation types)
# print(len(map_by_ont_no_cl[~map_by_ont_no_cl['UBERON'].isna()].index.unique()))
# print(len(map_by_ont[~map_by_ont['UBERON'].isna()].index.unique()))
# print(len(map_by_ont_no_cl[map_by_ont_no_cl['UBERON'].isna()].index.unique()))
# unmapped_by_ont = map_by_ont[map_by_ont['UBERON'].isna()].index.unique()
# print(len(unmapped_by_ont))
```

```python
# samples = list(pd.read_csv('data/cleaned_pre_input/ff_accessions_to_keep.txt', sep='\t', header=None, comment='#')[0])
# samples
```

```python
tissue_relations = merged.sample_map_by_ont(names_info.index)
```

```python
print(len(names_info.index), tissue_relations.shape)
```

```python
# TODO: Move example of checking if something is a stem cell to Ontolopy section

# stem_cell = [
#     'CL:0011115', # precursor cell exclude precursor cells because they only develop into one cell type
#     'CL:0000048', # multi fate stem cell
# #     'CL:0000034', # stem cell
# #     'CL:0000723', # stomatic stem cell
# #     'CL:0008001', # hematopoietic precursor cell (-> missing to `is_a` precursor cell)
# ]

# relations = ['is_a','related_to','part_of','intersection_of','union_of', 'derives_from']  # NOT 'develops_from'
# for unmapped in map_by_ont[map_by_ont['UBERON'].isna()].index:
#     print(unmapped, fantom_obo.ont[unmapped]['name'])
#     tissue_relations = obo.Relations(
#         relations_of_interest=relations, 
#         source_terms=[unmapped],
#         target_term=stem_cell,
#         ont=merged_ont,
# #         print_=True
#     )

#     if pd.isna(tissue_relations.relations[0][0]):
#         print('NON STEM CELL')
#         print(unmapped, fantom_obo.ont[unmapped]['name'])
#         print(samples_info.loc[unmapped]['Characteristics[Tissue]'])
#     else:
#         print('STEM CELL')
#         print(unmapped, fantom_obo.ont[unmapped]['name'])
#         print(samples_info[samples_info.index.str.contains(unmapped)]['Characteristics[Tissue]'])

#     print('\n\n')
```




(tissue-to-phenotype)=
#### Mapping uberon terms to phenotype terms
[//]: # (TODO: explain it's equally easy to add in more)
We make use of two ontologies (and therefore two `.obo` files) to create the uberon-to-phenotype mapping, these are:
- Uberon, UBERON, uberon-ext.obo, tissue
- Gene Ontology, GO go.obo, phenotype

These also contain references to other external ontologies, such as the the Human Phenotype Ontology, the Disease Ontology, Cell Ontology, the NCBI Taxonomy Ontology, etc.

(combining-background)=
#### Combining into background file

### Quality of mapping-by-ontology
#### Overall


```python
# TODO Create table with FF, FF name, tissue_col, to, and to['name'] and discuss
display(tissue_relations)
```

#### Unclassifiable

```python
# TODO: put in a table so that I can discuss
# TODO: explain that the mapping including CL terms and all types of mapping, does find a mapping for everything that the ontology-creators finishing classifying. And then lacking any expertise, I will map these manually to T-cell.
unmapped_by_ont = tissue_relations[tissue_relations['to'].isna()].index
for sample_id in unmapped_by_ont:
    print('Unmapped', sample_id, merged[sample_id]['name'])
```

```python
# TODO: Write about how unclassifable stuff maps to too general tissue.
samples_info[tissue_col].unique()
unclassifiables = samples_info[samples_info[tissue_col]=='unclassifiable']
# unclassifiables.index 
for unclassifiable in unclassifiables.index:
    print(tissue_relations.loc[unclassifiable]['relation_text'])
```

#### ANATOMICAL SYSTEM

```python
# TODO: Write about how ANANTOMICAL SYSTEM stuff maps to tissues accurately.
# TODO: Put in a table
samples_info[tissue_col].unique()
unclassifiables = samples_info[samples_info[tissue_col]=='ANATOMICAL SYSTEM']
for unclassifiable in unclassifiables.index:
    print(merged[unclassifiable]['name'], merged[tissue_relations.loc[unclassifiable]['to']]['name'])
```

```python

samples_info[tissue_col].unique()
```

### Via ontologies
[//]: # (TODO: Write)

The extended Uberon ontology is first interrogated for any existing relation to the term in the ontology using `uberon-py`. 

-->

+++ {"tags": ["remove-input", "remove-output"]}

<!--
```python
# TODO: Do nothing with this (except maybe explain that it was checked, maybe add it as an uberon-py example)
def get_missing_human_annotation(samples, ont):
    human_relations_of_interest = ['is_a']
    human_related = opy.Relations(
        allowed_relations=human_relations_of_interest, 
        sources=samples,
        targets=['FF:0000210'], 
        ont=ont,
    )
    missing_human_ann = human_related[human_related['to'].isna()]
    return missing_human_ann
missing_human_ann = get_missing_human_annotation(names_info.index, ont=merged)
missing_human_ann['name'] = pd.Series([merged[x]['name'] for x in missing_human_ann.index], index= missing_human_ann.index)
species_col = 'Chracteristics [Species]'
missing_human_ann['labeled species'] = pd.Series([samples_info.loc[x][species_col] for x in missing_human_ann.index], index=missing_human_ann.index)
display(missing_human_ann)

human = 'Human (Homo sapiens)'
assert(pd.Series.all(samples_info[samples_info.index.isin(list(missing_human_ann.index))][species_col] == human))
```
-->

```{code-cell} ipython3
:tags: [remove-input, remove-output]

# mapped_by_tissue_name = merged.sample_map_by_name(names_info[tissue_col])


# # TODO: Choose some of these rows and put into a table and disucss
# # For example, limitations of Ontolopy, FF:10189-103D9 has name: appendix, adult, rep1, but no tissue, therefore it hasn't been mapped by name to appendix... We might be able to create tissue information from names, but it's not necessary since we're defaulting to the ontology mapping anyway.
# mapped_by_tissue_name[mapped_by_tissue_name['to'].isna()]

# mapped_by_tissue_name.loc['FF:10379-105H1']

# num_uberon_mapped = len(overall['overall'].unique()) - 1
# print(f'{len(overall.index)} samples mapped to {num_uberon_mapped} unique UBERON terms.')

# old_to_new_ff = {}
# for new_ff in samples_info.index:
#     old_ff = new_ff.split('_')[0]
#     try:
#         old_to_new_ff[old_ff].append(new_ff)
#     except:
#         old_to_new_ff[old_ff] = [new_ff]

# total = 0
# for uberon in overall_mapping['overall'].unique():
#     if uberon is None:
#         continue
#     tissue_accession = [len(old_to_new_ff[x]) for x in overall_mapping[overall_mapping['overall'] == uberon].index]
#     # TODO: might be mulitple samples per accession
# #     break
#     total += sum(tissue_accession)
#     print(uberon, merged_ont[uberon]['name'], sum(tissue_accession))
    
# print(total)
```

## Running Filip

### Mapping between Uberon tissues and phenotypes
I used an early version of {ref}`ontolopy<c06-ontolopy>` to map between uberon tissues and phenotypes.
I describe this process in detail in {numref}`ontolopy-mapping-example`: for CAFA3, I used phenotypes present in DcGO predictions as targets, and looked for mappings only including Uberon terms (not Cell Ontology terms).

### Choosing an expression cut-off
The cut-off was chosen by plotting the distribution of TPM expression and choosing a value below which there appeared to be little noise (50 TPM) between biological and technical replicates.

+++

(cafa-validation-method)=
## Validation Methodology

### CAFA Validation 
This confidence score allows for a range of possible sets of predictions, depending on the threshold parameter {math}`\tau`. 
Precision (the proportion of selected items that are relevant), and recall (the proportion of relevant items that are selected) are defined as:

{math}`precision = p = \frac{t_p}{t_p + f_p}`
{math}`recall = r = \frac{t_p}{t_p + f_n}`

Precision-recall curves are generally used to validate a predictors performance, but the {math}`F_1` measure combines these into a single measure of performance:

{math}`F_1 =2/ \frac{precision \cdot recall}{precision + recall}`

Since the precision and recall will be different for any {math}`\tau`, the {math}`F_{max}` score is the maximum possible {math{`F_1`} for any value of $\tau$.

[//]: # (TODO: explain the below a little more: how many measures does that make? 2 x2 = 4?)
CAFA validation can either be term-centric or protein-centric. For each option, submissions are assessed per species and for wholly unknown and partially known genes separately.

### Limitations of validation method
There is no penalty for making a broad guess, or reward for making a precise one. 
This is one of the reasons that the naive method does so well: for example it is not penalised for guessing that the root term of the GO BPO ontology Biological Process is related to every gene. 

[//]: # (TODO: Link to gene section)
Due to the nature of the validation set, it’s possible that the best-scoring CAFA methods simply predict which associations are likely to be discovered soon (i.e. associations to genes people are currently studying, which is well-predicted by genes that are currently being studied).
