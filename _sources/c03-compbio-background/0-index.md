(c03-compbio-bg)=
# How genotype and phenotype are measured and researched
We have {ref}`just introduced<c02-biology-bg>` the biological mechanisms linking genotype and phenotype.
Next, we will discuss the details of how this connection is studied, including how data about DNA and RNA is captured, organised and stored, and how this data is used in computational biology research.

This chapter begins with a short {ref}`description of popular sequencing technologies<sequencing-technology>`, as this is relevant to both DNA and RNA.

Then in the {ref}`second section<measuring-genotype-phenotype>`, we will retrace the steps we took in {ref}`the previous chapter<c02-biology-bg>`, looking again at DNA, RNA, proteins, and phenotypes in turn, but this time considering the data gathered about each of these entities, and the data gathered about the connections between them. 
Sprinkled throughout the chapter, as they become relevant, I describe some specific examples of resources and tools used in bioinformatics and computational biology that are relevant to this thesis.

Two types of tools and resources, however, have their own sections.
The first are {ref}`biological ontologies<what-are-ontologies>`, which are efforts to unify some of the information gained in the experiments just described in earlier parts of this chapter.
Secondly, predictive computational biology methods and the ecosystem of competitions that are often used to validate them are also described separately in {numref}`section %s<predictive-methods>`. 
In this section, I also explain {ref}`my contribution to the update to the SUPERFAMILY resource<my-superfamily-contribution>`{cite}`Oates2015-li`.

I then describe some of the potential {ref}`sources of bias<compbio-bias>` in the data and tools used throughout this thesis, followed by my contribution to a project designed to counter some of these issues, {ref}`the Proteome Quality Index (PQI)<pqi>`{cite}`Zaucha2015-ez`.

Finally, I {ref}`summarise<c03-summary>` the data we currently have (and don't have) on the link between genotype and phenotype.

```{admonition} Contributions in this Chapter
:class: hint
This chapter primarily summarises the work of others, but it also contains my contributions to the following collaborative projects:
- 2014 Superfamily update paper{cite}`Oates2015-li`
    - Added some cyanobacteria genomes to the resource
    - Contributed to paper-writing/editing
- The Proteome Quality Index paper{cite}`Zaucha2015-ez`
    - Contributed to development of metrics for measuring proteome quality
    - Contributed to paper-writing/editing
```