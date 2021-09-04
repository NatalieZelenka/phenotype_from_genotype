# Discussion
This Chapter is simply supposed to present Ontolopy as a {ref}`usable<usable-ontolopy>` tool for finding relationships in OBO ontologies, from which {ref}`useful<useful-ontolopy>` outputs can be obtained.

(useful-ontolopy)=
## Usefulness
Ontolopy fills a need for quickly searching OBO files for relationships between ontology terms, and as the examples (both {ref}`simple<ontolopy-examples-2>` and {ref}`complex<ontolopy-mapping-example>`) show, it fulfils this role well: it works quickly and finds the relationships that you would expect to find ({ref}`when you know what to ask for<what-to-ask-for>`).

By building on top of the extremely well-used data analysis tool of Pandas, when Ontolopy doesn't have a function written to do something (for example defining new relations, or combining mappings), users can fall back on the functionality of Pandas to create what they need with Ontolopy's outputs.
By not (yet) integrating well with other OBO tools in development, however, it does miss potential impact.

Ontolopy is only as useful as the ontologies that it can query, so it has all of the limitations of those tools: they're missing some links because they are constantly being updated as our knowledge increases.
At the same time, it is useful *because* it builds on these resources: these resources are created by biological curators with heaps of experience working with academic and medical communities.
Ontolopy has already proved useful at least in providing a valuable way of feeding back into experimental data and ontologies.
By {ref}`checking for inconsistencies<FANTOM5-inconsistencies-example>` between multiple ways of labelling data, multiple issues in these resources and data sets have been identified and some of these revisions have been accepted. 

(usable-ontolopy)=
## Usability
### Documentation
One key feature of Ontolopy's usability is that it is well-documented.
At the time of writing, it is much more so than other {ref}`alternatives<other-ont-tools>` for working with OBO files.
The documentation is versioned and contains well-worked examples and a descriptive API.

### Installation
It is quick and easy to install, lightweight, and has a small number of dependencies (the upside of the lack of integration with other tools).

### Speed
[//]: # (TODO: Compare with speeds of Protege/OwlReady2 for similar tasks: would need to use SPARQL queries to find all relations between objects - https://owlready2.readthedocs.io/en/v0.32/sparql.html - https://stackoverflow.com/questions/39560665/find-all-relations-between-2-nodes-using-sparql )
Ontolopy runs quickly for a wide variety of tasks.
As we saw in the {ref}`examples<ontolopy-examples-2>`, Ontolopy runs quickly for most uses involving operations on or queries to ontology objects (typically less than half a second). 
The time taken depends on the size of the ontology, the number of the chosen relations, and the popularity of those relations within the ontology.
However, making a query with a large number of relations to check can inflate how long a query takes to run.

The name mapping (`Uberon.map_by_name`), however is the exception to this, which runs fairly slowly (on the order of seconds). 
There are more interesting text-mining techniques that could be integrated into Ontolopy if gains in speed where made here, for example using fuzzy-text matching to catch typos in sample information files (which are often present as they are often created by hand).

## Limitations
Ontolopy is a small and lightweight package, so it hasn't got as much functionality as some larger tools, as well as having some limitations due to it's reliance on underlying ontologies.

(what-to-ask-for)=
### You still need to understand the structure of the ontology
While Ontolopy makes it easy to query biological ontologies in Python, it doesn't prevent the user from needing to understand the structure of the ontology (what kind of relations it contains and what these mean) to be able to ask meaningful queries.
Ontolopy will allow you to ask for nonsense relations, e.g. combining any relations which may give misleading responses if you are only looking at what it is mapping to and from (rather than the path that the mapping represents).

### "Missing" functionality
There is plenty of non-existent functionality for Ontolopy that could be useful, namely:
- {ref}`Text search functionality<text-search-ont>`.
- {ref}`Functions to facilitate more complex queries<complex-queries-ont>`.
I talk about both of these in {ref}`Ontolopy future work<ont-fw>`.
While I think including both of these pieces of functionality would be helpful to Ontolopy, it is completely beyond the scope of the package to re-implement SPARQL or semantic reasoners.

[//]: # (TODO: Explain quality of coverage where that's relevant - if anywhere)
<!--
(quality-coverage)=
### Mapping quality and coverage are constrained by ontologies
[//]: # (TODO: Write)
-->


[//]: # (TODO: Move this to a limitation of the mapping itself)
<!--
### Only maps to one term
When mapping by ontology or name, multiple mappings can be retrieved, but when finding an overall mapping, only one (per method) is chosen. 
An good example of this is leukocytes, which are part of the blood and the immune system.
-->

### Improving choosing from multiple synonym options
The `Uberon.sample_map_by_name` function simply looks up the strings provided and looks for important external references to decide between synonyms. If this information is not provided or doesn't help us to make the choice, we currently just choose the first term that we found, ignoring information about  {ref}`synonym<synonym-class>`, or which synonym-having term is more specific.

```{margin} Classes of synonyms
:name: synonym-class
There are different [classes of synonyms](https://ontology-development-kit.readthedocs.io/en/latest/Synonyms.html) defined for synonyms. 
`EXACT` synonyms mean that the meaning of the synonym term would be identical to the term's name, for example *mononuclear cell* has the exact synonym *mononuclear leukocyte*. 
On the other hand, `NARROW` synonyms have more specific definitions than the name itself (in some cases they might eventually become a subclass of the original term), for example *mononuclear cell* has the narrow synonym *peripheral blood mononuclear cell*.
There are also *BROAD* and *RELATED* synonyms.
```

### Implementation
[//]: # (TODO: Write)

Some of the implementation choices are a little unusual, for example:
- representing relationships internally as relation paths (strings).
- not matching up with existing tools

## Fit-for-purpose
[//]: # (TODO: Write)

Further to the examples given in this chapter, {numref}`c05.3-data-wrangling` shows an example of how this Ontolpy is especially useful for harmonising sample to tissue mappings for different gene expression data sets, which may have different levels of specificity.