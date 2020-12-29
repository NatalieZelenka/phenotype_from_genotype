# Introduction

<!--
NOTES:
* Around 3 pages long - like a longer version of the abstract
* List my contributions
* Explain what each chapter is and why it is there.
Short, so can probably be a bit more fussy about style, e.g.:
* No passive voice (zombie test).
* Varied sentence length.

Notes on chapters:
-->

[//]: # (TODO: Explain Jupyter Book: link to latest online versoin and side notes about racists)

[//]: # (TODO: Check that this is true)

The central theme of this thesis is the relationship between protein function - at either a molecular or phenotypic level - and the sequence of its associated DNA and RNA. A recurring motif is impact of the provenance of related data and what that means for attempts to make genome-wide predictions about these relationships. 

In the spirit of trying to make my work as reproducibly and Open as possible, this thesis is available online as a Jupyter Book: the latest version is available online [here](). 

{ref}`Chapter 2<c02-biology-bg>` contains the biological background information on which the rest of the thesis is based. It tells the story of how phenotype arises from genotype, and introduces the different biological molecules that are involved. It begins at the very basics: what are DNA, RNA, proteins, and phenotypes? How do we measure them? And how do we measure the connections between them? This background is intended to make this thesis readable to someone without a background in biology. This chapter does not contain any of my own research. In the light of Black Lives Matter, I have included asides in this book where I mention researchers who have been involved in eugenics and/or racism. I have done this as I don't want to highlight the scientific achievements of these individuals, without also acknowledging their legacy of scientific racism.

{ref}`Chapter 3<c03-compbio-bg>` is a second background chapter, which contains some of my own work. It follows on from the first by discussing popular resources in computational biology, their provenance, and the impact of this on the field. This includes mathematical modelling of publications of named genes and sensitivity analysis of gene enrichment analyses. I also present here my contributions to reproducibility-related collaborative projects that I have and continue to be involved with: the Proteome Quality Index paper{cite}`Zaucha2015-ez`, my contribution to the collaborative 2014 SUPERFAMILY update paper{cite}`Oates2015-li`, and the (ongoing) MAPS project. 

In {ref}`Chapter 4<c04-snowflake>`, I describe my preliminary efforts to integrate the data sources described in the background chapters into Snowflake, a phenotype predictor{cite}`Gough2017-ik`. I discuss potential reasons for the poor performance of the predictor.

{ref}`Chapter 5<c05-combining>` discusses a combined tissue-specific RNA-Seq data sets from four experiments. I present this alongside two resources that I created in order to create this: a Python package for mapping samples to tissues, and a set of simulated tissue-specific data-sets.

[//]: # (TODO: Add a zenodo reference to uberon-py, and cite it)
[//]: # (TODO: Upload data and give it a zenodo reference and cite it)

In {ref}`Chapter 6<c06-filter>`, I discuss a filter-based gene function predictor that I entered in the CAFA3 competition{cite}`Zhou2019-jk`.

Finally, I discuss my conclusions in {ref}`Chapter 7<c07-conclusion>`.

---
**References**
```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```
