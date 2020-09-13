(c03-compbio-bg)=
# Computational Biology Background

This chapter is a second background chapter. While {ref}`the previous chapter<c02-biology-bg>` gave an introduction to the biology of the molecules involved in genotype, and it's connection to phenotype, this chapter is about the details of how information about these connections is created, used, stored, and re-used. 

[//]: # (TODO: Add some images of data or logos or some boring-ass graphs or /something/ to the endless desert of this section)
[//]: # (TODO: Fix all the [] citations)
[//]: # (TODO: Perhaps put the third part in a different chapter after snowflake, but no use doing that while I'm just trying to migrate things. In which case delete "in the first part...")
[//]: # (TODO: Explain very briefly what the different papers/contributions are and cite them.)
[//]: # (TODO: Cite SUPERFAMILY and the update paper below)

In the first section of this chapter, we will retrace our steps from the last chapter, walking again from DNA to RNA to proteins to phenotypes, but this time we will consider the data gathered about each of these stages, and the data gathered about the connections between them. When I reach certain data (particularly RNA-Seq data), it will be also necessary to talk about some of the data processing pipeline. As we look at these different data types, I will describe some specific examples of resources and tools used in bioinformatics and computational biology, particularly those which are important in later chapters. This includes biological ontologies, tools for variant prioritisation, and databases of protein structure, sequence and domain assignments. In this part of the chapter, I will explain {ref}`my contribution to the update to the SUPERFAMILY resource<my-supfam-contribution>`.

[//]: # (TODO: Write this paragraph)
The second section will then touch upon how some of these datasets are used.

Finally, in the third section of this chapter, I will consider what potential sources of bias this data contains. Here I mention my contributions to two collaborative projects: PQI and MAPS (ongoing).

## From genotype to phenotype: what is measured

Cataloguing and classifying has been a successful scientific endeavour in other disciplines (e.g. the periodic table) but it’s particularly a cornerstone of biology. Biological ontologies date back to the Linnaean taxonomy from the mid 1700s {numref}`linneaus_ehret`, which describes species and their features and the relationships between them{cite}`Jensen2010-fk`. 

```{figure} ../images/linneaus_ehret.jpg
---
height: 220px
name: linneaus_ehret
---
Carl Linneaus developed a system of classifying plants, animals and minerals, including plant classification based on their number of stamens{cite}`Blunt2001-wr`. The left image is a key to this classification system taken from his book, while the right image is a depiction of how the system works, drawn by botanist George Ehret{cite}`Ehret1748-bx`. 
``` ``

[//]: # (TODO: Cite PDB online database, Margaret Dayhoff)

Biology today continues in this tradition, classifying and cataloguing biology in ever more (molecular) detail. Computational biology is fueled by big community efforts to develop these databases, vocabularies, and annotations. While in other fields, data inaccessibility is a major barrier to reproducible research in other fields, this is the field that had an online database system that remote computers could access in the 1960s! These efforts remain central to computational biology and have enabled investigations into whole genomes, transcriptomes, organisms, or the entire phylogenetic tree. This openness, and the focus on well-organised and archived data is not something that we should take for granted.

There are large datasets on everything from gene functions to cells, and diseases to anatomical entities. These datasets create a shared vocabulary that we can all use to discuss these entities, as well as capturing knowledge about them so that it can elucidate other research these entities, or be used in larger-scale analysis. We will now delve into the details of these datasets.

### DNA

[//]: # (TODO: Signposting DNA, RNA, etc)
[//]: # (TODO: Decide whether going bigger-> smaller eg genome->variant or the other way around)

#### Complete genome sequences

[//]: # (TODO: PQI here?? Or in later part, and anything to do with assemblies)

(pqi)=
##### PQI

The Proteome Quality Index (PQI) is an attempt to provide quality metrics about completed genome sequences. It was a group effort, which resulted in a paper{cite}`Zaucha2015-ez`, of which I am an author, as well as [an associated website (http://pqi-list.org/)](http://pqi-list.org/). I contributed to discussions about metrics, and paper editing.

The motivation for creating the index came from problems of reproducibility in the field of genomics. In creating a daily-updated tree of life (sTOL, sequenced Tree Of Life), it was found that many sequenced genomes were missing vital proteins due to poor sequencing{cite}`Fang2013-et`. Such genomes are reused by many researchers, for example in comparative genomics, and omissions of whole proteins and poor accuracy of others are likely to affect research results. 

The PQI website was intended to be both a way for users of past genomes to look up the quality of a genome in advance of some research and, more importantly as a talking point for quality guidelines for genomes/proteomes. While quality control and data submission guidelines were more developed in other areas of computational biology, similar guidelines for genome quality were lacking.

##### PQI features 

The PQI website provides a scoring system for proteomes, bringing together numerous different metrics which are normalised before being averaged into an intuitive star-rating (1-5 stars) with equal weight given to each metric. Proteomes can be searched for, filtered by the various ratings, downloaded, user-rated and commented on. Additional proteomes and metrics can be added/suggested by users via the website and documentation describing this is provided.

##### The original PQI metrics

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
* - 1. Percentage X-content
  - Global
  - Percentage of proteome with amino acids denoted by ‘X’, excluding the first residue of each protein.
  - Amino acids that cannot be identified, or can have more than one value are represented by an ‘X’ in the amino acid sequence[139]. This occurs when coverage of the sequencing is low. Uncertainty in translation start sites mean the first residue of a protein is often uncertain (‘X’) even in the highest quality proteomes, so these are excluded from this measurement. Row1 under Col1
* -  2. PubMed Publication Count
  - Global
  - The total number of publications related to the genome as listed for that entry in the PubMed database[140].
  - This is a measure of how well-studied a proteome is, assuming that proteomes that have been studied more will be of higher quality. 
* - 3. CEG Domain
  - Global
  - Proportion of CEG set which contains homologous domains in the proteome, according to SUPERFAMILY
  - This method assumes that all eukaryotic genomes should contain a core set of well-conserved of eukaryotic genes. This score is not calculated for non-eukaryotes. This was done using the Core Eukaryotic Gene (CEG) library used by the CEGMA tool[141], which comes from the Eukaryotic Orthologous Group (KOG) sequence orthology database[142]. Domain-architecture similarity is calculated using the SUPERFAMILY HMM library.
* - 4. Combination Homology
  - ???
  - ???
  - ???
* - 5. Percentage of sequences in Uniprot
  - Global
  - Percentage of proteome sequences that appear in Uniprot with 100% sequence identity
  - This metric assumes that the majority of discrepancies between Uniprot protein sequences and the proteome protein sequences are due to proteome inaccuracies.
* - 6. Number of domain superfamilies
  - Clade-based
  - Number of proteins assigned to domain superfamilies by SUPERFAMILY compared to average for clade.
  - Assignment to domain superfamilies was obtained using the SUPERFAMILY HMM Library. The number of superfamilies gives an indication of the diversity of the proteome, so a low number compared to the clade may indicate an incomplete proteome, while a high number could indicate that the proteome contains domain superfamiles that it shouldn’t. 
* - 7. Percentage of sequence covered
  - Clade-based
  - Percentage of amino acid residues in proteome sequence that are covered by SCOP domain superfamily assignments, compared to the average for the clade. 
  - This metric measures the portion of structured protein sequences found in the proteome as opposed to disordered regions and gaps. This measure assumes related species have a similar breakdown of these types of proteins. A mismatch could indicate that the parts of the genome that are supposed to be protein-coding are an incorrect length, that it is missing proteins, or contains proteins that it shouldn’t.
* - 8. Percentage of sequences with assignment
  - Clade-based
  - Percentage of amino acid residues in proteome that have SCOP superfamily assignment according to SUPERFAMILY, compared to the average for the clade.
  - Related species are assumed to have a similar percentage of domains with SUPERFAMILY assignments to SCOP superfamilies
* - 9. Mean sequence length
  - Clade-based
  - The average length of proteins in the proteome (in amino acids), compared to the average for the clade.
  - This measure assumes that mean sequence length of proteins should be comparable with those of related species. 
* - 10. Mean hit length
  - Clade-based
  - Average number of amino acids in superfamily assignments, compared to the average for the clade.
  - Longer hits represent better matches to SCOP domains. These are assumed to be similar for similar species.
* - 11. Number of domain families
  - Clade-based
  - Number of distinct SCOP protein domain families that are annotated to the proteome, compared to the average for the clade.
  - The SCOP protein domain families are annotated to the proteome using a hybrid HMM/pairwise similarity method from the SUPERFAMILY resource. Similarly to the number of domain superfamilies, the number of families gives an indication of the diversity of the proteome at the SCOP family level. Domain families were included in addition to domain superfamilies, since they are more specific and may reveal differences that are not apparent at the superfamily level. 
* - 12. Number of domain architectures
  - Clade-based
  - Number of unique domain architectures (combinations of SCOP domain superfamilies and gaps) in the proteome, according to SUPERFAMILY, compared to the average for the clade.
  - Similarly to the number of domain families superfamilies, the number of domain architectures gives an indication of the diversity of the proteome at the SCOP family level.

```

[//]: # (TODO: Format table caption better:)

{numref}`pqi-table` shows the original PQI metrics. 

As a proteome will get low scores in clade-based metrics when they are unusual compared to the rest of its clade, model organisms (e.g. Homo Sapiens) can get a low score in clade-based metrics since for the wrong reasons - since they are of such higher quality compared to those in it’s clade. The PQI website’s comment and user-rating features can be used to alert its users to these cases.

Since the publication of the PQI paper, the DOGMA metric{cite}`Dohmen2016-iv`, which scores proteomes based on conserved arrangements of protein domains, has been added to the PQI website. 

##### Potential improvements
The mapping from raw score to star rating for some metrics could be improved. For example, homo sapiens has ‘0’ X-content (the lowest/best possible value), but 4.1 stars.

[//]: # (TODO: Rephrase)
PQI was created with the potential to add further quality metrics by other researchers. Although the DOGMA metric was added and it is based on BUSCO{cite}`Simao2015-gc`, it might be sensible to add BUSCO, since it has become very popular, and any proteome/genome quality index would probably be seen as incomplete without it. The continued inclusion of the CEG Domain Combination Homology metric may be questioned since CEGMA is no longer being updated (nor is the KEG database upon which it is based), but BUSCO and CEGMA may be complementary since BUSCO has a weaker requirement for inclusion in the set of proteins, which means that it has more proteins, and vice versa.

To impact on the problem for model organisms for clade-based metrics, one solution would be to treat model-organisms differently in these circumstances, for example score clades containing model organisms against the model organism. An more subtle alternative to this would be using the NCBI’s Assembly database{cite}`Kitts2016-eo`, which has been released since PQI was published. The database tracks how many assemblies there are for each species as well as how many versions of each assembly there has been. This information could be used to weight the importance of proteomes in clade-based metrics. The number of assemblies and versions could also form a separate score.

Sequencing depth (coverage) and read length are also known markers of genome quality{cite}`Sims2014-df`. Average coverage for an assembly (except reference genomes) is also available in the NCBI Assembly database{cite}`Kitts2016-eo`. 

Some “third-generation” sequencing technologies create much longer read lengths, but potentially lower accuracies. A third category of metrics “technology-based” metrics could exist for proteomes where the metric is only really comparable within similar types of technologies. If technology-based metrics were implemented, it may also be sensible to have some metrics which only exist for specific technologies. For example, for nanopore sequencing, we could implement an indel-based quality metric{cite}`Watson2019-pz`. Including sequencing-technology-specific metrics may encourage contributions from other researchers who specialise in particular technologies. Sequencing technology is also available in the NCBI Assembly database{cite}`Kitts2016-eo`. 

The development of additional measures is required to deal with other potential problems in genome sequencing, for example GC content, amino acid bias, or contamination from other genomes. 

#### Genes

##### Functional annotation databases

[//]: # (TODO: Is this section at the level of genes only?)
Databases like Uniprot KnowledgeBase (UniprotKB) and Gene Ontology Annotation (GOA) connect proteins to functions by annotating them to ontology terms (e.g. from GO), and giving information about why and how this annotation was done (e.g. giving DOI of a paper containing the evidence for the annotation). This is done by a combination of manual and electronic annotation. 

Annotations can also include more information, for example modifiers specifying the type of interaction between the gene and the ontology term, the binding partners of the protein, etc. Further extensions to annotations such as these are currently being developed, but are in their infancy. It is particularly sad that negative annotations between genes and diseases/functions are lacking. Although there is a ‘NOT’ modifier (i.e. gene A does not affect function B), it is generally only used in cases where there is a known disagreement between the electronic and manual annotations, rather than for any highly powered negative result. This is a shame as it makes the benchmarking of any protein function predictor extremely difficult. The GO handbook does mention than an increase in ‘NOT’ modifiers would be useful in achieving a gold standard set of annotations for benchmarking{cite}`Thomas2017-vm`. It may be that publication bias in experimental work prevents annotators from finding supporting evidence to support such annotations. 

#### Variants

[//]: # (TODO: Sentence about variants)

Databases like dbSNP, clinVar, and SNPedia contain information about the location of SNVs, their possible alleles, and their association to diseases. These are often used as part of a variant prioritisation pipeline, as well as by individuals who are investigating their own SNVs.

##### dbSNP
The NCBI’s dbSNP{cite}`Sherry2001-nm` is the world’s largest database of nucleotide variations, including their locations, possible alleles, and associations to diseases. It contains information from ten organisms (including human) and has information on indels and short tandem repeats in addition to SNVs. It was designed to store the annotations that are outputted from GWAS studies. Anyone can submit their findings about variants, and they must indicate what sort of evidence they have for the association. The database gives SNVs unique identifiers (Reference SNP cluster IDs, a.k.a. RSIDs) of the form rs###, which are used by many other resources.

### RNA

[//]: # (TODO: Rewrite this section, and maybe move it to section 1, so that it fits properly and is less wordy)

DNA can’t tell us the whole story. On it's own it can’t tell us what we’d like to know about a gene’s function or a person’s traits. Nonetheless, I’d like to spell out why that is for those who do not have that background. The central dogma of molecular biology can be paraphrased as “DNA makes RNA makes proteins”. So, if we know what a person’s DNA is, then why would we also want to know about their RNA?

The answer boils down to the effect of the environment. “DNA makes RNA makes proteins” is shorthand for “DNA interacts with the environment to make RNA, and RNA interacts with the environment to make proteins”. The environment, of the cell, and of the individual, and even of modifications to the DNA molecules, is the reason why DNA alone is not enough to explain how we function. DNA is the collection of blueprints for what can be made, but the environment decides what goes into production; which RNA and proteins are made and how much. 

In any given individual, the same DNA is present in their liver cells, skin cells, and neurons. The difference in how these cells/tissues look and function is due to differences in which proteins are actually being made at any given time. Gene expression is a way of measuring how the environment of the cell is affecting the process of making proteins from DNA.

Gene expression data is used to understand the function of genes, to identify housekeeping genes, to re-engineer gene regulatory networks, and more. This kind of insight can not be gained from looking at DNA alone.

[//]: # (TODO: Write something breif reminding what gene expression is and why it is measured, referring back to Ch1)

One of the most popular measures of gene expression, is the measure of how much RNA is in a cell at a given time. 

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

## How large computational biology datasets are used
[//]: # (TODO: rename title)
[//]: # (TODO: Include?? As the amount of data from high-throughput sequencing experiments has piled up, computational approaches have been ever-more necessary to make sense of the data.)

### Making sense of lists
The output of high throughput sequencing experiments can often be a long list of variants or genes (e.g. the outputs of GWAS studies or differential expression). 

[//]: # (TODO: Check where GO is first mentioned!)
#### Term enrichment
Ontologies are often used to try to make sense of a list of genes that are found to be differentially expressed across different experimental conditions. In the context of GO, a term enrichment analysis can be carried out to see which GO terms are overrepresented (aka enriched) for a given group of genes, thus saying something about the function of the list of genes. 

##### DcGO
The aim of the Domain-centric Gene Ontology (DcGO){cite}`Fang2013-ms,Fang2013-ix` tool is to give insight into uncharacterised or poorly characterised proteins by leveraging information about the content of their constituent protein domains. It annotates domains and combinations of domains (supradomains) to phenotype terms from a variety of ontologies, including the Gene Ontology (GO), Mammalian Phenotype ontology (MP), Disease Ontology (DOID), Zebrafish ontology (ZFA). Domain information comes from SUPERFAMILY, and annotations between (supra)domains and phenotype terms are made below a cut-off of FDR-adjusted statistical associations between the entities. Using phenotypes from a range of species serves to make use of greater numbers of experiments, and therefore increases the number of little-known proteins across species that DcGO can make predictions about.

#### Variant prioritisation
To narrow down a long list of genes or variants to a shorter list of variants or genes which is more likely to be causal, variant prioritisation is used.

##### FATHMM
Functional Analysis through Hidden Markov Models (FATHMM){cite}`Shihab2013-pk` is a tool for predicting the functional effects of protein missense mutations using sequence conservation information (via HMMs), which can be (optionally) weighted by how likely a mutation in a protein/domain would be to lead to disease. Weightings are calculated from the frequency of disease-associated and functionally neutral amino acid substitutions in protein domains from human variation databases (the Human Gene Mutation Database{cite}`Stenson2009-jc` and Uniprot-KB/Swiss-prot{cite}`Pundir2016-ya`).

Consequence files describing whether an amino acid results in a missense, nonsense or synonymous SNP must first be obtained by using Ensembl’s Variant Effect Predictor{cite}`McLaren2016-di` in order to create input to FATHMM. FATHMM then calculates conservation scores which are a measure of the difference in amino acid probabilities for a SNP according to the HMM, i.e. between a wild type amino acid and it’s substitution. A reduction in amino acid probabilities is interpreted as a prediction of deleteriousness, and the larger the reduction the greater the predicted harm. 

## Sources of bias in computational biology datasets

### Why we care
#### We want to trust science
[//]: # (TODO: Restructure this section so that the different sources of bias are in a sensible order and that I have proof for each. Rename "why we care" and "we want to trust science")

```{epigraph}
The imposing edifice of science provides a challenging view of what can be achieved by the accumulation of many small efforts in a steady objective and dedicated search for truth.

-- Charles H. Townes
```

[//]: # (TODO: Rewrite this so that the vibe is more "hey we all agree that we want to be able to rely on science and less "FUCK ALL OF YOU")

We want to trust the results of scientific research. Not only when it’s our own (because it’s fun and exciting to look for and find the truth), but because scientific research is generally paid for by tax, and the results that are generated by it drive policy, drug treatments, and innovations. 

In all fields, science is a search for the truth. And in all fields, there are concerns about what makes bad, unreliable, un-useful, or biased research; what must be done or not done to uphold science’s claim to truth, or at least reliability. Computational biology has a number of unique characteristics which make these questions worth discussing in its specific context. 

[//]: # (TODO: REf the "earlier" below:)
As mentioned earlier, in contrast to other fields, many bioinformatics datasets have been freely available and accessible on the internet since its inception. Computational biology might be a good place to look for what is required to really benefit from those open datasets, what can be gained from them (and what can’t), and what the next steps in reproducibility should be, beyond making data accessible.c

Secondly, the creation of these databases has birthed a lot of research that is highly reliant on a handful of large ontologies and databases, the completeness of which is unknown, and the cataloging process by which they are added to is extremely uneven. 

Thirdly, many of the new publications in this field showcase novel software and models which build on these resources, despite the fact that much of it is difficult to validate due to the lack of gold standard datasets. 

When scientific results are often based on statistics, it’s inevitable that some proportion of published scientific results will not be true. This isn’t a problem, as over time, researchers can double-check interesting scientific results, and the literature can be updated to reflect that. This is sciences self-correcting mechanism. If a result can be replicated in a different circumstance by a different person, it reinforces the likelihood that the result is true. A replication doesn’t have to reveal the exact same level of statistical significance  or effect size to be successful, but (usually, depending on definitions) just a similar result.

#### The reproducibility crisis 

```{epigraph}
In science consensus is irrelevant. What is relevant is reproducible results.

-- Michael Crichton
```

The reproducibility crisis is the realisation that worryingly large proportions of research results do not reproduce. Replication studies have found that only 11% of cancer research findings[113], 20-25% of drug-target findings[113,114], and 39% of psychology findings[115] reproduced. Surveys of researchers across disciplines reveal that more than 70% of scientists say they have failed to reproduce another paper’s result, and over 50% say they have failed to reproduce their own results[116]. It seems that science’s self-correcting mechanism is not working as intended.

This shocking irreproducibility is thought to be due to a multitude of factors, including poor data management, lack of available materials/details of experiments, publication bias, poor statistical knowledge, and questionable research practices[117]. 

[//]: # (TODO: Any time I explain any of this, I better be able to say WHY it's there: Go through and check that I can)

##### Null Hypothesis Significance Testing

```{epigraph}
Statistical significance is the least interesting thing about the results. You should describe the results in terms of measures of magnitude –not just, does a treatment affect people, but how much does it affect them.

-- Gene V. Glass
```

Null Hypothesis Significance Testing (NHST) is the most popular method by which scientific hypotheses are tested and reported. This reporting usually consists mostly of a p-value, a measure of statistical significance: the likelihood that a false positive could be obtained just by chance. In other words p-values are a measure of type 1 error (false positives). The threshold for this, usually denoted  is most often set to 0.05, as recommended by Fischer, however there have been many debates about whether this is the most sensible cut-off for science today. Despite the dominance of p-values as main or only reported statistic across scientific fields, they do not imply that a result is interesting (the effect might be small or the hypothesis uninteresting), or even that it’s likely to be true. Sometimes the p-value is not even reported, but only whether or not it crossed the p<0.05 threshold.

Two other useful quantities of NHST are effect size and statistical power. Effect size is the magnitude of the effect found by the statistical test. A very small effect can only be detected with a large enough sample size. Statistical power is a measure related to the type 2 error (false negatives), it is 1- where  is the false positive rate. A statistical power of 80% is customary, where it is calculated, in which case there is a 20% chance that a result is a false negative if the null hypothesis is accepted. A very highly powered test with a high (non-significant) p-value represents strong evidence that the null hypothesis is true, although it may often be reported as “failing to reach significance”. Low-powered tests, coinciding with low sample sizes, mean that both the acceptance or rejection of the null hypothesis is likely to be unreliable. 

[//]: # (TODO: Fix math below:)
P-values do not have a high prediction value for reproducibility, since they have a high spread, even when a test is reasonably highly powered. Statistician Geoff Cumming refers to this as the “dance of the p-values”. Instead, a measure of the expected truth of a finding can be estimated from the proportion of hypotheses that are true in a given field, the statistical power, the p-value threshold as:
ppv=(1-)ptrueptrue(1--)+

Where ppvstands for positive predictive value and ptrue is the proportion of true hypotheses in a field[118]. 

For this version of the formula (there is also a version that includes bias, which was instrumental in the Ionnaidis’ claim that “most published research findings are false”[118]), and standard choices for power and statistical significance of =0.05 and=0.2, we would expect more findings to false than true if ptrue<0.0588(3.s.f). That might seem like a small number, but in some bioinformatics experiments, we hypothesise that millions of SNPs may be responsible for a trait, when only small numbers are. On the other hand, if half of researchers hypotheses were correct for a given field (ptrue=0.5), the formula would yield ppv=0.941(3.s.f.), but the low reproducibility of GWAS results, gene annotations, etc, implies that the proportion of true hypotheses is less than this.

The same approach can be used to calculate the limit for ptrue for which we’d expect there to be more false positives than false negatives. Using the same values for and  and , we get ptrue=0.2, i.e. if less than 20% of hypotheses are true, then we are more likely to get false positives than false negatives. This is interesting as most published scientific results are claiming a positive result, so we are essentially erring on the side of publishing erroneous errors.


Figure 24: Images that are illustrative of researchers approaches to p-values and p-hacking. Left image a popular tweet (taken from twitter.com), right image from xkcd.com.

In addition to poor reporting and underpowered tests, the pressure on scientists to publish means that researchers may be tempted to (or may accidentally, due to statistical ignorance) employ data-mining tactics in order to harvest significant p-values. This practice is known as “p-hacking”, and evidence for its existence can be found in distributions of p-values in scientific literature[119], as well as popular culture (see Figure 6). This can include rerunning analysis with different models/covariates, collecting data until a significant p-value is reached, or performing 20 experiments and only publishing the results of one. 

```{epigraph}
The first principle is that you must not fool yourself – and you are the easiest person to fool. 
-- Richard Feynman 
```

There are several suggested tonics to the problem of uninformative and ubiquitous p-values. Reporting p-values as numbers rather than in relation to a threshold (e.g. “p<0.05) is starting point. Information about statistical power and effect size should also be provided. In addition to giving researchers reading a paper a better idea of the quality of it, this also allows science to self-correct a little easier, since individual p-values can then be combined into more reliable p-values, using for example Fischer’s method[120]. 

A more interesting solution is pre-registration, as used in clinical trials. This involves a detailed publication in advance of the analysis protocols that will be used in order to prevent tweaking analysis based on seeing the data. This solves p-hacking related problems, and makes a distinction between hypothesis-generating and hypothesis-testing research.

For cases where many hypotheses are being generated at once (for example in GWAS), multiple hypothesis corrections (e.g. the Bonferroni correction[121] or the False Discovery Rate[122]) can be employed to adjust the p-value to account for this.

##### Publication bias
Although with current standard p-value and power cut-offs, negative results are more likely to be true than positive ones, negative results are much harder to publish. This bias is likely to be responsible for the draw of questionable research practices like p-hacking. It also means that there is a lot of unpublished, negative results which are likely to be repeated, since there is no way that someone could know it has already been done. A highly powered negative result could be very interesting, for example, we know hardly anything about which genes do not appear to affect phenotypes, since these results are not published[24], but they would help enormously with the challenge of creating a gold standard dataset for gene function prediction.

Registered reports are an attempt to remove these problems associated with publication bias, by linking the concept of pre-registration with that of publishing. Essentially, authors submit their introduction and methods section to a journal and at this point they undergo peer review and the journal agrees to publish the results, regardless of the result. At the time of writing over 170 journals were accepting registered reports and the number has been growing in recent months, across disciplines, although they are currently most popular in psychology and neuroscience[123]. This solution also offers peer-review at a more helpful stage in the manuscript, when it’s still possible to make changes to the experiment.

#### Reproducibility in bioinformatics
In a field that has long had a huge number of open data repositories, and a relatively high level of statistical knowledge among researchers, in some ways bioinformatics might be expected to be ahead of the curve in terms of reproducible research. It certainly seems that as a field, it excelling at open research. At the same time, however, it is even more important for the work to be reproducible if data and software are being reused by multiple researchers.

The Gene Ontology Annotations (GOA) are a combination of experimental and computational annotations. While the supporting publications for the experimental annotations are available, the GO consortium do not provide the statistical evidence that they used alongside this (e.g. p-value, effect size), etc. 

[//]: # (TODO: Delete the when is a model useful section if I don't have any thoughts about it:)

#### When is a model useful? 
```{epigraph}
All models are wrong, but some are useful

-- George Box
```

Models are most useful to us when they generate testable hypotheses about the underlying mechanisms of a process. In this way, they can help to advance science. They can also be useful to us if they generate predictions for forecasts. These predictions can be tested, which helps us to improve the model, and if they are accurate, they can also help us to generate hypotheses, or they may be useful in and of themselves. 
