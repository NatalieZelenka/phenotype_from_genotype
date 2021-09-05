(c06-filter)=
# Filtering computational predictions with tissue-specific expression information

This chapter presents a more focused approach to improving phenotype and protein function predictions.
I present a prototype filter for protein function prediction methods (Filip) which I developed for the CAFA3 competition, which filters out predictions where the gene is not expressed in the tissue relating to the phenotype.
This approach was prompted by the discovery that this is one of the sources of noise in Snowflake, as described {ref}`earlier<dcgo-expression-problem>`.

[//]: # (TODO: cite zenodo for filip)

```{admonition} Contributions in this chapter
:class: hint
- The Filip method for filtering protein function prediction based on tissue-specific gene expression.
- Entering predictors using Filip in the CAFA3 competition, which contributes to the CAFA3 paper{cite}`Zhou2019-jk`,
```

