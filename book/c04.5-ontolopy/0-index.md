# `Ontolopy`

As described in {ref}`the previous Chapter<dcgo-expression-problem>`, I found that one of the sources of noise in the `Snowflake` phenotype predictor is the existence of predictions where the gene is not expressed at all in the tissue relating to the phenotype. 
After discovering this, I was keen to focus on removing these predictions, but in order to do so, I needed to be able to map between samples and phenotypes according to their tissues.

This short Chapter describes [`Ontolopy`](https://nataliethurlby.github.io/ontolopy/): a Python package for manipulating OBO ontology files and describes {ref}`how the package was used<ontolopy-mapping-example>` to create the mapping between sample names or identifiers to phenotypes that are known to effect that type of tissue, which are then used in {numref}`c06-filter`.

The package also has many other potential uses, some of which are {ref}`explored in this Chapter, too<ontolopy-examples-2>`. 
For example, it is particularly useful for finding inconsistencies/disagreements between data sources, which enabled me to contribute back to improve some of the resources that `Ontolopy` relies on.

[//]: # (TODO: check links)
At time of writing, `Ontolopy v1.0.1-beta` ([PyPi](), [GitHub](), [Docs]()) is the current release.

[//]: # (TODO: put all contributions for other chapters in "hints")

```{hint} Contributions
The contributions in this chapter include:
- Development of the `Ontolopy` and it's [documentation](https://nataliethurlby.github.io/ontolopy/).
- Contributions to improve the FANTOM5 and Uberon ontologies, based on using the package to  discover data inconsistencies.
- Mapping data-sets created using `Ontolopy`:
    + FANTOM5-tissue mappings
    + tissue-phenotype mappings
```

