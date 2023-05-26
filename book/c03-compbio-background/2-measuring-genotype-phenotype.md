(measuring-genotype-phenotype)=
# From genotype to phenotype: what is measured
[//]: # (TODO: Check through and signpost where resources are just humans or model organisms or loads of things)
[//]: # (TODO: Have an aside about model organisms)
This subsection now delves into the details of the data that is collected, looking in turn at measurements of {ref}`DNA<dna-measurements>`,  {ref}`RNA<rna-measurements>`, {ref}`proteins<protein-measurements>`, and {ref}`phenotypes<phenotype-measurements>`.
This is to illustrate what kinds of data exist within the databases of the bioinformatics landscape, as well as some of the subtle issues that arise when using and linking them.

(dna-measurements)=
## DNA
In the {ref}`previous Chapter<what-is-dna>`, DNA was described, as well as the working scientific model of it's link to phenotype. 
In this section, the focus is on the details of how this is measured and stored: and how these details impact computational biology research. 
Once again, these details are introduced from big to small scale, beginning with whole genomes and moving through to individual SNPs.

(whole-genome)=
### Whole genomes
[//]: # (TODO: What databases is SUPERFAMILY built on? What is PQI based on? Put them here.)
[//]: # (TODO: MEntion anyone can submit/collaborative nature of databases)
Whole genome sequencing (WGS) is the sequencing of {ref}`all<really-wgs>` the genetic material of an organism, whether or not it is transcribed into RNA, or translated into protein.
In humans, this includes all chromosomal and mitochondrial DNAs.
Whole genomes are {ref}`sequenced<sequencing>` and {ref}`assembled<assembly-and-alignment>` as previously described.

```{margin} The *whole* genome?
:name: really-wgs
In practice, almost complete genomes are also referred to as whole genomes, particularly for more complex genomes.
Even the human genome still a small outstanding amount of unassembled DNA{cite}`Miga2015-zl` - satellite DNA which is thought to be part of the structure of chromosomes.
```

[//]: # (TODO: Mention 1000Genomes?)
[//]: # (TODO: Remove mention of VCF here as I explain it later and it's not really relevant yet here)

(individual-wgs)=
When WGS is carried out for an organism that has already been sequenced, the sequence data is mapped to the organism's {ref}`reference genome<human-reference-genome>`.
This provides a more detailed and more accurate alternative to {ref}`genotyping<genotyping>` data.
When cohorts have their whole genomes sequenced, this allows information from WGS data to be compressed into Variant Call Format (VCF) files, which stores only the allele calls for locations where there is variation in the population.

Whole genomes for different species can be compared to one another to give us insight about these organisms, or within one species, individuals can be compared to understand the importance of genes or mutations for that organism.
Genomes from different species are stored in databases such as the University of California Santa Cruz (UCSC) Genome Browser database{cite}`Kent2002-jg`, the US National Centre for Biotechnology Information (NCBI) Genome Sequence database{cite}`Harger2000-vr`, or the European Bioinformatics Institute's (EBI) Ensembl Genome database{cite}`Hubbard2002-oi`.

(human-reference-genome)=
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

(gene-measurement)=
### Genes
Once scientists have an {ref}`assembled<assembly-and-alignment>` genome, genes are identified within them.
The first step in this process is to look for nucleotides that code for the start codon (i.e. the amino acid methionine) (`ATG`) and end with one of the stop codons (`TAA`, `TGA`, or `TAG`).
The potential genes found through this search are then checked in the lab, e.g. through sequencing transcripts.

Like whole genomes, the sequences and positions of genes relative to the reference genome are stored in databases.
Again these are part of the UCSC, NCBI and EMBL-EBI ecosystem and these resources are vital to bioinformatics.
However, having multiple sources of gene information does cause some ambiguities when there are disagreements between databases. 
They can sometimes disagree on fundamental details such as locations of genes or the number of genes in an organism{cite}`Salzberg2018-yc` since the different databases take different decisions about how to store information.

```{margin} Persistent identifiers
:name: identifiers
Persistent identifiers are long-lasting digital reference to entities{cite}`Meadows2019-zy`. 
Gene names can change; scientists might agree to change them because Excel keeps converting them to dates{cite}`Vincent2020-ih` or because what were thought to be two genes turns out to be one.
Gene identifiers should be unique and persistent over time, for example between genome builds and as more islearned about their function, but they can still be merged or retired.
```

Each of these databases also have their own {ref}`identifiers<identifiers>` and these names and symbols can change over time. 
For this reason, it can sometimes be difficult to map between identifiers from different sources.

Due to the history of the gene, and the amount of information that researchers have collected through {ref}`gene knockouts<gene-knockouts>` and gene expression experiments, it is at the level of the gene that a lot of mappings about function take place.
This includes, for example, information about a gene's involvement in a gene regulatory network or in a {ref}`biological pathway<biological-pathways>`, and information about gene function according to {ref}`observational studies<observational-studies>`.

Even in the most-studied genomes, there are many genes for which databases contain sequence information, but no functional information.
This is due to the low cost in sequencing experiments in comparison to the expense of knock-out or other function-determining experiments, and the inequality of studied proteins/genes. 
This missing functional information is not likely to appear soon, without some sort of revolution in funding priorities or technology.

(variants-measurements)=
### Variants
Information about which variants individuals have comes from either {ref}`genotype<genotyping>` or {ref}`whole genome sequencing<individual-wgs>` data.
Some of this data is owned by private companies, such as 23andMe.

Databases like dbSNP{cite}`Sherry2001-nm`, clinVar, and SNPedia contain information about the location of these variants, their possible alleles, their frequency in populations, their functions, and associated phenotypes. 

The largest SNP database - NCBI’s dbSNP{cite}`Sherry2001-nm` - contains information from ten organisms (including human) and has information on indels and short tandem repeats in addition to SNPs. 
Anyone can submit their findings about variants to dbSNP, and they must indicate what sort of evidence they have for the association.
dbSNP gives SNPs unique identifiers (Reference SNP cluster IDs, a.k.a. RSIDs) of the form `rs###`, which are used by many other resources.


(rna-measurements)=
## RNA
For RNA there are three main types of data: sequence (and mappings), structure, and gene expression data.

(rna-sequence-structure)=
### RNA Sequence and Structure
The sequences of RNA (including miRNAs, tRNAs, rRNAs, etc), and their locations relative to reference geneomes are stored in databases such as Ensembl.
For mRNAs that encode for proteins, this also enables mappings between transcript IDs, gene IDs, and protein IDs, and again these are integrated with previously mentioned gene databases. 

Functional RNA has structure with recurring motifs similar to those of proteins. 
There are also databases of functional RNA structure{cite}`Andrews2017-tr,Richardson2020-wa` (similar to {ref}`those for proteins<protein-stucture-measurements>`), but those for RNA are at an earlier stage.

(gene-expression-measurements)=
### Gene Expression

```{margin} Housekeeping genes
:name: housekeeping-genes
Genes whose core functionality are to perform basic cell maintainance are known as *housekeeping genes*.
```

As I've already explained RNA abundance in samples can be measured through RNA microarrays and RNA-Seq, and recently, RNA-Seq has been much more popular.
Measures of mRNA abundance (i.e. gene expression data) are generally the most popular measures of translation (compared to {ref}`protein abundance<protein-abundance>` for example), and are therefore it is the most diverse data currently in databases, which makes it ideal for informing us how DNA's blueprints are being used in different {ref}`scenarios<gene-expression-scenarios>`.
Together with mappings, this data is used to understand the function of genes, to identify {ref}`housekeeping genes<housekeeping-genes>`, to re-engineer gene regulatory networks, and more - knowledge about DNA function that wouldn't be possible to glean without measuring RNA.
Like other bioinformatics data, gene expression data is also available in databases such as the EBI's Gene Expression Atlas (GxA){cite}`Petryszak2016-je` and Single Cell Expression Atlas{cite}`Papatheodorou2020-ib` (for {ref}`bulk and single cell gene expression<bulk-scRNA-seq>`, respectively).

```{margin} Bulk versus Single-cell RNA-Seq
:name: bulk-scRNA-seq
Most RNA-Seq experiments sequence RNA from millions of cells at a time: this is bulk RNA-seq. Bulk RNA-Seq may take place for many cells of the same type or for a collection of different cell types (e.g. a tissue). Single-cell RNA-Seq (scRNA-seq) allows RNA to be sequenced from a single cell and is becoming increasingly widespread{cite}`Ashraful_Haque_Jessica_Engel_Sarah_A_Teichmann_Tapio_Lonnberg2017-rj`.
```

**Differential expression versus baseline experiments**: 
In order to reveal genes that are involved in specific diseases or functions, a popular type of gene expression experiment involves comparing the gene expression between two types of samples, for example between healthy samples and cancerous samples.
This is known as a *differential* expression experiment. 
In contrast, a *baseline* experiment would measure the amount of expression in a range of more regular circumstances, aiming to characterise the range of expected expression in healthy individuals.

(rna-seq-pipeline)=
### RNA-Seq bioinformatics pipeline

RNA-Seq data *counts* the number of times a sequence matching that gene or transcript has been sequenced.
The amount of RNA from a particular transcript that is found in a sample in a given experiment is dependent on the sequencing depth and the transcript length.
The rate of transcription is dependent on time of day, tissue, location, cell type, etc, so measures of RNA are also dependent on all of these conditions: this can make RNA measurements difficult to compare between experiments.
To make matters worse, RNA-Seq and RNA microarray measurements are also sensitive to differences in laboratory conditions and experimental design, creating artefacts in the resulting data known as *batch effects*. 
Taken together, these things mean that there is a substantial data preparation pipeline for RNA-Seq data.

(quality-control)=
**Quality Control**: 
Before RNA-Seq data undergoes {ref}`alignment<assembly-and-alignment>`, it undergoes quality control.
This involves comparing sequencing parameters to a data set of known accuracy{cite}`Illumina2014-nd` and is usually done as part of the sequencing.

(rna-normalisation)=
**Normalisation - within-sample normalisation: TPM and FPKM**: 
Within-sample normalisation methods are designed to account for sequencing depth and transcript length so that gene expression values from the same sample (e.g. different replicates) can be more easily compared. 
Longer genes will have more reads mapped to them for an equal level of expression, so RNA-seq will report more counts. 
Similarly, without normalising, samples with greater sequencing depth will have higher counts for an equal level of expression. 

RPKM/FPKM (Reads/Fragments Per Kilobase Million) and TPM (Tags Per Million) are the three major normalisation techniques used for this purpose. 
In RPKM and FPKM, counts are first normalised for sequencing depth, and then for gene length. 
This means that they are suitable for comparing within a sample (e.g. between replicates). 
TPM, however performs the same steps in the opposite order, which has the desirable effect of ensuring that columns corresponding to TPM normalised samples sum to the same number. 
This means that TPM gives us a measure of relative abundance; the proportion of counts are from each gene can be compared across samples. 
For this reason, TPM is now generally preferred over RPKM/FPKM{cite}`Wagner2012-ac,Pimentel2014-xm`.

**Normalisation - between-sample**:
While TPM gives us a measure of relative abundance, it does not give us a measure of absolute abundance. 
One outlying gene which is highly expressed will have the effect of making all other genes look relatively less expressed. 
This might be expected to occur, particularly when samples are under different conditions (e.g. disease/treatment). 
Between-sample normalisation methods are designed to counter this issue, and enable researchers to compare different samples.

These methods adjust counts to reduce the impact of outlying expression values. 
Examples include scale normalisation methods like TMM (used in edgeR{cite}`Robinson2010-kl`), the Log Geometric Mean (used in DESeq2{cite}`Robinson2010-kl,Love2014-vx`), and quantile normalisation (giving samples the same distribution of counts).

(protein-measurements)=
## Proteins
Similar to RNA, proteins also have (amino acid) sequence data, mappings to genes and transcripts, structure data and protein abundance data. 
While for RNA, abundance (gene expression) data is the most popular type, for proteins, it is structure data, and from this structural information, there is a very detailed system of protein classification.

Proteins are where the history of bioinformatics databases that any researcher can contribute to began.
Margaret Dayhoff created the first bioinformatics database in 1969, to store protein structures imaged using X-ray crystallography, related to her publication of Atlas of Protein Sequence and Structure{cite}`Hersh1967-ox`. 
The Uniprot{cite}`Pundir2016-ya` database of protein sequence and functional information is the heir to this early database, it contains information about protein sequence, domain architecture, and function.

(protein-sequence)=
### Protein Sequence
Just as DNA and RNA can be {ref}`sequenced<sequencing>` in nucleic acids, proteins can be sequenced by their amino acids, although the technology behind doing this is quite different (e.g. using mass spectrometry is the most common way).
This is often done for a small part of a protein, to allow it to be matched to the expected amino acid sequence based on gene or transcript sequences.
This is how mappings from protein IDs to gene IDs and transcript IDs are available through databases (e.g. Ensembl).

Protein sequencing is also used to characterise protein's {ref}`post-translational modifications<post-translational-modifications>`.

(protein-abundance)=
### Protein Abundance 
```{margin} Mass spectrometry
:name: mass-spec
Mass spectrometry is the process of ionising a sample and accelerating it through an electric or magnetic field to deduce it's mass-to-charge ratio.
```

The abundance of proteins in a sample can be measured through various quantitative proteomics techniques. 
These are carried out using electrophoresis, or {ref}`mass spectrometry<mass-spec>`, for example.
Similar to gene expression, this technique is often used to compare between two different samples (e.g. disease and control groups).
Data from such experiments are also available in databases{cite}`Wang2012-pv,Samaras2020-mg`.

```{margin} Gene Expression and Protein Abundance data
:name: gene-expression-protein-abundance
It's interesting to note that gene expression levels (from RNA-Seq and microarray data) are not necessarily strongly correlated with protein abundance; this has been found in mice{cite}`Schwanhausser2011-tm`, yeast{cite}`Gygi1999-lr`, and human{cite}`Kosti2016-gt`. 

In human, Spearman correlations between protein abundance and gene expression levels vary between 0.36 and 0.50, depending on tissue, meaning that they are only weakly or moderately correlated{cite}`Kosti2016-gt`.
```

(protein-stucture-measurements)=
### Protein Structure
The Protein DataBank (PDB){cite}`noauthor_undated-ow` was established not long after Dayhoff's database, it contains three dimensional protein structures, typically obtained using X-ray Crystallography or NMR spectroscopy. 
The PDB continues to be well-used and updated, at the time of writing holding structures of 148,827 biological molecules.
These structures are used for {ref}`protein classification<protein-classification>`, and for Molecular Dynamics simulations (simulating the physical interactions of molecules).


(phenotype-measurements)=
## Phenotypes
As described in {numref}`what-is-phenotype`, most phenotypes that are studied today are based in medicine: this can range from the results of a blood test, to the presence of a disease diagnosis. 
Neutral traits like height, eye colour, baldness, etc, are also sometimes measured.

Phenotypic traits can be measured in a variety of ways, depending on the phenotype.
One important type is data collected via survey or interview, where participants self-identify as having certain illnesses, or symptoms.
This type of data can suffer from biases due to what people feel comfortable answering{cite}`Furnham1986-yt,Knauper1994-wl`.

Phenotype data must be connected to genotype data in order to be useful for validating genotype-to-phenotype predictions, and due to the sensitivity of this kind of information, there are a limited number of these kinds of data sets.
Some data sets focus on particular phenotypes, while others are cohort studies that record everything about a cohort (for example the the Avon Longitudinal Study of Parents and Children, ALSPAC{cite}`Golding2001-oj`, and the UK Biobank{cite}`Bycroft2018-mw`). 
In the latter case, it is not easy for researchers to access the whole data set, due to concerns about de-anonymisation{cite}`Powell2021-vc`.

Knowledge about how phenotypes are related to each other (e.g. liver cancer is a type of cancer that is found in the liver) is organised in {ref}`ontologies<what-are-ontologies>`, which are described in their own section. 
These ontologies also form a defined vocabulary for terms, with identifiers, definitions, and links to other information.
This information can then be used as one way to investigate the connection between genotype and phenotype.

(connection-genotype-phenotype)=
## Measuring the connection between genotype and phenotype

[//]: # (TODO: Mention molecular dynamics)

There are many different methods of investigating the connection between genotype and phenotype.
Some methods focus solely on the "what", seeking to answer the question "*what phenotypes(s)* does this gene have an effect on?", while some focus also on the "how", i.e. answering "*what is the mechanism* behind this phenotype?".
{ref}`Genome Wide Association Studies (GWAS)<observational-studies>` are the most popular way of finding potential or actual "what" connections, while {ref}`gene knockouts<gene-knockouts>` and building {ref}`biological pathways<biological-pathways>` is currently the main way of finding "why" connections.
There are also many more specific kinds of experiments which can contribute pieces of the puzzle. 

Efforts to uncover the links between genotype and phenotype broadly take one of three approaches:
1. __DNA-centric:__ Looking closely at one particular variant (e.g. SNP or gene) at a time, and comparing data to a change in only this variable (knocking out a gene). This is a successful, but expensive methodology, but it isn't hugely successful at finding multi-genic (aka complex) traits. In addition to it's success at uncovering simpler traits, these methods create a wealth of information  which are collected in databases.
2. __Phenotype-centric:__ Looking closely at one particular phenotype and comparing the genetics of people with the phenotype to those without it. Again this is expensive and it also has the problem of finding that in lists of potentially involved genes, some will be there by random chance.
3. __Cross-cutting:__ Computational methods which aim to uncover protein or variant function, and protein interactions across the genome, and across phenotypes. These methods tend to rely on data from (1) and (2). I will discuss some of these in the {numref}`predictive-methods`.

Connections to phenotype can be made with different scales and types of genetic features, from SNPs, genes, transcripts, and proteins to networks thereof and variation within populations.
Computational biology links these resources well, so that knowledge at these different scales can be investigated, the {ref}`Gene Ontology Annotation<gene-ontology-annotation>` resource for example, connects information from many of these computational and experimental sources at the level of the gene. 
Similarly, OMIM.org{cite}`amberger2019omim` (Online Mendelian Inheritance Map) and the Human Gene Mutation Database{cite}`stenson2017human` are also resources which seek to catalog links between (human) genetic and phenotype information - both of which contain and share resources with Gene Ontology.

(observational-studies)=
### Genome Wide Association Studies
Genome Wide Association Studies (GWAS) are large observational studies where the genotypes of a cohort with a specific phenotype (e.g. diabetes) are compared to the genotypes of a cohort lacking in that phenotype (i.e. a control group) in order to find genomic loci that are statistically associated with the phenotype. 
This has been a popular type of scientific enquiry since the first GWAS study in 2005. 
GWAS generally results in lists of SNPs, often in the hundreds, ordered by p-value. 
Disentangling which of these SNPs (if any) *cause* the trait (in addition to correlating with it) is tricky, particularly since GWAS specifically interrogates common variants. 

The GWAS catalog database{cite}`Buniello2019-cv,L_Emery2017-rd` was founded in 2008, to provide a consistent and accessible location for published SNP-trait associations, which extracts information about experiments from the literature (currently over 70000 associations from over 3000 publications).

Phenome-Wide Association{cite}`Denny2010-pn` Studies (PheWAS) are an extension of these where multiple phenotypes are investigated at once in the same cohort of people.

(gene-knockouts)=
### Gene Knockouts
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
