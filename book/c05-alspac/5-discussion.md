(alspac-discussion)=
# Discussion
[//]: # (TODO: List phenotypes)
The results of this chapter show that Snowflake cannot currently be used to accurately predict the following phenotypes in the ALSPAC cohort: .

(alspac-phenotype-problems)=
## Selection of phenotypes
For valid ethical reasons, it was only possible to request a small number of phenotypes from ALSPAC.
Snowflake isn't expected to work for all phenotypes, since we know there are many other mechanisms (some not even genetic) behind phenotype besides only the disruption of proteins through missense SNPs in protein-coding genes.
The fact that Snowflake was not successful in predicting any of the requested phenotypes could be an indication that none of these phenotypes has this mechanism behind it.
Alternatively, it could be an indication that Snowflake is not a successful method for predicting phenotypes even in these cases, and there are many reasons why that could be the case since Snowflake relies on a lot of other pieces of research and software to function. 

In selecting phenotypes, I considered only (1) whether Snowflake considered these to be phenotypes where it could make a confident prediction and (2) whether the phenotypes in ALSPAC could be used to validate this prediction.
I did not consider additional information that might indicate whether these were phenotypes we might expect to be able to predict, for example, whether these phenotypes were heritable, or consider whether they are desirable to predict.
Since I chose these purely by looking at the distribution of scores for Snowflake, our lack of promising results could be an indication that the phenotype-score (finding interesting distributions of phenotypes) is unsuccessful.

[//]: # (TODO: Aside missing heritability)
A more interesting test of Snowflake's abilities might be to choose phenotypes with high heritability, and specifically high missing heritability.

[//]: # (TODO: discuss the heritability of the requested phenotypes)

(alspac-overlap-problem)=
## Overlap between training and validation data
ALSPAC is a popular cohort study for use in GWAS analyses.
Many links between genotype loci and phenotypes have been published from this data set, for example loci associated with birthweight{cite}`Horikoshi2013-la`, asthma and allergies{cite}`Hinds2013-gi`, autism spectrum disorders{cite}`Robinson2016-pj`, problematic peer relationships{cite}`St_Pourcain2015-be`, and lung function{cite}`Repapi2010-vx`.
This data informs GOA genotype-phenotype annotations, and through dcGO this data could already be present in Snowflake, meaning that there may be in some sense, overlap between the training and validation data, which could overestimate the accuracy of the predictor on unseen data{cite}`Wray2013-nl`.

For this reason, I do not think that it is sensible to try any further to use ALSPAC to validate or test Snowflake.

