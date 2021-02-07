(measuring-genotype-phenotype)=
# From genotype to phenotype: what is measured
We will now delve into the details of some of these datasets, looking first at {ref}`DNA<dna-measurements>`, then {ref}`RNA<rna-measurements>`, then {ref}`proteins<protein-measurements>`, then {ref}`phenotypes<phenotype-measurements>`.

(dna-measurements)=
## DNA
In the {ref}`previous Chapter<what-is-dna>`, we looked at what DNA is and how that links to phenotype. 
Now we're going to look at the details of how this is measured and stored: and how these details impact computational biology research. 
We'll once again go from big to small, beginning with whole genomes and moving through to individual SNPs.

### Whole genome
The whole genome is all the genetic material of an organism, whether or not it is transcribed into RNA, or translated into protein.
In humans, this includes all chromosomal and mitochondrial DNAs.
Whole genomes for different organisms can be compared to one another to give us insight about the organisms, or within an organism, individuals can be compared to understand the importance of sections of DNA for that organism.

#### The human reference genome
As {ref}`previously mentioned<genomes>`, reference genomes are designed to represent whole organisms: these genomes aim to have the most common allele at any given nucleotide, and are then annotated at positions where individuals differ. 

(different-builds)=
**Builds and patches:** 
Reference genomes are {ref}`assembled<assembly-and-alignment>` as previously described.
Then as more genomes are sequenced, more information comes to light about the nature of the human genome. 
For example, some locations are revealed to be likely sequencing artifacts. 
New major versions of genomes are released every few years to fix these changes. 
These versions are called *builds*. 
Between builds and patches, sequences may be added, removed, or moved to different locations on chromosomes.

**Differences between GRC and UCSC builds:**
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

### Genes
Once we have an {ref}`assembled` genome 

There can be disagreements about the locations of genes on the genome, and popular databases of genes fundamentally disagree on this and on the number of genes{cite}`Salzberg2018-yc`. 
Gene names and symbols change over time, and can be difficult to map between for this reason.

