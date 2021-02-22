(c06-filter)=
# Filtering computational predictions with tissue-specific expression information

This Chapter presents a more focused approach to improving phenotype and protein function predictions.
I present a prototype filter for protein function prediction methods (`filip`) which I developed for the CAFA3 competition, which filters out predictions where the gene is not expressed in the tissue relating to the phenotype.
This approach was prompted by the discovery that this is one of the sources of noise in `snowflake`, as described in {ref}`the previous Chapter<dcgo-expression-problem>`, 

[//]: # (TODO: Cross-reference and cite zenodo for uberon-by and filip)

The research outputs in this chapter include:
- The `filip` method for filtering protein function prediction based on tissue-specific gene expression.
- The `uberon-py` Python package for mapping biological samples to the Uberon tissue ontology, which was necessary to create for `filip`.
- Contributions to improve the FANTOM5 and Uberon ontologies, based on inconsistencies discovered using the `uberon-py` package.
- The CAFA3 paper{cite}`Zhou2019-jk`, in which I entered predictors using `filip`.