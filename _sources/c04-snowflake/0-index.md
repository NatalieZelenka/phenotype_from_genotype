(c04-snowflake)=
# Phenotype prediction with Snowflake

[//]: # (TODO: Check)
[//]: # (TODO: Cite ALSPAC here)
[//]: # (TODO: Put in other datasets if I mention them)
[//]: # (TODO: Cross-reference to the sections of the Chapter)

This chapter describes the Snowflake algorithm for phenotype prediction that I developed in collaboration with Jan Zaucha, Ben Smithers and Julian Gough. 
The development of `snowflake` resulted in a patent{cite}`Gough2017-ik`, of which I am an author.
This chapter deals with the functionality and design of the Snowflake algorithm, while the {ref}`next<c05-alspac>` describes it's application to the ALSPAC dataset.

At it's heart, Snowflake is a {abbr}`CLI (Command Line Interface)` tool and private Python package that allows the user to detect outliers for each phenotype of interest, according to their genotype. 
Individuals with unusual combinations of variants in highly conserved protein domains associated with a phenotype will score highly for (be indicated as likely to have) a phenotype.

The original idea for Snowflake was Julian's, as well as the initial Perl implementation. 
The initial translation of the code from Perl to Python was carried out by Ben. 
Working from Ben's translation, Jan and I both worked on increasing the algorithms functionality and robustness together, before forking the project into two different versions which we each took ownership of.

[//]: # (TODO: List features I am responsible for here, and link to the sections below where I describe them)

```{admonition} Contributions in this chapter
:class: hint
 - Writing part of the patent{cite}`Gough2017-ik` relating to intrinsic dimensionality.
 - Software development to increase and test the algorithm's functionality, including:
    - With Jan and Ben:
        - Running with different formats and numbers of inputs and background cohorts
        - Dealing with missing calls 
        - Development of tools to create input files for Snowflake
        - Improvements to memory-usage and speed
    - And individually:
        - Creation of inputs to Snowflake
        - Alternative clustering and scoring methods, particularly for intrinsic dimensionality
        - Scoring outputs
        - Further improvements to speed and memory usage
        - Multiple imputation for missing calls
        - Inclustion of dimensionality reduction        
```
