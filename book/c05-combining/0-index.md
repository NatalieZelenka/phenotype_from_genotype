(c05-combining)=
# Combining RNA-seq datasets

This chapter describes my attempts to create a simulated tissue-specific dataset and to combine gene expression data from 4 large tissue-specific RNA-Seq experiments. All work in this chapter is my own.

## Motivation

Gene expression data measures the number of transcribed proteins in a sample at a specific time.
It's a popular experimental technique as demonstrated by the 3,564 studies and 112,225 assays currently available on Gene Expression Atlas website {cite}`Petryszak2016-je`. 
Researchers use this data to characterise gene function.

Yet each individual measure of expression is only a snapshot of what a gene can do. 
It only tells us about the transcription of proteins at that one time. 
If we want a full understanding of what a gene does, we must understand how it's expressed in a variety of scenarios. 
For example, in different tissues, from different people, at different times of day, and across many repeats. 
That kind of data would allow us to answer questions that aren't currently possible. Data to enable this is not easy to come by. 
It would be too expensive for one experiment to measure so many samples. 

Combining expression data from many different experiments could overcome this problem. 
There are already an example of this happening for two experiments{cite}`Wang2018-rz`. 
It would result in the rich information about genes that we desire. 
Unfortunately, this approach reveals another problem: batch effects. 
Batch effects are measurement artifacts that appear due to differences in experimental protocol.
Their prevalence makes gene expression experiments very difficult to compare or combine.

This chapter combines four gene expression data sets, collating sample and tissue information about them into a common format. A simulated data set for tissue-specific batch-effected data is created as a starting point for exploring batch effect removal for this combined data set.

[//]: # (TODO: Explain the structure of this chapter here)
[//]: # (TODO: Add figures)
[//]: # (TODO: Tidy structure of 0-index and 1-background)
