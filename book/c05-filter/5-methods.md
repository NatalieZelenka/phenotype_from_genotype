<!-- #region -->
(filter-methods)=
# Methods
[//]: # (TODO: Functionality/links to package in another section)

[//]: # (TODO: Overview of design of "experiment" here: write)
In order to test `filip`...
- Create inputs
- Interrogate mapping quality
- Run filip
    - Choose cut-off
- Validate prediction improvement
- 


## Creating inputs
Two types of input are needed for `filip`: protein function predictions and a background file.
If `filip` was a filter coffee machine, the background file would be the filter paper. 
It is the part that determines what can and cannot pass through the `filip` filter and it can be used with any kind of input predictions (coffee). 
The metaphor (mercifully) ends here, since once we have the background file can be reused for any different protein function predictor, as long as they are predicting phenotype terms that are in our background file.

There are multiple steps that must be carried out in order to create these inputs:
1. {ref}`Create *Protein function predictions*<create-protein-function-predictions>` by running a predictor on the CAFA2 and CAFA3 targets.
2. {ref}`Create the *Background file*<create-background-file>` is created from the expression data and mappings, by:
    A. Mapping {ref}`from gene/transcript expression to protein<gene-to-protein-expression>`.
    B. Mapping from expression samples to phenotype terms using `Ontolopy`. We can break this down into:
        i. Mapping {ref}`from samples to tissue<samples-to-tissue>` (Uberon terms)
        ii. Mapping {ref}`from tissue to phenotype<tissue-to-phenotype>`

Steps (2A) and (2Bi) and  must be done for each different input expression data set. 
Step (2Bii) currently needs to be done for each set of predictions (phenotype terms) - since it's the most computationally expensive part of the process, so it's necessary to do it for the smallest number of predictions possible (and therefore do it last).

[//]: # (TODO: Signpost order)
<!-- #endregion -->

(create-protein-function-predictions)=
### Creating protein function predictions

[//]: # (TODO: Explain choice)

[//]: # (TODO: Create naive)

#### DcGO
To create the input to DcGO, I used:
- BioPython{cite}`Cock2009-py`'s `Bio.SeqIO` interface for reading CAFA FASTA files.
- SUPERFAMILY{cite}`Gough2001-ct` [domain assignments for Homo Sapiens](https://supfam.mrc-lmb.cam.ac.uk/SUPERFAMILY/cgi-bin/save.cgi?var=ht;type=ass).
- UniprotKB{cite}`Pundir2016-vv`'s [mapping tool](https://www.uniprot.org/uploadlists/) to create a mapping between the UniprotKB id's provided by CAFA and the ENSP ID's used by SUPERFAMILY. 

[//]: # (TODO: Make reproducible by also having scripts that I used to run etc)

The script to create the UniprotKB IDs is {download}`available here<scripts/fasta_to_uniprot.py>`, to create the input for DcGO is {download}`here<scripts/make_dcgo_input.py>`.
Then, to create the DcGO-only entry, I used the `DcGOR` library{cite}`Fang2014-hx` (the `dcAlgoPredictMain` function).

```python
%load_ext autoreload
%autoreload 2

import logging
import ontolopy as opy
import pandas as pd 
import filip
from myst_nb import glue

# TODO: Stop this cell showing up
```

```python
# TODO: Make drop-down. Glue table.
dcgo_predictions = pd.read_csv('data/created/dcgo_submission.txt', sep='\t', skiprows=4, index_col=0, header=None)
dcgo_predictions.drop('END', inplace=True)
dcgo_predictions.columns = ['phenotype', 'confidence']
dcgo_predictions.index.rename('protein', inplace=True)
display(dcgo_predictions.head())
glue('dcgo-cafa2-predictions', len(dcgo_predictions.index), display=False)
glue('dcgo-cafa2-proteins',len(dcgo_predictions.index.unique()), display=False)
glue('dcgo-cafa2-phenotypes', len(dcgo_predictions.phenotype.unique()), display=False)
```

The DcGO predictions contain only {glue:text}`dcgo-cafa2-predictions` of {glue:text}`dcgo-cafa2-proteins` proteins and {glue:text}`dcgo-cafa2-phenotypes` phenotype terms (all of which are `GO` terms).

[//]: # (TODO: Explain why all GO terms)


(create-background-file)=
### Create *background* file

(gene-to-protein-expression)=
#### Mapping from gene to protein expression






(samples-to-tissue)=
#### Mapping from samples to tissue

```python
# Read in CAFA phenotypes
fantom_obo_file = '../c06-combining/data/experiments/fantom/ff-phase2-170801.obo.txt'

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
uberon_obo_file = '../c06-combining/data/uberon_ext_210321.obo' # TODO: maybe want to use old one and compare

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

```{margin} Stop words
:name: stop-words
Stop words are words that are filtered out before processing text using Natural Language Processing (NLP) methods.
These are usually very common words (e.g. “and”, ”the”), or word which are meaningless in the context of the analysis. 
```
Failing this, text-matching is used to assist in mapping based on phenotype term names:
- First {ref}`stop words<stop-words>` are removed, using the base list in the Natural Language Toolkit (`nltk`) Python Package{cite}`Bird2006-xu`, and a small number of manually curated phenotypic stopwords (e.g. “phenotype”, “abnormality”).
- Then, an exact match between an UBERON term’s name or synonyms and phenotype term’s name is searched for. 
- If such a match does not exist, individual words from the phenotype term name or synonyms are then searched for exactly, such that the HP term “abnormality of the head and neck” would be mapped to UBERON’s “head” and “neck” terms (but never “neck of radius”). 
- In cases where multiple terms are found, a common parent would be searched for, in the case of this example, “craniocervical region”. 

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
#     'CL:0011115', # precursor cell --> exclude precursor cells because they only develop into one cell type
# #     'CL:0000048', # multi fate stem cell
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

<!-- #region -->


(tissue-to-phenotype)=
#### Mapping uberon terms to phenotype terms
[//]: # (TODO: explain it's equally easy to add in more)
We make use of two ontologies (and therefore two `.obo` files) to create the uberon-to-phenotype mapping, these are:
- Uberon, UBERON, uberon-ext.obo, tissue
- Gene Ontology, GO go.obo, phenotype

These also contain references to other external ontologies, such as the the Human Phenotype Ontology, the Disease Ontology, Cell Ontology, the NCBI Taxonomy Ontology, etc.

(combining-background)=
#### Combining into background file
<!-- #endregion -->

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

```python
# TODO: EDA of mapping coverage (CL, UBERON, name)
```





```python

```

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

```python
mapped_by_tissue_name = merged.sample_map_by_name(names_info[tissue_col])
```

```python
# TODO: Choose some of these rows and put into a table and disucss
# For example, limitations of Ontolopy, FF:10189-103D9 has name: appendix, adult, rep1, but no tissue, therefore it hasn't been mapped by name to appendix... We might be able to create tissue information from names, but it's not necessary since we're defaulting to the ontology mapping anyway.
mapped_by_tissue_name[mapped_by_tissue_name['to'].isna()]
```

```python
overall, disagreements = merged.get_overall_tissue_mappings(map_by_ont=tissue_relations, map_by_name=mapped_by_tissue_name)
```

```python
display(overall)
```

```python
display(disagreements)
# TODO: Map by hand and put in thesis, e.g. nasal epithelial cells should be neither: but actually: UBERON:0005384 nasal cavity epithelium
```

```python
mapped_by_tissue_name.loc['FF:10379-105H1']
```

```python
num_uberon_mapped = len(overall['overall'].unique()) - 1
print(f'{len(overall.index)} samples mapped to {num_uberon_mapped} unique UBERON terms.')
```

```python
# TODO: read in accession to new sample id
old_to_new_ff = {}
for new_ff in samples_info.index:
    old_ff = new_ff.split('_')[0]
    try:
        old_to_new_ff[old_ff].append(new_ff)
    except:
        old_to_new_ff[old_ff] = [new_ff]
```

```python
total = 0
for uberon in overall_mapping['overall'].unique():
    if uberon is None:
        continue
    tissue_accession = [len(old_to_new_ff[x]) for x in overall_mapping[overall_mapping['overall'] == uberon].index]
    # TODO: might be mulitple samples per accession
#     break
    total += sum(tissue_accession)
    print(uberon, merged_ont[uberon]['name'], sum(tissue_accession))
    
print(total)
```


### Further data cleaning: adding disease model information and non-tissue-specific samples
[//]: # (TODO: Write: removal of non-tissue-specific samples: do it in the previous section "unclassifiable")


<!-- #region -->
## When are transcripts "expressed"?

The idea behind `filip` is that some proteins are predicted to affect phenotypes that they are unable to affect, because the environment in the tissue or cell means that the protein isn't around to perform it's function (or fail to). 
And, we have a measure of gene expression, for which many proteins have `0` counts (and therefore `0` TPM) in many tissues, so we could apply the filter to this cut-off. But is it meaningful to do so?

[//]: # (TODO: Image showing gene expression as stochastic, e.g. mRNAs and ribosomes running into eachother/ribosomes running into some promoters before others)

Like all chemical reactions, transcription is a stochastic process; there is an element of randomness; to describe if a transcription event will happen at a specific moment you have to use statistics.
Genetically identical organisms with the same environment have different measured gene expression patterns{cite}`Raj2008-jy` and the same can be said for single cells from the same organism{cite}`Kim2015-mc`.
The reason that it's hard to predict with precision whether a given protein will be transcribed at a given moment is that it depends on the concentration of different molecules in the cell and the energy of the system. 
Transcription events which have a very low probability of occuring will happen sometimes and we will measure this. 
If we sequenced the transcriptome in infinite depth, we might expect all transcripts to be expressed at some level.


[//]: # (TODO: check that I mentioned counts in sequencing technology section)
[//]: # (TODO: Cite gene expression known phenotypes)

```{margin} Transcriptional noise
:name: transcriptional-noise
Transcriptional noise is variation in rates of transcription due to the implicit stochasticity of the reaction process. The implication is that many transcripts with low counts do not play a big role and cells are known to have mechanisms to protect themselves from this noise{cite}`Raj2008-jy,Eling2019-hn`. Since is difficult to distinguish between meaningful and non-meaningful and expression, in differential expression analyses it is common to remove low count transcripts{cite}`Anders2013-zh,Love2021-jf`. 
Similar noise occurs in the process of translation (translational noise).
```

[//]: # (TODO: Cross-ref batch effects, or put in an aside here)

When we look at expression data for a sample, it will just be a snapshot of the transcription in that sample, and one that isn't necessarily representative of what's happening all the time.
As we saw in {num-ref}`fantom-protein-distribution`, very low count values in a sample are extremely common, and these are usually considered to be difficult to distinguish from {ref}`transcriptional-noise`: low levels of transcription with little effect are often randomly happening in the cell. 
In addition to the biological stochasticity (which could possibly create phenotypic differences), RNA-Seq is sensitive to technical experimental artefacts (batch effects) due to differences in RNA extraction and library preparation{ref}`Conesa2016-gq`.
In both cases, it is low counts where this is most difficult to correct for
So, it isn't necessarily meaningful to take all genes expressed above `0` TPM as a sensible cut-off for whether a gene counts as "expressed" or not in a tissue: when I dichotomise proteins as "expressed" or "not expressed", I am using this as a convenient shorthand for "meaningfully expressed" or "not meaningfully expressed".

We also know that proteins that do cause phenotypes are likely to be highly expressed in tissues related to the phenotype, so we definitely want to keep protein-phenotype predictions where proteins are produced at high levels in the tissue of interest, but when do TPM levels become low enough that we would want to exclude them?

### Expression cut-off
[//]: # (TODO: Write about other papers that have used a cut-off for expression)
[//]: # (TODO: Do a way zoomed in graph that shows just the first 1-200 for a small number of samples, including biological and technical replicates - but choose tissue-mappable, non-disease samples)

One straight forward way is to choose a cut-off, and choosing this for TPM-normalised data rather than counts or R/FKPM values is sensible as it allows for comparing between different samples. 
The cut-off was chosen by plotting the distribution of TPM expression and choosing a value below which there appeared to be little noise (10 TPM) between biological and technical replicates.

### Expression score
[//]: # (TODO: Write)
However, for CAFA, it wasn't necessary to choose a single cut-off, since the submission format is to choose a single score.
<!-- #endregion -->

```python

```

## Creation of input predictions
[//]: # (TODO: describe why necessary and what done with)
[//]: # (TODO: Link to sent-in dcGO file)

### Naive predictions



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
There is no penalty for making a broad guess, or reward for making a precise one. This is one of the reasons that the naive method does so well: for example it is not penalised for guessing that the root term of the GO BPO ontology Biological Process is related to every gene. 

Due to the nature of the validation set, it’s possible that the best-scoring CAFA methods simply predict which associations are likely to be discovered soon (i.e. associations to genes people are currently studying).

```python

```


