---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.9.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(snowflake-preprocessing)=
# Preprocessing

In the preprocessing stage, the `snowflake preprocess` command looks at all the inputs together, in order to filter them only for the useful parts before running the predictor.

In particular, `snowflake preprocess` always calculates the following in all running modes:
- A list of SNPs associated with each term (`.snp` files)
- Sets of equivalent terms, i.e. terms which have the exact same set of SNPs associated with them (`.polist` files)

And it also calculates the following if an input cohort is provided:
- A list of overlapping SNPs between the background and input cohort 
- A combined VCF file containing only these snps, including dealing with ambiguous flips. 

In this section, I will run through and explain the preprocessing step for the 1000 genomes only (no input cohort) as this represents an approximation of the maximum number of SNPs that `snowflake` can predict on, since the 1000 genomes project uses {abbr}`WGS (Whole Genome Sequencing)`.

<!--
In this section, I will run through and explain the preprocessing step for:
1. The 1000 genomes only (no input cohort) as this represents an approximation of the maximum number of SNPs that `snowflake` can predict on, since the 1000 genomes project uses {abbr}`WGS (Whole Genome Sequencing)`.
2. The 1000 genomes with the ALSPAC input cohort, as this shows a more typical use of `snowflake`, where the inputs represent genotyped data.

## 1000 Genomes only: without input cohort
[//]: # (TODO: How do you run it? Etc)

### SNPs per term
[//]: # (TODO: Graph... explain these are the numbers of dimensions that we are looking through for a group of 1000 people)

### Redundant terms
[//]: # (TODO: Are the redundant terms always meaningful?)

<!--
+++

## 2500 Genomes and ALSPAC: with input cohort
[//]: # (TODO: How to run)
### Overlapping SNPs
### Ambiguous flips
### SNPs per term
### Redundant terms
-->

+++

(combining-vcf-files)=
## Combining VCF files, a.k.a. missing SNPs and ambiguous flips
Due to the cost, far more humans have been genotyped than have had their whole genomes sequenced. 
Genotyped and {abbr}`WGS (Whole Genome Sequencing)` data look similar once in a VCF file, but the data cannot necessarily be treated the same in both cases. 

(missing-snps-vcf)=
### Missing SNPs in VCF files
Many VCF files only store the differences between individuals in the file, a SNP being missing from a VCF file does not necessarily mean that the original sequencing or genotyping didn't record the calls at that position.

If combining two genotyped files, we would want to discard all SNPs that are not measured by both chips, but when combining a genotype VCF file with a WGS VCF file, we usually want to keep all SNPs from the genotyped VCF (since these locations will also have been sequenced by WGS).

[//]: # (TODO: Mention `.snps` file)

(ambiguous-flips)=
### Ambiguous Flips
[//]: # (TODO: Explain ambigious flips a bit better, +1 from Tom)
The majority of input data to the predictor is 23andMe data. 
In testing earlier versions of Snowflake with the 2500G background and a cohort of 23andMe genomes, it became clear that for many phenotypes, the background was forming a separate cluster to the cohort. 
This led to the realisation that there are 23andMe calls which had the opposite ratio of wild type:mutant than the 2500 genomes. 
Some further reading revealed this to be a known problem{cite}`Church2005-zv`, which may be due to ambiguous flips{cite}`Sand2007-ed`. 

[//]: # (TODO: Finish writing this sentence:)
Implausible distributions of SNPs in the input cohort (given the background) are therefore discarded using a cutoff.

<!--
### Example: ALSPAC and 2500G

### Example: CAGI5 and 2500G
-->