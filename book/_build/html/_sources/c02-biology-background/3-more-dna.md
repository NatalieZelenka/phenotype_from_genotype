(dna-organised)=
## A closer look at DNA: Genomes, Genes, and Genetic Variation
Now that we have a basic overview of how DNA can influence phenotype, we can discuss the way that DNA is organised and categorised in a little more detail. We'll look from big ({ref}`genomes<genomes>`) to small ({ref}`single nucleotides<single-nucleotides>`).

### Genomes, exomes, proteomes

(genomes)=
#### Genomes
The genome is the full amount of DNA belonging to an organism. We can talk about the genome of an individual, or about the genome of an organism (e.g. the human genome).
When we talk about an organism's genome, we are actually talking about an example genome for that organism: the organisms' *reference* genome. 
The reference genome not belong to any individual organism, but instead is supposed to have the most common nucleotide each DNA location. 

Reference genomes allow us to make general statements about an organism (e.g. "the human genome is 3 billion base pairs long"), and also to make comparisons between organisms (e.g. {ref}`"humans share 1% of their DNA with a banana"<human-banana-dna>`). 
We also discuss individuals' genomes in relation to the difference between the individual and the reference genome.

(human-banana-dna)= 
```{margin} Humans and bananas
Humans share 50% of their *protein-coding* dna with bananas, but only 1% of their genome.
``` 

#### The exome and the proteome
Still thinking big, we have the *exome* and the *proteome*. 
Both of these refer to locations across the whole genome, but missing stretches in between.
The exome describes the set of all exons (protein-coding nucleotides) across the genome. 
The proteome is generally used to mean the set of all proteins in in an organism (which can be much larger than the set of genes due to {ref}`alternate splicing<alternative-splicing>`), but it can also be used to describe the part of the genome with relating to the set of protein sequences.

### Genes and the regions around them

#### Genes
DNA is often considered at the level of the gene.
Genes have been so central to the historical study of dna (hence the name *gene*tics), and the gene-centric view of molecular biology continues to this day.
For example, many researchers have favourite genes, which they primarily study, and understand the mechanisms of in detail. 
And for this reason, diseases and phenotypes are often attributed at level of the gene, rather than at a more fine-grained level of the specific mutation.

As {ref}`previously mentioned<genes-first-mentioned>`, we define genes are the stretches of DNA which can be transcribed into RNA.
However, the seemingly simple definition hides a lot of complexities: due to their long history, the word "gene" has had different uses and meanings.

