(measuring-genotype-phenotype)=
## From genotype to phenotype: what is measured
[//]: # (TODO: Mention that Linneaus is a racist)
Cataloguing and classifying has been a successful scientific endeavour in other disciplines (e.g. the periodic table) but it’s particularly a cornerstone of biology. Biological classification dates back to the Linnaean taxonomy from the mid 1700s (see {numref}`linneaus_ehret`), which described species and their features and the relationships between them{cite}`Jensen2010-fk`. Biology today continues in this same tradition, classifying and cataloguing biology in ever more (molecular) detail. Computational biology is fueled by big community efforts to develop these databases, vocabularies, and annotations. While in other fields, data inaccessibility is a major barrier to reproducible research in other fields, this is the field that had an online database system that remote computers could access in the 1960s! These efforts remain central to computational biology and have enabled investigations into whole genomes, transcriptomes, organisms, or the entire phylogenetic tree. This openness, and the focus on well-organised and archived data is not something that we should take for granted.

```{figure} ../images/linneaus_ehret.jpg
---
height: 220px
name: linneaus_ehret
---
Carl Linneaus developed a system of classifying plants, animals and minerals, including plant classification based on their number of stamens{cite}`Blunt2001-wr`. The left image is a key to this classification system taken from his book, while the right image is a depiction of how the system works, drawn by botanist George Ehret{cite}`Ehret1748-bx`. 
``` `` 
[//]: # (TODO: remove extra backticks)
[//]: # (TODO: Cite PDB online database, Margaret Dayhoff)

There are large datasets on everything from gene functions to cells, and diseases to anatomical entities. These datasets create a shared vocabulary that we can all use to discuss these entities, as well as capturing knowledge about them so that it can elucidate other research these entities, or be used in larger-scale analysis. We will now delve into the details of these datasets.

(what-are-ontologies)=
#### A word on ontologies
[//]: # (TODO: Maybe move this to the first mention of ontologies?)
For many of different biological molecules, ontologies a a popular way of storing information about anatomical entities. 
All ontologies contain entities names and descriptions (e.g. diseases, gene functions), different classifications of those entities (e.g. immune system disorders) and relate these classifications to one another hierarchically, sometimes with multiple types of relationships (e.g “is a”, “part of”). Hierarchical ontologies can be thought of as having a tree-like structure with one, or just a few root terms which are very general terms that all other terms in the ontology are related to, for example “biological process”, and leaf terms, which are the most specific terms in the ontology (e.g “positive regulation of cardiac muscle tissue regeneration”). 

Relations between terms are directional, for example “positive regulation of cardiac muscle tissue regeneration” is a “regulation of cardiac muscle tissue regeneration”, but not vice versa. In such relationships the parent term is the more general term closer to the root (“positive regulation of…”) and the child term is the more specific term (“regulation of..”). It is not permitted for there to be cycles in ontologies, for example “term A” is a “term B” is a “term C” is a “term A”. 

Terms in ontologies are given identifiers, usually of the form: XXX:#######, where XXX is an upper-case identifier for the whole ontology, e.g. “GO” for Gene Ontology, “CL” for Cell Ontology, etc. For example, GO:0008150 is the GO term for “biological process”.

Ontologies are generally created through some combination of manual curation by highly skilled biocurators and logic-testing (checking for illogical relationships, for example using ROBOT{cite}`Overton2015-vo`). Creating an ontology is generally a long-term project, with new suggestions and updates to the ontologies being made as new knowledge accumulates, or just as more people have time to add to them. As well as being the work of dedicated curators, contributions to ontologies can usually be crowd-sourced from the scientific community using GitHub issues, mailing list discussions, web forms, and dedicated workshops. In this way, they are similar to other bioinformatics community-driven efforts like structural and sequence databases. 

There are also cross-ontology mappings and annotations, where terms from one ontology are linked to those in another (e.g. relating gene functions and tissues) or to entities in a database (e.g. gene functions to genes). These also require the work of dedicated curators, who search through literature, assessing various criteria for the inclusion of an annotation (such criteria vary by ontology). Since this is a laborious process, there are also many computational methods to annotate ontology terms automatically. 
 
There are two major file formats in which ontologies are currently stored. The OBO format is a human-readable format, while the OWL format is more complex, but has more functionality. The OWL format can be queried using querying languages, for example SPARQL (an SQL-like querying language).  

Ontologies can be used by researchers to investigate specific genes, tissues, functions of interest, or more generally to get a big-picture viewpoint on large groups of such entities. Ontologies and particularly their annotations are varying degrees of incomplete, and this will have an impact on the results of any downstream use of them. 


### DNA
In the {ref}`previous Chapter<what-is-dna>`, we looked at what DNA is and how that links to phenotype. 
Now we're going to look at the details of how this is measured and stored in computational biology. 
Since smaller pieces of DNA are generally talked about in relation to the whole genome, we'll go from big to small, beginning with whole genomes and moving through to individual SNPs.

#### Complete genome sequences
[//]: # (TODO: Move sequencing technology bit to here?)
Whichever {ref}`technology<sequencing-technology>` is used, DNA is sequenced in smalls sections, which must then be *{ref}`assembled<assembly-and-alignment>`* to make the full genome, organised into chromosomes. We are also left with some sequences that could not be placed, and some parts of the genome that we still don't know about. 


##### File and field formats
**FASTA**

[//]: # (TODO: Write)

**VCF**
Reference genomes are commonly described by Variant Call Format (VCF) files, which describe the locations on the genome of variations between individuals, given by chromosome, position, variant identifiers, and the variation between a given number of individuals.

**Position and BED formats**

[//]: # (TODO: Write)


(human-references)=
##### Human Reference Genomes
As {ref}`previously mentioned<genomes>`, reference genomes are designed to represent whole organisms: these genomes aim to have the most common allele at any given nucleotide, and are then annotated at positions where individuals differ.

(reference-genome-versions)=
###### Versions
[//]: # (TODO: cite sequencing artifacts)
**Builds and patches**
As more genomes are sequenced, more information comes to light about the nature of the human genome. 
For example, some locations are revealed to be likely sequencing artifacts. 
New major versions of genomes are called *builds*.
In addition, smaller *patch* updates are sometimes added to the builds.

[//]: # (TODO: insert table of builds here. Name, year, size?)

Between builds and patches, sequences may be added, removed, or moved to different locations on chromosomes. 

[//]: # (TODO: Explain and cite differences between grc and uscs build versions)
**Differences between GRC and UCSC builds**
Different versions of the builds are released by the Genome Reference Consortium (GRC) and the University of California Santa Cruz (UCSC) Genomics Institute. 
These are generally used interchangeably by researchers, but there are some differences between them. 
These differences including formatting differences (storing chromosome as integers rather than strings like 'chr1'), the inclusion of mitochondrial DNA, and the 


###### Alternate Contigs
[//]: # (TODO: Write)
The latest version of the human reference genome (hg38/GRCh38) also 

(pqi)=
##### PQI
[//]: # (TODO: Move this section to part 3: sources of bias)
[//]: # (TODO: Explain that it is about where there is also proteins/proteomes)

The Proteome Quality Index (PQI) is an attempt to provide quality metrics about completed genome sequences. It was a group effort, which resulted in a paper{cite}`Zaucha2015-ez`, of which I am an author, as well as [an associated website (http://pqi-list.org/)](http://pqi-list.org/). I contributed to discussions about metrics, and paper editing.

The motivation for creating the index came from problems of reproducibility in the field of genomics. In creating a daily-updated tree of life (sTOL, sequenced Tree Of Life), it was found that many sequenced genomes were missing vital proteins due to poor sequencing{cite}`Fang2013-et`. Such genomes are reused by many researchers, for example in comparative genomics, and omissions of whole proteins and poor accuracy of others are likely to affect research results. 

The PQI website was intended to be both a way for users of past genomes to look up the quality of a genome in advance of some research and, more importantly as a talking point for quality guidelines for genomes/proteomes. While quality control and data submission guidelines were more developed in other areas of computational biology, similar guidelines for genome quality were lacking.

###### PQI features 

The PQI website provides a scoring system for proteomes, bringing together numerous different metrics which are normalised before being averaged into an intuitive star-rating (1-5 stars) with equal weight given to each metric. Proteomes can be searched for, filtered by the various ratings, downloaded, user-rated and commented on. Additional proteomes and metrics can be added/suggested by users via the website and documentation describing this is provided.

###### The original PQI metrics

[//]: # (TODO: Check how this paragraph ended in Google Doc. Had weird punctuation.)

PQI originally provided 11 measures of proteome quality, that are either local i.e. “clade-based” (in which proteomes are compared to similar organisms) or global (in which case it is compared to all other proteomes). A clade is a group of organisms that consists of a common ancestor and all its descendants, i.e. is a branch on the tree of life{cite}`Cracraft2004-ud`, so an appropriate ancestor must be chosen to define the clade. For PQI, since the purpose of these clades was to compare its’ constituent proteomes, we wanted clades that had similar variability. This was achieved by choosing parent nodes that are at least 0.01 in branch length away from the proteome (leaf node), and such that the clade contains at least 10 species. Trees and branch lengths to carry out these calculations were taken from sToL{cite}`Fang2013-et`. For clade-based metrics, proteomes score well if they have similar scores to the rest of the clade.

[//]: # (TODO: Check combination homology 3 and 4 from table below)

```{list-table}
:header-rows: 1
:name: pqi-table

* - Metric name
  - Type
  - Description
  - Notes
* - 1\. Percentage X-content
  - Global
  - Percentage of proteome with amino acids denoted by ‘X’, excluding the first residue of each protein.
  - Amino acids that cannot be identified, or can have more than one value are represented by an ‘X’ in the amino acid sequence[139]. This occurs when coverage of the sequencing is low. Uncertainty in translation start sites mean the first residue of a protein is often uncertain (‘X’) even in the highest quality proteomes, so these are excluded from this measurement.
* - 2\. PubMed Publication Count
  - Global
  - The total number of publications related to the genome as listed for that entry in the PubMed database[140].
  - This is a measure of how well-studied a proteome is, assuming that proteomes that have been studied more will be of higher quality. 
* - 3\. CEG Domain
  - Global
  - Proportion of CEG set which contains homologous domains in the proteome, according to SUPERFAMILY
  - This method assumes that all eukaryotic genomes should contain a core set of well-conserved of eukaryotic genes. This score is not calculated for non-eukaryotes. This was done using the Core Eukaryotic Gene (CEG) library used by the CEGMA tool[141], which comes from the Eukaryotic Orthologous Group (KOG) sequence orthology database[142]. Domain-architecture similarity is calculated using the SUPERFAMILY HMM library.
* - 4\. Combination Homology
  - ???
  - ???
  - ???
* - 5\. Percentage of sequences in Uniprot
  - Global
  - Percentage of proteome sequences that appear in Uniprot with 100% sequence identity
  - This metric assumes that the majority of discrepancies between Uniprot protein sequences and the proteome protein sequences are due to proteome inaccuracies.
* - 6\. Number of domain superfamilies
  - Clade-based
  - Number of proteins assigned to domain superfamilies by SUPERFAMILY compared to average for clade.
  - Assignment to domain superfamilies was obtained using the SUPERFAMILY HMM Library. The number of superfamilies gives an indication of the diversity of the proteome, so a low number compared to the clade may indicate an incomplete proteome, while a high number could indicate that the proteome contains domain superfamiles that it shouldn’t. 
* - 7\. Percentage of sequence covered
  - Clade-based
  - Percentage of amino acid residues in proteome sequence that are covered by SCOP domain superfamily assignments, compared to the average for the clade. 
  - This metric measures the portion of structured protein sequences found in the proteome as opposed to disordered regions and gaps. This measure assumes related species have a similar breakdown of these types of proteins. A mismatch could indicate that the parts of the genome that are supposed to be protein-coding are an incorrect length, that it is missing proteins, or contains proteins that it shouldn’t.
* - 8\. Percentage of sequences with assignment
  - Clade-based
  - Percentage of amino acid residues in proteome that have SCOP superfamily assignment according to SUPERFAMILY, compared to the average for the clade.
  - Related species are assumed to have a similar percentage of domains with SUPERFAMILY assignments to SCOP superfamilies
* - 9\. Mean sequence length
  - Clade-based
  - The average length of proteins in the proteome (in amino acids), compared to the average for the clade.
  - This measure assumes that mean sequence length of proteins should be comparable with those of related species. 
* - 10\. Mean hit length
  - Clade-based
  - Average number of amino acids in superfamily assignments, compared to the average for the clade.
  - Longer hits represent better matches to SCOP domains. These are assumed to be similar for similar species.
* - 11\. Number of domain families
  - Clade-based
  - Number of distinct SCOP protein domain families that are annotated to the proteome, compared to the average for the clade.
  - The SCOP protein domain families are annotated to the proteome using a hybrid HMM/pairwise similarity method from the SUPERFAMILY resource. Similarly to the number of domain superfamilies, the number of families gives an indication of the diversity of the proteome at the SCOP family level. Domain families were included in addition to domain superfamilies, since they are more specific and may reveal differences that are not apparent at the superfamily level. 
* - 12\. Number of domain architectures
  - Clade-based
  - Number of unique domain architectures (combinations of SCOP domain superfamilies and gaps) in the proteome, according to SUPERFAMILY, compared to the average for the clade.
  - Similarly to the number of domain families superfamilies, the number of domain architectures gives an indication of the diversity of the proteome at the SCOP family level.
```

[//]: # (TODO: Format table caption better:)

{numref}`pqi-table` shows the original PQI metrics. 

As a proteome will get low scores in clade-based metrics when they are unusual compared to the rest of its clade, model organisms (e.g. Homo Sapiens) can get a low score in clade-based metrics since for the wrong reasons - since they are of such higher quality compared to those in it’s clade. The PQI website’s comment and user-rating features can be used to alert its users to these cases.

Since the publication of the PQI paper, the DOGMA metric{cite}`Dohmen2016-iv`, which scores proteomes based on conserved arrangements of protein domains, has been added to the PQI website. 

###### Potential improvements
The mapping from raw score to star rating for some metrics could be improved. For example, homo sapiens has ‘0’ X-content (the lowest/best possible value), but 4.1 stars.

[//]: # (TODO: Rephrase)
PQI was created with the potential to add further quality metrics by other researchers. Although the DOGMA metric was added and it is based on BUSCO{cite}`Simao2015-gc`, it might be sensible to add BUSCO, since it has become very popular, and any proteome/genome quality index would probably be seen as incomplete without it. The continued inclusion of the CEG Domain Combination Homology metric may be questioned since CEGMA is no longer being updated (nor is the KEG database upon which it is based), but BUSCO and CEGMA may be complementary since BUSCO has a weaker requirement for inclusion in the set of proteins, which means that it has more proteins, and vice versa.

To impact on the problem for model organisms for clade-based metrics, one solution would be to treat model-organisms differently in these circumstances, for example score clades containing model organisms against the model organism. An more subtle alternative to this would be using the NCBI’s Assembly database{cite}`Kitts2016-eo`, which has been released since PQI was published. The database tracks how many assemblies there are for each species as well as how many versions of each assembly there has been. This information could be used to weight the importance of proteomes in clade-based metrics. The number of assemblies and versions could also form a separate score.

Sequencing depth (coverage) and read length are also known markers of genome quality{cite}`Sims2014-df`. Average coverage for an assembly (except reference genomes) is also available in the NCBI Assembly database{cite}`Kitts2016-eo`. 

Some “third-generation” sequencing technologies create much longer read lengths, but potentially lower accuracies. A third category of metrics “technology-based” metrics could exist for proteomes where the metric is only really comparable within similar types of technologies. If technology-based metrics were implemented, it may also be sensible to have some metrics which only exist for specific technologies. For example, for nanopore sequencing, we could implement an indel-based quality metric{cite}`Watson2019-pz`. Including sequencing-technology-specific metrics may encourage contributions from other researchers who specialise in particular technologies. Sequencing technology is also available in the NCBI Assembly database{cite}`Kitts2016-eo`. 

The development of additional measures is required to deal with other potential problems in genome sequencing, for example GC content, amino acid bias, or contamination from other genomes. 

#### Genes

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

The Gene Ontology (GO){cite}`Ashburner2000-cr` is one of the first biomedical ontologies, and continues to be one of the most popular. It is a collection of resources for cataloging the functions of gene products and designed for supporting the computational representation of biological systems{cite}`Thomas2017-vm`. It includes:
1. The standard gene ontology, which is a hierarchical set of terms describing functions.
2. The gene ontology annotations (GOA) database, which contains manual and computationally derived mappings from gene products to gene ontology terms.
3. Tools for using and updating these resources.

The Gene Ontology defines the “universe” of possible functions a gene might have, while the functions of particular genes are captured as GO annotations{cite}`Thomas2017-vm`.

The terms in the GO ontology are subdivided into three types (molecular function, biological process, and cellular component), meaning that GO is actually a collection of three ontologies{cite}`Ashburner2000-cr`. Gene products in GO are assumed to carry out molecular-level process or activity (molecular function) in a specific location relative to the cell (cellular component), and this molecular process contributes to a larger biological objective (biological process){cite}`Thomas2017-vm`.


##### Functional annotation databases
[//]: # (TODO: Is this section at the level of genes only?)
[//]: # (TODO: cite UniprotKB and GOA?)

Databases like Uniprot KnowledgeBase (UniprotKB) and Gene Ontology Annotation (GOA) connect proteins to functions by annotating them to ontology terms (e.g. from GO), and giving information about why and how this annotation was done (e.g. giving DOI of a paper containing the evidence for the annotation). This is done by a combination of manual and electronic annotation. 

Annotations can also include more information, for example modifiers specifying the type of interaction between the gene and the ontology term, the binding partners of the protein, etc. Further extensions to annotations such as these are currently being developed, but are in their infancy. It is particularly sad that negative annotations between genes and diseases/functions are lacking. Although there is a ‘NOT’ modifier (i.e. gene A does not affect function B), it is generally only used in cases where there is a known disagreement between the electronic and manual annotations, rather than for any highly powered negative result. This is a shame as it makes the benchmarking of any protein function predictor extremely difficult. The GO handbook does mention than an increase in ‘NOT’ modifiers would be useful in achieving a gold standard set of annotations for benchmarking{cite}`Thomas2017-vm`. It may be that publication bias in experimental work prevents annotators from finding supporting evidence to support such annotations. 

#### Variants

[//]: # (TODO: Sentence about variants)

Databases like dbSNP, clinVar, and SNPedia contain information about the location of SNVs, their possible alleles, and their association to diseases. 
These are often used as part of a variant prioritisation pipeline, as well as by individuals who are investigating their own SNVs.

##### dbSNP
The NCBI’s dbSNP{cite}`Sherry2001-nm` is the world’s largest database of nucleotide variations, including their locations, possible alleles, and associations to diseases. 
It contains information from ten organisms (including human) and has information on indels and short tandem repeats in addition to SNVs. It was designed to store the annotations that are outputted from GWAS studies. 
Anyone can submit their findings about variants, and they must indicate what sort of evidence they have for the association.
 The database gives SNVs unique identifiers (Reference SNP cluster IDs, a.k.a. RSIDs) of the form rs###, which are used by many other resources.

[//]: # (TODO: mention the ss numbers, and that the dbSNP builds don't "line up" with the human reference builds, how they are merged and the fact that they might map to different alternate contigs)

### RNA
[//]: # (TODO: Rewrite this section, and maybe move it to section 1, so that it fits properly and is less wordy)

DNA can’t tell us the whole story. On it's own it can’t tell us what we’d like to know about a gene’s function or a person’s traits. Nonetheless, I’d like to spell out why that is for those who do not have that background. The central dogma of molecular biology can be paraphrased as “DNA makes RNA makes proteins”. So, if we know what a person’s DNA is, then why would we also want to know about their RNA?

The answer boils down to the effect of the environment. “DNA makes RNA makes proteins” is shorthand for “DNA interacts with the environment to make RNA, and RNA interacts with the environment to make proteins”. The environment, of the cell, and of the individual, and even of modifications to the DNA molecules, is the reason why DNA alone is not enough to explain how we function. DNA is the collection of blueprints for what can be made, but the environment decides what goes into production; which RNA and proteins are made and how much. 

In any given individual, the same DNA is present in their liver cells, skin cells, and neurons. The difference in how these cells/tissues look and function is due to differences in which proteins are actually being made at any given time. Gene expression is a way of measuring how the environment of the cell is affecting the process of making proteins from DNA.

Gene expression data is used to understand the function of genes, to identify housekeeping genes, to re-engineer gene regulatory networks, and more. This kind of insight can not be gained from looking at DNA alone.

[//]: # (TODO: Write something breif reminding what gene expression is and why it is measured, referring back to Ch1)

One of the most popular measures of gene expression, is the measure of how much RNA is in a cell at a given time. 

#### FANTOM Consortium
[//]: # (TODO: ADd Fantom5 citation, move this bit to somewhere sensible.)
As the human genome project was nearing completion, researchers had a parts list of human biology, but few of the functions of these parts (genes) were known. A consortium of scientists formed, named after the challenge they were addressing: the Functional ANnoTation Of the MAmmalian genome (FANTOM). 

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

### Proteins

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

### Phenotypes

[//]: # (TODO: Write something about "gene function" and "protein function" and their relationship to phenotypes, ontologies, etc)

---
**Chapter References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```