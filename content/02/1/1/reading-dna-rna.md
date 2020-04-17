### Reading DNA and RNA

#### Sequencing technology

The process of reading DNA and RNA is called sequencing. From the late 1970’s until the mid 2000s, Sanger sequencing was the most popular sequencing technology, although it underwent various improvements over this timescale. In Sanger sequencing (and other first-generation methods), reads of around 800bp are sequenced, one at a time. The human genome project sequenced the first human genome using this method{% cite Venter2001-wn %}, and it’s still used in some circumstances, for example validating next generation sequencing. It was much more popular to sequence DNA than RNA with this type of technology.

Second, or next generation sequencing (NGS), also referred to as high-throughput sequencing, is a catch-all term for the faster and cheaper sequencing technologies which replaced the previously used Sanger sequencing. A feature that is common to NGS methods is that many shorter reads (around 100bp, exact numbers depending on the specific technology) are sequenced in parallel. The process is massively parallel: millions to billions of short sequences can be read at a time. This is a huge factor in making NGS much faster (and therefore cheaper) than Sanger sequencing. In turn, this speed and cheapness means that more repeats can be sequenced, increasing the overall accuracy of NGS over Sanger (despite the accuracy of each individual read being generally lower). NGS can be used for sequencing either DNA or RNA (known as RNA-seq when applied to the whole transcriptome). 

There are now also third generation sequencing technologies that allow much longer reads to be sequenced.

##### RNA-seq 
While (NGS) DNA-sequencing and RNA-seq can use the same underlying NGS technologies, there exist some notable differences. For example, RNA is reverse-transcribed into strands of complementary DNA, before being sequenced, since sequencing DNA is currently easier than sequencing RNA. RNA-seq is used much less often for de novo sequencing, and is generally mapped to a reference sequence. 

Since transcription is dependent on time, tissue, location, cell, etc, RNA-seq experiments are also dependent on all of these conditions. Furthermore, they are sensitive to differences in laboratory conditions and experimental design, creating artefacts in the resulting data known as batch effects. 

##### Microarrays
Through the 1970s into the early 2000s, DNA arrays/microarrays developed alongside sequencing as a way of measuring the presence of previously sequenced DNA in new samples. These arrays contain pre-chosen fragments of DNA (probes) arranged in spots, with each spot containing many copies of the probe, on a solid surface, e.g. glass, silicon or plastic. The probes consist of single strands of DNA, and arrays operate on the principle that the complementary DNA from the sample will bind tightly to it.

These arrays were originally macro-sized, one of the first being 26 × 38 cm and containing 144 probes{% cite Bumgarner2013-hg %}, but are now on small chips, which can contain up to millions of probes.

Arrays were extremely popular for measuring gene expression, but this technology has largely been superseded by the more accurate and comprehensive RNA-seq. However, microarrays are still commonly used by companies like 23andMe for genotyping an individual (measuring specific alleles).

#### Assembly and alignment

![Figure X_alignment: Image showing how RNA-Seq reads are mapped to the genome (image from Advancing RNA-Seq Analysis {% cite Haas2010-lm %}). A similar process is followed for DNA.](/content/images/alignment.png)

[//]: # (TODO: Have I said the word exome before this point? What about de novo?)
The short reads that are the output of initial sequencing must be assembled to create longer sequences of DNA, whether that’s sequencing of individual genes, whole exome sequencing (WES) or whole genome sequencing (WGS). This is done by aligning reads to one another and (if available) to an existing reference sequence. This of course requires the reads to overlap, so longer and more numerous reads make this task easier. The process and underlying algorithms differ considerably whether the sequence being assembled can be mapped to an existing sequence or is being created de novo.

The current estimate for raw sequencing accuracy of an individual NGS read is around 0.24%{% cite Pfeiffer2018-kt %}, meaning that on average one base pair will be incorrect for a 500pb read. Multiple repeats are therefore required to obtain a more accurate measurement of the assembled sequence, which is further necessary since there are many repeated sequences (perhaps over two thirds of the human genome{% cite De_Koning2011-ac %}). The depth (or coverage) for a nucleotide is the number of reads that overlap that nucleotide. Similarly, the average depth of a sequence can be calculated. 

---

{% bibliography --cited %} 