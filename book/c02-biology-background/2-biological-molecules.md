(biological.molecules)=
## Biological molecules: DNA, RNA, Proteins and the central dogma of molecular biology.
Here I explain the classes of biological molecules that are vital in our understanding of genetics: the nucleic acids, DNA and RNA, and their product - proteins.

(what-is-dna)=
### DNA

[//]: # (TODO: Sort out figure labelling. Use TOC to go through in order and replace for the site and PDF)
[//]: # (TODO: Cite Watson + Crick again) 

```{figure} ../images/dna_metalmodel.jpg
---
height: 220px
name: dna-metal-model
---
A photo of the original six-foot tall metal model of DNA made by Watson and Crick in 1953. Image from the Cold Spring Harbor Archives{cite}`noauthor_undated-ih`.
``` ``

[//]: # (TODO: delete backticks)

Most people recognise the double helix of deoxyribonucleic acid (DNA) shown in {numref}`dna-metal-model`, it’s a twisted ladder consisting of four nucleotides; adenine, cytosine, thymine, and guanine (A, C, T, G). 
It the “code of life” that contains the instructions for making all of the things which make up our bodies and the obvious starting point for understanding how they work. 
A given nucleotide on one strand is always linked to its partner on the other strand - A with T, and G with C - which creates redundancy and a convenient copying mechanism.
Lengths of DNA are measured in these base pairs (bp). 

[//]: # (TODO: Explain chromosomes and mitochondria v. briefly.)

(central-dogma)=
#### How DNA affects us: the central dogma of molecular biology
The way in which DNA affects the body can be understood through the *central dogma of molecular biology*, and in doing so we will also become acquainted with two more important biological molecules: RNA and proteins.

The central dogma of molecular biology can be paraphrased as **"DNA makes RNA makes proteins"**. The idea is that as the “code of life”, DNA contains the instructions for making RNA, which contains the instructions for making proteins, and proteins are the molecules which constitute and make up {ref}`almost everything<almost-everything>` in our bodies. 

(almost-everything)= 
```{margin} *Almost* everything
Proteins make up a lot of molecular machinery in the body as well as structures, however there are other actors, too. There are functional RNA molecules, and fats (which may or may not be synthesised using proteins) can also make up structural parts of the body (for example in cell membranes).
``` 

The central dogma describes the process of gene expression. Gene expression has two parts: transcription (“DNA makes RNA”) and translation (“RNA makes proteins”).

(what-is-rna)=
### RNA
RNA was originally discovered alongside DNA as a nucleic acid (acidic substances found in the nucleus of cells). It was later discovered that they are also found in bacterial and archeal cells (which don't have nuclei). 

#### "DNA makes RNA", a.k.a, transcription

[//]: # (TODO: Cite DNA makes RNA makes proteins.)


The process by which "DNA makes RNA" is known as transcription. The process happens to lengths of DNA at a time. These lengths of DNA are called genes, and they may be various sizes, and be transcribed more or less frequently than one another. 

The action of transcription is largely carried out by an enzyme called RNA polymerase, which binds to a promoter region of the DNA, close to but outside the gene. This region is only accessible in certain cellular conditions. A rough model is that in conditions in which it is unfavourable for the gene to be transcribed, other molecules will block the promoter. 

The RNA polymerase then splits the DNA and adds complementary RNA nucleotides to the DNA, after which the RNA sugar backbone is formed. The RNA-DNA helix is then split, at which point we have what is known as pre-RNA. The pre-RNA is then processed into mature RNA (known as the transcript), ready to be translated into a protein. 

The process of what is transcribed and how quickly is affected by many different kinds of proteins (as well as other molecules, e.g. histone modifications). Transcription factors are of particular note, which are proteins that bind to DNA close to or in the promoter region, and either activate the gene (increasing it’s rate of transcription), by for example recruiting RNA polymerase, or repress it (decrease it’s rate of transcription). These transcription factors are in turn regulated by other transcription factors, which creates a network of gene regulation; a gene regulatory network (GRN).

(what-are-proteins)=
### Proteins

Proteins were named by Dutch chemist Gerardus Mulder in his 1839 paper{cite}`Mulder1839-rf`, where he found that all proteins from animals and plants have more or less the same elemental makeup -  approximately C<sub>400</sub>H<sub>620</sub>N<sub>100</sub>O<sub>120</sub>. 
This intriguing result bolstered research in this area, eventually resulting in our current understanding of proteins as biological macromolecules composed of amino acids.

In 1969, Margaret Dayhoff created the first bioinformatics database to store protein structures imaged using X-ray crystallography, related to her publication of Atlas of Protein Sequence and Structure{cite}`Hersh1967-ox`. 
Soon after, in 1972, the Protein DataBank (PDB){cite}`noauthor_undated-ow` was established. 
This continues to be well-used and updated, at the time of writing holding structures of 148,827 biological molecules. 

#### "RNA makes Proteins", a.k.a. Translation
The second part of the central dogma is "RNA makes proteins" a.k.a. translation.

Translation is process by which RNA is read to create proteins. First the RNA is converted into a string of amino acids, and then the string of amino acids automatically folds into its’ usual three dimensional structure. The protein folding aspect is not part of translation.


```{figure} ../images/amino_acid_chart.png
---
height: 270px
name: amino-acid-wheel
alt: The figure shows an amino acid chart. It consists of three concentric circles. At the centre is a circle divided into 4 quadrants, labelled for each nucleotide (U, C, A and G). In the second circle, the arcs of the inner quadrants are again divided into 4 (again labelled U, C, A, and G), so that these letters appear 16 times in the middle circle. On the outer circle, each letter from the middle circle is divided into 4 a final time. And these are labelled with the amino acids that they map to, e.g. "Val", "Arg", "Leu"
---
An amino acid wheel chart (from sigmaaldrich.com{cite}`noauthor_undated-ic`) showing the mapping between nucleotide codons and amino acids. The chart is read from the inside out, so for example, UGA is a stop codon, and UUG encodes for leucine ("Leu").
``` ``

[//]: # (TODO: Delete extra backticks)

This process is mostly carried out by a large and complex piece of molecular machinery called the ribosome. The ribosome reads and processes RNA in sets of three nucleotides at a time - these are called codons. Each codon is either a flag to the ribosome (e.g “stop here”, “start here”) or corresponds to an amino acid. Although we would expect $4^3=64$ permutations of nucleotides, there are only 21 different amino acids which can be incorporated into proteins in humans, so there is redundancy: multiple codons can encode for the same amino acids. We can see this clearly in {numref}`amino-acid-wheel`, for example, UAA, UGA, and UAG are all read as stop codons.

#### The protein folding problem
As mentioned above, translated strings of amino acids fold automatically (or sometimes with the help of *chaperone* proteins) into the 3D structure of proteins. It’s the structure of proteins which define their function since their shape effects what they can bind to. Predicting what the structure of a protein will be from the string of amino acids is known as the protein folding problem. It’s has been one of the grandest challenges in biology for over half a century. If it were solved, it would revolutionise protein function and phenotype prediction. 

[//]: # (TODO: Mention google deep mind?)

#### Post-translational modifications
After translation, many proteins can be modified by the addition of various functional groups (parts of molecules which are responsible for chemical properties), e.g. phosphorous or ubiquitin. Such modifications change the functionality of the proteins, and are also believed to aid in protein folding.

### "...and proteins do everything."
The unwritten addendum implied by “DNA makes RNA makes proteins” is “...and proteins do ({ref}`almost<almost-everything>`) everything”. If DNA encodes for life, then proteins are what make up life. They are the material building blocks of our bodies, and they also have a vast number of other functions: they can be enzymes catalysing reactions, hormones controlling metabolism, transporters for other proteins, signalling proteins, they might be transcription factors (controlling the expression of genes), or have many other functions.

In turn, these processes influence our phenotypes. A phenotype can be something like the level of a certain hormone in the bloodstream, so in a very simple case, a  could effect the phenotype by it's difference in the speed of expression. A phenotype could alternatively be something like height, which could have a number of genetic (and non-genetic) influences.

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```