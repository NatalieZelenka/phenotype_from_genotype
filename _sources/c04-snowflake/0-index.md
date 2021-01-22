(c04-snowflake)=
# Phenotype prediction with `Snowflake`

[//]: # (TODO: Cite ALSPAC here)
[//]: # (TODO: Put in other datasets if I mention them)
[//]: # (TODO: Cross-reference to the sections of the Chapter)

This Chapter describes:
 - The `Snowflake` algorithm for phenotype prediction and my contributions to it, including:
    * Development to increase the algorithm's functionality, including:
        + Running with different formats and numbers of inputs and background cohorts
        + Dealing with missing calls 
        + Alternative clustering and scoring methods
        + Development to outputs
    * Improvements to memory-usage and speed
    * Development of tools to create input files for the `Snowflake`
 - Comparisons of possible ways to cluster SNPs which were investigated in the creation of the algorithm.
 - Attempts to validate the algorithm with it's application to the ALSPAC data set.

The development of the  `Snowflake` algorithm resulted in a patent{cite}`Gough2017-ik`, on which I am an author.

---
**Page References**

```{bibliography} /_bibliography/references.bib
:filter: docname in docnames
:style: unsrt
```