(snowflake-discussion)=
# Discussion

<!--

## Software Engineering Best-practices
The most time-consuming aspect of working on Snowflake was it's Research Software Engineering requirements, writing and testing the research code to ensure that it ran in a reasonable time and without bugs, and giving it the features needed to be able to test it's use as a research tool.

Test suite
Documentation
??? Publishing

## Dependencies and interoperability
[//]: # (TODO: Write from RSE oint of view)
The phenotype predictor relies heavily on all forms of it's input data: `dcGO`, `FATHMM` and the background cohort.
`dcGO` decides which SNPs we consider at all for a phenotype, while `FATHMM` decides to what extent SNPs within that set would be interesting if we see a rare combination.
And how rare the combination appears is defined by the background cohort.
A limitation of this method is that it's hard to test Snowflake's approach to combining these types of data and clustering independently from these inputs.

Snowflake uses FATHMM-MKL rather than the newer FATHMM-XF. 
[//]: # (TODO: Cite FATHMM-XF and various independent)

FATHMM-XF is my many independent researchers, the most accurate variant prioritisation tool currently available, much more so than FATHMM-MLK.
FATHMM-MKL is constrained to build 37 of the human reference genome which is no longer up to date.

### Background
- 1000 genomes has different priorities than us: does not care about rare SNPs - most likely to cause rare diseases
- As diverse a bg set as we can get, but not very diverse.
- Size/diversity of background set constrains how many SNPs we can hae
- Same problem as PQI, the results are very sensitive to our background set (test?)

[//]: # (TODO: rename next section)

## Difficulty in finding a test set
[//]: # (TODO: reqrite - look at what Jan wrote)
[//]: # (TODO: Rewrite in light of the fact that all the other phenotype predictors managed... just say something about coverage being massive in Snowflake)

The `snowflake` project could be considered "blue-sky" curiosity-led research. 
The motivation for creating `snowflake` was our curiosity in seeing if the resources of Computational Biology could0 be used for the practical outcome of creating phenotype predictions.
This was far from incremental, since other leading approaches predicted phenotypes on a phenotype-per-phenotype basis, or restricted the problem to prioritising variants.
We can only test `snowflake` on data sets with both genetic and phenotype information across many phenotypes, which means it is very difficult to conclusively test (we have very low statistical power over all phenotypes).

It is disappointing that the phenotype predictor does not produce statistically significant results.
However, the phenotype predictor may yet be useful for revealing candidate SNPs for certain kinds of diseases, and when a suitable data set becomes available (e.g. through the growing number of publicly available genotypes on platforms such as OpenSNP{cite}`Greshake2014-mp`), this method will still be ready to be tested. 
An alternative validation would be experimentally testing a prediction (e.g. with knockouts) of a phenotype with a highly interesting distribution of scores.

[//]: # (TODO: Write + cross reference)
[//]: # (TODO: Negative results are still interesting)


[//]: # (TODO: How many terms appear to be successful? How many more than we would expect? Does this imply how much of our biology is influenced by missense mutations versus other tyoes? Or is it more of a relfection of the quality of our data.)

[//]: # (TODO: Optional: Phenotypes where haplotype is not how things are clustering versus where they are)

[//]: # (TODO: Discuss that genotyping data may not collect the right information for many phenotypes. Since genotype data contains far less variants.)
-->

(snowflake-limitations)=
## Limitations

<!--
### Curse of dimensionality/feature selection
[//]: # (TODO: Write)

There are too many snps for our number of individuals
-->

(genotype-data-problems)=
### Genotype data
Genotype chips contain only a small fraction of the known disease-causing variants.
For example, 23andMe tests for [only 3](https://www.23andme.com/brca/) of thousands of known variants on the BRCA1 and BRCA2 genes implicated in hereditary cancer. 

(equivalent-terms)=
### Equivalent terms
[//]: # (TODO: Add examples from a polist file)
Despite much development effort, there remain some idiosyncrasies to the predictor. 
For example, DcGO can map multiple terms to the same set of SNPs. 
This can sometimes be a diverse group of phenotypes which do not tend to co-occur in individuals and when this occurs, it is likely that we cannot make a good prediction. 
A semantic similarity measure, such as GOGO{cite}`Zhao2018-rw` or Wang’s method{cite}`Wang2007-yc` could be used to check this, and update the confidence score accordingly.

(coverage)=
### Coverage: Synonymous SNPs, nonsense and non-coding variants
[//]: # (TODO: Explain why not included)
There are also clearly many aspects of the molecular biology mentioned in {numref}`chapter %s<c02-biology-bg>` that are not represented in the model used by the phenotype predictor. 
For example nonsense mutations, synonymous SNPs, regulatory networks, and non-coding variants. 
Updating the predictor to include these things could potentially give the predictor enough power to be validated on existing data sets. 

For example, non-coding variants could be included by extending `dcGO` annotations to SNPs in linkage disequilibrium, and using the non-coding version of `FATHMM`, `FATHMM-XF`{cite}`Rogers2018-rc`.

(dcgo-expression-problem)=
### Localised expression
[//]: # (TODO: Give actual example of a polist file)

Another example is that dcGO does not take account of the environment of the cell (e.g. tissue-specific gene expression) in its' predictions. 
Although domains which are statistically associated with phenotype can be present in a protein, there is no guarantee that the protein will have the opportunity to impact the phenotype (be transcribed).

[//]: # (TODO: Cross-ref next Chapter)

In investigating some of the ALSPAC phenotype predictions, I identified that some of the predicted dcGO relations between proteins and ontology terms may not be expressed in the tissue of interest. 
This makes sense, since dcGO makes predictions on the basis of structure, but it's common in molecular biology that cells, proteins or genes have theoretical functionality that is repressed or silenced by another mechanism, for example most human transposable elements or silenced, or in this case, repressors preventing gene expression in some cell types.
Filtering out predictions for SNPs in these repressed genes is therefore a potential route to improve Snowflake, and this is the focus of the next part. 

<!--
### Miscellaneous
[//]: # (TODO: Write)
[//]: # (TODO: Cite PhenIX)
Successful phenotype prediction methods are successful for different reasons. 
For example, PhenIX performs only for human genetic diseases, and includes information about the mode of inheritance of the disease in order to filter out false positives.
-->

(snowflake-ethics-self-assessment)=
## Ethics self-assessment

```{epigraph}
Your scientists were so preoccupied with whether or not they could, they didn't stop to think if they should.
 -- Dr Ian Malcolm, Jurassic Park, Michael Crighton
```

Like the creation of dinosaurs, the Snowflake methodology itself (rather than a particular use of it) is not the sort of research that usually requires ethical review by Institutional Review Boards (IRBs).
This is because most IRBs focus on issues of informed consent, data privacy, and other matters which could cause legal problems for universities, while Snowflake's core methodology uses only publicly available data.
As {ref}`I previously mentioned<ethical-considerations-phenotype>`, there are more general (wider, societal) ethical considerations relating to research in predicting phenotype.

```{margin} Data Hazards
:name: data-hazards
The [Data Hazards](https://very-good-science.github.io/data-hazards/) framework is a set of resources to help data science and methodological researchers apply ethics hazards labels to their work. These resources include a set of [hazard labels](https://very-good-science.github.io/data-hazards/contents/materials/workshop/data-hazards.html) inspired by COSSHH chemical hazard labels with suggested safety precautions, as well as materials to help researchers apply them.

Just as we still use bleach, but do so wearing gloves, data hazard labels are not necessarily statements against doing or using the research, but rather an appeal to "handle with care".
Similarly, data hazards aren't meant to be statments of certainty or likelihood of the hazards occuring. 
They represent worst-case scenarios and apply not only to the specific research project, but also future impacts of further deployments.

```

With this in mind, I performed a self-assessment of the worst-case scenario outcomes of this research, in order to understand potential issues and think about what precautions should be put in place to avoid them.
These extend out from this research itself, imagining future deployments.
To this, I used the {ref}`Data Hazards<data-hazards>` framework: a framework that is currently under development, and which I am currently working with the data science research community to develop.
{numref}`data-hazards-snowflake` contains the hazards that I felt applied to Snowflake, the reasons why, and what I recommend could be done to prevent these worst-case scenarios.

[//]: # (TODO: Reference minority groups less likely to be represented in medicine)

```{list-table} The seven data hazards which I assessed as applying to Snowflake.
:header-rows: 1
:name: data-hazards-snowflake
:align: center

* - Label name
  - Label description
  - Label image
  - Reason for applying
  - Relevant safety precautions
* - **Contains Data Science**
  - Data Science is being used in this output, and any negative outcome of using this work are not the responsibility of “the algorithm” or “the software”, but the people using it.
  - ```{image} ../images/general-hazard.png
    :alt: fishy
    :width: 200px
    :align: center
     ```
  - Snowflake uses data, makes predictions, and uses unsupervised learning.
  - When snowflake is deployed in new contexts (e.g. patent licenses sold), it should be done with the understanding that the licensee becomes accountable for using it responsibly.
* - **Reinforces existing biases**
  - Reinforces unfair treatment of individuals and groups. This may be due to for example input data, algorithm or software design choices, or society at large.
  - ```{image} ../images/reinforce-bias.png
    :alt: hazard label for reinforces existing bias
    :width: 200px
    :align: center
     ```
  - Project does not check that the algorithm works just as well for non-white races, and we would expect it to work less well for them since they are less represented in the input data linking variants and diseases{cite}`Popejoy2016-tx`. 
  - Snowflake's efficiacy should be tested separately for each demographic that any deployment may effect.
* - **Ranks or classifies people**
  - Ranking and classifications of people are hazards in their own right and should be handled with care.
  - ```{image} ../images/classifies-people.png
    :alt: hazard label for ranks or classifies people
    :width: 200px
    :align: center
     ```
  - Project does not check that the algorithm works just as well for minority groups, who are less likely to be represented in the input data linking variants and diseases. 
  - + Snowflake's efficiacy should be tested separately for minority groups, before deployment outside research (e.g. healthcare). 
    + Appropriate phenotype terms should be curated before deployment (e.g. removing things like social behaviours, "intelligence" related terms, etc)
    + When or if to share rankings should be consdered carefully.
* - **Lacks Community Involvement**
  - This applies when technology is being produced without input from the community it is supposed to serve.
  - ```{image} ../images/lacks-community.png
    :alt: hazard label for lacks community involvement
    :width: 200px
    :align: center
     ```
  - The communities of people with the phenotypes have no current involvement in this process.
  - Relevant communities should be asked about their feelings towards phenotype prediction before deployment in order to curate a list of appropriate phenotype terms.
* - **Danger of misuse**
  - There is a danger of misusing the algorithm, technology, or data collected as part of this work.
  - ```{image} ../images/misuse.png
    :alt: hazard label for danger of misuse
    :width: 200px
    :align: center
     ```
  - The phenotype predictor is not expected to be accurate for all phenotypes, but It could even be used to try to predict phenotypes that are caused by the environment or regions of DNA it does not consider, if these are defined as genetic phenotypes in other literature.
  - If deployed outside of research, Snowflake should be tested for different types of phenotypes and which ones it does work for should first be understood.
* - **Difficult to understand**
  - There is a danger that the technology is difficult to understand. This could be because of the technology itself is hard to interpret (e.g. neural nets), or it’s implementation (i.e. code is hidden and we are not allowed to see exactly what it is doing).
  - ```{image} ../images/difficult-to-understand.png
    :alt: hazard label for difficult to understand
    :width: 200px
    :align: center
     ```
  - Doesn’t use "black-box" machine learning (e.g. deep learning), but has closed source code and a complicated data pipeline.
  - + If published for research, the code should be Open sourced and the code should be thoroughly documented and tested.
    + If provided for members of the public, explainers should be created similar to [those that 23andMe has](https://www.23andme.com/en-gb/brca/).
* - **Privacy hazard**
  - This technology may risk the privacy of individuals whose data is processed by it.
  - ```{image} ../images/privacy.png
    :alt: hazard label for difficult to understand
    :width: 200px
    :align: center
     ```
  - Individual’s genetic data is required to run the phenotype predictor. This has many privacy risks, for example identification, use by insurers, being contacted by unknown relatives.
  - + Ensure there is explicit and well-informed consent from any future participants/users.
    + Store data securely.
```

Despite the tongue-in-cheek use of the Jurassic Park quote opening this subsection, I do think that phenotype prediction is something that we should attempt, due to its potential to help people.
In "stop\[ping] to think" about it, however, I applied 7 of the 11 existing data hazard labels, and set out some specific precautions for using it that I hope will be seriously considered by anyone using the method further.
While some of these may seem far-fetched, Snowflake has already been trialled by a genomic analysis company used in clinical decision support.

The question of whether we "could" predict phenotype accurately is also a huge ethical barrier to using it at present. 
Currently, it's not clear to what extent, or for which types of variants, the phenotype predictor works.
The next chapter explains my attempts to validate the predictor using the ALSPAC dataset.

