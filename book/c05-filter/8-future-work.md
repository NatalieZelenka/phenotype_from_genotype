(filip-future-work)=
# Future work


## Development and release of `filip`
[//]: # (TODO: Write - the above is out of date: show the roadmap, and mention continuing to validate - with new versions of GO, etc.)
`filip` should first be tested on a more protein function prediction methods, and then be made available as a resource for others to use in future CAFA competitions or similar. 
The mappings between phenotype terms and tissues should also be made available at this time, so that other people can easily interrogate it for individual genes.

Other functionality/usability:
- Pre-calculate the filter for all tissue-phenotype pairs (use `itertools`) and make it available as a web app. Didn't do it now because it's about 15,000 x 15,000 for all tissue-phenotype pairs , which would take ages. Easier to just do for list of interesting tissues/phenotypes. Then this step would only need to be repeated if we want to include a wider range of phenotype terms (i.e. from a new ontology file). 

Other investigations:
- Different TPM cut-off for different genes or phenotypes.
- For unmappable phenotypes, is it advantageous to use all samples, i.e. if a protein that is never expressed is predicted, filter it out.
- Treat developing gene expression samples differently.

## Protein abundance
### Including protein abundance data
[//]: # (TODO: Write)

### Predicting protein abundance from mRNA abundance
[//]: # (TODO: Write: there are loads more)
There are some attempts to predict protein abundance from mRNA abundance{cite}`Terai2020-lv,`. 

## CAFA5
[//]: # (TODO: Write: wait is it CAFA6 next?)
[//]: # (TODO: Aside about how naive works weirdly well)

- Inclusion of mapping improvements made in the in {ref}`the next Chapter<c05-combining>`, specifically:
    - mapping improvements made by including the cell ontology (in addition to Uberon) and by using simple natural language processing to generate potential mappings.
    - using the combined tissue-specific gene expression data set for a greater coverage of tissues.
- Enter with naive predictor + `filip` 