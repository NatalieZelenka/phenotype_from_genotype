(sequencing-technology)=
# Sequencing and microarrays
Sequencing are microarrays are how we get measurements of DNA and RNA.

We measure DNA so that we can understand what organisms genetic material is capable of doing: and understand what the differences between different species and individuals is.

These measures of DNA can tell us (among other things) what proteins it is possible to make. 
If we think of genes as a collection of blueprints, then one major reason that we measure RNA to tell us how much each blue print is in production.

## Sequencing overview
Sequencing technologies are used to read strings of DNA or RNA: this can be done *de novo*, i.e. even when we don't know the sequences ahead of time.
No sequencing technology can read whole chromosomes end to end, however, all work by reading shorter lengths of DNA (called *reads*).

From the late 1970’s until the mid 2000s, *Sanger sequencing* was the most popular sequencing technology, although it underwent various improvements over this timescale. 
In Sanger sequencing (and other first-generation methods), reads of around 800bp are sequenced, one at a time. 
The human genome project sequenced the first human genome using this method{cite}`Venter2001-wn`, and it’s still used in some circumstances, for example validating next generation sequencing. 

Second, or *next generation sequencing* (NGS), also referred to as high-throughput sequencing, is a catch-all term for the faster and cheaper sequencing technologies which replaced the previously used Sanger sequencing. 
A feature that is common to NGS methods is that many shorter reads (around 100bp, exact numbers depending on the specific technology) are sequenced in parallel. 
The process is massively parallel: millions to billions of short sequences can be read at a time. 
This is a huge factor in making NGS much faster (and therefore cheaper) than Sanger sequencing. 
In turn, this speed and cheapness means that more repeats can be sequenced, increasing the overall accuracy of NGS over Sanger (despite the accuracy of each individual read being generally lower).

(rna-seq-ngs)=
NGS can be used for sequencing either DNA or RNA (known as RNA-seq when applied to the whole transcriptome).
While (NGS) DNA-sequencing and RNA-seq can use the same underlying NGS technologies, there exist some differences, e.g. RNA is reverse-transcribed into strands of complementary DNA, before being sequenced, since sequencing DNA is currently easier than sequencing RNA. 

There are now also third generation sequencing technologies that allow much longer reads to be sequenced, e.g. nanopore technology.

[//]: # (TODO: Mention CAGE here?)

(assembly-and-alignment)=
## Alignment and assembly
Whichever {ref}`technology<sequencing-technology>` is used, DNA and RNA is sequenced in small sections.
This means that reads must then be *aligned* to an existing sequence (e.g. reference genome, known gene, or transcript), to allows us to know where on the genome (which chromosome and position on that chromosome) the read came from.

If an existing sequence does not yet exist, we say that we are sequencing *de novo*. 
In this case, reads are aligned with one another, as illustrated in {numref}`assembly` so that they can be *assembled* into a new sequence. 

In both cases, alignment requires the reads to overlap, so longer and more numerous reads make these tasks easier.

```{figure} ../images/de_novo_assembly.png
---
height: 140px
name: assembly
---
Image illustrating how reads of DNA are aligned with one anther to assemble genomes *de novo*.
```

The current estimate for raw sequencing inaccuracy of an individual NGS read is around 0.24%{cite}`Pfeiffer2018-kt`, meaning that on average one base pair will be incorrect for a 500pb read.
Multiple repeats are therefore required to obtain a more accurate measurement of the assembled sequence, which is further necessary since there are many repeated sequences (perhaps over two thirds of the human genome{cite}`De_Koning2011-ac`).
The depth for a nucleotide is the number of reads that overlap that nucleotide. 
Similarly, the average depth of a sequence can be calculated. 

After assembly, even in the most complete genomes, we are still left with some sequences that could not be placed, and some parts of the genome that we still don't know about. 

```{figure} ../images/alignment.png
---
height: 240px
name: alignment
---
Image showing how RNA-Seq reads are mapped to the genome (image from Advancing RNA-Seq Analysis {cite}`Haas2010-lm`). 
RNA-seq is used much less often for de novo sequencing, and is generally mapped to a reference sequence. 
``` 
{numref}`alignment` shows how alignment and assembly are used in the context of RNA sequencing.

## Microarrays
Through the 1970s into the early 2000s, DNA arrays/microarrays developed alongside sequencing as a way of measuring the presence of previously sequenced DNA in new samples. 
These arrays contain pre-chosen fragments of DNA (probes) arranged in spots, with each spot containing many copies of the probe, on a solid surface, e.g. glass, silicon or plastic. 
The probes consist of single strands of DNA, and arrays operate on the principle that the complementary DNA from the sample will bind tightly to it.

These arrays were originally macro-sized, one of the first being 26 × 38 cm and containing 144 probes{cite}`Bumgarner2013-hg`, but are now on small chips, which can contain up to millions of probes.

Arrays were extremely popular for measuring {ref}`gene expression<gene-expression>`, but this technology has largely been superseded by the more accurate and comprehensive RNA-seq. 
However, microarrays are still commonly used by companies like 23andMe for genotyping an individual (measuring specific alleles).

Microarrays were also extremely popular for measuring gene expression through RNA microarrays before the advent of RNA-Seq (next generation sequencing for RNA).