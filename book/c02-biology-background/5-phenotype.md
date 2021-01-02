### Linking genotype and phenotype: associations between regions of DNA and traits
[//]: # (TODO: Does this section fit?)
[//]: # (TODO: Heritability?)

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
