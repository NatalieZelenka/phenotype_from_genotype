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

[//]: # (TODO: Check that this is true)

The central theme of this thesis is the relationship between protein function - at either a molecular or phenotypic level - and the sequence of its associated DNA and RNA. 
A recurring motif is impact of the provenance of related data and what that means for attempts to make genome-wide predictions about these relationships. 

## Weird stuff

There are a few unusual things about the format of this thesis. 
They are some extras that made it easier for me to push through and finish this thesis, and they also represent some of the things I like most about research: making it trustworthy and transparent, inclusive, and accessible.

[//]: # (TODO: Cite Jupyter Book)

First, in the spirit of trying to make my work as reproducibly and Open as possible, this thesis is available online as a Jupyter Book.
This means that the book is written in markdown documents and Jupyter Notebooks - which means that some of the (later) graphs are created directly from these notebooks.
The latest version is available online [here](https://nataliethurlby.github.io/phenotype_from_genotype/) - which is where it is best to view it (as html rather than a pdf). 

[//]: # (TODO: Crest compare)

```{margin} Bristol Crest
:name: bristol-crest
The original crest has symbols for the Wills, Fry, and Colston families. 
These families made their wealth in industries built on slavery and used some of that wealth to found the University of Bristol.
The alternative crest has symbols for three of my favourite Bristol festivals: Upfest, the Balloon Fiesta, and St Paul's Carnival.
```

This brings me to the second unusual thing about this thesis, which is that I have mentioned as asides in this thesis researchers who have been involved in eugenics and/or racism. 
I did this because I don't want to highlight the scientific achievements of these individuals, without also acknowledging their legacy of scientific racism, particularly in the light of the Black Lives Matter movement.

The Black Lives Matter movement also inspired my alternative University of Bristol crest, which you can see on the title page and in this margin comment.
This is an example of the third weird thing about this thesis, which is that I drew some {ref}`illustrations` for it (using Krita{cite}`noauthor_undated-ns`), particularly in the background Chapters.
My aim in including the majority of these drawings was to illustrate concepts, and help the reader (and myself) imagine some of the amazing stuff that is going on in the body.

```{margin} Illustrations 
:name: illustrations
The illustrations are CC-BY licensed (use freely, with attribution) in case they are useful to anyone. 
```

## Chapter Structure

{ref}`Chapter 2<c02-biology-bg>` contains the biological background information on which the rest of the thesis is based. 
It tells the story of how phenotype arises from genotype, and introduces the different biological molecules that are involved. 
It begins at the very basics: what are DNA, RNA, proteins, and phenotypes? 
How are they related?
How do we categorise them?
This background is intended to make this thesis readable to someone without a background in biology. 
It does not contain any of my own research. 

{ref}`Chapter 3<c03-compbio-bg>` is a second background chapter, which contains some of my own work. 
It follows on from the first by discussing popular resources in computational biology, their provenance, and the impact of this on the field. 
This includes mathematical modelling of publications of named genes and sensitivity analysis of gene enrichment analyses. 
I also present here my contributions to reproducibility-related collaborative projects that I have and continue to be involved with: the Proteome Quality Index paper{cite}`Zaucha2015-ez`, my contribution to the collaborative 2014 SUPERFAMILY update paper{cite}`Oates2015-li`, and the (ongoing) MAPS project. 

In {ref}`Chapter 4<c04-snowflake>`, I describe my preliminary efforts to integrate the data sources described in the background chapters into Snowflake, a phenotype predictor{cite}`Gough2017-ik`. I discuss potential reasons for the poor performance of the predictor.

In {ref}`Chapter 5<c06-filter>`, I discuss a filter-based gene function predictor that I entered in the CAFA3 competition{cite}`Zhou2019-jk`. 

[//]: # (TODO: Add a zenodo reference to uberon-py, and cite it)
[//]: # (TODO: Upload data and give it a zenodo reference and cite it)

{ref}`Chapter 6<c05-combining>` discusses a combined tissue-specific RNA-Seq data sets from four experiments.
I present this data set as a resource, alongside a Python package that I created in order to do this: `uberon-py`.

Finally, I discuss my overall conclusions in {ref}`Chapter 7<c07-conclusion>`.
