(ontolopy-functionality)=
# Functionality
[//]: # (TODO: link from overview to specific functionality/API, e.g. leaf/root terms)
[//]: # (TODO: Make sure documentation links are versioned)

This section describes the low-level functionality of `Ontolopy`: what it can do. 
For examples of how this functionality is of practical use, please see the {ref}`Examples<ontolopy-examples>` section.
You can find a full and up-to-date API Reference [in the documentation](https://nataliethurlby.github.io/ontolopy/contents/reference.html).

(subclass)=
:::{margin} Subclass
Python is an object-orientated language, meaning that it's designed so that classes can inherit from one another.

If a class subclasses another, it means it inherits it's attributes and methods.
:::

The functionality of `Ontolopy` can be summarised as follows: `Ontolopy` takes OBO files and:
1. makes them into an intuitive Python object (which {ref}`subclasses<subclass>` a Python `dict`, meaning that you can do everything with it that you can do with this familiar and useful data type.
2. provides a set of tools for doing some useful manipulations and queries to these objects, which are particular to ontologies. This includes for example propagating relationships between terms, finding leaf/root terms, and merging ontologies.
3. Further to this, it provides an extra class for manipulating and querying the Uberon anatomy specifically. 

## Structure
:::{margin} `import ontolopy as opy`
Note: you will see `ontolopy` shortened to `opy` in code segments.
:::

`Ontolopy` is organised into three submodules, each centred around classes with the same names: `opy.Obo()` for OBO ontology objects, `obo.Relations()` for finding relationships between terms in an ontology object, and `opy.Uberon()` for finding tissue mappings.

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

### The `Obo` class
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

### Merging ontologies
It's also possible to merge (a list of) ontologies into the base ontology. 
This can be useful for investigating relationships between ontologies
For example, to find relationships between samples and tissues, that might go via cells, you may want to merge a sample ontology, cell, and tissue ontology to find all possible relationships.

````{admonition} Obo.merge reference
:class: hint
```{eval-rst}
.. currentmodule:: ontolopy.obo
.. automethod:: Obo.merge
```
````

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

## Finding relationships

```{eval-rst}
.. currentmodule:: ontolopy.relations

.. autosummary::
   relation_path_to_text
   Relations
```

### The `Relations` class
[//]: # (TODO: Write explain how mapping works: what is prioritised, etc)
[//]: # (TODO: mention pandas data frames)

```{eval-rst}
.. currentmodule:: ontolopy.relations

.. autoclass:: Relations

   
   .. automethod:: __init__
 
```


### Disagreements
(disagreement-finding)=
**Using disagreements between mappings to improve biological ontologies and sample mappings:**

As described, the `uberon_py` package has two methods of mapping to tissues. 
Where both can be ran, disagreements between these mappings can be checked. 
When these two methods disagree, logical inconsistencies in either the mappings or the ontologies is revealed. 
See the {ref}`example<FANTOM5-inconsistencies-example>` of how this worked for the FANTOM5 data set.

### Miscellaneous
- Relation strings to text
- Simplifying relationships


## Creating Uberon Mappings

There are four parts to the process in creating Uberon mappings:
1. **{ref}`Mapping via name<mapping-by-name>`:** Map from sample-to-tissue via informal tissue names given in experimental design information (e.g. “eye stalk”) to an Uberon term (`UBERON:0010326`, Optic Pedicel). 
2. **{ref}`Mapping via ontology term<mapping-by-term>`:** Map from CL cell types (e.g. `CL:0000235`, Macrophage), sample ontology term to Uberon tissues (e.g. `UBERON:0002405`, Immune system). Or from sample ontology terms (like FANTOM terms, such as `FF:10048-101G3`, *Smooth Muscle, Adult, Pool1*) to Uberon terms (`UBERON:0001135`, Smooth Muscle Tissue). Returns relationships between source term and Uberon term.
3. **Create sample-to-tissue mappings** based on (3) and (4)
4. **{ref}`Find disagreements in mappings<disagreement-finding>`** based on (3) and (4), which my indicate errors in sample metadata or ontologies.


```{eval-rst}
.. currentmodule:: ontolopy.uberon

.. autosummary::
   uberon_from_obo
   Uberon
```

### The `Uberon` class

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
### Mapping by name
Informal tissue names are mapped Uberon term identifiers by checking for exact name matches to Uberon term names and their synonyms in the extended Uberon ontology.

(mapping-by-term)=
### Mapping by term
**Mapping by term: regular mapping**

[//]: # (TODO: Cite cell ontology)

A mapping between a provided term (e.g. a FANTOM sample identifier or CL identifier) associated with a sample and an Uberon term is created by:
* Finding all relationships of interest (e.g. `is_a`, `related_to`, `part_of`, `derives_from`, `intersection_of`, `union_of`) to any other sample, cell or Uberon term (i.e. all *parents* of our term of interest).
* Propagate any relationships found using the same list of relationships, until either an Uberon term is found, or no new relationships are found, or you reach the root terms of the ontology. 

In this way, some mappings can be made via the cell ontology, which cannot be made through Uberon alone, for example: Macrophage - monocyte derived, donor3 `is_a` Human macrophage sample `derives_from` Macrophage `is_a` Monocyte `is_a` Leukocyte `part_of` Immune System, e.g. this sample is related to the immune system.

[//]: # (TODO: Add example code for child-mapping melanocyte.)
(child-mapping)=
**Mapping by term: child mapping**
Some samples may be pools of cell types that may come from more than one anatomical location.
In this case, there will be no regular mapping, since no parent terms will have a mapping to a tissue. 
In this case, we can look at tissue mappings (in the usual way, described above), for all of the children of our parent term of interest.
I call this mode "child mapping" and it is off by default.

So, for example *melanocytes* are are melanin-producing cells found in many different places in the body (skin, hair, heart), and therefore they (nor any of their parents map to a specific Uberon term).
If we choose {python}`child_mapping=TRUE`, then for this term, we will get a list of all Uberon terms that cells of this type can come from.
This mode isn't currently used in the context of the rest of this thesis.
