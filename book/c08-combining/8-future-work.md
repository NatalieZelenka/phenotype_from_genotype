## Future Work

### Mapping improvements
Firstly, there are also some mapping improvements which might improve the quality of the data set as a resource for other people. 

**Multiple membership of tissues and cells** 
It is sometimes appropriate for samples to map to two apparently distinct Uberon terms. 
For example, leukocytes are known to be part of the immune system, but are found in the blood. 
In the FANTOM mapping, they would be mapped by name to blood, but by ontology to immune system. 
In this case, we could imagine mapping to two Uberon terms rather than defaulting to where the cells were collected, since researchers interested in blood or the immune system would both like to access the information. 

In addition, it would be preferable to map simultaneously to tissue and cell type, since this enables researchers to, for example, make queries about expression about the same cell types in different tissue locations, query the data set against scRNA-seq data, or simply find cell as well as tissue specific information.  
This could be achieved partly with relative ease by using the ontological mapping between CL and Uberon. 
Improvement of the CL-Uberon mapping would then allow for a complete understanding of which cell types are in a tissue, but not their relative abundances. 

**Cell type deconvolution:**
In order to understand the relative abundances of cell types in each sample, a cell type deconvolution programme (e.g. CIBERSORT{cite}`Newman2015-le`, BSEQ-sc{cite}`Gaujoux_undated-ru`, or MuSiC{cite}`Wang2019-hc`) could be used.
These algorithms estimate percentages of cell types making up a tissue. 
This would require the input of a large scRNA-seq data set as input, and there doesn’t yet exist enough diversity to deconvolve all tissue types.
As well as improving the mapping, this is likely to improve the quality of the batch effect correction.

### Simulation to ensure suitability for ComBat
[//]: # (TODO:Write: medium priority)
The obvious next step is to test batch effect removal such as ComBat on the simulated data set. 

### Alternative batch effect removal
[//]: # (TODO: Make sure I explain somewhere what scRNA is)

Since ComBat is known to suffer from unbalanced datasets, an alternative might be used: Mutual Nearest Neigpiphbour (MNN) method for bulk RNA-Seq data. 
MNN is a batch effect removal methodology for scRNA-seq data which was recently developed by Haghverdi et al{cite}`Haghverdi2018-ig`. 
The benefit of this methodology (in addition to its superior batch effect removal) is its ability to cope with unbalanced sample compositions.  
Despite being developed for scRNA-seq, it works well on heterogeneous tissues like the pancreas, so it may be possible to use or extend it to bulk RNA-seq, especially if cell type deconvolution can be employed on the bulk RNA-seq. 
If this was possible, using an MNN-based method would allow us to overcome ComBat’s requirement for a balanced experimental design since it requires only one cell in common between, although more cells in common will increase the accuracy. 

As the number of scRNA-seq experiments increase, including them in a combined dataset of tissue-specific expression will become more statistically viable. 
A prerequisite of including scRNA-seq data would be the use of an alternative batch effect removal algorithm that is suitable for single cell data, (e.g. MNN).
It would be interesting to compare how the expression of cells which can exist in multiple tissue types differs across those different tissue types, and to investigate whether some gene expression is truly tissue-specific rather than cell-type specific.

