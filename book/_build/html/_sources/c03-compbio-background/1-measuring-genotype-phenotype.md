(measuring-genotype-phenotype)=
## From genotype to phenotype: what is measured

### Introduction

```{figure} ../images/linneaus_ehret.png
---
height: 220px
name: linneaus_ehret
---
Carl Linneaus developed a system of classifying plants, animals and minerals, including plant classification based on their number of stamens{cite}`Blunt2001-wr`. The left image is a key to this classification system taken from his book, while the right image is a depiction of how the system works, drawn by botanist George Ehret{cite}`Ehret1748-bx`. 
``` 

(linneus-racist)=
```{margin} Linneus and scientific racism
Linneus' classifications included a racist hierarchical classification of human beings{cite}`Charmantier_undated-wy`.
```

Cataloguing and classifying has been a successful scientific endeavour in other disciplines (e.g. the periodic table), but it’s a cornerstone of biology. 
Biological classification dates back to the Linnaean taxonomy from the mid 1700s (see {numref}`linneaus_ehret`), which described species, their features, and the relationships between them{cite}`Jensen2010-fk`. 
The work contains some {ref}`unforgivable, hateful ideas<linneus-racist>`.
Nonetheless the idea of measuring and connecting the biological world also birthed an enduring tradition of classification in biology.
 
