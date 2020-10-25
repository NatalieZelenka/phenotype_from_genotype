
## Data
### Criteria for choosing datasets
Datasets were chosen from the EBI’s Gene Expression Atlas (GxA). A major benefit of the GxA is that experiments using the same sequencing technology are re-analysed by GxA using the same data analysis pipeline (iRAP[94] for RNA-Seq). In addition to ensuring the quality of each dataset included, and running it through the same pipeline, the GxA adds additional metadata for the experiments by using the literature to biologically and technically annotate each sample. 

Datasets from the GxA were chosen based on the following requirements: 
Next generation sequencing, including RNA-Seq and CAGE (no microarrays).
Breadth of tissues and genes included (after quality control) to aid batch correction by facilitating the most balanced dataset design in terms of batch (experiment) to group (tissue), and in order to have good coverage of genes and tissues, which is necessary for downstream use.

Not disease-focused. In order to reduce the complexity of the analysis and the interpretation of the resulting dataset, samples of diseased tissues or cell lines were discarded. Experiments where the focus of the dataset was to investigate a particular disease or classes of diseases were discarded. Besides reducing the complexity of the analysis, this choice also made sense based on the previous guideline, since most disease datasets (with the exception of cancer datasets) tended to have a narrow breadth of tissues. I feel that including disease gene expression would be a natural extension to this work if the data allowed for it, but most GxA baseline gene expression experiments which listed organism part as a variable were focused on cancer, which is known to be tissue-non-specific[49,77].

Of the over 3000 experiments in the GxA, 1134 contain human samples, and just less than 3% of those (30 experiments) are baseline gene expression experiments. Of these there are 4 which offer a good coverage of non-disease organism parts. The data sets that were chosen to be used in the combined data set are detailed below.

#### Measures of gene expression
As described in the introduction chapter, there are many ways to measure which proteins are being created. Here, I justify my choices of measures to include in the combined dataset.

##### Gene expression vs protein abundance
Gene expression levels are not necessarily strongly correlated with protein abundance; this has been found in mice[95], yeast[96], and human[97]. In human, spearman correlations between protein abundance and gene expression levels vary between 0.36 and 0.50, depending on tissue, meaning that they are only weakly or moderately correlated[97].
There are many interacting reasons why this is the case. One reason is that there is something preventing the mRNA from being translated, such as slow codons, the temperature, ribosome occupancy, or regulatory RNAs and proteins[98]. In these cases, the DNA is transcribed into mRNA, but the protein is never produced, meaning that using gene expression data as a measure of how much protein is produced would be overestimating the protein abundance. If these factors were a large contribution to the weak correlation, it could provide better results to use protein abundance data instead of mRNA abundance data to make predictions about how proteins are affecting human phenotypes.
On the other hand, it could equally be possible that proteins are being produced, but not measured by protein abundance techniques. Protein half-lives range over orders of magnitude from seconds to days[98,99]. In this case, gene expression data may be a more reliable measure of protein production than protein abundance, since proteins may degrade before being measured. In yeast, protein degradation was shown to be the largest contribution to the protein-mRNA correlation compared to codon and amino acid usage (the two other factors estimated in the study), and more influential than those other two factors combined[100].
In summary, there's no perfect measure of translation, but since gene expression data is more readily available, and protein degradation appears to account for most of the differences between correlations, gene expression data presents the best proxy for translation for the downstream uses discussed here.

##### Gene expression vs Transcript expression
It's likely that transcript expression data would provide more insight than gene expression data if it were available, since it is likely that there are tissue-specific transcripts which do not correspond to tissue-specific genes, e.g. where different transcripts from the same gene are expressed in different tissues. Transcript expression data, however, is harder to come by and this approach relies on a wealth of available data. Furthermore, transcript expression data can be straightforwardly converted to gene expression data (by summing over the transcripts), while the conversion of gene to transcript expression data is decidedly less accurate. When transcript-expression (CAGE) measurements are aggregated at the gene/protein level, measures of tissue-specificity have been found to largely (75-93%) match up with measures of tissue-specificity resulting from gene-expression measurements, as found in a comparison between the HPA and FANTOM5 experiments[101]. 
For these reasons, I have taken a gene-centric approach here. It may be important, however, to consider whether a gene has multiple transcripts in downstream analysis, for example, if including tissue-specific gene expression information when predicting the function of a protein-coding SNV (since it may not be in the relevant transcript).

##### Inclusion of CAGE data
CAGE is transcript expression, rather than gene expression, and there are likely to be different transcripts measured by CAGE than by RNA-Seq. As mentioned above, however, it is possible to calculate gene expression from transcript expression. It’s also possible to map between CAGE transcription start sites and existing transcript IDs that may be featured in RNA-Seq arrays. When this is done, it has been observed that the results of CAGE are comparable to those of RNA-seq, so the inclusion of CAGE data in a combined dataset is reasonable.

“We found that the quantified levels of gene expression are largely comparable across platforms and conclude that CAGE and RNA-seq are complementary technologies that can be used to improve incomplete gene models”[102]

### Chosen data sets
In addition to the FANTOM5 data (described in the previous chapter), three other large gene expression experiments were chosen:

#### Human Protein Atlas
The Human Protein Atlas (HPA) project[103,104] aims to map all human proteins in cells (including subcellular locations), tissues and organs. The HPA project’s data is not limited to the gene expression data that can be found in GxA, but that is the only part of the data that is used here. The gene expression data that was used (E-MTAB-2836 in GxA) excludes cell lines and includes tissue samples of 122 individuals and 32 different non-diseased tissue types. 

#### Genotype Tissue Expression
The Genotype Tissue Expression (GTEx) project[105] was developed specifically for the purpose of studying tissue-specific gene expression in humans and gene expression data from over 18,000 samples, including 53 non-diseased tissue types and 550 individuals (ranging in age from 20s to 70s). 

#### Human Developmental Biology Resource
The Human Developmental Biology Resource (HDBR) Expression data[106] is slightly different from the other data sets in that contains a much narrower range of sample types. All HDBR samples are human brain samples at different stages of development, ranging from 3 to 20 weeks after conception. 

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```