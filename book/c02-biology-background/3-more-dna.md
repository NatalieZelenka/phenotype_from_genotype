(dna-organised)=
# A closer look at DNA: Genomes, Genes, and Genetic Variation
Now that we have a basic overview of how DNA can influence phenotype, we can discuss the way that DNA is organised and categorised in a little more detail. We'll look from big ({ref}`genomes<genomes>`) to small ({ref}`single nucleotides<single-nucleotides>`).

(genomes)=
## Genomes
The genome is the full amount of DNA belonging to an organism. We can talk about the genome of an individual, or about the genome of an organism (e.g. the human genome).
When we talk about an organism's genome, we are actually talking about an example genome for that organism: the organisms' *reference* genome. 
The reference genome does not belong to any individual organism, but instead is supposed to have the most common nucleotide at each DNA location. 

Reference genomes allow us to make general statements about an organism (e.g. "the human genome is 3 billion base pairs long"), and also to make comparisons between organisms (e.g. {ref}`"humans share 1% of their DNA with a banana"<human-banana-dna>`). 
We also discuss individuals' genomes in relation to the difference between the individual and the reference genome.

(human-banana-dna)= 
```{margin} Humans and bananas
Humans share 50% of their *protein-coding* dna with bananas, but only 1% of their genome.
``` 

(exome-proteome)=
## The exome and the proteome
Still thinking big, we have the *exome* and the *proteome*. 
Both of these refer to locations across the whole genome, but missing stretches in between.
The exome describes the set of all exons (protein-coding nucleotides) across the genome. 
The proteome is generally used to mean the set of all proteins in an organism (which can be much larger than the set of genes due to {ref}`alternate splicing<alternative-splicing>`), but it can also be used to describe the part of the genome relating to the set of protein sequences.

(omics)=
```{margin} Omics
As well as genomics (the science of genomes) and proteomics (proteins), there is also transcriptomics (transcripts),  metabolomics (metabolites, e.g. sugars, lipids, etc). 
Together these research areas are known as *omics* and research which combines these fields is known as multi-omics.
```

(what-are-genes)=
## Genes
DNA is often considered at the level of the gene.
Genes have been so central to the historical study of DNA (hence the name *gene*tics), and the gene-centric view of molecular biology continues to this day.
For example, many researchers have favourite genes, which they primarily study, and understand the mechanisms of in detail. 
And for this reason, diseases and phenotypes are often attributed at the level of the gene, rather than at a more fine-grained level of the specific mutation.

(genes-are-complex)=
As {ref}`previously mentioned<genes-first-mentioned>`, in this thesis, I use genes to mean a stretches of DNA which can be transcribed into RNA (i.e. I include "RNA genes" in my definition).
However, the seemingly simple definition hides a lot of complexities: due to their long history, the word "gene" has had different uses and meanings.

