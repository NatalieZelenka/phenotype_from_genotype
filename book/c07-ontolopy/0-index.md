(c06-ontolopy)=
# Ontolopy

[//]: # (TODO: Mention a bit more of the semantic web and describe the fact that what I'm looking at here is Semantic Associations...)
[//]: # (TODO: Explain the fact that Bioinformatics is mostly done in scripting languages like R and Python)
[//]: # (TODO: Rewrite to make it more like an abstract)


This chapter describes [Ontolopy](https://nataliethurlby.github.io/ontolopy/): a small Python package that I created for manipulating OBO ontology files.
This chapter also includes some uses of ontolopy, for example {ref}`mapping between samples and phenotypes<ontolopy-mapping-example>`, and {ref}`other uses<ontolopy-examples-2>`.
For example, it is particularly useful for finding inconsistencies/disagreements between data sources, which enabled me to contribute back to improve some of the resources that Ontolopy relies on.

[//]: # (TODO: check links)
At time of writing, `Ontolopy v1.0.1-beta` ([PyPi](), [GitHub](), [Docs]()) is the current release.

[//]: # (TODO: put all contributions for other chapters in "hints")
[//]: # (TODO Link to the mappings sections and make sure they're available for dowload)

```{admonition} Contributions in this chapter
:class: hint
The contributions in this chapter include:
- Creation of the Ontolopy package and it's [documentation](https://nataliethurlby.github.io/ontolopy/).
- Contributions to improve the FANTOM5 and Uberon ontologies, based on using the package to  discover data inconsistencies.
- Mapping data-sets created using `Ontolopy`:
    + FANTOM5-tissue mappings
    + tissue-phenotype mappings
    + Combined FANTOM5-phenotype mappings
```

