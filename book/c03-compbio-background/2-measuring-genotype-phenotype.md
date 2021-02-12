(measuring-genotype-phenotype)=
# From genotype to phenotype: what is measured
[//]: # (TODO: Image of bioinformatics landscape?)
We will now delve into the details of some of these data sets, looking first at {ref}`DNA<dna-measurements>`, then {ref}`RNA<rna-measurements>`, then {ref}`proteins<protein-measurements>`, then {ref}`phenotypes<phenotype-measurements>`.
This is to give us a sense of the data that exists within the databases of the bioinformatics landscape, as well as some of the subtle issues that arise when using and linking them.

(dna-measurements)=
## DNA
[//]: # (TODO: Why measure dna: what's it used for? We're trying to decode those big questions.)
In the {ref}`previous Chapter<what-is-dna>`, we looked at what DNA is and our understanding of how that links to phenotype. 
Now we're going to look at the details of how this is measured and stored: and how these details impact computational biology research. 
We'll once again go from big to small, beginning with whole genomes and moving through to individual SNPs.

### Whole genomes
[//]: # (TODO: What databases is SUPERFAMILY built on? What is PQI based on?)
[//]: # (TODO: MEntion anyone can submit/collaborative nature of databases)
The whole genome is all the genetic material of an organism, whether or not it is transcribed into RNA, or translated into protein.
In humans, this includes all chromosomal and mitochondrial DNAs.
Whole genomes are {ref}`assembled<assembly-and-alignment>` as previously described.
Whole genomes for different organisms can be compared to one another to give us insight about the organisms, or within an organism, individuals can be compared to understand the importance of sections of DNA for that organism.
Genomes from different species are stored in databases such as the University of California Santa Cruz (UCSC) Genome Browser database{cite}`Kent2002-jg`, the US National Centre for Biotechnology Information (NCBI) Genome Sequence database{cite}`Harger2000-vr`, or the European Bioinformatics Institute's (EBI) Ensembl Genome database{cite}`Hubbard2002-oi`.

### The human reference genome
As {ref}`previously mentioned<genomes>`, reference genomes are designed to represent whole organisms: these genomes aim to have the most common allele at any given nucleotide, and are then annotated at positions where individuals differ. 

(different-builds)=
**Builds and patches:** 
As more whole genomes for an organism are sequenced, more information comes to light about the nature of the genome. 
For example, some locations are revealed to be likely sequencing artifacts. 
New major versions of genomes are released every few years to fix these changes. 
These versions are called *builds*. 
Between builds and patches, sequences may be added, removed, or moved to different locations on chromosomes.

Different versions of the builds are released by the Genome Reference Consortium (GRC) and the University of California Santa Cruz (UCSC) Genomics Institute. 
{numref}`build-table` shows information about the most recent human reference builds, taken from the UCSC website{cite}`noauthor_undated-ci`.
For example, `hg19` (**h**uman **g**enome build **19**), is largely equivalent to `GRCh37` (**G**enome **R**eference **C**onsortium **h**uman build **37**).
These are generally used interchangeably by researchers, but there are some differences between them. 
This includes formatting differences (storing chromosome as integers rather than strings like `chr1`), the inclusion of mitochondrial DNA, as well as small numbers of differences of the locations of some variants on some chromosomes {cite}`GATK_Team2020-au`.

```{list-table} Table showing human reference genome builds
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

[//]: # (TODO: VCF format here?)

### Genes
Once we have an {ref}`assembled` genome, genes are identified within them.
The first step in this process is to look for nucleotides that code for the start codon (i.e. the amino acid methionine) (`ATG`) and end with one of the stop codons (`TAA`, `TGA`, or `TAG`).
The potential genes found through this search are then checked in the lab, e.g. through sequencing transcripts.

```{margin} Persistent identifiers
Persistent identifiers are long-lasting digital reference to entities{cite}`Meadows2019-zy`. 
Gene names can change; we might agree to change gs because Excel keeps converting them to dates{cite}`Vincent2020-ih` or because two genes turn out to be one.
Gene identifiers should be unique, and persistent over time, for example between genome builds, and as we learn more about their function, but they can still be merged or retired.
```

Like whole genomes, the sequences and positions of genes relative to the reference genome are stored in databases.
Again these are part of the UCSC, NCBI and EMBL-EBI ecosystem and these resources are vital to bioinformatics.
However, having multiple sources of gene information does cause some ambiguities when there are disagreements between databases. 
They can sometimes disagree on fundamental details such as locations of genes or the number of genes in an organism{cite}`Salzberg2018-yc` since the different databases take different decisions about how to store information.

Each of these databases also have their own identifiers and these names and symbols can change over time. 
For this reason, it can sometimes be difficult to map between identifiers.

In part, due to the amount of information that researchers have collected through through {ref}`gene knockouts<gene-knockouts>` and gene expression experiments, it is at the level of the gene that a lot of mappings about function take place.
This includes, for example, information about a gene's involvement in a gene regulatory network or in a {ref}`biological pathway<biological-pathway>`, and information about gene function according to {ref}`observational studies<observational-studies>`.

#### Variants
[//]: # (TODO: Cite databases)
[//]: # (TODO: Rephrase: haven't mentioned variant prioritisation yet)
[//]: # (TODO: Insert example of some data.)

Databases like dbSNP{cite}`Sherry2001-nm`, clinVar, and SNPedia contain information about the location of SNVs, their possible alleles, and their association to diseases. 
These are often used as part of a variant prioritisation pipeline, as well as by individuals who are investigating their own SNVs.

The NCBI’s dbSNP{cite}`Sherry2001-nm` is the world’s largest database of nucleotide variations, including their locations, possible alleles, and associations to diseases. 
It contains information from ten organisms (including human) and has information on indels and short tandem repeats in addition to SNVs. It was designed to store the annotations that are outputted from GWAS studies. 
Anyone can submit their findings about variants, and they must indicate what sort of evidence they have for the association.
The database gives SNVs unique identifiers (Reference SNP cluster IDs, a.k.a. RSIDs) of the form rs###, which are used by many other resources.

[//]: # (TODO: mention the ss numbers, and that the dbSNP builds don't "line up" with the human reference builds, how they are merged and the fact that they might map to different alternate contigs)

(rna-measurements)=
## RNA
[//]: # (TODO: Move protein abundance here: margin?)

```{margin} Gene expression = DNA + cellular environment
:name: gene-expression-scenarios
The environment, of the cell, and of the individual, and even of modifications to the DNA molecules, can affect the rate of gene expression.
This is obvious when we think about the fact that the same DNA is present in their liver cells, skin cells, and neurons and realise that the difference in how these cells/tissues look and function is due to differences in which proteins are actually being made at any given time. 
```

As I've already explained RNA can be measured through microarrays and RNA-Seq, but recently, RNA-Seq has been much more popular.
Measures of RNA are generally the best measures of gene expression, and this is important because it tells us about how DNA is used in different {ref}`scenarios<gene-expression-scenarios>`.
The location of transcripts, and which genes they map to is also available through databases.
Together, this information is used to understand the function of genes, to identify housekeeping genes, to re-engineer gene regulatory networks, and more. 

Since transcription is dependent on time, tissue, location, cell, etc, measures of RNA are also dependent on all of these conditions. 
Furthermore, they are sensitive to differences in laboratory conditions and experimental design, creating artefacts in the resulting data known as *batch effects*. 

**Differential expression versus baseline**: 
In order to reveal genes that are involved in specific diseases or functions, a popular type of gene expression experiment involves comparing the gene expression between two types of samples.
This is known as a differential expression experiment. 
On the other hand, a baseline experiment would measure the amount of expression in a range of more regular circumstances, aiming to characterise the range of expected expression in healthy individuals.

**Gene expression data pipeline**: 
Whether gene expression data gathered is gathered using microarrays or RNA-Seq, it goes through a substantial pipeline before it is used in a statistical analysis, or made available as a resource.

**Quality Control**: 
Before RNA-Seq data undergoes alignment, it undergoes quality control.
This involves comparing sequencing parameters to a data set of known accuracy{cite}`Illumina2014-nd` and is usually done as part of the sequencing.

[//]: # (TODO: add TPM/FKPM formula?)

(rna-normalisation)=
**Normalisation - within-sample normalisation: TPM and FPKM**: 
Within-sample normalisation methods are designed to account for sequencing depth and gene length so that gene expression values from the same sample (e.g. different replicates) can be more easily compared. 
Longer genes will have more reads mapped to them for an equal level of expression, so RNA-seq will report more counts. 
Similarly, without normalising, samples with greater sequencing depth will have higher counts for an equal level of expression. 

RPKM/FPKM (Reads/Fragments Per Kilobase Million) and TPM (Tags Per Million) are the three major normalisation techniques used for this purpose. 
In RPKM and FPKM, counts are first normalised for sequencing depth, and then for gene length. This means that they are suitable for comparing within a sample (e.g. between replicates. 
TPM, however performs the same steps in the opposite order, which has the desirable effect of ensuring that columns corresponding to TPM normalised samples sum to the same number. 
This means that TPM gives us a measure of relative abundance; we can compare across samples which proportion of counts are from each gene. 
For this reason, TPM is now generally preferred over RPKM/FPKM{cite}`Wagner2012-ac,Pimentel2014-xm`.

[//]: # (TODO: Move to combining section:)
**Normalisation - between-sample**:
While TPM gives us a measure of relative abundance, it does not give us a measure of absolute abundance. 
One outlying gene which is highly expressed will have the effect of making all other genes look relatively less expressed. 
We might expect this to occur, particularly when samples are under different conditions (e.g. disease/treatment). 
Between-sample normalisation methods are designed to counter this issue, and enable researchers to compare different samples.

These methods adjust counts to reduce the impact of outlying expression values. 
Examples include scale normalisation methods like TMM (used in edgeR{cite}`Robinson2010-kl`), the Log Geometric Mean (used in DESeq2{cite}`Robinson2010-kl,Love2014-vx`), and quantile normalisation (giving samples the same distribution of counts).

(protein-measurements)=
## Proteins
[//]: # (TODO: Mention how proteins map to transcripts and to genes and variants and whole genomes)

### Protein Structures
[//]: # (TODO: Make sure this makes sense here I just moved it)
[//]: # (TODO: Picture of a protein structure)
[//]: # (TODO: rewrite)

In 1969, Margaret Dayhoff created the first bioinformatics database to store protein structures imaged using X-ray crystallography, related to her publication of Atlas of Protein Sequence and Structure{cite}`Hersh1967-ox`. 
Soon after, in 1972, the Protein DataBank (PDB){cite}`noauthor_undated-ow` was established. 
This continues to be well-used and updated, at the time of writing holding structures of 148,827 biological molecules.

### Protein classification
[//]: # (TODO: Check not duplucated from earlier:)
Scientists are often interested in a "favourite" gene or protein, or have obtained a list of genes or proteins that they are interested in through a recent experiment. 
If an experiment about the specific protein has been carried out (e.g. to determine its function or structure), then a database like Uniprot (containing function and sequence information) or PDB (structure information) can be queried. 
However, this kind of information is not available for all proteins, so this is often necessary to make inferences about protein structure or function based on for example sequence similarity or protein classification.

[//]: # (TODO: Rewrite below based on section 2.4)

**SCOP:** 
The Structural Classification of Proteins (SCOP) database{cite}`Murzin1995-se` classifies all proteins with known structure based on their structural similarities, based on the consideration of the protein’s constituent domains. 
The classification is mostly done at the level of families, superfamilies, and folds arranged in a tree structure. 
Families represent the most similar proteins, which share a “clear evolutionary relationship”, while superfamilies represent less close evolutionary relationships, and folds represent the same secondary structure. This protein classification task, while aided by automation, was carried out largely by manual visual inspection.

SCOP was updated until 2009, but has been succeeded by SCOP2{cite}`Andreeva2014-om`. 
However, SCOP2 has a different underlying classification system, based on a complex graph, rather than a hierarchy. 
The CATH (Class, Architecture, Topology, Homologous superfamily){cite}`Orengo1997-vf` database provides another classification system, (also operating hierarchically), but created mostly via automation, which leads to major differences between the classifications{cite}`Csaba2009-of`.

#### SUPERFAMILY 
SUPERFAMILY{cite}`Gough2001-ct` uses HMMs to assign sequences to SCOP domains, primarily at the superfamily level. 
This allows the functions of poorly understood proteins to be inferred based on how closely they match known superfamilies. 
HMMs are very successful at such assignments since pairwise correlations between proteins (or their domains) and other proteins in the family may be weak, but consistently for many proteins; this can be picked up by an HMM. 
The superfamily level is chosen since it is the broadest level which suggests evolutionary relationships, but SUPERFAMILY also generates assignments at the (stricter) family level.

[//]: # (TODO: What are homologs?)

```{margin} BLAST
:name: blast
The Basic Local Alignment Search Tool{cite}`Altschul1990-zf`, is an extremely popular tool that is used to perform a basic search of nucleotide or amino acid sequences to known sequences, based on statistically significant similarities between parts of the sequence.
```

HMMs are created by first finding closely relating protein homologs for a given protein superfamily using {ref}`BLAST<blast>`, and then extending it by comparing the HMM to more distantly related homologs. 
The resulting HMM library is fine-tuned by some manual curation. 

The SUPERFAMILY website also contains other tools, including a database of all sequences (genomes) which are used to generate the HMM library.

(my-supfam-contribution=)
**SUPERFAMILY update**
I contributed to SUPERFAMILY’s 2014 update{cite}`Oates2015-li` by editing the paper, and adding a small number of proteomes. 
The SUPERFAMILY database of proteomes doubled from 1400 to over 3200 from 2010 to 2014. 
The update paper described this development, as well as highlighting SUPERFAMILY as a resource for unique proteomes that are not found elsewhere (e.g. Uniprot). 
Although SUPERFAMILY’s primary resource is it’s HMM library, it also integrates a range of other tools for sequence analysis, for example protein disorder prediction (D2P2) and GO annotation (dcGO), as well as a domain-based phylogenetic tree. 

(phenotype-measurements)=
## Phenotypes
As described in {numref}`what-is-phenotype`, most phenotypes that are studied today are based in medicine: this can range from the results of a blood test, to presence of a disease diagnosis. 
Neutral like height, eye colour, baldness, etc, are also measured.

Phenotypic traits can be measured in a variety of ways, depending on the phenotype.
One important type is data collected via survey or interview, where participants self-identify as having certain illnesses, or symptoms.
This type of data can suffer from biases due to what people feel comfortable answering{cite}`Furnham1986-yt,Knauper1994-wl`.

Phenotype data must be connected to genotype data in order to be useful for validating genotype-to-phenotype predictions, and due to the sensitivity of this kind of information, there are a limited number of these kinds of data sets.
Some data sets focus on particular phenotypes, while others are cohort studies that record everything about a cohort (for example the the Avon Longitudinal Study of Parents and Children, ALSPAC{cite}`Golding2001-oj`, and the UK Biobank{cite}`Bycroft2018-mw`). 
In the latter case, it is not easy for researchers to access the whole data set, due to concerns about de-anonymisation{cite}`Powell2021-vc`.

Knowledge about how phenotypes are related to each other (e.g. liver cancer is a type of cancer that is found in the liver) is organised in {ref}`ontologies<what-are-ontologies>`, which are described in their own section. 
These ontologies also form a defined vocabulary for terms, with identifiers, definitions, and links to other information.

## Measuring the connection between genotype and phenotype
[//]: # (TODO: Example biological pathway illustration here)
[//]: # (TODO: Mention state of computational prediction here, too)
[//]: # (TODO: Mention information at level of genes is in gene ontology annotation database, signposting to next section)
There are many different methods of investigating the connection between genotype and phenotype.
Some methods focus solely on the "what", seeking to answer the question "*what phenotypes(s)* does this gene have an effect on?", while some focus also on the how, i.e. "*what phenotype(s)* does this gene have an effect on, and *what are the mechanisms* by which this takes place?".
{ref}`Genome Wide Association Studies (GWAS)<observational-studies>` and {ref}`gene knockouts<gene-knockouts>` are two methods of finding potential or actual "what" connections, while building {ref}`biological pathways<biological-pathways>` is currently the main way of finding "why" connections.
There are also many experiments which can contribute pieces of the puzzle, for example elucidating an indirect link in a biological pathway.

Connections to phenotype can be made with different scales and types of genetic features, from SNPs, genes, transcripts, and proteins to populations.

(observational-studies)=
### Genome Wide Association Studies
[//]: # (TODO: Have I mentioned p-value? Margin? Margin Graph?)
Genome Wide Association Studies (GWAS) are large observational studies where the genotypes of a cohort with a specific phenotype (e.g. diabetes) are compared to the genotypes of a cohort lacking in that phenotype (i.e. a control group) in order to find genomic loci that are statistically associated with the phenotype. 
This has been a popular type of scientific enquiry since the first GWAS study in 2005. 
GWAS generally results in lists of SNPs, often in the hundreds, ordered by p-value. 
Disentangling which of these SNPs (if any) *cause* the trait (in addition to correlating with it) is a tricky, particularly since GWAS specifically interrogates common variants. 
The process of identifying causal variants generally involving identifying regions in linkage disequilibrium, and re-sequencing regions of interest in further detail.

The GWAS catalog database{cite}`Buniello2019-cv,L_Emery2017-rd` was founded in 2008, to provide a consistent and accessible location for published SNP-trait associations, which extracts information about experiments from the literature (currently over 70000 associations from over 3000 publications).

(gene-knockouts)=
## Gene Knockouts
Insight into gene function can be gained by “knocking out” a gene, preventing it from being translated into a working protein, for example using CRISPR. 
Combinations of up to four genes can be knocked out in a single experiment. 
Knocking out a gene can lead to a difference in phenotype, and differences in gene expression, which can be used to help determine gene regulatory networks. 
There is a lot of existing data on the phenotypic results of mouse knockouts, since they are often used to create mouse models for diseases. 
Unfortunately, it is not always well-recorded when knockouts lead to no detectable phenotypic change{cite}`Barbaric2007-zm`.

(biological-pathways)=
### Biological Pathways
Biological pathways are generally built either through a data-centric method, i.e. beginning with {ref}`gene expression<rna-measurements>` or mass spectrometry data{cite}`Zhang2016-ty`, or through a knowledge-centric method, by beginning with a graph based on knowledge from publications and domain experts{cite}`Viswanathan2008-tn`.
There are a number of popular databases which store pathways, for example Reactome{cite}`Fabregat2018-na` and KEGG{cite}`Kanehisa2008-wz`. 
These resources are well-linked to other sources of information, for example gene, rna, protein and chemical databases.
