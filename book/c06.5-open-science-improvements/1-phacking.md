<!--
Two other useful quantities of NHST are effect size and statistical power. 
Effect size is the magnitude of the effect found by the statistical test. 
A very small effect can only be detected with a large enough sample size. 
Statistical power is a measure related to the type 2 error (false negatives), it is $1-\beta$ where $\beta$ is the false positive rate. 
A statistical power of 80% is customary, where it is calculated, in which case there is a 20% chance that a result is a false negative if the null hypothesis is accepted. 
A very highly powered test with a high (non-significant) p-value represents strong evidence that the null hypothesis is true, although it may often be reported as “failing to reach significance”. Low-powered tests, coinciding with low sample sizes, mean that both the acceptance or rejection of the null hypothesis is likely to be unreliable. 

[//]: # (TODO: Check math below and formatting.)
[//]: # (TODO: Add link to dance of the p-values)
P-values do not have a high prediction value for reproducibility, since they have a high spread, even when a test is reasonably highly powered. 
Statistician Geoff Cumming refers to this as the “[dance of the p-values](https://www.youtube.com/watch?v=5OL1RqHrZQ8)”. 
Instead, a measure of the expected truth of a finding can be estimated from the proportion of hypotheses that are true in a given field, the statistical power, the p-value threshold as:

$$
ppv=\frac{(1-\beta)p_{true}}{p_{true}(1-\beta-\alpha)+\alpha}
$$

Where $ppv$ stands for positive predictive value and $p_{true}$ is the proportion of true hypotheses in a field{cite}`Ioannidis2005-mo`. 

For this version of the formula (there is also a version that includes bias, which was instrumental in the Ioannidis’ claim that “most published research findings are false”{cite}`Ioannidis2005-mo`), and standard choices for power and statistical significance of $\alpha=0.05$ and $\beta=0.2$, we would expect more findings to false than true if $p_{true}<0.0588$ (3.s.f). 
That might seem like a small number, but in some bioinformatics experiments, we hypothesise that millions of SNPs may be responsible for a trait, when only small numbers are. 
On the other hand, if half of researchers hypotheses were correct for a given field ($p_{true}=0.5$), the formula would yield $ppv=0.941$ (3.s.f.), but the low reproducibility of GWAS results, gene annotations, etc, implies that the proportion of true hypotheses is less than this.

The same approach can be used to calculate the limit for $p_{true}$ for which we’d expect there to be more false positives than false negatives. 
Using the same values for and  and , we get $p_{true}=0.2$, i.e. if less than 20% of hypotheses are true, then we are more likely to get false positives than false negatives. 
This is interesting as most published scientific results are claiming a positive result, so we are essentially erring on the side of publishing erroneous errors.

[//]: # (TODO: Instert image and fix reference and citations/links)

### Pre-registration

A more interesting solution is pre-registration, as used in clinical trials. 
This involves a detailed publication in advance of the analysis protocols that will be used in order to prevent tweaking analysis based on seeing the data. 
This solves p-hacking related problems, and makes a distinction between hypothesis-generating and hypothesis-testing research.

### Registered reports
Registered reports are an attempt to remove these problems associated with publication bias, by linking the concept of pre-registration with that of publishing. 
Essentially, authors submit their introduction and methods section to a journal and at this point they undergo peer review and the journal agrees to publish the results, regardless of the result. At the time of writing over 170 journals were accepting registered reports and the number has been growing in recent months, across disciplines, although they are currently most popular in psychology and neuroscience{cite}`Hardwicke_undated-jj`. 
This solution also offers peer-review at a more helpful stage in the manuscript, when it’s still possible to make changes to the experiment.


<!--
#### Reproducibility in bioinformatics
In a field that has long had a huge number of open data repositories, and a relatively high level of statistical knowledge among researchers, in some ways bioinformatics might be expected to be ahead of the curve in terms of reproducible research. 
It certainly seems that as a field, it excelling at open research. 
At the same time, however, it is even more important for the work to be reproducible if data and software are being reused by multiple researchers.

The Gene Ontology Annotations (GOA) are a combination of experimental and computational annotations. 
-->
-->