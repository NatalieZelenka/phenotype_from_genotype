(ontolopy-intro)=
# Introduction

:::{margin} What are ontologies again?
Ontologies are controlled vocabularies of terms and relationships. You can read more about them in {numref}`what-are-ontologies`.
:::

[//]: # (TODO: Mention https://monarchinitiative.org/about/monarch - here or in intro to contextualise within idea of this very generalising biology world)
[//]: # (TODO: Make a Zenodo for ontolopy and reference it here)
[//]: # (TODO: Explain relationship between DAGS and ontologies... they're not really DAGS - they used to be DAGS because they come from phylogenetic trees)
[//]: # (TODO: Ensure that relationship between SPARQL - for QUERYING ontologies, and reasoners - totally different thing - are spoken about differently)

(opy-motivation)=
## Motivation

I created Ontolopy in order to create a high-coverage mapping between tissues and gene expression samples, which I hoped would aid in phenotype and protein function prediction.
An earlier version of the package was used to create a mapping between gene expression sample names or identifiers to phenotypes that are known to affect that type of tissue for {numref}`c06-filter`.
Removing wrong-tissue predictions proved successful in improving protein function predictions, but was constrained by a low coverage, despite using one of the most extensive tissue-specific gene expression experiments. 
In order to improve this coverage, I needed to extend it's functionality to allow mapping more generally between samples and phenotypes according to their tissues.

[//]: # (TODO: There's some flanged up italics in PDF)
There are many gene expression data sets, and the reporting for tissue metadata is not at all standardised between them.
This is true even within databases of gene expression data where great care has been taken to harmonise the metadata such as the Gene Expression Atlas.
If tissue type is recorded at all, it is usually manually given a label tissue using a name (e.g. "blood", "kidney"), or perhaps as part of the sample name ("blood adult donor1"). 
In other cases, cell type might be recorded instead (e.g. "leukocyte", "cardiac fibroblast").
In other circumstances still, the samples might be annotated to existing ontologies, and some even have their own ontologies of samples (such as FANTOM5).
Names like *blood* can be useful, but if you'd like to compare across samples, then it's helpful to have a controlled vocabulary such as ontology terms: that way even a computer can figure out what *mature basophils*, *plasma* and *fibrinogen complex* have in common.

In addition to the benefits of ontologies' controlled vocabulary (the terms themselves), they also contain a wealth of additional information and links to other ontologies. 
For example, Uberon contains information about synonyms for different anatomical entities: the *pituitary stalk* is also known as the *infundibular stem* which is *part of the brain* that *connects to the hypothalamus*. 
Ontologies are therefore also sources of text that could be used to map sample names to terms. 
Once samples are mapped to ontologies they can leverage on all of the information inside them, for example, to find all the samples that are capable of *hormone secretion*.

(obo-files)=
## OBO files
There are two file formats which rule the ontology world. 

[//]: # (TODO: Cite Hermit + sparql)
Open Biomedical Ontology (OBO, `.obo` files) is the format that biomedical ontologies such as Gene Ontology or Human Phenotype Ontology were originally built in.
Meanwhile, the other file format is the Ontology Web Language (OWL), which is built upon XML. 
Although it has not always been the home of biomedical ontologies, many now release both OBO and OWL versions. 
Both file types are human-readable, although the OBO format is a little easier (for humans) to edit and read directly, and is generally considered easier to work with.
The major benefit of the OWL format is that it is formally axiomised and there exists a large suite of tools available for performing logical reasoning (e.g. using HermiT and SPARQL)

I found that at the time of creating, I needed files which were only available in OBO format, and OBO-to-OWL converters were not able to extract all the information that I needed. 

(obo-anatomy)=
### Anatomy of an OBO file
[//]: # (TODO: write, excerpt of obo file here mention *terms* *relations* *attributes*)
[//]: # (TODO: Add TODOs from Ontolopy to milestone)
OBO files are text files. 
The top of an OBO file contains metadata about the ontology itself, for example it's version in terms of format (`format-version`) and contents (`data-version`), name (`ontology`), the definitions of any subsets of ontology terms (`subsetdef`), the definition of synonym types (`synonymtypedef`), among many others.

Below are some example lines from this top section of the extended Uberon ontology file:
```
format-version: 1.2
ontology: uberon/ext
data-version: uberon/releases/2021-02-12/ext.owl
subsetdef: non_informative "abstract class brought in to group ontology classes but not informative"
synonymtypedef: HUMAN_PREFERRED "preferred term when talking about an instance of this class in Homo sapiens"
```

The rest of the file has the following format, a blank line followed by `[Term]` indicates a new term is being defined, followed by different types of attributes, such as `id`, `name`, definition (`def`), external reference (`xref`), links to parent terms `is_a`, and other relationships such as `part_of` or `located_in`. 
See for example the *pupillary membrane* term, `UBERON:0002269`:
```
[Term]
id: UBERON:0002269
name: pupillary membrane
def: "The pupillary membrane in mammals exists in the fetus as a source of blood supply for the lens. It normally atrophies from the time of birth to the age of four to eight weeks." [http://en.wikipedia.org/wiki/Persistent_pupillary_membrane]
xref: FMA:77663
xref: http://en.wikipedia.org/wiki/Persistent_pupillary_membrane
xref: MA:0001293
is_a: UBERON:0000158 ! membranous layer
is_a: UBERON:0004121 ! ectoderm-derived structure
relationship: located_in UBERON:0001771 {source="MA-modified"} ! pupil
relationship: part_of UBERON:0000922 ! embryo
relationship: part_of UBERON:0001769 ! iris
```

(ontolopy-purpose)=
## Purpose

[//]: # (TODO: Add alt text for ontolopy logo)

```{figure} ../images/ontolopy_logo.png
---
height: 220px
name: ontolopy-logo
---
Figure showing the purpose of Ontolopy as an ontology.
```

(propagate)=
:::{margin} Propagating
I use the word *propagate* to applying information about one ontology term, to describe it's parents or children.
For example `UBERON:0009865` (*[Hatschek's pit](http://en.wikipedia.org/wiki/Hatschek's_pit)* - part of a fish-like lancelet) is `capable_of GO:0070254` (*mucus secretion*) and also `is_a UBERON:0006846` (*surface groove*).

If we propagate this relationship to the parent term, we find out that *surface groove*s can be `capable_of` *mucus secretion*.
:::

```{admonition} Purpose statement
Ontolopy makes it easier to work with OBO ontologies in Python using familiar data types such as Python `dict`s (dictionary objects) and Pandas `DataFrame`s.
In particular, this supports finding and {ref}`propagating<propagate>` relationships between ontology terms (such as tissue and phenotype terms), and enables matching of sample names to ontology terms.
```

To my knowledge, no other existing package fulfils this particular need, however there are of course many other tools for working with ontologies.

(other-ont-tools)=
## Other available tools
There are a number of other tools that are available for building and logically querying ontologies, but these tend to be standalone platforms like [Protégé](https://protege.stanford.edu/) (a Desktop platform primarily for building ontologies) or OWL-specific like [OwlReady2](https://owlready2.readthedocs.io/en/latest/intro.html). 
I tested Protégé (using it's built-in reasoner HermiT with SPARQL queries) for extracting uberon-phenotype mappings, but perhaps due to the size of the ontologies, this was prohibitively slow.

Ontologies are widely used by biomedical researchers, mostly for ontology enrichment analyses. 
There are easy to use tools in popular programming languages like R and Python for performing specialised analyses (such as GO enrichment, like GOATools{cite}`Klopfenstein2018-eh`, or the older [goenrich](https://github.com/jdrudolph/goenrich)) but tools for querying them generally are either very specialised or browser-based (like Ontobee{cite}`Ong2017-gh`).

Pronto{cite}`Larralde2021-sg` is a nice Python package which is one of the exceptions to this rule, however it has some "missing" (missing for my needs, out of scope for them) functionality: being able to propagate relationships between nodes (terms).

OntoBio{cite}`Albuquerque2015-ls` is another Python package with similar functionality, which remains in active development. It is made by the same team as GOATools. 
It has a rich functionality in terms of querying common attributes of biological ontologies, for example their synonyms or definitions. Again, the missing functionality for me is to be able to merge and query ontologies for relationships.

It would be beneficial for Ontolopy to make use of Pronto or OntoBio's underlying data structures as I discuss in {numref}`pronto-integration`.