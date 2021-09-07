(c01-philosophy)=
# Thesis style and philosophy

The abstract and background chapters provide the scientific introduction to this thesis, describing the research aims and context.
This short chapter, on the other hand, explains the choices of style and research philosophy.  

(unusual-things)=
## Unusual stylistic choices in this thesis

There are a few unusual things about the format of this thesis: some easter eggs that made it easier for me to push through and finish it, and which also represent some of the things I like most about research: making it transparent, inclusive, and accessible.

````{margin} Bristol Crest
:name: bristol-crest

```{image} ../images/bristol-crest.png
:width: 185px
:align: center
```

The official University of Bristol crest (above) has symbols for the Wills, Fry, and Colston families. These families made their wealth in industries built on slavery and used some of that wealth to found the University of Bristol.

```{image} ../images/bristol-alt-crest-red.png
:width: 185px
:align: center
```

I drew an alternative crest which has symbols for three of my favourite Bristol festivals instead: Upfest, the Balloon Fiesta, and St Paul's Carnival.
````

First, in the spirit of trying to make my work as reproducible and Open as possible, this thesis is available online as a Jupyter Book{cite}`Executable_Books_Community2020-ls` [here](https://nataliethurlby.github.io/phenotype_from_genotype/).
I would recommend reading it online unless you really like your PDF viewer, since it includes some interactive features which don't translate to PDF.
This book was written entirely in markdown documents and Jupyter Notebooks - which means that most of the graphs within are created directly from these notebooks.

The second unusual thing about this thesis is that you will see asides mentioning researchers who have been involved in eugenics and/or racism.
This is the unfortunate reality of much of the history of the field, and I didn't want to highlight the scientific achievements of these individuals, without also acknowledging their legacy of scientific racism, particularly in the light of the Black Lives Matter movement.

```{margin} Illustrations 
:name: illustrations
The illustrations are CC-BY licensed (use freely, with attribution) in case they are useful to anyone. 
```

For the same reason, I also drew an alternative University of Bristol crest, which you can see on the title page and in {ref}`this<bristol-crest>` margin comment.
This is also an example of the third weird thing about this thesis, which is that I drew some {ref}`illustrations<illustrations>` for it (using Krita{cite}`noauthor_undated-ns`), particularly in the background chapters.
My aim in including the majority of these drawings was simply to illustrate concepts, and help the reader (and myself) imagine some of the incredible stuff that is going on in all of our bodies.

(research-philosophy)=
## Research philosophy
Here I explain a little about my approach to the work in this thesis.
I'm including this to add clarity about the lenses through which I did this work, as well as what I consider to be a scientific contribution.

(rp-complexity-science)=
### Complexity science, systems biology and multi-omics

This PhD was completed as part of the Bristol Centre for Complexity Science.
Complexity science is the study of systems of interacting parts, i.e. the study of parts of the world where reductionism breaks down. 
Typical applications of complexity science are predator-prey models, epidemiological modelling (e.g. of pandemics), protein-protein interaction networks, or models of neurons.
When applied to biology, it often falls under the banner of Systems Biology.

````{margin} 
```{admonition} Emergence
:name: emergence
Emergent properties of systems are properties that are found only when the consistuent entities of those systems interact, for example traffic jams emerge when vehicles interact on a network of roads{cite}`Bonabeau2002-fk`, or cheetah's spots emerge when chemicals diffuse across cells{cite}`Turing1990-ay`. 
```
````

Everything in this thesis looks at biology at the level of whole genomes, whole organisms, whole species, or even across the tree of life, and takes the view that this is necessary if we want to understand {ref}`emergent<emergence>` properties of these interactions.
Where I do "zoom in" to a particular case study or the details of some data, I am usually doing so either to understand how the complex systems approach is working, or in order to feed back and improve the resources that make the systems approach possible.

The work in this thesis could also be considered multi-omics.
 I integrate, combine and harmonise some of the large, collaborative "omics" (e.g. genomics, proteomics) data projects that are available in this field, to create new resources and make new predictions.

A complex systems approach does not mean taking into account all parts of a system.
In modelling our infinitely complicated reality, we have to simplify to some extent, whether this means not taking properties such as location or speed of reactions into account, not taking certain entities or classes of processes into account. 
Discovering what must be included and what can be left out is one outcome of this type of research. 

(rp-team-science)=
### Team science
Computational biology is a field which I see as characterised by excellent examples of team science, from the Human Genome Project to Biomedical Ontologies.
I think that the best progress can be made when we all work together to create robust resources and build on each other's work and are fairly credited for that.
I recognise that not everyone shares this view, computational biologists who use the results of other scientists experiments have been referred to by some as [“research parasites"](https://www.nejm.org/doi/full/10.1056/nejme1516564), or seen as a branch of IT services to whom "real" scientists can export technical work. 
In this thesis, however, I take the view that contributing to existing scientific resources (Open Source or curated information), software engineering, writing, coming up with hypotheses all fall under the banner of scientific contribution.
This is in line with policies like the [Contributor Roles Taxonomy](https://www.elsevier.com/authors/policies-and-guidelines/credit-author-statement), and the recent additions of data sets and [research software](https://www.software.ac.uk/REF2021guidance) to the Research Excellent Framework (REF) research outputs.

(rp-open-reproducible)=
### Open and reproducible science
[//]: # (TODO: link to reproducibility crisis bit)
During my PhD, one aspect of research came as quite a surprise to me, which was that I couldn't trust the results of peer-reviewed papers to the extent that I originally assumed. 
As the {ref}`reproducibility crisis<reproducibility-crisis>` unfolded, it became clear that the "untrustworthiness" of research was also an issue for many other researchers.
Since then, it has been an important part of the way that I do research, and I have made as much of my work as reproducible and Open as I could, taking new items from the Buffet of Open Research{cite}`Whitaker2020-bx` as I continued.
I describe the ways in which I do this as they come up.
Some earlier parts of my work, particularly {numref}`chapter %s<c04-snowflake>` do remain closed-source. 

[//]: # (TODO: link to MAPS)
We might like to think that scientific research is the "view from nowhere", that it is objective, and simply measuring reality.
The reality, however, is that there are many, often equally valid, decisions to make when doing research and these decisions will impact the results of that research (as I will explain later).
If these decisions are not documented, the validity of the research can be obscured, and in addition, one aspect of scientific work that makes it difficult for other people to build on is that materials or details of analyses are not freely shared.
For these reasons, in this thesis, I tried to include enough detail so that the work could be reproduced (repeated to get the same answer), and the decisions made understood.
