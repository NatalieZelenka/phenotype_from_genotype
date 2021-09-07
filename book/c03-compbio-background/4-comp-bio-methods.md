(predictive-methods)=
# Predictive computational methods

[//]: # (TODO: Mention validation in this little bit if I manage to describe that here)
[//]: # (TODO: Recap precision/recall)

The low cost of sequencing means that databases of sequences have been expanding very rapidly in comparison to other information, which is much harder to determine.
Computational predictive methods aim to predict structure or function from sequence in order to bridge this gap.
Here I describe some of the challenges and methods in this space.

(protein-classification-prediction)=
## Prediction tasks: Protein classification prediction
[//]: # (TODO: Move SCOP to earlier since it's mostly categorisation not prediction, but keep BLAST here)
[//]: # (TODO: Cite low sequence similarity, high homology: https://www.mrc-lmb.cam.ac.uk/rlw/text/bioinfo_tuto/structure.html)
[//]: # (TODO: Mention PFAM?)

As {ref}`previously mentioned<protein-classification>`, proteins are often classified by structural similarities. 
This information is often used because researchers identify a gene of interest, but information about it's function or structure (in PDB) has not yet been captured and stored.
In such cases, it's often necessary to make inferences about protein structure or function based on their similarity to known proteins.
This is sometimes done using sequence similarity (e.g. {ref}`BLAST<blast>`), but sequence similarity can vary considerably between proteins with the same underlying structure. 
This is why structural similarity searches based on protein classification are preferred.

```{margin} BLAST
:name: blast
The Basic Local Alignment Search Tool{cite}`Altschul1990-zf`, is an extremely popular tool that is used to perform a basic search of nucleotide or amino acid sequences to known sequences, based on statistically significant similarities between parts of the sequence.
```

(scop)=
### SCOP
The Structural Classification of Proteins (SCOP) database{cite}`Murzin1995-se` classifies all proteins with known structure based on their structural similarities, based on the consideration of the protein’s constituent domains. 
The classification is mostly done at the level of families, superfamilies, and folds arranged in a tree structure. 
Families represent the most similar proteins, which share a “clear evolutionary relationship”, while superfamilies represent less close evolutionary relationships, and folds represent the same secondary structure. This protein classification task, while aided by automation, was carried out largely by manual visual inspection.

SCOP was updated until 2009, but has been succeeded by SCOP2{cite}`Andreeva2014-om`. 
However, SCOP2 has a different underlying classification system, based on a complex graph, rather than a hierarchy. 
The CATH (Class, Architecture, Topology, Homologous superfamily){cite}`Orengo1997-vf` database provides another classification system, which operates hierarchically, but is created mostly via automation, which leads to major differences between the classifications{cite}`Csaba2009-of`.

(superfamily-update)=
### SUPERFAMILY
SUPERFAMILY{cite}`Gough2001-ct` uses Hidden Markov Models (HMMs) to assign sequences to SCOP domains, primarily at the superfamily level. 
This allows the functions of poorly understood proteins to be inferred based on how closely they match known superfamilies. 
HMMs are very successful at such assignments since pairwise correlations between proteins (or their domains) and other proteins in the family may be weak, but consistently for many proteins; this can be picked up by an HMM. 
The superfamily level is chosen since it is the broadest level which suggests evolutionary relationships, but SUPERFAMILY also generates assignments at the (stricter) family level.

HMMs are created by first finding closely relating protein homologs for a given protein superfamily using {ref}`BLAST<blast>`, and then extending it by comparing the HMM to more distantly related homologs. 
The resulting HMM library is fine-tuned by some manual curation. 

The SUPERFAMILY website also contains other tools, including a database of all sequences (genomes) which are used to generate the HMM library.

[//]: # (TODO: Cite dcGO + D2P2 + stol)
[//]: # (TODO: Add my contribution in a box)

(my-superfamily-contribution)=
**SUPERFAMILY update**
I contributed to SUPERFAMILY’s 2014 update{cite}`Oates2015-li` by editing the paper and adding a small number of proteomes. 
The SUPERFAMILY database of proteomes doubled from 1400 to over 3200 from 2010 to 2014. 
The update paper described this development, as well as highlighting SUPERFAMILY as a resource for unique proteomes that are not found elsewhere (e.g. Uniprot). 
Although SUPERFAMILY’s primary resource is it’s HMM library, it also integrates a range of other tools for sequence analysis, for example protein disorder prediction (D2P2) and GO annotation (dcGO), as well as a domain-based phylogenetic tree (sTol). 


## Prediction tasks: Protein function prediction
Human genes can have multiple functions, but currently, we don't even know one function for all of them.
Although we have their sequence, some genes are completely functionally unknown to us.
Protein function prediction is the task of predicting protein function (usually in terms of ontology terms) from protein sequence.

(dcgo)=
### DcGO
```{margin} Error types and False Discovery Rate (FDR)
:name: fdr
In making predictions, there are two types of errors that we can make, false positives $F_p$ (Type I errors) in which we wrongly think something is true, and false negatives $F_n$ (Type II errors) in which we wrongly thing something is false. Similarly we can get predictions right in two ways, correctly thinking something is the case (true positives $T_p$) or isn't (true negatives $T_n$).

The FDR is a measure of the false positives, which takes into account the number of predictions:
$FDR = \frac{F_p}{F_p + T_p}$

```
The aim of the domain-centric Gene Ontology (dcGO){cite}`Fang2013-ms,Fang2013-ix` tool is to give insight into uncharacterised or poorly characterised proteins by leveraging information about the content of their constituent protein domains. 
It annotates domains and combinations of domains (a.k.a. supradomains) to phenotype terms from a variety of ontologies, including the Gene Ontology (GO), Mammalian Phenotype ontology (MP), Disease Ontology (DOID), Zebrafish ontology (ZFA). 
Domain information comes from SUPERFAMILY, and annotations between (supra)domains and phenotype terms are made below a cut-off of {ref}`FDR<fdr>`-adjusted statistical associations between the entities. 
Using phenotypes from a range of species serves to make use of greater numbers of experiments, and therefore increases the number of little-known proteins across species that DcGO can make predictions about.

(CAFA)=
## CAFA
Critical Assessment of Functional Annotation{cite}`Zhou2019-jk,Jiang2016-rz,Radivojac2013-wh` (CAFA) is an international community-wide competition for the prediction of protein function, which aims both to stimulate research in the field of protein function prediction, and to measure progress in the field.
It has been running approximately every 2-3 years since 2013. 

Each CAFA challenge begins by the organisers releasing a large number of target sequences (over one hundred thousand) across multiple species, about which participant teams must make predictions. 
After the competition closes, the organisers wait 3 months, by which time, new experimentally verified protein functions will be found (representing ~3% of sequences in past competitions) and these are the data set against which the predictors are measured. 

Participants can use any additional data they see fit to make predictions, which must be triples containing a sequence ID, ontology term ID (e.g. a GO/HP identifier), and a confidence score between 0 and 1. 
A score of 1 indicates a completely confident prediction, while a score of 0 is equivalent to not returning the prediction. 
Each team may submit up to three models, the best of which is ranked.

[//]: # (TODO write results of CAFA and also move the more specific bits back to the Filter chapter)

(no-limited-knowledge)=
The target sequences consist of a mixture of "no-knowledge" and "limited-knowledge" sequences. 
No-knowledge sequences are sequences which upon release have zero experimentally-validated GO annotations to any of GO's three constituent ontologies (biological process, cellular component, and molecular function).
Limited-knowledge sequences are sequences with one or more annotations in one or two GO ontologies, but not all three.

<!--
### Past CAFAs
In 2014, the CAFA2 experiment began: 100,8216 target sequences from 27 different species were released to participants. 
In addition to the GO Biological Process and Molecular Function ontologies used in CAFA1, predictions were also requested for the Human Phenotype Ontology and GO Cellular Component ontology. 
-->


## Prediction tasks: Variant prioritisation
Variant prioritisation is a version of protein function prediction in which long list of genes or variants (obtained for example through a GWAS experiment) are narrowed down to a shorter list of variants or genes which are more likely to be causal.

(fathmm)=
### FATHMM
Functional Analysis through Hidden Markov Models (FATHMM){cite}`Shihab2013-pk` is a tool for predicting the functional effects of protein missense mutations using sequence conservation information (via HMMs), which can be (optionally) weighted by how likely a mutation in a protein/domain would be to lead to disease. 
FATHMM can only score missense mutations because it scores SNPs based on the probability of specific amino acids existing in proteins.
Weightings are calculated from the frequency of disease-associated and functionally neutral amino acid substitutions in protein domains from human variation databases (the Human Gene Mutation Database{cite}`Stenson2009-jc` and Uniprot-KB/Swiss-prot{cite}`Pundir2016-ya`).

Consequence files describing whether an amino acid results in a missense, nonsense or synonymous SNP must first be obtained by using Ensembl’s Variant Effect Predictor{cite}`McLaren2016-di` in order to create input to FATHMM. 
FATHMM then calculates conservation scores which are a measure of the difference in amino acid probabilities for a SNP according to the HMM, i.e. between a wild type amino acid and it’s substitution. 
A reduction in amino acid probabilities is interpreted as a prediction of deleteriousness (likelihood to cause harm), and the larger the reduction the greater the predicted harm. 

(prediction-phenotype)=
## Prediction tasks: Phenotype prediction
[//]: # (TODO: Cite 23andMe and Promethease health reports)
Phenotype prediction is the task of predicting phenotypes from genotypes. 
Specific tests of phenotype prediction might look like matching genotypes to profiles of traits, or predicting specific phenotypes from genotypes.

(phenotype-protein-prediction-link)=
Although it's often presented as a separate task, phenotype prediction is closely linked to protein function prediction.
When variants on the protein-coding genome are known to be responsible for phenotypes, the assumption is that variant impacts the protein and the protein has a function that causes the phenotype when it behaves differently than usual.
This is the assumption that underlies annotations between genes or proteins and phenotype terms, and it's also the assumption that underlies phenotype "prediction" algorithms like 23andMe or Promethease's health reports, which count the presence or absence of individual variants thought to be associated with disease, in order to inform potential phenotypes e.g. "You have 2 alleles associated with causing Breast Cancer".

[//]: # (TODO: Add CAGI here)

(cagi)=
### CAGI
Critical Assessment of Genome Intepretation{cite}`McInnes2019-ov` (CAGI) is a prediction competition open to the research community, in the same tradition as CAFA, this time aiming to objectively assess predictive methods for determining the phenotypic impacts of genomic variation across a number of different challenges.

[//]: # (TODO: Write)
The precision of the best methods in phenotype prediction of rare illnesses is still below 50%{cite}`Kasak2019-bb`.

<!--
## Validating computational methods

### Predictive competitions

**CAFA**

**CAGI**
-->