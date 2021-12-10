(ontolopy-functionality)=
# Functionality
[//]: # (TODO: link from overview to specific functionality/API, e.g. leaf/root terms)
[//]: # (TODO: Make sure documentation links are versioned)

This section describes the low-level functionality of Ontolopy: what it can do. 
For examples of how this functionality is of practical use, please see the {ref}`examples<ontolopy-examples-2>` sections.
You can find a full and up-to-date API Reference [in the documentation](https://nataliethurlby.github.io/ontolopy/contents/reference.html).

(subclass)=
:::{margin} Subclass
Python is an object-orientated language, meaning that it's designed so that classes can inherit from one another.

If a class subclasses another, it means it inherits it's attributes and methods.
:::

The functionality of the package can be summarised as follows: Ontolopy takes OBO files and:
1. makes them into an intuitive Python object (which {ref}`subclasses<subclass>` a Python `dict`, meaning that you can do everything with it that you can do with this familiar and useful data type.
2. provides a set of tools for doing some useful manipulations and queries to these objects, which are particular to ontologies. This includes for example propagating relationships between terms, finding leaf/root terms, and merging ontologies.
3. Further to this, it provides an extra class for manipulating and querying the Uberon anatomy specifically. 

(opystructure)=
## Structure
:::{margin} `import ontolopy as opy`
Note: you will see `ontolopy` shortened to `opy` in code segments.
:::

Ontolopy is organised into three submodules, each centred around classes with the same names: `opy.Obo()` for OBO ontology objects, `obo.Relations()` for finding relationships between terms in an ontology object, and `opy.Uberon()` for finding tissue mappings.
These three submodules are automatically loaded with `import ontolopy`.

(opyobo)=
## Working with OBO ontologies
[//]: # (TODO: reorganise with sphinx-argparse)

(callables)=
:::{margin} Callables
In Python callables are functions, classes, and class methods that you can call, i.e. where you use syntax like `function()` or `MyClass()` to run some code. 
:::

The `opy.obo` module contains the following {ref}`callables<callables>` that make it easier to work with OBO ontologies:

```{eval-rst}
.. currentmodule:: ontolopy.obo

.. autosummary::
   load_obo
   download_obo
   Obo
   Obo.merge
```

(oboclass)=
### The `Obo` class
[//]: # (TODO: Example/excerpt of Obo structure)

The `Obo` class is an OBO ontology object, which subclasses `dict`. 
New `Obo` objects can be created from nested dictionaries. 
At the top level of the dictionary, keys are terms and values are dictionaries.
This dictionary structure also allows you to add new terms.

````{admonition} Obo reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.obo

.. autoclass:: Obo

   
   .. automethod:: __init__

   
   .. rubric:: Methods

   .. autosummary::

      ~Obo.merge
      
      
   .. rubric:: Attributes
   
   .. autosummary::
   
      ~Obo.leaves
      
      ~Obo.terms   
```
````

````{admonition} Obo usage example
:class: note
```python
import ontolopy as opy

new_ontology = opy.Obo({'TERM:000001': {'name': 'Example term'}})
new_ontology['TERM:000002'] = {'name': 'Second example term', 'is_a': ['TERM:000001']}
```
````

(obomerge)=
### Merging ontologies
It's also possible to merge (a list of) ontologies into the base ontology. 
This can be useful for investigating relationships between ontologies.
For example, to find relationships between samples and tissues, that might go via cells, you may want to merge a sample ontology, cell, and tissue ontology to find all possible relationships.

````{admonition} Obo.merge reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.obo
.. automethod:: Obo.merge
```
````

(oboload)=
### Loading ontologies from file
While creating ontologies from dictionaries is useful for adding bespoke terms, most of the time we want to load an official and curated OBO from a file.

````{admonition} load_obo reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.obo
.. autofunction:: load_obo
```
````

[//]: # (TODO: Describe how it works and what types of relationships are considered, especially when references are terms of interest)

(obodownload)=
### Downloading OBO files
[//]: # (TODO: List what can be downloaded)
[//]: # (TODO: Check via URL works)

It's also possible to download OBO files, either from a list of popular OBO files by name, or via a URL.

````{admonition} download_obo reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.obo
.. autofunction:: download_obo
```
````

(opyrelations)=
## Finding relationships
The most key functionality in Ontolopy is the ability to infer relationships between terms, across ontologies (be it between tissue terms and phenotype terms, or something else).
This functionality is inside the `opy.relations` module and handled by the {ref}`Relations<relations-class>` class.

````{admonition} Relations reference

```{eval-rst}
.. currentmodule:: ontolopy.relations

.. autosummary::
   relation_path_to_text
   Relations
```
````

(relations-class)=
### The `Relations` class

[//]: # (TODO: Docstrings could be tidied, tuple airs, in *a* specific source)

The `Relations` class finds relationships of certain types between sources and targets.
It subclasses a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) since that is a convenient and familiar format for the relationship information to be returned.

```{eval-rst}
.. currentmodule:: ontolopy.relations

.. autoclass:: Relations

   .. automethod:: __init__
 
```

[//]: # (TODO: Example here)
<!--
````{admonition} Relations usage example
:class: note
```python
import ontolopy as opy


```
````
-->


[//]: # (TODO: how much quicker is any than all.)

To find relationships, the code loops through sources, and for each source it will look at the `allowed_relations` to find relationships with other terms, then for each of these terms it will look for relationships with other terms in the same manner, etc.

(relation-paths)=
Internally, Ontolopy stores these relationships as a list of strings, where each string details the relations between the source term and other terms, e.g. `UBERON:123913.is_a~UBERON:1381239.is_a~UBERON:987890`. 
Let's call these strings *relation paths*.

Cyclic relationships are not permitted (a term can only be present in a relation path once).
Relationships continue to be searched for until either the ontology provided can no longer add any new relation paths OR we found what we were looking for.

In "any" mode, finding what we're looking for means finding any target term as the last term in the relation string, while in "all" mode, we must find all target terms for the source term.


**The `mode` parameter** can be either `any` or `all`, and this represents whether we are looking for relations from our source terms to any one target term, or to all target terms for which we can find a relationship.
It is much quicker to run in "any" mode, so this mode is the default, and it is preferable when we simply need the most direct mapping between our source and target terms, for example we want to know which (one) tissue does the sample map to best? 

The "all" mode tends to be more useful when we are equally interested in the targets as the source terms for example: when looking at mappings between tissues and phenotypes, there is likely to be many different phenotypes that a tissue can exhibit and we are equally interested in all of them.

**Provide either `sources` and `targets` OR `source-targets`**. 
It's possible to provide a list of `sources` and a list of `targets`, OR a list of tuple `source-targets`. 
It does not make sense to provide both. 
The latter option only works in `all` mode: i.e. we are interested in all source-target pairs.
Essentially, the `sources-targets` option provides a quicker way of running `Ontolopy` in "all" mode when we know in advance which specific pairs of sources and targets we are interested in. 
If `sources` and `targets` are provided and `mode==all`, then `Ontolopy` will generate a combination of all possible sources and targets (removing `excluded` target terms if provided).

(relationspathstotext)=
### Converting "relation paths" to text
Since relationships are internally stored as {ref}`relation paths<relation-paths>` as explained above, it is useful to turn these strings into more readable text, which is what the `relation_path_to_text` function does.

[//]: # (TODO: No return statement)

````{admonition} relation_path_to_text reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.relations
.. autofunction:: relation_path_to_text
```
````

<!--Simplifying relationships-->

(opyuberon)=
## Creating Uberon Mappings

The `opy.uberon` submodule contains the specific tools for working with the Uberon ontology: finding mappings between tissues and phenotypes {ref}`via ontology terms<mapping-by-term>` by making use of the {ref}`Relations<relations-class>` class, as well as {ref}`doing this mapping using text<mapping-by-name>`, and {ref}`comparing these two mappings<comparing-mappings>`. 
The vast majority of this functionality sits in the `Uberon` class.


```{eval-rst}
.. currentmodule:: ontolopy.uberon

.. autosummary::
   uberon_from_obo
   Uberon
```

(uberonclass)=
### The `Uberon` class
Calling the `Uberon` class itself simply checks if there are any `Uberon` terms in the merged ontology, and then allows the ontology to be used to create Uberon sample-to-tissue mappings, through class methods (which should be called separately).

There are three parts to the process in creating Uberon mappings, the functionality for which lives in three different `Uberon` class methods:
1. **{ref}`Mapping via name<mapping-by-name>`:** Map from sample-to-tissue via informal tissue names given in experimental design information (e.g. “eye stalk”) to an Uberon term (`UBERON:0010326`, Optic Pedicel). 
2. **{ref}`Mapping via ontology term<mapping-by-term>`:** Map from CL cell types (e.g. `CL:0000235`, Macrophage), sample ontology term to Uberon tissues (e.g. `UBERON:0002405`, Immune system). Or from sample ontology terms (like FANTOM terms, such as `FF:10048-101G3`, *Smooth Muscle, Adult, Pool1*) to Uberon terms (`UBERON:0001135`, Smooth Muscle Tissue). Returns relationships between source term and Uberon term.
3. **{ref}`Create sample-to-tissue mappings and disagreements between mappings<comparing-mappings>`** based on (1) and (2).


```{eval-rst}
.. currentmodule:: ontolopy.uberon

.. autoclass:: Uberon

   
   .. automethod:: __init__

   
   .. rubric:: Methods

   .. autosummary::

      ~Uberon.__init__
      ~Uberon.sample_map_by_ont
      ~Uberon.sample_map_by_name
      ~Uberon.get_overall_tissue_mappings

```

(mapping-by-name)=
### Mapping from sample to tissue via name using `Uberon.sample_map_by_name`
Informal tissue names are mapped from Uberon term identifiers by checking for exact name matches to Uberon term names and their synonyms in the extended Uberon ontology.

```{margin} Stop words
:name: stop-words
Stop words are words that are filtered out before processing text using Natural Language Processing (NLP) methods.
These are usually very common words (e.g. “and”, ”the”), or word which are meaningless in the context of the analysis. 
```

If an exact match does not exist, individual words from the phenotype term name or synonyms are then searched for exactly. 
First {ref}`stop words<stop-words>` are removed, using the base list in the Natural Language Toolkit (`nltk`) Python Package{cite}`Bird2006-xu` (e.g. and, or), and a small number of manually curated phenotypic stopwords (e.g. “phenotype”, “abnormality”).
This would mean that the {abbr}`HP (Human Phenotype)` term “abnormality of the head and neck” would search for the words "head" and "neck" in the UBERON terms, and would be mapped the terms of the same name (but never to “neck of radius” - which is related to bone). 
In cases where multiple terms are found, a common parent would be searched for, in this case the result is “craniocervical region” . 

[//]: # (TODO: No return statement)

````{admonition} Uberon.sample_map_by_name reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.uberon
.. automethod:: Uberon.sample_map_by_name
```
````

(mapping-by-term)=
### Mapping from sample to tissue via ontology term using `Uberon.sample_map_by_ont`
The `sample_map_by_ont` function uses the Relations class in "any" mode to find relationships via ontologies in much the same way described {ref}`above<relations-class>`. 
This is essentially a wrapper that provides convenient default settings for allowed relations and targets.

[//]: # (TODO: rename relation_types to match allowed_relations, and to to targets)

Mappings can be made via any term in the merged ontology, which allows mappings that cannot be made through Uberon alone, for example: Macrophage - monocyte derived, donor3 `is_a` Human macrophage sample `derives_from` Macrophage `is_a` Monocyte `is_a` Leukocyte `part_of` Immune System, which means this sample is derived from part of the immune system.

[//]: # (TODO: Cite cell ontology)
[//]: # (TODO: Rewrite with Relations class in mind)
[//]: # (TODO: No return statement)


````{admonition} Uberon.sample_map_by_ont reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.uberon
.. automethod:: Uberon.sample_map_by_ont
```
````

[//]: # (TODO: Add example code for child-mapping melanocyte.)
(child-mapping)=
**Mapping by term: child mapping**
Some samples may be pools of cell types that may come from more than one anatomical location.
In this case, there will be no regular mapping, since no parent terms will have a mapping to a tissue. 
In this case, we can look at tissue mappings (in the usual way, described above), for all of the children of our parent term of interest.
I call this mode "child mapping" and it is off by default.

So, for example *melanocytes* are are melanin-producing cells found in many different places in the body (skin, hair, heart), and therefore they don't (nor any of their parents) map to a specific Uberon term.
If we choose `child_mapping==TRUE`, then for this term, we will get a list of all Uberon terms that cells of this type can come from.
This mode isn't currently used in the context of the rest of this thesis.

(comparing-mappings)=
### Getting overall mappings and finding disagreements using `Uberon.get_overall_tissue_mappings`
As described, Ontolopy has two methods of mapping to tissues, and it also provides a method of harmonising these two mappings, and for finding any disagreements between them.
This can be very useful for revealing logical inconsistencies in either the mappings or the ontologies (as was the case in the {ref}`FANTOM5 example<FANTOM5-inconsistencies-example>`).

````{admonition} Uberon.get_overall_tissue_mappings reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.uberon
.. automethod:: Uberon.get_overall_tissue_mappings
```
````

