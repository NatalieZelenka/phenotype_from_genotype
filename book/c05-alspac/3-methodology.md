---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.9.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Methodology
## Snowflake preprocessing
**Missing SNPs and ambiguous flips**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for ALSPAC. Known phenotypes included, dotted lines showing max scores for any SNP.)


```{code-cell} ipython3
:tags: [hide-input]

import os
import pandas as pd
import plotly.express as px
import numpy as np
from myst_nb import glue

# Read in all the 'snp' files and count the number of SNPs
# TODO: symlink this data to somewhere and add to the data dir
output_dir = '/Users/nataliethurlby/old/RecoveredData/NatHardDrive/work/CAGI_2015/cagi_output'
all_term_descriptions_loc = '/Users/nataliethurlby/phd/athletes/old/data/allTermDescriptions.txt'

snps = {}
for file in os.listdir(output_dir):
    term, suffix = file.split('.')
    if not suffix == 'snp':
        continue
    
    with open(os.path.join(output_dir, file)) as f:
        snps[term] = len(f.readlines())

# TODO: Make sure the graph is the last thing in the box/in it's own box, potentially with some other subplots.
snps = pd.Series(snps, name = 'Number of snps')

large_num_snps = 800
glue('num-phen-many-snps', len(snps[snps>large_num_snps]))
glue('num-phen-single-snp', len(snps[snps==1]))

# Find the names of terms from allTermsDescriptions.txt
term_descriptions = pd.read_csv(all_term_descriptions_loc, sep='\t', header=None, usecols = [1,4])
term_descriptions.rename(columns={1: 'Term ID', 4:'Term name'}, inplace=True)
term_descriptions.set_index('Term ID', inplace=True)

many_snp_terms = pd.DataFrame(snps[snps>large_num_snps])
many_snp_terms['Term name'] = term_descriptions.loc[many_snp_terms.index]['Term name']

glue('over-many-terms-table', many_snp_terms)
glue('percent-less-than-100', f"{100*len(snps[snps<100])/float(len(snps)):.0f}")
```

```{code-cell} ipython3
:tags: [hide-input]

# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
fig = px.histogram(snps)

fig.update_layout(
    xaxis_title_text='Number of SNPs mapped to phenotype',
    yaxis_title_text='Count', 
    showlegend=False,
)
fig.show()
```

```{glue:figure} over-many-terms-table
:figwidth: 400px
:name: tbl:over-many-terms
:align: center
Table showing phenotypes with over {glue:text}`large-num-snps` SNPs.
```

[//]: # (TODO: Make sure fig-hist-terms is ok)
[//]: # (TODO: Make sure that I include CTD chemical MESH ids in input in Snowflake section)

Looking at {numref}`fig-hist-terms`, we can see that the majority of terms (>{glue:text}`percent-less-than-100`%) have less than 100 SNPs associated with them, however there are also some with large numbers, for which clustering would be unreliable.
There are {glue:text}`num-phen-many-snps` phenotype terms that have over {glue:text}`large-num-snps` associated SNPs that Snowflake can predict on. 
In {numref}`tbl:over-many-terms`, we can see that these terms are either Comparitive Toxicogenomics Database chemicals, or extremely general disease terms such as *disease of anatomical entity*.

+++

## Requested phenotypes for validation
[//]: # (TODO: Mapping phenotypes to ALSPAC measurements. Write - was done by hand using the ALSPAC catalogue)

the following phenotypes in the ALSPAC cohort: `MP:0001501` *Abnormal Sleep Pattern* (measured using `FJCI250` *Sleep symptom score*), `MP:0001933` *Abnormal litter size* (measured by `mz010a` *Pregnancy size*), `MESH:D001259` *Ataxia* (measured by `kw2030` *Child ever thought to have a problem with clumsiness/coordination*), and `HP:0001249` *Intelligence/intellectual disability* (measured by `f8ws150` *Child had special needs*). 



### Distribution of phenotype scores

### Chosen phenotypes

```{code-cell} ipython3
:tags: [hide-input]

# chosen_phenotypes = ['MESHD001259', 'MP0001933', 'HP0001249', 'HP0007703', 'MP0001501']
# TODO: rerun to get MP.snps files
chosen_phenotypes = ['MESHD001259','HP0001249', 'HP0007703']
chosen_phenotypes_df = term_descriptions.loc[chosen_phenotypes]
chosen_phenotypes_df['Number of SNPs'] = snps.loc[chosen_phenotypes]
display(chosen_phenotypes_df)
```
