(sources-of-error)=
# Sources of error in computational biology


(pqi)=
## PQI
[//]: # (TODO: Check this is in a reasonable position and has the right level of headings.)
[//]: # (TODO: Explain that it is about where there is also proteins/proteomes)

The Proteome Quality Index (PQI) is an attempt to provide quality metrics about completed genome sequences. It was a group effort, which resulted in a paper{cite}`Zaucha2015-ez`, of which I am an author, as well as [an associated website (http://pqi-list.org/)](http://pqi-list.org/). I contributed to discussions about metrics, and paper editing.

The motivation for creating the index came from problems of reproducibility in the field of genomics. In creating a daily-updated tree of life (sTOL, sequenced Tree Of Life), it was found that many sequenced genomes were missing vital proteins due to poor sequencing{cite}`Fang2013-et`. Such genomes are reused by many researchers, for example in comparative genomics, and omissions of whole proteins and poor accuracy of others are likely to affect research results. 

The PQI website was intended to be both a way for users of past genomes to look up the quality of a genome in advance of some research and, more importantly as a talking point for quality guidelines for genomes/proteomes. While quality control and data submission guidelines were more developed in other areas of computational biology, similar guidelines for genome quality were lacking.

###### PQI features 

The PQI website provides a scoring system for proteomes, bringing together numerous different metrics which are normalised before being averaged into an intuitive star-rating (1-5 stars) with equal weight given to each metric. Proteomes can be searched for, filtered by the various ratings, downloaded, user-rated and commented on. Additional proteomes and metrics can be added/suggested by users via the website and documentation describing this is provided.

###### The original PQI metrics

[//]: # (TODO: Check how this paragraph ended in Google Doc. Had weird punctuation.)

PQI originally provided 11 measures of proteome quality, that are either local i.e. “clade-based” (in which proteomes are compared to similar organisms) or global (in which case it is compared to all other proteomes). A clade is a group of organisms that consists of a common ancestor and all its descendants, i.e. is a branch on the tree of life{cite}`Cracraft2004-ud`, so an appropriate ancestor must be chosen to define the clade. For PQI, since the purpose of these clades was to compare its’ constituent proteomes, we wanted clades that had similar variability. This was achieved by choosing parent nodes that are at least 0.01 in branch length away from the proteome (leaf node), and such that the clade contains at least 10 species. Trees and branch lengths to carry out these calculations were taken from sToL{cite}`Fang2013-et`. For clade-based metrics, proteomes score well if they have similar scores to the rest of the clade.

[//]: # (TODO: Check combination homology 3 and 4 from table below)

```{list-table} Description of the quality metrics in PQI
:header-rows: 1
:name: pqi-table

* - Metric name
  - Type
  - Description
  - Notes
* - 1\. Percentage X-content
  - Global
  - Percentage of proteome with amino acids denoted by ‘X’, excluding the first residue of each protein.
  - Amino acids that cannot be identified, or can have more than one value are represented by an ‘X’ in the amino acid sequence[139]. This occurs when coverage of the sequencing is low. Uncertainty in translation start sites mean the first residue of a protein is often uncertain (‘X’) even in the highest quality proteomes, so these are excluded from this measurement.
* - 2\. PubMed Publication Count
  - Global
  - The total number of publications related to the genome as listed for that entry in the PubMed database[140].
  - This is a measure of how well-studied a proteome is, assuming that proteomes that have been studied more will be of higher quality. 
* - 3\. CEG Domain
  - Global
  - Proportion of CEG set which contains homologous domains in the proteome, according to SUPERFAMILY
  - This method assumes that all eukaryotic genomes should contain a core set of well-conserved of eukaryotic genes. This score is not calculated for non-eukaryotes. This was done using the Core Eukaryotic Gene (CEG) library used by the CEGMA tool[141], which comes from the Eukaryotic Orthologous Group (KOG) sequence orthology database[142]. Domain-architecture similarity is calculated using the SUPERFAMILY HMM library.
* - 4\. Combination Homology
  - ???
  - ???
  - ???
* - 5\. Percentage of sequences in Uniprot
  - Global
  - Percentage of proteome sequences that appear in Uniprot with 100% sequence identity
  - This metric assumes that the majority of discrepancies between Uniprot protein sequences and the proteome protein sequences are due to proteome inaccuracies.
* - 6\. Number of domain superfamilies
  - Clade-based
  - Number of proteins assigned to domain superfamilies by SUPERFAMILY compared to average for clade.
  - Assignment to domain superfamilies was obtained using the SUPERFAMILY HMM Library. The number of superfamilies gives an indication of the diversity of the proteome, so a low number compared to the clade may indicate an incomplete proteome, while a high number could indicate that the proteome contains domain superfamiles that it shouldn’t. 
* - 7\. Percentage of sequence covered
  - Clade-based
  - Percentage of amino acid residues in proteome sequence that are covered by SCOP domain superfamily assignments, compared to the average for the clade. 
  - This metric measures the portion of structured protein sequences found in the proteome as opposed to disordered regions and gaps. This measure assumes related species have a similar breakdown of these types of proteins. A mismatch could indicate that the parts of the genome that are supposed to be protein-coding are an incorrect length, that it is missing proteins, or contains proteins that it shouldn’t.
* - 8\. Percentage of sequences with assignment
  - Clade-based
  - Percentage of amino acid residues in proteome that have SCOP superfamily assignment according to SUPERFAMILY, compared to the average for the clade.
  - Related species are assumed to have a similar percentage of domains with SUPERFAMILY assignments to SCOP superfamilies
* - 9\. Mean sequence length
  - Clade-based
  - The average length of proteins in the proteome (in amino acids), compared to the average for the clade.
  - This measure assumes that mean sequence length of proteins should be comparable with those of related species. 
* - 10\. Mean hit length
  - Clade-based
  - Average number of amino acids in superfamily assignments, compared to the average for the clade.
  - Longer hits represent better matches to SCOP domains. These are assumed to be similar for similar species.
* - 11\. Number of domain families
  - Clade-based
  - Number of distinct SCOP protein domain families that are annotated to the proteome, compared to the average for the clade.
  - The SCOP protein domain families are annotated to the proteome using a hybrid HMM/pairwise similarity method from the SUPERFAMILY resource. Similarly to the number of domain superfamilies, the number of families gives an indication of the diversity of the proteome at the SCOP family level. Domain families were included in addition to domain superfamilies, since they are more specific and may reveal differences that are not apparent at the superfamily level. 
* - 12\. Number of domain architectures
  - Clade-based
  - Number of unique domain architectures (combinations of SCOP domain superfamilies and gaps) in the proteome, according to SUPERFAMILY, compared to the average for the clade.
  - Similarly to the number of domain families superfamilies, the number of domain architectures gives an indication of the diversity of the proteome at the SCOP family level.
```

[//]: # (TODO: Format table caption better:)

{numref}`pqi-table` shows the original PQI metrics. 

As a proteome will get low scores in clade-based metrics when they are unusual compared to the rest of its clade, model organisms (e.g. Homo Sapiens) can get a low score in clade-based metrics since for the wrong reasons - since they are of such higher quality compared to those in it’s clade. The PQI website’s comment and user-rating features can be used to alert its users to these cases.

Since the publication of the PQI paper, the DOGMA metric{cite}`Dohmen2016-iv`, which scores proteomes based on conserved arrangements of protein domains, has been added to the PQI website. 

###### Potential improvements
The mapping from raw score to star rating for some metrics could be improved. For example, homo sapiens has ‘0’ X-content (the lowest/best possible value), but 4.1 stars.

[//]: # (TODO: Rephrase)
PQI was created with the potential to add further quality metrics by other researchers. Although the DOGMA metric was added and it is based on BUSCO{cite}`Simao2015-gc`, it might be sensible to add BUSCO, since it has become very popular, and any proteome/genome quality index would probably be seen as incomplete without it. The continued inclusion of the CEG Domain Combination Homology metric may be questioned since CEGMA is no longer being updated (nor is the KEG database upon which it is based), but BUSCO and CEGMA may be complementary since BUSCO has a weaker requirement for inclusion in the set of proteins, which means that it has more proteins, and vice versa.

To impact on the problem for model organisms for clade-based metrics, one solution would be to treat model-organisms differently in these circumstances, for example score clades containing model organisms against the model organism. An more subtle alternative to this would be using the NCBI’s Assembly database{cite}`Kitts2016-eo`, which has been released since PQI was published. The database tracks how many assemblies there are for each species as well as how many versions of each assembly there has been. This information could be used to weight the importance of proteomes in clade-based metrics. The number of assemblies and versions could also form a separate score.

Sequencing depth (coverage) and read length are also known markers of genome quality{cite}`Sims2014-df`. Average coverage for an assembly (except reference genomes) is also available in the NCBI Assembly database{cite}`Kitts2016-eo`. 

Some “third-generation” sequencing technologies create much longer read lengths, but potentially lower accuracies. A third category of metrics “technology-based” metrics could exist for proteomes where the metric is only really comparable within similar types of technologies. If technology-based metrics were implemented, it may also be sensible to have some metrics which only exist for specific technologies. For example, for nanopore sequencing, we could implement an indel-based quality metric{cite}`Watson2019-pz`. Including sequencing-technology-specific metrics may encourage contributions from other researchers who specialise in particular technologies. Sequencing technology is also available in the NCBI Assembly database{cite}`Kitts2016-eo`. 

The development of additional measures is required to deal with other potential problems in genome sequencing, for example GC content, amino acid bias, or contamination from other genomes. 
