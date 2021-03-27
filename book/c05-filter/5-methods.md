<!-- #region -->
(filter-methods)=
# Methods
[//]: # (TODO: Overview here?)
[//]: # (TODO: Code here)
[//]: # (TODO: Links to packages, etc)
[//]: # (TODO: See how/if I use the uberon-obo file)

## Further data cleaning: adding disease model information and non-tissue-specific samples
[//]: # (TODO: Write: removal of disease and non-tissue-specific samples?)

### Mapping samples to uberon terms

### Data cleaning

### Creating `filip` input


## Mapping multi-species phenotype terms to samples

### Mapping phenotype terms to uberon terms

### Matching via uberon terms
<!-- #endregion -->

```python
%load_ext autoreload
%autoreload 2
```

```python
import logging

# TODO: make sure `is_obsolete` is loaded in uberon_py. If not: make sure it now is. Also make sure `replaced_by` is captured. And make sure this is a relation of interest by default.
# TODO: add merge ontologies to uberon_py
# TODO: fix comment in uberon_py - it only saves part of the line (first word)
# TODO: have merge check for ontology wrongness + have that separately (for when you edit ontologies)

def merge(a, b, path=None):
    c = a.copy()
    "Recursively merges (nested) dictionary b into dictionary a. Prefers a: a should be the more up-to-date ontology."
    if path is None: path = []
    for key in b:
        if key in c:
            if isinstance(c[key], dict) and isinstance(b[key], dict):
                merge(c[key], b[key], path + [str(key)])
            elif c[key] == b[key]:
                pass # same leaf value
            elif isinstance(c[key], list) and isinstance(b[key], list):
                c[key] = list(set(b[key]) | set(c[key]))
            else:
                if key == 'namespace':
                    c[key] = f"Combined {c[key]} and {b[key]}"
                elif key == 'name':
                    # we expect some differences in name, due to e.g. terms becoming obsolete 
                    logging.info(f"Unmatching names: {c[key]} =/= {b[key]}, keeping the former.")
                else:
                    logging.error(f"For key {key}, {c[key]} =/= {b[key]}. Unsure which to choose.")
        else:
            c[key] = b[key]
    assert(len(c) == (len(a) + len(b) - len(set(a.keys()) & set(b.keys()))))
    return c

```

```python
# TODO: Map to UBERON + CELL tissues

fantom_obo_file = '../c06-combining/data/experiments/fantom/ff-phase2-170801.obo.txt'
# uberon_obo_file = '../c06-combining/data/uberonext_obo.txt' # TODO: maybe want to use new one and compare
uberon_obo_file = '../c06-combining/data/uberon_ext_210321.obo' # TODO: maybe want to use old one and compare

fantom_obo = obo.Obo(fantom_obo_file, ont_ids = ['HP', 'GO', 'CL', 'UBERON', 'FF', 'DOID'])
uberon_obo = obo.Obo(uberon_obo_file, ont_ids = ['GO', 'HP', 'UBERON','CL'])
merged_ont = merge(uberon_obo.ont, fantom_obo.ont)

# TODO: glue sizes of ontologies maybe
```

```python
from uberon_py import obo

```

```python
# TODO: write
# NOTE: would need to ensure that NCBI taxon ontology is present in order to be able to do this, since there are taxon terms for vertebrates, etc, not just individual species.
# def restrict_to_taxon(ont, ncbi_id, valid_terms = ['UBERON'], keep_dubious=False, only_yes=False):
#     """
#     Loops through valid_terms terms in ontology `ont`, and removes any that are never in taxon with ID `ncbi_id`
#     """
#     yes_relations = ['only_in_taxon', 'present_in_taxon']
#     never = 'never_in_taxon'
#     dubious = 'dubious_for_taxon'
    
#     for term in ont.keys():
#         if term.split(':')[0] not in valid_terms:
#             continue
        
        
        
    # TODO: check that you've read in the 
```

```python
import pandas as pd 
samples = list(pd.read_csv('data/cleaned_pre_input/ff_accessions_to_keep.txt', sep='\t', header=None, comment='#')[0])
# samples
```

```python
samples_info = pd.read_csv('data/cleaned_pre_input/samples_info.csv', sep='\t', comment='#', index_col=0)
samples_info
```

```python

```

```python
def map_tissue_by_ontology(sample_ids, 
                           combined_obo, 
                           too_general_tissues = None,
                           tissue_relations_of_interest = None,
):
    """
    """
    if not too_general_tissues:
        too_general_tissues = [
            'UBERON:0000061',  # anatomical structure
            'UBERON:0000479',  # tissue
            'UBERON:0000467',  # anatomical system
            'UBERON:0011216',  # organ system subdivision
            'UBERON:0000922',  # embryo
        ]

    if not tissue_relations_of_interest:
        tissue_relations_of_interest = [
            'is_a', 
            'related_to', 
            'part_of', 
            'derives_from', 
            'intersection_of', 
            'union_of', 
            'is_model_for', 
            'replaced_by', 
            'develops_from',
        ]
        
    # TODO: Change uberon_py and add this functionality.
    # TODO: Write function string
    # TODO: Change uberon-py excluded tissues.
    uberon_identifier = 'UBERON'  # interested in relationships to uberon terms.
    tissue_relations = obo.Relations(
        relations_of_interest=tissue_relations_of_interest, 
        source_terms=sample_ids,
        target_term=uberon_identifier,
        ont=combined_obo, 
        excluded_terms=too_general_tissues,
    )
    
    tissue_map_ont = []
    for index, row in tissue_relations.relations.iterrows():
        relation_string = row[0]
        if pd.isna(relation_string):
            uberon = None
        else:
            uberon = relation_string.split('_')[-1]
        tissue_map_ont.append([index, relation_string, uberon])
    tissue_map_ont = pd.DataFrame(tissue_map_ont, columns = ['Sample IDs', 'Relation String', 'UBERON'])
    tissue_map_ont = tissue_map_ont.set_index('Sample IDs')
        
    return tissue_map_ont
```

```python
no_cl = {}
for key in merged_ont.keys():
    if key[:2] != 'CL':
        no_cl[key] = merged_ont[key]
map_by_ont_no_cl = map_tissue_by_ontology(samples, no_cl)
```

```python
map_by_ont = map_tissue_by_ontology(samples, merged_ont)
```

```python
def get_leaves(ont, term_types=None, relations_of_interest=None):
    """
    term_types = None: get all leaf terms
    """
    if not relations_of_interest:
        relations_of_interest = [
            'is_a', 
            'related_to', 
            'part_of', 
            'derives_from', 
            'intersection_of', 
            'union_of', 
            'is_model_for', 
            'replaced_by', 
            'develops_from',
        ]
    
    leaves = set(ont.keys())
    if term_types is not None:
        assert(isinstance(term_types, list))
        assert(all([':' not in x for x in term_types])) # don't want 'UBERON:1231239' must be of form 'UBERON', 'GO'
        leaves = {x for x in leaves if x.split(':')[0] in term_types}
    for key in ont.keys():
        for relation in relations_of_interest:
            if relation not in ont[key].keys():
                continue
            related_terms = ont[key][relation]
            assert(isinstance(related_terms, list))
            leaves -= set(related_terms)
    return leaves

leaves = get_leaves(merged_ont, term_types=['UBERON'])
print(len(leaves))
```

```python
# TODO: Create table showing how adding CL increases coverage (and maybe also relation types)
print(len(map_by_ont_no_cl[~map_by_ont_no_cl['UBERON'].isna()].index.unique()))
print(len(map_by_ont[~map_by_ont['UBERON'].isna()].index.unique()))
print(len(map_by_ont_no_cl[map_by_ont_no_cl['UBERON'].isna()].index.unique()))
unmapped_by_ont = map_by_ont[map_by_ont['UBERON'].isna()].index.unique()
print(len(unmapped_by_ont))
```

```python
# TODO: explain that the mapping including CL terms and all types of mapping, does find a mapping for everything that the ontology-creators finishing classifying. And then lacking any expertise, I will map these manually to T-cell.
# TODO: Add functionality to `uberon-py` to add new stuff.

for term in unmapped_by_ont:
    try:
        print(term, fantom_obo.ont[term]['name'], fantom_obo.ont[term]['comment'])
    except:
        print(term, fantom_obo.ont[term]['name'])
```

```python
stem_cell = [
    'CL:0011115', # precursor cell --> exclude precursor cells because they only develop into one cell type
#     'CL:0000048', # multi fate stem cell
#     'CL:0000034', # stem cell
#     'CL:0000723', # stomatic stem cell
#     'CL:0008001', # hematopoietic precursor cell (-> missing to `is_a` precursor cell)
]

relations = ['is_a','related_to','part_of','intersection_of','union_of', 'derives_from']  # NOT 'develops_from'
for unmapped in map_by_ont[map_by_ont['UBERON'].isna()].index:
    print(unmapped, fantom_obo.ont[unmapped]['name'])
    tissue_relations = obo.Relations(
        relations_of_interest=relations, 
        source_terms=[unmapped],
        target_term=stem_cell,
        ont=merged_ont,
#         print_=True
    )

    if pd.isna(tissue_relations.relations[0][0]):
        print('NON STEM CELL')
        print(unmapped, fantom_obo.ont[unmapped]['name'])
        print(samples_info.loc[unmapped]['Characteristics[Tissue]'])
    else:
        print('STEM CELL')
        print(unmapped, fantom_obo.ont[unmapped]['name'])
        print(samples_info[samples_info.index.str.contains(unmapped)]['Characteristics[Tissue]'])

    print('\n\n')
```

```python
print(map_by_ont.index)
```

```python
# TODO: Get uberon to output a more reasonable table (of mappings (with names))
# TODO: uberon should use a hyphen - instad of an underscore for relation strings

# TODO: Write about how unclassifable stuff maps to too general tissue.
tissue_col = 'Characteristics[Tissue]'
samples_info[tissue_col].unique()
unclassifiables = samples_info[samples_info[tissue_col]=='unclassifiable']
# unclassifiables.index 
for unclassifiable in unclassifiables.index:
    print(map_by_ont.loc[unclassifiable]['Relation String'])
```

```python
samples_info.loc['FF:11322-117D8']  
# Skeletal muscle myoblast, develops_into skeletal muscle
```

```python

```

```python
samples_info[samples_info.index.str.contains('FF:12225-129F2')]
```

```python
merged_ont['CL:0000037']
```

### Via ontologies
[//]: # (TODO: Write)

The extended Uberon ontology is first interrogated for any existing relation to the term in the ontology using `uberon-py`. 

```python
# TODO: EDA of mapping coverage (CL, UBERON, name)
```





```python
# TODO: Do nothing with this (keep in disease for now), maybe add it as an uberon-py example
def get_disease_related_samples(samples, ont, print_=False):
    disease_relations_of_interest = ['is_a','is_model_for']
    disease_related = obo.Relations(
        relations_of_interest=disease_relations_of_interest, 
        source_terms=list(samples),
        target_term='DOID',
        ont=ont,
        print_=print_,
    ).relations
    disease_related = disease_related[~disease_related[0].isna()]
    return disease_related
disease_related = get_disease_related_samples(samples=samples, ont=merged_ont)
# display(disease_related)
# print(len(disease_related.index))

# 32 samples are disease related
```

```python
# TODO: Do nothing with this (except maybe explain that it was checked, maybe add it as an uberon-py example)
def get_missing_human_annotation(samples, ont, print_=False):
    human_relations_of_interest = ['is_a']
    human_related = obo.Relations(
        relations_of_interest=human_relations_of_interest, 
        source_terms=samples,
        target_term='FF:0000210', 
        ont=ont,
        print_=print_,
    ).relations
    missing_human_ann = human_related[human_related[0].isna()]
    return missing_human_ann
missing_human_ann = get_non_human_samples(samples, merged_ont)
missing_human_ann['name'] = pd.Series([merged_ont[x]['name'] for x in missing_human_ann.index], index= missing_human_ann.index)
# display(missing_human_ann)

species_col = 'Chracteristics [Species]'
human = 'Human (Homo sapiens)'
assert(pd.Series.all(samples_info[samples_info.index.isin(list(missing_human_ann.index))][species_col] == human))
```

```python
def map_by_name(samples_to_names, samples, ont, target_terms=['UBERON']):
    """
    :param samples_to_names: Pandas series with samples as index and names as values
    :param samples:
    :param ont:
    :param target_terms: A list of target terms, can be a length-1 list. Can be either specific terms (e.g. 'UBERON:0000310') or general term labels (e.g. 'UBERON')
    """
    # TODO: Speed up
    # TODO: Update uberon-py with this version
    samples_to_names = samples_to_names[samples_to_names.index.isin(samples)]
    samples_to_names.dropna(inplace=True)
    assert(isinstance(target_terms, list))
    # TODO: allow dict, if it's a dict convert to a series or vice versa
    assert(isinstance(samples_to_names, pd.Series))

    name2uberon = []
    for sample_id, tissue_name in samples_to_names.iteritems():
        found = False
        tissue_name = tissue_name.lower()
        
        for ont_term in ont.keys():
            
            # Don't check terms that aren't of interest:
            terms_general = isinstance(target_terms, list) and (not ':' in target_terms[0])
            terms_specific = isinstance(target_terms, list) and (':' in target_terms[0])
            if  terms_general and ont_term.split(':')[0] not in target_terms:
                continue
            elif terms_specific and (ont_term not in target_terms):
                continue
            
            # Check exact names and synonyms:
            try:
                synonyms = ont[ont_term]['synonyms']
            except:
                synonyms = []    
            if (ont[ont_term]['name'].lower() == tissue_name) or (tissue_name in synonyms):
                name2uberon.append([sample_id, ont_term, tissue_name])
                found = True
        
        if found == False:
            name2uberon.append([sample_id, None, tissue_name])

    name2uberon = pd.DataFrame(name2uberon, columns = ['Sample ID','Ontology term', 'Name matched on'])
    name2uberon = name2uberon.set_index('Sample ID')
    name2uberon = name2uberon[~name2uberon['Ontology term'].isna()]
    return name2uberon
```

```python
name_col = 'Charateristics [description]'
sample_to_name = samples_info[tissue_col]
map_by_tissue_name = map_by_name(sample_to_name, samples, merged_ont)
display(map_by_tissue_name)
```

```python
relation_string, uberon = map_by_ont.loc['FF:10057-101H3']
print(relation_string, uberon)
```

```python
# for sample_id in map_by_tissue_name[map_by_tissue_name.index.duplicated()].index:
#     terms = map_by_tissue_name.loc[sample_id]['Ontology term']
#     # choose more specific
# #     print(len(terms))
#     if len(terms)>2:
#         for term in terms:
#             if 'only_in_taxon' in merged_ont[term].keys():
#                 print(term, merged_ont[term]['name'], merged_ont[term]['only_in_taxon'])
#             else:
#                 print(term, merged_ont[term]['name'])

                
#         break
```

```python
def get_overall_tissue_mappings(samples, map_name, map_ont, ont):
    """
    """
    map_name = map_name[~map_name.index.duplicated(keep='first')]

    map_ont.drop_duplicates(inplace=True)
    map_ont.dropna(inplace=True)
    
    rel = ['is_a', 'part_of']  # relations of interest between by name and by ont terms.
    overall_mapping = []
    mapping_columns = [
        'sample id','by name','by ont','relation string', 'name label', 'name string', 'overall', 'mapped by'
    ]
    disagreements = []
    disagreement_columns = ['sample id', 'by name', 'by ont','relation string', 'name label']
    unmappable = []
    for sample in samples:    
        #check if mappable by name:
        if sample in map_name.index:
            by_name, name_matched_on = map_name.loc[sample]
        else:
            by_name, name_matched_on = None, None

        #check if mappable by ontology:
        if sample in map_ont.index:
            relation_string, by_ont = map_by_ont.loc[sample]
            name_string = obo.relation_string_2_name_string(ont, relation_string)
        else:
            by_ont, relation_string, name_string = None, None, None

        if by_name and not by_ont:  # by name only
            overall = by_name
            mapped_using = "name"
        elif by_ont and not by_name:  # by ont only
            overall = by_ont
            mapped_using = "ontology"
        elif not by_name and not by_ont:  # both unmappable
            overall = None
            unmappable.append([sample])
            mapped_using = None
        elif by_name == by_ont: # both the same
            overall = by_ont
            mapped_using = "both (same)"
        elif by_name != by_ont:  # mappable but different
            # TODO: this is so messy, relations should be able to give back first relation.
            # TODO: fix 'one way vs other way'
            one_way = obo.Relations(rel, [by_name], by_ont, uberon_obo.ont).relations[0][0]
            other_way = obo.Relations(rel, [by_ont], by_name, uberon_obo.ont).relations[0][0]

            if pd.isna(one_way) and pd.isna(other_way): # no relation between by_ont and by_name
                dis_line = [sample, by_name, by_ont, relation_string, ont[sample]['name']]
                disagreements.append(dis_line)
                overall = by_name
                mapped_using = "name"
                #If one is (part of) another:
            elif pd.isna(one_way) and not pd.isna(other_way):
                overall = by_name
                mapped_using = "name"
                logging.info("name", other_way)
            elif not pd.isna(one_way) and pd.isna(other_way):
                overall = by_ont
                mapped_using = "ontology"
                logging.info("ont", one_way)
        
        mapping_line = [sample, by_name, by_ont, relation_string, name_matched_on, name_string, overall, mapped_using]
        overall_mapping.append(mapping_line)
    
    overall_mapping = pd.DataFrame(overall_mapping, columns=mapping_columns)
    overall_mapping.set_index('sample id', inplace=True)

    disagreements = pd.DataFrame(disagreements, columns=disagreement_columns)
    disagreements = disagreements.set_index('sample id')

    return overall_mapping, disagreements
```

```python
overall_mapping, disagreements = get_overall_tissue_mappings(samples, map_by_tissue_name, map_by_ont, merged_ont)
```

```python
for x in overall_mapping[overall_mapping.overall.isna()].index:
    print('unmapped', x, merged_ont[x]['name'])

```

```python
num_uberon_mapped = len(overall_mapping['overall'].unique()) - 1
print(f'{len(overall_mapping.index)} samples mapped to {num_uberon_mapped} unique UBERON terms.')
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

<!-- #region -->
### Creating an alternate mapping with text-mining

```{margin} Stop words
:name: stop-words
Stop words are words that are filtered out before processing text using Natural Language Processing (NLP) methods.
These are usually very common words (e.g. “and”, ”the”), or word which are meaningless in the context of the analysis. 
```


Failing this, text-mining is used to assist in mapping based on phenotype term names:
- First {ref}`stop words<stop-words>` are removed, using the base list in the Natural Language Toolkit (`nltk`) Python Package{cite}`Bird2006-xu`, and a small number of manually curated phenotypic stopwords (e.g. “phenotype”, “abnormality”).
- Then, an exact match between an UBERON term’s name or synonyms and phenotype term’s name is searched for. 
- If such a match does not exist, individual words from the phenotype term name or synonyms are then searched for exactly, such that the HP term “abnormality of the head and neck” would be mapped to UBERON’s “head” and “neck” terms (but never “neck of radius”). 
- In cases where multiple terms are found, a common parent would be searched for, in the case of this example, “craniocervical region”. 
- Failing that, a similarity measure is used to search a list of related words. This finds important words in the document using {ref}`TF-IDF<tf-idf>`, and then creates a similarity measure based on co-occurance, e.g. “mental” and “brain” have high similarity since they often appear in the same document  (documents are term descriptions).
- This list was then used to aid in manually mapping to relevant phenotype terms where one existed. 

```{margin} TF-IDF
:name: tf-idf
Term Frequency, Inverse Document Frequency is a common and basic measure in NLP which attempts to measure how representative a term (word) is of a document. 
It is defined by {math}`tfidf=tf(t,d) \cdot idf(t,D) = (f_{t,d}) \cdot (\frac{N}{abs{d \in D : t \in d}) ` where {math}`f_{t,d}` is the frequency of a term {math}`t` in a document {math}`d`, {math}`N` is the number of documents, and {math}`{abs{d \in D : t \in d}` is the number of documents containing the term.
```
<!-- #endregion -->

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

### dcGO
To create the input to DcGO, I used:
- BioPython{cite}`Cock2009-py`'s `Bio.SeqIO` interface for reading CAFA FASTA files.
- SUPERFAMILY{cite}`Gough2001-ct` [domain assignments for Homo Sapiens](https://supfam.mrc-lmb.cam.ac.uk/SUPERFAMILY/cgi-bin/save.cgi?var=ht;type=ass).
- UniprotKB{cite}`Pundir2016-vv`'s [mapping tool](https://www.uniprot.org/uploadlists/) to create a mapping between the UniprotKB id's provided by CAFA and the ENSP ID's used by SUPERFAMILY. 

Then, to create the DcGO only entry, I used the `DcGOR` library{cite}`Fang2014-hx` (the `dcAlgoPredictMain` function).


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