[//]: # (TODO: Cite data inaccessibility)
[//]: # (TODO: Cite proteindatabank Margaret Dayhoff)
[//]: # (TODO: Cross ref RNA, proteins, and phenotypes)
Modern biology continues in this tradition of classification, cataloguing biology in ever more (molecular) detail: cells, genes, transcripts, proteins, and pathways. 
While in other fields, data inaccessibility is a major barrier to reproducible research, this is the field that had an online database system that remote computers could access in the 1960s!
So, the catalogued information populates freely available databases, vocabularies, and annotations, creating controlled and shared vocabularies that fuel computational methodologies.
We will now delve into the details of some of these datasets, looking first at {ref}`DNA<dna-measurements>`, then {ref}`RNA<rna-measurements>`, then {ref}`proteins<protein-measurements>`, then {ref}`phenotypes<phenotype-measurements>`.

(dna-measurements)=
### DNA
In the {ref}`previous Chapter<what-is-dna>`, we looked at what DNA is and how that links to phenotype. 
Now we're going to look at the details of how this is measured and stored in computational biology. 
Since smaller pieces of DNA are generally talked about in relation to the whole genome, we'll go from big to small, beginning with whole genomes and moving through to individual SNPs.

#### Whole genome
The entire whole genome is all the genetic material of an organism. In humans, this means all chromosomal and mitochondrial DNA, whether or not it is transcribed into RNA, or translated into proteins.
No sequencing technology can read whole chromosomes end to end: all work by reading shorter lengths of DNA (*reads*).

(sequencing-technology)=
##### Sequencing

From the late 1970’s until the mid 2000s, *Sanger sequencing* was the most popular sequencing technology, although it underwent various improvements over this timescale. 
In Sanger sequencing (and other first-generation methods), reads of around 800bp are sequenced, one at a time. 
The human genome project sequenced the first human genome using this method{cite}`Venter2001-wn`, and it’s still used in some circumstances, for example validating next generation sequencing. 

Second, or *next generation sequencing* (NGS), also referred to as high-throughput sequencing, is a catch-all term for the faster and cheaper sequencing technologies which replaced the previously used Sanger sequencing. 
A feature that is common to NGS methods is that many shorter reads (around 100bp, exact numbers depending on the specific technology) are sequenced in parallel. 
The process is massively parallel: millions to billions of short sequences can be read at a time. 
This is a huge factor in making NGS much faster (and therefore cheaper) than Sanger sequencing. 
In turn, this speed and cheapness means that more repeats can be sequenced, increasing the overall accuracy of NGS over Sanger (despite the accuracy of each individual read being generally lower).

There are now also third generation sequencing technologies that allow much longer reads to be sequenced.

(assembly-and-alignment)=
##### Assembly
Whichever {ref}`technology<sequencing-technology>` is used, DNA is sequenced in smalls sections, which must then be *assembled* to make the full genome, organised into chromosomes. 

[//]: # (TODO: Check that aligment is referenced in the text and that the image is)
[//]: # (TODO: Replace with better more DNA-centric image)

```{figure} ../images/alignment.png
---
height: 240px
name: alignment
---
Image showing how RNA-Seq reads are mapped to the genome (image from Advancing RNA-Seq Analysis {cite}`Haas2010-lm`). A similar process is followed for DNA.
``` ``

[//]: # (TODO: delete extra backticks)

The short reads that are the output of initial sequencing must be assembled to create longer sequences of DNA, whether that's genes or whole genomes. 
This is done by aligning reads to one another and (if available) to an existing reference sequence. 
This of course requires the reads to overlap, so longer and more numerous reads make this task easier.

The current estimate for raw sequencing accuracy of an individual NGS read is around 0.24%{cite}`Pfeiffer2018-kt`, meaning that on average one base pair will be incorrect for a 500pb read.
Multiple repeats are therefore required to obtain a more accurate measurement of the assembled sequence, which is further necessary since there are many repeated sequences (perhaps over two thirds of the human genome{cite}`De_Koning2011-ac`).
The depth (or coverage) for a nucleotide is the number of reads that overlap that nucleotide. Similarly, the average depth of a sequence can be calculated. 

After assembly, even in the most complete genomes, we are still left with some sequences that could not be placed, and some parts of the genome that we still don't know about. 

(human-references)=
##### The human reference genome
As {ref}`previously mentioned<genomes>`, reference genomes are designed to represent whole organisms: these genomes aim to have the most common allele at any given nucleotide, and are then annotated at positions where individuals differ. 

[//]: # (TODO: cite sequencing artifacts)
**Builds and patches:** 
As more genomes are sequenced, more information comes to light about the nature of the human genome. 
For example, some locations are revealed to be likely sequencing artifacts. 
New major versions of genomes are released every few years to fix these changes. 
These versions are called *builds*.

[//]: # (TODO: insert table of builds here. Name, year, size?)

```{list-table} Table showing human reference genome builds.
:header-rows: 1
:name: build-table

* - Release name
  - UCSC
  - Release date
* - GRCh38
  - hg38
  - December 2013
* - GRCh37
  - hg19
  - February 2009
* - NCBI Build 36.1
  - hg18
  - March 2006
```

Between builds and patches, sequences may be added, removed, or moved to different locations on chromosomes.

[//]: # (TODO: Explain and cite differences between grc and uscs build versions, cross-ref table)
**Differences between GRC and UCSC builds: **
Different versions of the builds are released by the Genome Reference Consortium (GRC) and the University of California Santa Cruz (UCSC) Genomics Institute. 
These are generally used interchangeably by researchers, but there are some differences between them. 
These differences including formatting differences (storing chromosome as integers rather than strings like 'chr1'), the inclusion of mitochondrial DNA, as well as small numbers of differences of the locations of some variants on some chromosomes.

##### Whole Genome Sequencing of individuals
When individual humans have their whole genomes sequenced, this is compared to the human reference genome. 
The alleles at each location are commonly stored in Variant Call Format (VCF) files. 
These describe the locations on the genome of variations between individuals, given by chromosome, position, variant identifiers, and the variation between a given number of individuals.

[//]: # (TODO: Include sample of VCF to break up text?)

**Position and BED formats**

[//]: # (TODO: Write)

#### Genes
[//]: # (TODO: Write: sequenced the same way, persistent identifiers, which map to genomes)

#### Variants
[//]: # (TODO: Sentence about variants)

[//]: # (TODO: Rewrite microarrays section below to be more about genotyping)
##### Microarrays
Through the 1970s into the early 2000s, DNA arrays/microarrays developed alongside sequencing as a way of measuring the presence of previously sequenced DNA in new samples. 
These arrays contain pre-chosen fragments of DNA (probes) arranged in spots, with each spot containing many copies of the probe, on a solid surface, e.g. glass, silicon or plastic. 
The probes consist of single strands of DNA, and arrays operate on the principle that the complementary DNA from the sample will bind tightly to it.

These arrays were originally macro-sized, one of the first being 26 × 38 cm and containing 144 probes{cite}`Bumgarner2013-hg`, but are now on small chips, which can contain up to millions of probes.

Arrays were extremely popular for measuring gene expression, but this technology has largely been superseded by the more accurate and comprehensive RNA-seq. 
However, microarrays are still commonly used by companies like 23andMe for genotyping an individual (measuring specific alleles).

##### Variant databases
Databases like dbSNP, clinVar, and SNPedia contain information about the location of SNVs, their possible alleles, and their association to diseases. 
These are often used as part of a variant prioritisation pipeline, as well as by individuals who are investigating their own SNVs.

The NCBI’s dbSNP{cite}`Sherry2001-nm` is the world’s largest database of nucleotide variations, including their locations, possible alleles, and associations to diseases. 
It contains information from ten organisms (including human) and has information on indels and short tandem repeats in addition to SNVs. It was designed to store the annotations that are outputted from GWAS studies. 
Anyone can submit their findings about variants, and they must indicate what sort of evidence they have for the association.
The database gives SNVs unique identifiers (Reference SNP cluster IDs, a.k.a. RSIDs) of the form rs###, which are used by many other resources.

[//]: # (TODO: mention the ss numbers, and that the dbSNP builds don't "line up" with the human reference builds, how they are merged and the fact that they might map to different alternate contigs)

[//]: # (TODO: mention snpedia?)

(rna-measurements)=
### RNA
[//]: # (TODO: Rewrite this section, and maybe move it to section 1, so that it fits properly and is less wordy)
[//]: # (TODO: Write about how transcripts map to the genes ENSEMBL)

DNA can’t tell us the whole story. On it's own it can’t tell us what we’d like to know about a gene’s function or a person’s traits. Nonetheless, I’d like to spell out why that is for those who do not have that background. The central dogma of molecular biology can be paraphrased as “DNA makes RNA makes proteins”. So, if we know what a person’s DNA is, then why would we also want to know about their RNA?

The answer boils down to the effect of the environment. “DNA makes RNA makes proteins” is shorthand for “DNA interacts with the environment to make RNA, and RNA interacts with the environment to make proteins”. The environment, of the cell, and of the individual, and even of modifications to the DNA molecules, is the reason why DNA alone is not enough to explain how we function. DNA is the collection of blueprints for what can be made, but the environment decides what goes into production; which RNA and proteins are made and how much. 

In any given individual, the same DNA is present in their liver cells, skin cells, and neurons. The difference in how these cells/tissues look and function is due to differences in which proteins are actually being made at any given time. Gene expression is a way of measuring how the environment of the cell is affecting the process of making proteins from DNA.

Gene expression data is used to understand the function of genes, to identify housekeeping genes, to re-engineer gene regulatory networks, and more. This kind of insight can not be gained from looking at DNA alone.


#### RNA-seq 
NGS can be used for sequencing either DNA or RNA (known as RNA-seq when applied to the whole transcriptome).

While (NGS) DNA-sequencing and RNA-seq can use the same underlying NGS technologies, there exist some notable differences. For example, RNA is reverse-transcribed into strands of complementary DNA, before being sequenced, since sequencing DNA is currently easier than sequencing RNA. RNA-seq is used much less often for de novo sequencing, and is generally mapped to a reference sequence. 

Since transcription is dependent on time, tissue, location, cell, etc, RNA-seq experiments are also dependent on all of these conditions. Furthermore, they are sensitive to differences in laboratory conditions and experimental design, creating artefacts in the resulting data known as batch effects. 

[//]: # (TODO: Write something breif reminding what gene expression is and why it is measured, referring back to Ch1)

One of the most popular measures of gene expression, is the measure of how much RNA is in a cell at a given time. 

#### FANTOM Consortium
[//]: # (TODO: ADd Fantom5 citation, move this bit to somewhere sensible.)
As the human genome project was nearing completion, researchers had a parts list of human biology, but few of the functions of these parts (genes) were known. A consortium of scientists formed, named after the challenge they were addressing: the Functional ANnoTation Of the MAmmalian genome (FANTOM). 

[//]: # (TODO: Fix FANTOM5 citation)
The consortium has run a range of large scale collaborative projects in five rounds to further this goal. The first FANTOM project used only the mouse genome, but later versions also included human. The latest project, FANTOM5[80] represents one of the most comprehensive collections of gene expression data. It contains a combination of human, mouse, health, and disease data, as well as time courses and cell perturbations

#### The Gene Expression Atlas
The Gene Expression Atlas{cite}`Petryszak2016-je` (GxA) is the European Bioinformatics Institutes’ open source gene and protein expression database, and the largest of its type. At the time of writing, it contains over 3,000 gene expression and protein abundance experiments across many organisms, organism parts (tissues), diseases, and sequencing technologies. There is a separate atlas for scRNA-seq experiments. 

#### Gene expression data pipeline
[//]: # (TODO: This section needs more work)

Whether gene expression data gathered is gathered using microarrays or RNA-Seq, it goes through a substantial pipeline before it is used in a statistical analysis, or made available as a resource.

##### Quality Control
[//]: # (TODO: This only cites illumina, obviously there are other ways to sequence rna)
Before RNA-Seq data undergoes alignment, it undergoes quality control. This involves comparing sequencing parameters to a data set of known accuracy{cite}`Illumina2014-nd` and is usually done as part of the sequencing.

##### Normalisation - within-sample normalisation
Within-sample normalisation methods are designed to account for sequencing depth and gene length so that gene expression values from the same sample (e.g. different replicates) can be more easily compared. Longer genes will have more reads mapped to them for an equal level of expression, so RNA-seq will report more counts. Similarly, without normalising, samples with greater sequencing depth will have higher counts for an equal level of expression. 

RPKM/FPKM (Reads/Fragments Per Kilobase Million) and TPM (Tags Per Million) are the three major normalisation techniques used for this purpose. In RPKM and FPKM, counts are first normalised for sequencing depth, and then for gene length. This means that they are suitable for comparing within a sample (e.g. between replicates. TPM, however performs the same steps in the opposite order, which has the desirable effect of ensuring that columns corresponding to TPM normalised samples sum to the same number. This means that TPM gives us a measure of relative abundance; we can compare across samples which proportion of counts are from each gene. For this reason, TPM is now generally preferred over RPKM/FPKM{cite}`Wagner2012-ac,Pimentel2014-xm`.

##### Normalisation - between-sample
While TPM gives us a measure of relative abundance, it does not give us a measure of absolute abundance. One outlying gene which is highly expressed will have the effect of making all other genes look relatively less expressed. We might expect this to occur, particularly when samples are under different conditions (e.g. disease/treatment). Between-sample normalisation methods are designed to counter this issue, and enable researchers to compare different samples.

These methods adjust counts to reduce the impact of outlying expression values. Examples include scale normalisation methods like TMM (used in edgeR{cite}`Robinson2010-kl`), the Log Geometric Mean (used in DESeq2{cite}`Robinson2010-kl,Love2014-vx`), and quantile normalisation (giving samples the same distribution of counts).

##### Batch correction
Even after all this normalising, systematic effects can be present in gene expression data, due to sequencing batch, or some correlated condition. All types of gene expression data are known to suffer from these batch effects{cite}`Leek2010-yw`; unwanted variation associated with the batch it was sequenced in, resulting from unknown variation during the process of sequencing for example the date, time, or location of sequencing{cite}`Irizarry2005-ie`, or the technician doing the work. Some of these effects may be due to factors that might be expected to genuinely influence expression of genes, such as temperature, time of year, humidity, diet, individual, age, etc. Covariates such as these are often unrecorded and/or not reported, so it is not easy to distinguish these from those due to protocol differences, such as reagents, personnel doing the sequencing, hardware, processing pipeline, etc. 

Batch effects can often confound and obscure the biological differences of interest between samples (e.g. tumour versus healthy tissue). At best, batch effects add random variation to expression measurements, which obscure signals. Often they can also add systematic differences that can lead to incorrect biological conclusions{cite}`Leek2010-yw`. They are a problem for analysing the output of an individual experiment where there are multiple sequencing batches, but pose a particular problem in combining data from different experiments, as there is almost certainly more variations between analysis pipelines.

When it is known, date of sequence processing is often used as a surrogate for batch, enabling researchers to check for, and then remove, batch effects if necessary. Principal components analysis is often used to visually inspect experimental results for batch effects; when biologically alike samples cluster together rather than those from like-batches, batch effects are often ignored. Batch effects may affect only specific subsets of genes, and may affect different genes in different ways{cite}`Leek2010-yw`. This means that normalisation (e.g. TPM, FKPM) will not account for batch.

(protein-measurements)=
### Proteins
[//]: # (TODO: Mention how proteins map to transcripts and to genes and variants and whole genomes)

#### Protein classification
Scientists are often interested in a "favourite" gene or protein, or have obtained a list of genes or proteins that they are interested in through a recent experiment. If an experiment about the specific protein has been carried out (e.g. to determine its function or structure), then a database like Uniprot (containing function and sequence information) or PDB (structure information) can be queried. However, this kind of information is not available for all proteins, so this is often necessary to make inferences about protein structure or function based on for example sequence similarity or protein classification.

[//]: # (TODO: Check BLAST is in the right place. Probably makes more sense in another section: DNA?)
##### BLAST
BLAST, or the The Basic Local Alignment Search Tool{cite}`Altschul1990-zf`, is an extremely popular tool that is used to perform a basic search of nucleotide or amino acid sequences to known sequences, based on statistically significant similarities between parts of the sequence.

##### SCOP
The Structural Classification of Proteins (SCOP) database{cite}`Murzin1995-se` classifies all proteins with known structure based on their structural similarities, based on the consideration of the protein’s constituent domains. The classification is mostly done at the level of families, superfamilies, and folds arranged in a tree structure. Families represent the most similar proteins, which share a “clear evolutionary relationship”, while superfamilies represent less close evolutionary relationships, and folds represent the same secondary structure. This protein classification task, while aided by automation, was carried out largely by manual visual inspection.

SCOP was updated until 2009, but has been succeeded by SCOP2{cite}`Andreeva2014-om`. However, SCOP2 has a different underlying classification system, based on a complex graph, rather than a hierarchy. The CATH (Class, Architecture, Topology, Homologous superfamily){cite}`Orengo1997-vf` database provides another classification system, (also operating hierarchically), but created mostly via automation, which leads to major differences between the classifications{cite}`Csaba2009-of`.

##### SUPERFAMILY 
SUPERFAMILY{cite}`Gough2001-ct` uses HMMs to assign sequences to SCOP domains, primarily at the superfamily level. This allows the functions of poorly understood proteins to be inferred based on how closely they match known superfamilies. HMMs are very successful at such assignments since pairwise correlations between proteins (or their domains) and other proteins in the family may be weak, but consistently for many proteins; this can be picked up by an HMM. The superfamily level is chosen since it is the broadest level which suggests evolutionary relationships, but SUPERFAMILY also generates assignments at the (stricter) family level.

HMMs are created by first finding closely relating protein homologs for a given protein superfamily using BLAST, and then extending it by comparing the HMM to more distantly related homologs. The resulting HMM library is fine-tuned by some manual curation. 

The SUPERFAMILY website also contains other tools, including a database of all sequences (genomes) which are used to generate the HMM library.

(my-supfam-contribution=)
**SUPERFAMILY update**
I contributed to SUPERFAMILY’s 2014 update{cite}`Oates2015-li` by editing the paper, uploading a small number of proteomes. The SUPERFAMILY database of proteomes doubled from 1400 to over 3200 from 2010 to 2014. The update paper described this development, as well as highlighting SUPERFAMILY as a resource for unique proteomes that are not found elsewhere (e.g. Uniprot). Although SUPERFAMILY’s primary resource is it’s HMM library, it also integrates a range of other tools for sequence analysis, for example protein disorder prediction (D2P2) and GO annotation (dcGO), as well as a domain-based phylogenetic tree. 

(phenotype-measurements)=
### Phenotypes

[//]: # (TODO: Explain that phenotypes can be at any "level", i.e. calcium level in blood, or height.)
[//]: # (TODO: Also explain that phenotypes can be associated with biological molecules at any level, e.g. SNPs, Genes, Populations)

(what-are-ontologies)=
#### A word on ontologies
[//]: # (TODO: Maybe move this to the first mention of ontologies?)
For many of different biological molecules, ontologies a a popular way of storing information about anatomical entities. 
All ontologies contain entities names and descriptions (e.g. diseases, gene functions), different classifications of those entities (e.g. immune system disorders) and relate these classifications to one another hierarchically, sometimes with multiple types of relationships (e.g “is a”, “part of”). Hierarchical ontologies can be thought of as having a tree-like structure with one, or just a few root terms which are very general terms that all other terms in the ontology are related to, for example “biological process”, and leaf terms, which are the most specific terms in the ontology (e.g “positive regulation of cardiac muscle tissue regeneration”). 

Relations between terms are directional, for example “positive regulation of cardiac muscle tissue regeneration” is a “regulation of cardiac muscle tissue regeneration”, but not vice versa. In such relationships the parent term is the more general term closer to the root (“positive regulation of…”) and the child term is the more specific term (“regulation of..”). It is not permitted for there to be cycles in ontologies, for example *term A* `is_a` *term B* `is_a` *term A*. 

Terms in ontologies are given identifiers, usually of the form: `XXX:#######`, where `XXX` is an upper-case identifier for the whole ontology, e.g. `GO` for Gene Ontology, `CL` for Cell Ontology, etc. For example, `GO:0008150` is the GO term for *Biological Process*.

Ontologies are generally created through some combination of manual curation by highly skilled biocurators and logic-testing (checking for illogical relationships, for example using ROBOT{cite}`Overton2015-vo`). Creating an ontology is generally a long-term project, with new suggestions and updates to the ontologies being made as new knowledge accumulates, or just as more people have time to add to them. As well as being the work of dedicated curators, contributions to ontologies can usually be crowd-sourced from the scientific community using GitHub issues, mailing list discussions, web forms, and dedicated workshops. In this way, they are similar to other bioinformatics community-driven efforts like structural and sequence databases. 

There are also cross-ontology mappings and annotations, where terms from one ontology are linked to those in another (e.g. relating gene functions and tissues) or to entities in a database (e.g. gene functions to genes). These also require the work of dedicated curators, who search through literature, assessing various criteria for the inclusion of an annotation (such criteria vary by ontology). Since this is a laborious process, there are also many computational methods to annotate ontology terms automatically. 
 
There are two major file formats in which ontologies are currently stored. The OBO format is a human-readable format, while the OWL format is more complex, but has more functionality. The OWL format can be queried using querying languages, for example SPARQL (an SQL-like querying language).  

Ontologies can be used by researchers to investigate specific genes, tissues, functions of interest, or more generally to get a big-picture viewpoint on large groups of such entities. Ontologies and particularly their annotations are varying degrees of incomplete, and this will have an impact on the results of any downstream use of them. 


##### Gene Ontology
[//]: # (TODO: Citations in GO section)
```{figure} ../images/go_rilla.png
---
height: 220px
name: go_rilla
---
A subsection of the Gene Ontology with arrows showing the existence of relationships (image generated using GOrilla{cite}`Eden2009-ic`)
``` ``

[//]: # (TODO: delete ``` above)

The Gene Ontology (GO){cite}`Ashburner2000-cr` is one of the first biomedical ontologies, and continues to be one of the most popular. 
It is a collection of resources for cataloging the functions of gene products and designed for supporting the computational representation of biological systems{cite}`Thomas2017-vm`. 
It includes:
1. The standard gene ontology, which is a hierarchical set of terms describing functions.
2. The gene ontology annotations (GOA) database, which contains manual and computationally derived mappings from gene products to gene ontology terms.
3. Tools for using and updating these resources.

The Gene Ontology defines the “universe” of possible functions a gene might have, while the functions of particular genes are captured as GO annotations{cite}`Thomas2017-vm`.

The terms in the GO ontology are subdivided into three types (molecular function, biological process, and cellular component), meaning that GO is actually a collection of three ontologies{cite}`Ashburner2000-cr`. 
Gene products in GO are assumed to carry out molecular-level process or activity (molecular function) in a specific location relative to the cell (cellular component), and this molecular process contributes to a larger biological objective (biological process){cite}`Thomas2017-vm`.


[//]: # (TODO: Write something about "gene function" and "protein function" and their relationship to phenotypes, ontologies, etc)

---
**Chapter References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```