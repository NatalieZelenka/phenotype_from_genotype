(biological.molecules)=
# Biological molecules: DNA, RNA, Proteins and the central dogma of molecular biology.
Here I introduce the classes of biological molecules that are vital in our understanding of genetics: the nucleic acids (DNA and RNA), and their product: proteins.

(what-is-dna)=
## DNA

```{figure} ../images/dna-both.png
---
height: 220px
name: dna-both
---
Left: A photo of the original six-foot tall metal model of DNA made by Watson and Crick in 1953, alongside their discovery{cite}`Watson1953-np`. Image from the Cold Spring Harbor Archives{cite}`noauthor_undated-ih`.
Right: A cartoon representation of DNA, showing the concept of the complementary strand.
```

Most people recognise the double helix of deoxyribonucleic acid (DNA) shown in {numref}`dna-both`, it’s a twisted ladder consisting of four nucleotides; adenine, cytosine, thymine, and guanine (A, C, T, G). 
It the “code of life” that contains the instructions for making (almost) all of the things which make up our bodies and therefore, an obvious starting point for understanding how they work. 
A given nucleotide on one strand is always linked to its partner on the other strand - A with T, and G with C - which creates redundancy and a convenient copying mechanism.
Lengths of DNA are measured in these base pairs (bp). 

Human DNA is organised into chromosomes, we have two copies of each of our 23 nuclear chromosomes within (almost) every cell, as well as a varying number of copies of our mitochondrial chromosome in the cells which have mitochondria. 

(central-dogma)=
### How DNA affects us: the central dogma of molecular biology
The way in which DNA affects the body can be understood through the *central dogma of molecular biology*, and in doing so we will also become acquainted with two more important biological molecules: RNA and proteins.

The central dogma of molecular biology can be paraphrased as "DNA makes RNA makes proteins". The idea is that as the “code of life”, DNA contains the instructions for making RNA, which contains the instructions for making proteins, and proteins are the molecules which constitute and make up {ref}`almost everything<almost-everything>` in our bodies. 

(almost-everything)= 
```{margin} *Almost* everything
Proteins make up a lot of molecular machinery in the body as well as structures, however there are other actors, too, for example, functional RNA molecules (some of which are explained further down this page). Fats (which may or may not be synthesised using proteins) can also make up structural parts of the body such as cell membranes.
``` 

(gene-expression)=
The central dogma describes the process of gene expression.
Gene exp ression has two parts: transcription (“DNA makes RNA”) and translation (“RNA makes proteins”).

### "DNA makes RNA", a.k.a, transcription

