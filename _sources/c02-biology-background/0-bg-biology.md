(c02-biology-bg)=
## Biology Background

I have three aims in this background Chapter: 
1. to anchor the work that I've done within the context of the big questions for computational biology.
1. to provide information about the provenance of data that computational biologists use, in order to aid in discussions about the limitations of the data in later chapters<!--TODO: which ones-->.
1. to provide a basic run-down of molecular biology, in order to allow someone without a biology background to understand the rest of this thesis. 

The biological background presented in this section begins at the very basics of molecular biology. This includes details of what biological molecules (e.g. {ref}`DNA<what-is-dna>`, {ref}`RNA<what-is-rna>` and {ref}`proteins<what-are-proteins>`) are, what they are made of, and how current research suggests that they effect the body. These details reveal the complexity of the entities and concepts that computational biologists are interested in. The additional complexities that arise from how we store data about these entities and use it in downstream analyses, is discussed in the {ref}`next Chapter<c03-compbio-bg>`. 

[//]: # (TODO: Update info on later Chapters below)
[//]: # (TODO: Check order and relevance of each part of this to later sections)
[//]: # (TODO: Consider limiting the number of subsections and just using bolded headings or perhaps dictionary/glossary style entries for more fine-grained bits)

(big.questions)=
### Big questions: What is genetically determined, and how?

As humans, we are curious and want to understand ourselves. 
We want to know the answers to questions like: "Why are people the way we are?", "Which aspects of ourselves have we inherited?", and "What is fixed and what can be changed by the way we live our lives?"
 
We also seek to improve and control our lives and environment.
This drive for control hasn't always been a good thing: in recent history, genetics has been used to justify extremely harmful and unethical racist eugenics policies.
While eugenics is thankfully no longer in vogue, there is no guarantee that scientific knowledge will be used ethically.
However, knowing more about ourselves clearly also has the capacity to be used for the good of all.
By understanding how our bodies work, researchers seek to develop new, more effective, and kinder treatments for diseases.

#### History of inheritable traits

Humanity has been trying to answer the big questions long before we discovered DNA. 
The ancient theory of soft inheritance{cite}`Zirkle1935-sb` said that people can pass on traits they gained during their lives, while 16th-century alchemists theorised that sperm contains tiny fully formed humans{cite}`Grafton_undated-af` (i.e. women didn't pass down anything). 

[//]: # (TODO: Gregor Mendel pea image)
[//]: # (TODO: Cite Mendel)


Gregor Mendel's famous pea experiments provided the earliest scientific basis for genetics through his experiments with independently inherited traits of peas (e.g. purple or white flowers, tall or shot plants, wrinkled or round seeds...). 
Importantly, he discovered rules of inheritance that indicated that offspring have combinations of discrete genetic material (rather than a blend).
He also showed that one trait that we can measure (e.g. purple flowers) can actually be caused by a number of different genetic combinations.

[//]: # (TODO: Cite Wilhelm Johannsen seed size work)

This concept was expanded by Wilhelm Johannsen, who coined the term "gene" as the name for this genetic material. 
Johnannsen's work also distinguished between "genotype" and "phenotype": *genotype* being is the genetic material organisms have, and *phenotype* being the measurable trait. 
His research showed that some phenotypes (e.g. seed size) could vary considerably even with genetically identical plants, due to their environment.

[//]: # (TODO: Cite Watson + Crick) 
[//]: # (TODO: Cite Human Genome Project)
[//]: # (TODO: Cite Watson racism)
[//]: # (TODO: Link aside watson racism: - with asterix?)
[//]: # (TODO: Cite IQ criticisms)
[//]: # (TODO: Cite hopes Human Genome Project)

Phenotypes are not only strictly Mendelian, with a fixed number of "types", or continuous and without a genetic basis. 
{ref}`Ronald Fischer<fischer-racism>` showed that variation in continuous traits (such as height in humans) can be consistent with Mendelian inheritance if multiple genes contributed additively to the trait.
Many traits are *complex* in this way, meaning that they are influenced by many different genetic factors, as well as the environment.

[//]: # (TODO: Cite Fischer racism)

(fischer-racism)=
```{margin} Ronald Fischer, racism and eugenics
Fischer has a legacy of scientific racism. For example, actively campaigning for the forced sterilisation of a tenth of the population in the name of eugenics.
```

When {ref}`Watson<watson-racism>` and Crick discovered the now familiar structure of DNA in 1953, we took a huge step towards being able to answer our big questions. 
We finally understood the molecular structure that underlies inherent traits. 
Then in 2003, with the completion of the Human Genome Project, it was possible to read the human version of this “code of life”.
Once researchers had access to the whole genetic code for a person, they could set about trying to decode it, hoping to discover the key to treating diseases like cancers and Alzheimer's. 

(watson-racism)=
```{margin} James Watson and racism
Watson's has publicly asserted that he believes differences in average measured IQ between blacks and whites are due to genetic differences.
```

We now have thousands of human genomes to investigate, and the promises of gene therapies and personalised medicine are now beginning to become reality. 
At the time of writing, there are 11 cell and gene therapies approved by the European Medicines Agency{cite}`Cynober2020-rx`, which treat a variety of cancers, as well as Crohn's disease, and eye and cartilage problems. 
In addition, the first personalised genomic medicine chemotherapy treatment is now available on the NHS, for cancer patients with the allele of the [DYPD](https://www.genecards.org/cgi-bin/carddisp.pl?gene=DPYD) gene that cause slower breakdown of chemotherapy toxins{cite}`Guardian_staff_reporter2020-lb`.

[//]: # (TODO: Timeline genetic history illustration)

#### The future

The eventual destination of this field is a full understanding of how our individual genomes and their interaction with the environment affects us. 
With this understanding, we would anticipate a much wider application of both personalised medicine and gene therapies.

[//]: # (TODO: Cite genes % of DNA)

These therapies are not yet a common occurrence: the 11 approved cell and gene therapies come from a pool of such 500 clinical trials{cite}`Cynober2020-rx`.
Perhaps it makes sense that we are not finding drug targets quickly, as we still don't know the functionality of approximately 20% of human genes.
And genes are only a small part (1.2%) of our DNA, and the part we understand best.
Beyond our DNA, there are many other aspects of our cellular and social environments that will effect which parts of our genes are being actively used, and how much.
This section provides an overview of our scientific current model for how DNA effects phenotype, so that we can identify the sources of information that we do have and can make use of.

Despite what we don't know, this is also the moment where when we have the fullest understanding of our genetics so far.
We have huge, expertly curated, databases containing the great collective knowledge of many experiments about our DNA, how it is being used, and what traits it effects.
Perhaps it is now possible to begin to synthesise some of this collective knowledge into a fuller understanding of complex traits.






[//]: # (TODO: Maybe move some of this to a discussion/wrap up summary bit for after people know what DNA is.)
[//]: # (TODO: The idea of what and how something is genetically determined is difficult to define. Intuitively, we define it based on how much of the variability we can measure is determined by genes: this is called *heritability*. 100% heritable - eye colour, 0% heritable - taste in clothes - or somewhere in between on this linear scale. This must be a simplification: a lot of the traits that we're trying to measure are more complex than that, for example athletic performance, aggressive behaviour, sexual preferences... Heritability also depends on the definition of a "normal" environment. It may be that there is an environmental influence we could dream up that would change our eye colour, then eye colour would no longer be 100% heritable. What we actually want to know is the relationship between genetics and the environment: a causal diagram for all phenotypes.)

### Biological molecules: DNA, RNA, Proteins and the central dogma of molecular biology.
Here I explain the classes of biological molecules that are vital in our understanding of genetics: the nucleic acids, DNA and RNA, and their product - proteins.

(what-is-dna)=
#### DNA

[//]: # (TODO: Sort out figure labelling. Use TOC to go through in order and replace for the site and PDF)
[//]: # (TODO: Cite Watson + Crick again) 

```{figure} ../images/dna_metalmodel.jpg
---
height: 220px
name: dna-metal-model
---
A photo of the original six-foot tall metal model of DNA made by Watson and Crick in 1953. Image from the Cold Spring Harbor Archives{cite}`noauthor_undated-ih`.
```

Most people recognise the double helix of deoxyribonucleic acid (DNA) shown in {numref}`dna-metal-model`, it’s a twisted ladder consisting of four nucleotides; adenine, cytosine, thymine, and guanine (A, C, T, G). 
It the “code of life” that contains the instructions for making all of the things which make up our bodies and the obvious starting point for understanding how they work. 
A given nucleotide on one strand is always linked to its partner on the other strand - A with T, and G with C - which creates redundancy and a convenient copying mechanism.
Lengths of DNA are measured in these base pairs (bp). 

[//]: # (TODO: Explain chromosomes and mitochondria v. briefly.)

(central-dogma)=
##### How DNA affects us: the central dogma of molecular biology
The way in which DNA affects the body can be understood through the *central dogma of molecular biology*, and in doing so we will also become acquainted with two more important biological molecules: RNA and proteins.

The central dogma of molecular biology can be paraphrased as **"DNA makes RNA makes proteins"**. The idea is that as the “code of life”, DNA contains the instructions for making RNA, which contains the instructions for making proteins, and proteins are the molecules which constitute and make up {ref}`almost everything<almost-everything>` in our bodies. 

(almost-everything)= 
```{margin} *Almost* everything
Proteins make up a lot of molecular machinery in the body as well as structures, however there are other actors, too. There are functional RNA molecules, and fats (which may or may not be synthesised using proteins) can also make up structural parts of the body (for example in cell membranes).
``` 

The central dogma describes the process of gene expression. Gene expression has two parts: transcription (“DNA makes RNA”) and translation (“RNA makes proteins”).

(what-is-rna)=
#### RNA
RNA was originally discovered alongside DNA as a nucleic acid (acidic substances found in the nucleus of cells). It was later discovered that they are also found in bacterial and archeal cells (which don't have nuclei). 

##### "DNA makes RNA", a.k.a, transcription

[//]: # (TODO: Cite DNA makes RNA makes proteins.)


The process by which "DNA makes RNA" is known as transcription. The process happens to lengths of DNA at a time. These lengths of DNA are called genes, and they may be various sizes, and be transcribed more or less frequently than one another. 

The action of transcription is largely carried out by an enzyme called RNA polymerase, which binds to a promoter region of the DNA, close to but outside the gene. This region is only accessible in certain cellular conditions. A rough model is that in conditions in which it is unfavourable for the gene to be transcribed, other molecules will block the promoter. 

The RNA polymerase then splits the DNA and adds complementary RNA nucleotides to the DNA, after which the RNA sugar backbone is formed. The RNA-DNA helix is then split, at which point we have what is known as pre-RNA. The pre-RNA is then processed into mature RNA (known as the transcript), ready to be translated into a protein. 

The process of what is transcribed and how quickly is affected by many different kinds of proteins (as well as other molecules, e.g. histone modifications). Transcription factors are of particular note, which are proteins that bind to DNA close to or in the promoter region, and either activate the gene (increasing it’s rate of transcription), by for example recruiting RNA polymerase, or repress it (decrease it’s rate of transcription). These transcription factors are in turn regulated by other transcription factors, which creates a network of gene regulation; a gene regulatory network (GRN).

(what-are-proteins)=
#### Proteins

Proteins were named by Dutch chemist Gerardus Mulder in his 1839 paper{cite}`Mulder1839-rf`, where he found that all proteins from animals and plants have more or less the same elemental makeup -  approximately C<sub>400</sub>H<sub>620</sub>N<sub>100</sub>O<sub>120</sub>. 
This intriguing result bolstered research in this area, eventually resulting in our current understanding of proteins as biological macromolecules composed of amino acids.

In 1969, Margaret Dayhoff created the first bioinformatics database to store protein structures imaged using X-ray crystallography, related to her publication of Atlas of Protein Sequence and Structure{cite}`Hersh1967-ox`. 
Soon after, in 1972, the Protein DataBank (PDB){cite}`noauthor_undated-ow` was established. 
This continues to be well-used and updated, at the time of writing holding structures of 148,827 biological molecules. 

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

##### The protein folding problem
As mentioned above, translated strings of amino acids fold automatically (or sometimes with the help of *chaperone* proteins) into the 3D structure of proteins. It’s the structure of proteins which define their function since their shape effects what they can bind to. Predicting what the structure of a protein will be from the string of amino acids is known as the protein folding problem. It’s has been one of the grandest challenges in biology for over half a century. If it were solved, it would revolutionise protein function and phenotype prediction. 

[//]: # (TODO: Mention google deep mind?)

##### Post-translational modifications
After translation, many proteins can be modified by the addition of various functional groups (parts of molecules which are responsible for chemical properties), e.g. phosphorous or ubiquitin. Such modifications change the functionality of the proteins, and are also believed to aid in protein folding.

#### "...and proteins do everything."
The unwritten addendum implied by “DNA makes RNA makes proteins” is “...and proteins do ({ref}`almost<almost-everything>`) everything”. If DNA encodes for life, then proteins are what make up life. They are the material building blocks of our bodies, and they also have a vast number of other functions: they can be enzymes catalysing reactions, hormones controlling metabolism, transporters for other proteins, signalling proteins, they might be transcription factors (controlling the expression of genes), or have many other functions.

In turn, these processes influence our phenotypes. A phenotype can be something like the level of a certain hormone in the bloodstream, so in a very simple case, a  could effect the phenotype by it's difference in the speed of expression. A phenotype could alternatively be something like height, which could have a number of genetic (and non-genetic) influences.

### A closer look at DNA: Genomes, Genes, and Genetic Variation
Now that we have a basic overview of how DNA can influence phenotype, we can discuss it in a little more detail.

(genomes)=
#### Genomes
The genome is the full amount of DNA belonging to an organism. We can talk about the genome of an individual, or about the genome of an organism (e.g. the human genome).
When we talk about an organism's genome, we do so in relation to an example genome for that organism.
This is called a *reference* genome, and does not belong to any particular individual, but instead is supposed to have the most common nucleotide each location.
We can then discuss individuals genomes in relation to the relevant reference genome.

#### Genes
As mentioned, genes are stretches of DNA that encode for RNA. Only a proportion of an organism's DNA is made up of genes. Regions of DNA that are not within genes are known as *non-coding* or *inter-genic*. These regions can still affect phenotype, by influencing the expression of other genes can include enhancers and promoters. 

[//]: # (TODO: Cite how much human DNA is genes in bp?)

The human genome is 3 billion base pairs long, and contains approximately 20,000 genes (which make up around 2% of the genome).

[//]: # (TODO: describe exome? Put in how much of genome is covered by SNPs?)

(introns-exons)=
Although we define genes as regions of DNA which encode for proteins, not all of the DNA of a gene is transcribed into mature RNA. There are two types of regions inside the gene: introns (regions which cannot be transcribed) and exons (which can be transcribed). 
The introns are removed during the processing step in a process known as *splicing*. 
In addition, many genes have the capability to be transcribed into multiple transcripts, via a process known as alternative splicing.
This can happen, for example, by skipping some of the exons during splicing.

Even where DNA can be expressed as proteins, the level of expression depends on the cell environment and other DNA.
 
[//]: # (TODO: link for regulating transcription) 

Genes are also not a straightforward unit. 
Just because a gene is transcribed, does not mean that RNA is always translated into a protein. 
Furthermore, there is not a 1:1 mapping of genes:proteins for those that do (one gene could be read to create multiple different proteins).
There can be disagreements about the locations of genes on the genome, and popular databases of genes fundamentally disagree on this and on the number of genes{cite}`Salzberg2018-yc`. 
Gene names and symbols change over time, and can be difficult to map between for this reason. 

Genes are also not necessarily a “unit of heritability” - we inherit regions around genes together with them and do not necessarily inherit whole copies of each gene from each parent (although this is rare). 

#### Genetic variation
As you are no doubt aware, individuals of the same species share the vast majority of their DNA. 
Genetic variation is the difference in DNA sequence between individuals in a population, and variants are locations on an organisms genome where we observe variation between individuals. 
There are different types of genetic variation, for example indels (insertions and deletions)- where small sections of DNA are inserted or deleted from the genome - and copy number variations (CNVs) where larger stretches of the genome are repeated. 
However, the most well-studied and common type of genetic variation between humans are single nucleotide polymorphisms (SNPs, pronounced “snips”).

The different forms that a variant can take in the population are called alleles, depending on the type of variant. 
Alleles could be different forms of a whole gene, or as small in length as an individual nucleotide.

##### SNPs and SNVs
A SNP is a location on an organism’s genome where there are differences of a single nucleotide (“A”,”C”,”T”,”G”) between individuals. In some fields, these variations are only considered to be Single Nucleotide *Polymorphisms* if they are relatively commonly occurring in the population (at least 1%), while Single Nucleotide Variants (SNVs) can include both rare and common variants. 

Variation at a location does not imply a disease-causing effect, many SNPs are neutral. Much of the time, the aim of studying such variants is to determine which are which. This is often done through looking at their rarity, either in a specific human population (e.g. people with diabetes), the entire human population, or across the tree of life. 

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

### Looking more closely at proteins: domains and disorder

Just as DNA has been classified at different levels (SNP, gene, genome), so too have proteins.

#### Primary, Secondary, Tertiary, and Quaternary

Proteins are described and classified in terms of the their primary, secondary, tertiary, and quaternary structure. 

The primary structure is simply the amino acid makeup of the protein, which describes the protein's chemical makeup, but not it's three-dimensional structure. 
These amino acid strings tend to form into a small number of familiar (secondary) three-dimensional structures, for example beta strands, beta sheets, and alpha helices.

At the next level, the tertiary structure describes folds: combinations of secondary structures, for example a TIM barrels (a torroidal structure made up of alpha helices and beta strands). 
At this level, similar structures do not imply an evolutionary or functional similarity.

##### Quaternary structures: protein domains

```{figure} ../images/lego.png
---
height: 100px
name: lego
alt: The figure shows a red lego block linked to a yellow lego block, which is then linked to another yellow lego block. The links are thin grey lego blocks.
---
An illustration of the lego analogy for protein domains. Coloured bricks represent protein domains - colour represents a specific protein domain type, while thin grey bricks represent polypeptide linkers which link domains. Image created using mecabricks{cite}`Jarraud2019-jj`
``` ``

[//]: # (TODO: delete extra ```)

The quaternary structures of proteins - protein domains - have proved particularly interesting for research. 
A simple and oft-used metaphor is to think of protein domains as lego building blocks ({numref}`lego`) which can be linked by polypeptide chains to make up a protein. 
These polypeptide chains (known as linkers) are often inflexible, in order to allow only one conformation of the protein. 
Small and simple proteins often consist of just one domain, while bigger proteins can contain many domains. 
An individual domain can be found in many different proteins, and multiple times in the same protein. 

[//]: # (TODO: Definitely definitely need this to be cited.)
Protein domains are interesting because they are highly conserved in evolution, and are thought of as units of function, evolution, and/or structure. 
The functions of proteins, at both low-level (e.g. “calcium signalling protein”) and high-level (e.g. annotated to “liver disease”), are costly and difficult to discern, so there are many proteins about which little is known. 
For this reason, often proteins are classified according to their similarity to proteins about which functions are known, for example those containing the same protein domains.

##### Disorder
While protein domains exist in one confirmation, not all linkers are rigid. 
Flexible regions of proteins which allow for various conformations are referred to as disordered. 
Disordered regions are not only relegated to linkers between domains. 
Proteins can be constituted entirely of disordered regions, or may have large disordered regions.

Intrinsically disordered proteins can exist in a number of conformations, rather than one fixed structure. 
On some occasions, the disordered regions are known to be functional, while on others, proteins may be non-functional until they bind with another macromolecule which forces them into a fixed conformation.

[//]: # (TODO: Potentially add something about protein families and superfamilies here.)

[//]: # (TODO: Rename this section to be about phenotype)

### Associations between regions of DNA and traits
#### Is there a gene for that?
Since “DNA makes RNA makes proteins” and proteins have functions, it might seem sensible to say that there is a gene “for” a given function. 
While this is sometimes true (single gene diseases do exist), most of the time the same gene can make multiple different proteins, the same protein can be involved in multiple different pathways and have multiple functions, and multiple proteins can contribute to one function. 

The interaction between DNA, RNA and proteins, and the environment is also important to consider. 
Although DNA makes RNA makes proteins and proteins do pretty much everything in our bodies, which proteins are made and how they behave is highly dependent on the environment. 
The function of a gene might not be evident in some environments since the protein is never transcribed, or it may behave differently. 
Furthermore, there are many traits may be entirely environmental.

#### Genome Wide Association Studies
Genome Wide Association Studies (GWAS) are large observational studies where the genotypes of a cohort with a specific phenotype (e.g. diabetes) are compared to the genotypes of a cohort lacking in that phenotype (i.e. a control group) in order to find genomic loci that are statistically associated with the phenotype. 
This has been a popular type of scientific enquiry since the first GWAS study in 2005. 
GWAS generally results in lists of SNPs, often in the hundreds, ordered by p-value. 
Disentangling which of these SNPs (if any) cause the trait is a tricky, particularly since GWAS specifically interrogates common variants. 
The process of identifying causal variants generally involving identifying regions in linkage disequilibrium, and re-sequencing regions of interest in further detail.

The GWAS catalog database{cite}`Buniello2019-cv,L_Emery2017-rd` was founded in 2008, to provide a consistent and accessible location for published SNP-trait associations, which extracts information about experiments from the literature (currently over 70000 associations from over 3000 publications).

[//]: # (TODO: Sections on Phenome Wide Association Studies and Polygenic risk scores ONLY IF they are relevant to later)
[//]: # (TODO: Explain CRISPR in an aside to below if haven't mentioned already)

#### Knockouts
Insight into gene function can also be gained by “knocking out” a gene, preventing it from being translated into a working protein, for example using CRISPR. Combinations of up to four genes can be knocked out in a single experiment. Knocking out a gene can lead to a difference in phenotype, and differences in gene expression, which can be used to help determine gene regulatory networks. There is a lot of existing data on the phenotypic results of mouse knockouts, since they are often used to create mouse models for diseases. Unfortunately, it is not always well-recorded when knockouts lead to no detectable phenotypic change{cite}`Barbaric2007-zm`.

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```