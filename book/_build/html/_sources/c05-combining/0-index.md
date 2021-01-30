(c05-combining)=
# Combining RNA-seq datasets

[//]: # (TODO: Link to outputs, i.e. combined dataset)
[//]: # (TODO: Cross-ref to this chapter's sections)
[//]: # (TODO: Check if UBERON has been mentioned yet: cross-ref - if not, mention in Background)
[//]: # (TODO: Check if I want to say UBERON or Uberon)

In this Chapter, four tissue-specific gene expression data sets are combined into one harmonised data set, which is available to the research community - as well as being useful in {ref}`the next Chapter<c06-filter>`.

The constituent data sets were chosen to minimise potential data artefacts, to maximise information about different tissues, and to ensure that we have as balanced an "experimental design" as possible (which is important for batch effect removal).
The meta-data about the experiments is also combined, and mapped to the UBERON tissue ontology, to ensure the interoperability of the final combined data set.
A simulated gene expression data set was created to test whether batch correction was appropriate for this data set. 
And after testing ComBat on the simulated gene expression data set, it was applied to the combined tissue-specific experiments data set.

All work in this Chapter was conducted independently. 