<!--
[//]: # (TODO: Cite how much human DNA is genes in bp?)
[//]: # (TODO: Cite the selfish gene)
[//]: # (TODO: Cite overlapping genes)
-->

(gene-for-x)=
### "A gene for X"
The word gene is often used as shorthand for "DNA that causes phenotypic differences" (for example in Richard Dawkin's best-seller "The Selfish Gene", and in news articles with titles of the form "Scientists have discovered a gene for...").
However, there are multiple reasons why this is an incomplete and in some ways outdated understanding. 
Single gene diseases do exist, however most of the time {ref}`the same gene can make multiple different final proteins (isoforms)<alternative-splicing>`) which may not all cause phenotypic differences, the same protein can be involved in multiple different pathways and have multiple functions, and multiple proteins can contribute to one function. 
Genes are also not guaranteed to cause phenotypic differences, and are not the only sections/types of DNA which can influence phenotype. 
Another complication is that genes can overlap, meaning that a single nucleotide mutation could impact on multiple genes.
And finally, sometimes entirely different genes can create identical proteins after translation.

The interaction between DNA, RNA and proteins, and the environment is also important to consider. 
Although DNA makes RNA makes proteins and proteins do pretty much everything in our bodies, which proteins are made and how they behave is highly dependent on the environment. 
The function of a gene might not be evident in some environments because the protein is never transcribed, or it may behave differently. 
Many traits may be mostly environmental.

<!--[//]: # (TODO: Cite not always genes whole inherited)-->

(units-heritability)=
### Units of heritability
Genes are also often touted as a “unit of heritability/heredity”, but this is similarly not always the case. 
DNA is more likely to be inherited together if it is close together on the chromosome, so generally we inherit whole copies of genes (and the regions around them) together - in fact usually we often inherit stretches of multiple genes together.
Despite this, it is also possible that genes are not inherited "in one piece" with one whole copy from each parent. 

(not-genes)=
## Things that are not genes
There are many related concepts that contain the word gene simply because they are stretches of DNA, but that do not fit our definition. 
For example {ref}`"jumping genes"<transposable-elements>` and {ref}`pseudogenes<psuedogenes>` are both important parts of the human genome, which may effect phenotype, but not via proteins.

```{margin} Transposable Elements
:name: transposable-elements
Transposable elements a.k.a. transposons or "jumping genes" are sections of DNA that move from one section of the genome to another. Their similarity with genes only extends as far as the fact that they are stretches of DNA. Despite making up 50% of the human genome, they only rarely overlap with protein-coding genes{cite}`Gotea2006-ll`. The vast majority of human transposons are *silent*, i.e. are incapable or prevented from moving.
```

```{margin} Pseudogenes
:name: psuedogenes
Pseduogenes are segments of DNA that look like genes (have high homology to known genes), but are missing some functionality such that they do not encode proteins. Some pseudogenes cannot be transcribed (e.g. due to missing regulatory regions), and some are transcribed, but not translated (e.g. due to a premature stop codon). 
Although they were originally characterised as non-functional, they have been found to have biological roles, for example through being transcribed into functional RNAs{cite}`Cheetham2020-jc`.
```

(genes-enhancers-promoters)=
In addition, there are also stretches of DNA that are of interest in relation to genes: enhancers, silencers, insulators, and promoters. 
These are stretches of DNA that control the regulation of specific gene's transcription.
Mutations in these stretches of DNA are often understood in relation to the genes that they regulate.

(other-variation)=
## Indels and Copy Number Variations
Smaller lengths of DNA are mostly of interest as *variants* where there are differences at those locations between individuals. 
These differences include insertions and deletions (*indels*) where sections of DNA, ranging from 1 to 10,000 base pairs, are inserted or deleted from the genome, and *copy number variations* where (generally larger) stretches of the genome are repeated. 
However, the most well-studied and common type of genetic variation between humans are single nucleotide polymorphisms (SNPs, pronounced “snips”).

(single-nucleotides)=
## Single Nucleotide Polymorphisms
<!--
[//]: # (TODO: Put in how much of genome is covered by SNPs?)
[//]: # (TODO: Draw image for SNPs)
-->

A SNP is a location on an organism’s genome where there are differences of a single nucleotide (A, C, T, G) between individuals. 
In some fields, these variations are only considered to be Single Nucleotide *Polymorphisms* if they are relatively commonly occurring in the population (at least 1%), while Single Nucleotide Variants (SNVs) can include both rare and common variants. 

Variation at a location does not imply a disease-causing effect, many SNPs appear to be neutral. 
Much of the time, the aim of studying such variants is to determine which are which.
This is often done through looking at their rarity, either in a specific human population (e.g. people with diabetes), the entire human population, or across the tree of life. 

```{margin} Alleles
:name: define-allele
The different forms that a variant can take in the population are called alleles. 
Alleles can be as big as different forms of a whole gene, or as small in length as an individual nucleotide.
```

SNPs are defined by their location on a human reference genome, for example "chromosome 5, position 7870860" (often written `5:7870860`). 
An individual {ref}`allele<define-allele>` for a given SNP is defined as “wild” type if it matches the reference genome and “mutant” if it does not. 
The reference genome does not always have the most common allele at each location, although this is it’s aim, so “wild” and “mutant” do not necessarily imply anything about rarity. 

If there are only two nucleotide possibilities for a SNP (e.g. it could be A or C at a given position), then it is called bi-allelic; the vast majority of SNPs are of this type. 
Multi-allelic SNPs such as tri-allelic SNPs (three choices, e.g. it could be A, T or C) are much rarer. 

Since humans mostly have two copies of each chromosome (except for X/Y chromosomes in genetically male people, and people with chromosomal anomalies), an individual will usually have two alleles for each SNP. 
These may match (which we call homozygous) or not (heterozygous). 
Sometimes a disease-causing allele can cause problems even for heterozygotes, while in other cases a person needs two copies of the disease-causing allele in order for it to have an effect.

SNPs can occur either in coding or non-coding regions of the genome. 
In non-coding regions, SNPs can still affect gene expression, for example by altering a regulatory site. 
SNPs in coding regions have two types: synonymous or non-synonymous, based on whether they alter the amino acid sequence.

(non-synonymous)=
### Non-synonymous SNVs
If a SNP alters the amino acid makeup of a protein, it is known as non-synonymous. 
Non-synonymous SNVs can cause either nonsense or missense mutations. 

Nonsense mutations occur where the SNP substitution results in a stop codon (e.g. TAG) in an unusual position, which signals for a ribosome to stop translating RNA into a protein. 
This results in an incomplete and usually nonfunctional protein. 
The effect of a nonsense mutation would be more or less severe depending on the location of the new stop codon. 
For example, if it was close to the end of the protein, the protein may still be functional. 
Sufficiently incomplete proteins are usually destroyed by the cell. 

(missense)=
On the other hand, missense mutations occur where the SNP substitution results in an amino acid substitution in the protein. 
Some amino acids can be substituted without causing any difference to the function of the protein, while others can severely impede the protein.

(synonymous)=
### Synonymous SNVs
Synonymous SNVs occur where substituting the usual nucleotide with another results in the same amino acid. 
The resulting protein will have the exact same functionality. 
However, synonymous SNVs could still have an effect on high-level traits, since different nucleotides are translated at different speeds.
This difference in translation speed has been shown to impact on both folding and abundance of proteins{cite}`kimchi2007silent`. 

<!--
[//]: # (TODO: Add a section about linkage disequalibrium/a mention of it ONLY if I have included it in Snowflake/Filter: From original:  Two alleles at given locations on the genome are in linkage disequilibrium when the association between them is more than would be expected at random. Linkage disequilibrium may occur between alleles even when there is no genetic linkage present, for example as a result of the presence of both alleles being selected for in a population.)
-->