(what-is-rna)=
RNA (or ribonucleic acid) was originally discovered alongside DNA as a nucleic acid, an acidic substance found in the nucleus of cells. It was later discovered that they are also found in bacterial and archeal cells (which don't have nuclei). 
In contrast to DNA, RNA is a single-stranded molecule, with the bases A, C, G and U (i.e. uracil instead of thymine), and with a different backbone (containing ribose, rather than dioxyribose).
There are different forms of RNA which perform different functions. It is messenger RNA (mRNA) that is the intermediate product between DNA and Proteins. 

```{figure} ../images/transcription.png
---
height: 220px
name: transcription
---
An illustration of the transcription and splicing processes, showing the role of RNA polymerase in building RNA.
``` 

(genes-first-mentioned)=
The process by which "DNA makes RNA" is known as transcription. The process happens to certain lengths of DNA, and these lengths of DNA are which {ref}`are called<complicated-genes-margin>` *genes*. In humans, genes vary in length from hundreds to millions of base pairs. 

(complicated-genes-margin)=
```{margin} Definining "genes"
Genes are not a straightforward unit, as I describe in a bit more detail {ref}`later<genes-are-complex>`.  
Some sources use "gene" only to describe genes which encode for proteins, but I include genes which encode for RNA.

```

The action of transcription is largely carried out by an enzyme called *RNA polymerase*, which binds to a promoter region of the DNA, close to but outside the gene. 
This region is only accessible in certain cellular conditions. A rough model is that in conditions in which it is unfavourable for the gene to be transcribed, other molecules will block the promoter. 

{numref}`transcription` illustrates the next part of this process. The RNA polymerase splits the DNA and adds complementary RNA nucleotides to the DNA, after which the RNA sugar backbone is formed. 
The RNA-DNA helix is then split, at which point we have what is known as precursor RNA or pre-RNA. 

After transcription, the pre-RNA then undergoes *post-transcriptional modifications* such as *splicing*, where parts of the RNA (*introns*) are removed, leaving only *exons*. 
This can also bee seen in {numref}`transcription`.
Splicing is part of the final processing step to create the finished product: a mature RNA transcript.

(alternative-splicing)=
During this step a gene could be transcribed into one of multiple transcripts, via a process known as *alternative splicing*.
This can happen, for example, by skipping some of the exons during splicing. 
So, "DNA makes RNA(*s*)".
This means that there's not a one-to-one relationship between genes and transcripts, and therefore between genes and proteins.

[//]: # (TODO: aside histone modifications/epigenetics)
What is transcribed and how quickly is affected by many different kinds of proteins, as well as other molecules, for example histone modifications. 
Transcription factors are of particular note, which are proteins that bind to DNA close to or in the promoter region, and either *activate* the gene (increasing it’s rate of transcription), by for example recruiting RNA polymerase, or *repress* it (decrease it’s rate of transcription).
These transcription factors are in turn regulated by other transcription factors, which creates a network of gene regulation; a gene regulatory network (GRN).

### "RNA makes Proteins", a.k.a. Translation
The second part of the central dogma is "RNA makes proteins" a.k.a. translation.

(what-are-proteins)=
Proteins have been investigated independently from DNA and RNA. 
They were named by Dutch chemist Gerardus Mulder in his 1839 paper{cite}`Mulder1839-rf`, where he found that all proteins from animals and plants have more or less the same elemental makeup -  approximately C<sub>400</sub>H<sub>620</sub>N<sub>100</sub>O<sub>120</sub>. 
This intriguing result bolstered research in this area, eventually resulting in our current understanding of proteins as biological macromolecules composed of amino acids. 

(what-is-translation)=
Translation describes the process in which a string of amino acids is created based on the RNA sequence.
Proteins are made of these amino acid strings (called *polypeptides*), and after translation, they will fold (potentially with the assistence of *chaperone* proteins) into the proteins usual globular three dimensional conformation. 

```{figure} ../images/amino_acid_ribosome.png
---
height: 220px
name: translation
alt: The lefthand figure shows an amino acid chart. It consists of three concentric circles. At the centre is a circle divided into 4 quadrants, labelled for each nucleotide (U, C, A and G). In the second circle, the arcs of the inner quadrants are again divided into 4 (again labelled U, C, A, and G), so that these letters appear 16 times in the middle circle. On the outer circle, each letter from the middle circle is divided into 4 a final time. And these are labelled with the amino acids that they map to, e.g. "Val", "Arg", "Leu".

---
Left: An amino acid wheel chart showing the mapping between nucleotide codons of RNA and amino acids. The chart is read from the inside out, for example UGA is a stop codon and UUG encodes for leucine "Leu").
Right: An illustration of the translation process, showing tRNAs delivering amino acids to the ribosome in order to build the polypeptide chain which makes up proteins.
``` ```

Translation is mostly carried out by a large and complex piece of molecular machinery called the ribosome, which is made up of proteins and ribosomal RNA (rRNA). 
The ribosome reads and processes RNA in sets of three nucleotides at a time - these are called codons. 
Each codon is either a flag to the ribosome (e.g “stop here”, “start here”) or corresponds to an amino acid. 
Transfer RNA (tRNA) transports the amino acids to the ribosome where the polypeptide chain of amino acids is created.

Although we would expect $4^3=64$ permutations of nucleotides, there are only 21 different amino acids which can be incorporated into proteins in humans, so there is redundancy: multiple codons can encode for the same amino acids. 
We can see this clearly in the left part of {numref}`translation`, for example, UAA, UGA, and UAG are all read as stop codons.

(post-translational-modifications)=
**Post-translational modifications:** 
Post translational modifications are changes to proteins which occur after translation, but they may happen before or after folding{cite}`Uversky2013-bt`.
These changes consist of chemicals bonding to the protein, which can change its function or structure, assist in folding, or target them for degradation, for example.

### "... and proteins do everything."
The unwritten addendum implied by “DNA makes RNA makes proteins” is “...and proteins do ({ref}`almost<almost-everything>`) everything”. 
If DNA encodes for life, then proteins are what make up life. 
They are the material building blocks of our bodies, and they also have a vast number of other functions: they can be enzymes catalysing reactions, hormones controlling metabolism, transporters for other proteins, signalling proteins, they might be transcription factors (controlling the expression of genes), or have many other functions.

In turn, these processes influence our phenotypes. 
A phenotype can be something like the level of a certain hormone in the bloodstream, so in a very simple case, a  could effect the phenotype by it's difference in the speed of expression.
A phenotype could alternatively be something like height, which could have a number of genetic (and non-genetic) influences.
