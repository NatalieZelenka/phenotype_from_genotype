# Future work

## Development of `uberon-py`
[//]: # (TODO: Add text-mining part to uberon-py and test on different data sets)

## Development and release of `filip`
[//]: # (TODO: Write - the above is out of date: show the roadmap, and mention continuing to validate - with new versions of GO, etc.)
`filip` should first be tested on a more protein function prediction methods, and then be made available as a resource for others to use in future CAFA competitions or similar. 
The mappings between phenotype terms and tissues should also be made available at this time, so that other people can easily interrogate it for individual genes.

Other investigations:
- Different TPM cut-off for different genes or phenotypes.
- For unmappable phenotypes, is it advantageous to use all samples, i.e. if a protein that is never expressed is predicted, filter it out.
- Treat developing gene expression samples differently.

## CAFA5
[//]: # (TODO: Write)
[//]: # (TODO: Aside about how naive works weirdly well)

- Inclusion of mapping improvements made in the in {ref}`the next Chapter<c05-combining>`, specifically:
    - mapping improvements made by including the cell ontology (in addition to Uberon) and by using simple natural language processing to generate potential mappings.
    - using the combined tissue-specific gene expression data set for a greater coverage of tissues.
- Enter with naive predictor + `filip` 