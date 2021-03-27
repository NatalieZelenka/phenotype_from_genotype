(c07-conclusion)=
## Conclusion
[//]: # (TODO: cross-ref this section, add in all publications incl. PQI, SUPERFAMILY)
[//]: # (TODO: Mention complexity... That I wanted to study that in relation to biology, but that the data doesn't really seem to be there quite yet: cite can a biologist fix a radio. Mention network with diffusion. )

To conclude:
- I present my contribution towards the `snowflake` phenotype prediction method, and it's use for finding unusual combinations of SNPs with possible explanatory mechanisms for phenotype.
- I have created research outputs in terms of a combined gene expression data set, and research software, which are useful:
    - To link existing data sets and ontologies
    - To discover inconsistencies in data and ontologies
    - For downstream research
- I showed that bringing baseline gene expression data into protein function predictions will (with current data) slightly increase the accuracy of those predictions. 

In my attempts to make explanative genome-wide predictions about protein function, I have continuously bumped up against the limits of what is possible with the data that we currently have.
These resources are absolutely vital to the efforts of computational biology, and are amazing feats of research and engineering, but there are some limits at present in using them for "big-picture" biology.
As such, some of the most satisfying work has been to contribute back to some of these resources.
Through linking them, and finding inconsistencies, I have in some small way been part of science's self-correcting mechanism, and hope that this brings us a little closer to their use for genome-wide explanatory predictions.

### Future work
[//]: # (TODO: Cross ref future work in individual chapters:)
While I describe many possibilities for future work in the individual chapters, there are some particular avenues that I would be keen to explore. 
My immediate next steps will be to make the tissue specific gene expression data set created in {ref}`Chapter 5<>` more usable, and to apply the tissue-specific gene expression data set to the phenotype prediction filter described in {ref}`Chapter 6<>`. 
I would like to make these contributions available as papers.

I also look forward to seeing what the researchers now working on the `snowflake` will be able to do in terms of validation and continued development with newer and larger data sets.

### Closing remarks
[//]: # (TODO: Mention Research Software Engineering, automation, etc)
[//]: # (TODO: Cite Uri Alon/Turing patterns)

I came from a background of mathematics and physics, and wanted to do a PhD in Complexity Sciences and mathematical biology in particular because I loved papers like Uri Alon's motifs in Protein-protein Interaction networks and Turing patterns that linked simple maths to complex biology that had really been measured, and because I liked programming (badly - and in Matlab).
I hadn't worked with much data, I didn't know any software engineering best practices or much biology at all, and I wasn't aware yet of how different a challenge predicting phenotype from genotype would be compared to a "toy" mathematical modelling problem.

Before I joined the Gough group, someone had written the following famous quote{cite}`Dobzhansky2013-no` on a whiteboard in my office:

```{epigraph}
"Nothing in biology makes sense... <br>
...except in the light of evolution"
```

By the time I arrived, however, someone had rubbed off the second line, leaving only "Nothing in biology makes sense..." and since I'd never heard the full phrase before, I didn't question this.
In fact, as I tried to piece together the accepted model of how genotype influences phenotype, I found myself agreeing!
Compared to maths and physics, there is so much in molecular biology that we don't know: there are so many moving parts and there is *always* an exception to the rule.
This is true for the processes themselves, and when you look a little closer - also the data that is collected.
Over time, my endless questions became less frustrating and more and more energising as I became a better judge of what questions it was possible to answer, and more able to create the resources needed to answer them.

[//]: # (TODO: Give example of snowflake not being useless)
[//]: # (TODO: Cross-reference)
Working on `snowflake` gave me a bird's eye view of our model of the connection between genotype and phenotype: and the data sets we have about that connection.
It is, of course, regrettable that we could not access enough data to conclusively test it as a phenotype predictor.
However, I have found a small way in which to improve phenotype predictions, with a mechanistic reason behind it - and I have found value in creating and contributing to resources which I hope will lead us towards more.