[//]: # (TODO: Write: sequenced the same way, persistent identifiers, which map to genomes)
#### Regulatory features
[//]: # (TODO: Explain that regulatory features are not as well defined yet, i.e. with IDs, etc.)
[//]: # (TODO: Mention http://www.ensembl.org/info/genome/funcgen/regulatory_features.html)

#### Variants
[//]: # (TODO: Sentence about variants)



#### Variant databases
Databases like dbSNP, clinVar, and SNPedia contain information about the location of SNVs, their possible alleles, and their association to diseases. 
These are often used as part of a variant prioritisation pipeline, as well as by individuals who are investigating their own SNVs.

The NCBI’s dbSNP{cite}`Sherry2001-nm` is the world’s largest database of nucleotide variations, including their locations, possible alleles, and associations to diseases. 
It contains information from ten organisms (including human) and has information on indels and short tandem repeats in addition to SNVs. It was designed to store the annotations that are outputted from GWAS studies. 
Anyone can submit their findings about variants, and they must indicate what sort of evidence they have for the association.
The database gives SNVs unique identifiers (Reference SNP cluster IDs, a.k.a. RSIDs) of the form rs###, which are used by many other resources.

[//]: # (TODO: mention the ss numbers, and that the dbSNP builds don't "line up" with the human reference builds, how they are merged and the fact that they might map to different alternate contigs)

[//]: # (TODO: mention snpedia?)

(rna-measurements)=
## RNA
[//]: # (TODO: Rewrite this section, and maybe move it to section 1, so that it fits properly and is less wordy)
[//]: # (TODO: Write about how transcripts map to the genes ENSEMBL)
One of the most popular measures of gene expression, is the measure of how much RNA is in a cell at a given time. 

DNA can’t tell us the whole story.
 On it's own it can’t tell us what we’d like to know about a gene’s function or a person’s traits. Nonetheless, I’d like to spell out why that is for those who do not have that background. The central dogma of molecular biology can be paraphrased as “DNA makes RNA makes proteins”. So, if we know what a person’s DNA is, then why would we also want to know about their RNA?

The answer boils down to the effect of the environment. “DNA makes RNA makes proteins” is shorthand for “DNA interacts with the environment to make RNA, and RNA interacts with the environment to make proteins”. The environment, of the cell, and of the individual, and even of modifications to the DNA molecules, is the reason why DNA alone is not enough to explain how we function. DNA is the collection of blueprints for what can be made, but the environment decides what goes into production; which RNA and proteins are made and how much. 

In any given individual, the same DNA is present in their liver cells, skin cells, and neurons. The difference in how these cells/tissues look and function is due to differences in which proteins are actually being made at any given time. Gene expression is a way of measuring how the environment of the cell is affecting the process of making proteins from DNA.

Gene expression data is used to understand the function of genes, to identify housekeeping genes, to re-engineer gene regulatory networks, and more. This kind of insight can not be gained from looking at DNA alone.

### RNA-seq 
Since transcription is dependent on time, tissue, location, cell, etc, RNA-seq experiments are also dependent on all of these conditions. Furthermore, they are sensitive to differences in laboratory conditions and experimental design, creating artefacts in the resulting data known as batch effects. 

#### Differential expression versus baseline
[//]: # (TODO: Write)

#### Gene expression data pipeline
[//]: # (TODO: This section needs more work)

Whether gene expression data gathered is gathered using microarrays or RNA-Seq, it goes through a substantial pipeline before it is used in a statistical analysis, or made available as a resource.

##### Quality Control
[//]: # (TODO: This only cites illumina, obviously there are other ways to sequence rna)
Before RNA-Seq data undergoes alignment, it undergoes quality control. This involves comparing sequencing parameters to a data set of known accuracy{cite}`Illumina2014-nd` and is usually done as part of the sequencing.

##### Normalisation - within-sample normalisation
Within-sample normalisation methods are designed to account for sequencing depth and gene length so that gene expression values from the same sample (e.g. different replicates) can be more easily compared. Longer genes will have more reads mapped to them for an equal level of expression, so RNA-seq will report more counts. Similarly, without normalising, samples with greater sequencing depth will have higher counts for an equal level of expression. 

RPKM/FPKM (Reads/Fragments Per Kilobase Million) and TPM (Tags Per Million) are the three major normalisation techniques used for this purpose. In RPKM and FPKM, counts are first normalised for sequencing depth, and then for gene length. This means that they are suitable for comparing within a sample (e.g. between replicates. TPM, however performs the same steps in the opposite order, which has the desirable effect of ensuring that columns corresponding to TPM normalised samples sum to the same number. This means that TPM gives us a measure of relative abundance; we can compare across samples which proportion of counts are from each gene. For this reason, TPM is now generally preferred over RPKM/FPKM{cite}`Wagner2012-ac,Pimentel2014-xm`.

(rna-normalisation)=
##### Normalisation - between-sample
While TPM gives us a measure of relative abundance, it does not give us a measure of absolute abundance. One outlying gene which is highly expressed will have the effect of making all other genes look relatively less expressed. We might expect this to occur, particularly when samples are under different conditions (e.g. disease/treatment). Between-sample normalisation methods are designed to counter this issue, and enable researchers to compare different samples.

These methods adjust counts to reduce the impact of outlying expression values. Examples include scale normalisation methods like TMM (used in edgeR{cite}`Robinson2010-kl`), the Log Geometric Mean (used in DESeq2{cite}`Robinson2010-kl,Love2014-vx`), and quantile normalisation (giving samples the same distribution of counts).

[//]: # (TODO: Explain batch effects here?)


(protein-measurements)=
## Proteins
[//]: # (TODO: Mention how proteins map to transcripts and to genes and variants and whole genomes)

### Protein Structures
[//]: # (TODO: Make sure this makes sense here I just moved it)

In 1969, Margaret Dayhoff created the first bioinformatics database to store protein structures imaged using X-ray crystallography, related to her publication of Atlas of Protein Sequence and Structure{cite}`Hersh1967-ox`. 
Soon after, in 1972, the Protein DataBank (PDB){cite}`noauthor_undated-ow` was established. 
This continues to be well-used and updated, at the time of writing holding structures of 148,827 biological molecules.

### Protein classification
[//]: # (TODO: Check not duplucated from earlier:)
Scientists are often interested in a "favourite" gene or protein, or have obtained a list of genes or proteins that they are interested in through a recent experiment. If an experiment about the specific protein has been carried out (e.g. to determine its function or structure), then a database like Uniprot (containing function and sequence information) or PDB (structure information) can be queried. However, this kind of information is not available for all proteins, so this is often necessary to make inferences about protein structure or function based on for example sequence similarity or protein classification.

[//]: # (TODO: Check BLAST is in the right place. Probably makes more sense in another section: DNA?)
#### BLAST
BLAST, or the The Basic Local Alignment Search Tool{cite}`Altschul1990-zf`, is an extremely popular tool that is used to perform a basic search of nucleotide or amino acid sequences to known sequences, based on statistically significant similarities between parts of the sequence.

##### SCOP
[//]: # (TODO: Rewrite below based on section 2.4)
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

[//]: # (TODO: Also explain that phenotypes can be associated with biological molecules at any level, e.g. SNPs, Genes, Populations)
[//]: # (TODO: Explain CRISPR in an aside to below if haven't mentioned already)
[//]: # (TODO: Phenotype data is fairly well protected: people don't like to share it)

## Knockouts
Insight into gene function can be gained by “knocking out” a gene, preventing it from being translated into a working protein, for example using CRISPR. 
Combinations of up to four genes can be knocked out in a single experiment. 
Knocking out a gene can lead to a difference in phenotype, and differences in gene expression, which can be used to help determine gene regulatory networks. 
There is a lot of existing data on the phenotypic results of mouse knockouts, since they are often used to create mouse models for diseases. 
Unfortunately, it is not always well-recorded when knockouts lead to no detectable phenotypic change{cite}`Barbaric2007-zm`.

## Genome Wide Association Studies
Genome Wide Association Studies (GWAS) are large observational studies where the genotypes of a cohort with a specific phenotype (e.g. diabetes) are compared to the genotypes of a cohort lacking in that phenotype (i.e. a control group) in order to find genomic loci that are statistically associated with the phenotype. 
This has been a popular type of scientific enquiry since the first GWAS study in 2005. 
GWAS generally results in lists of SNPs, often in the hundreds, ordered by p-value. 
Disentangling which of these SNPs (if any) cause the trait is a tricky, particularly since GWAS specifically interrogates common variants. 
The process of identifying causal variants generally involving identifying regions in linkage disequilibrium, and re-sequencing regions of interest in further detail.

The GWAS catalog database{cite}`Buniello2019-cv,L_Emery2017-rd` was founded in 2008, to provide a consistent and accessible location for published SNP-trait associations, which extracts information about experiments from the literature (currently over 70000 associations from over 3000 publications).