(genes-are-complex)=
##### The complexities of genes
[//]: # (TODO: Cite how much human DNA is genes in bp?)
[//]: # (TODO: Cite the selfish gene)
[//]: # (TODO: Explain/link to alternative splicing)
[//]: # (TODO: Mention overlapping genes)

The word gene is often used as shorthand for "DNA that causes phenotypic differences" (for example in Richard Dawkin's best-seller "The Selfish Gene", and in news articles with titles of the form "Scientists have discovered a gene for...").
However, there are multiple reasons why this is an incomplete and outdated understanding.
Firstly, genes are not guaranteed to cause phenotypic differences.
More importantly, nor are genes the only sections of DNA which can influence phenotype. 
Thirdly, there is not a one-to-one mapping from genes-to-proteins: one gene could be read to create multiple different proteins (due to {ref}`alternate splicing<alternative-splicing>`), and sometimes only one of those proteins might cause a phenotypic difference.

[//]: # (TODO: Cite not always genes whole inherited)
[//]: # (TODO: Rephrase chromosomal crossover so that I don't say that?)
Genes are also often touted as a “unit of heritability/heredity”, but this is similarly not always the case. 
DNA is more likely to be inherited together if it is close together on the chromosome,so generally we inherit whole copies of genes (and the regions around them) together - in fact usually we often inherit stretches of multiple genes together.
It is possible however, for chromosomal crossover to occur within a gene (i.e. for genes not to be inherited "in one piece" with one whole copy from each parent).

[//]: # (TODO: Move this paragraph to compbio-background)
There can be disagreements about the locations of genes on the genome, and popular databases of genes fundamentally disagree on this and on the number of genes{cite}`Salzberg2018-yc`. 
Gene names and symbols change over time, and can be difficult to map between for this reason. 

(genes-enhancers-promoters)=
#### Gene regulation
[//]: # (TODO: Draw Genes, alternate transcripts, enhancers, promoters)
[//]: # (TODO: Write)
[//]: # (TODO: Explain in Ch3 that regulatory features are not as well defined yet, i.e. with IDs, etc.)

Other nearby stretches of DNA are also of interest in relation to genes: enhancers, silencers, insulators, and promoters. These are stretches of DNA that proteins can bind to 

Even where DNA can be expressed as proteins, the level of expression depends on the cell environment and other DNA.

(single-nucleotides)=
##### SNPs and SNVs
[//]: # (TODO: Put in how much of genome is covered by SNPs?)
[//]: # (TODO: Image for SNPs)

A SNP is a location on an organism’s genome where there are differences of a single nucleotide (“A”,”C”,”T”,”G”) between individuals. In some fields, these variations are only considered to be Single Nucleotide *Polymorphisms* if they are relatively commonly occurring in the population (at least 1%), while Single Nucleotide Variants (SNVs) can include both rare and common variants. 

Variation at a location does not imply a disease-causing effect, many SNPs appear to be neutral. Much of the time, the aim of studying such variants is to determine which are which. This is often done through looking at their rarity, either in a specific human population (e.g. people with diabetes), the entire human population, or across the tree of life. 

[//]: # (TODO: Chr1: ??)
SNPs are defined by their location on a human reference genome, for example Chr1: . An individual allele for a given SNP is defined as “wild” type if it matches the reference genome and “mutant” if it does not. The reference genome does not always have the most common allele at each location, although this is it’s aim, so “wild” and “mutant” do not necessarily imply anything about rarity. 

If there are only two nucleotide possibilities for a SNP (e.g. A or C), then it is called bi-allelic; the vast majority of SNPs are of this type. Multi-allelic SNPs (e.g. A, T or C) are much rarer. 

Since (except for X/Y chromosomes) humans have two copies of each chromosome, an individual will have two alleles for each SNP. These may match (which we call homozygous) or not (heterozygous). Sometimes a disease-causing allele can cause problems even for heterozygotes, while in other cases a person needs two copies of the disease-causing allele in order for it to have an effect.

SNPs can occur either in coding or non-coding regions of the genome. 
In non-coding regions, SNPs can still affect gene expression, for example by altering a promoter site. 
SNVs in coding regions have two types: synonymous or non-synonymous, based on whether they alter the amino acid sequence.

###### Non-synonymous SNVs
If a SNP alters the amino acid makeup of a protein, it is known as non-synonymous. 
Non-synonymous SNVs can cause either nonsense or missense mutations. 

Nonsense mutations occur where the SNP substitution results in a stop codon (e.g. TAG) in an unusual position, which signals for a ribosome to stop translating RNA into a protein. 
This results in an incomplete and usually nonfunctional protein. 
The effect of a nonsense mutation would be more or less severe depending on the location of the new stop codon. 
For example, if it was close to the end of the protein, the protein may still be functional. 
Sufficiently incomplete proteins are usually destroyed by the cell. 

[//]: # (TODO: Is this true? About location of stop codon. If so, I want the link!)

On the other hand, missense mutations occur where the SNP substitution results in an amino acid substitution in the protein. 
Some amino acids can be substituted without causing any difference to the function of the protein, while others can severely impede the protein.

###### Synonymous SNVs
Synonymous SNVs occur where substituting the usual nucleotide with another results in the same amino acid. 
The resulting protein will have the exact same functionality. 
However, synonymous SNVs could still have an effect on high-level traits, since different nucleotides are translated at different speeds. 

[//]: # (TODO: Add a section about linkage disequalibrium/a mention of it ONLY if I have included it in Snowflake/Filter: From original:  Two alleles at given locations on the genome are in linkage disequilibrium when the association between them is more than would be expected at random. Linkage disequilibrium may occur between alleles even when there is no genetic linkage present, for example as a result of the presence of both alleles being selected for in a population.)

(other-variation)=
### Genetic variation
[//]: # (TODO: Move/rewrite.)

As you are no doubt aware, individuals of the same species share the vast majority of their DNA. 
Genetic variation is the difference in DNA sequence between individuals in a population, and variants are locations on an organisms genome where we observe variation between individuals. 
There are different types of genetic variation, for example indels (insertions and deletions)- where small sections of DNA are inserted or deleted from the genome - and copy number variations (CNVs) where larger stretches of the genome are repeated. 
However, the most well-studied and common type of genetic variation between humans are single nucleotide polymorphisms (SNPs, pronounced “snips”).

The different forms that a variant can take in the population are called alleles, depending on the type of variant. 
Alleles could be different forms of a whole gene, or as small in length as an individual nucleotide.


---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```