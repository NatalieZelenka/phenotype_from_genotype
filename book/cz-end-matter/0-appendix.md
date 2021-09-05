---
jupytext:
  formats: md:myst,ipynb
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

(appendix)=
# Appendix

[//]: # (TODO: Maybe split out into different sections if I add the  gene study)

<!--
## Gene study
[//]: # (TODO: Gene study)
[//]: # (TODO: If I don't put in anything major e.g. Athletes, put it here)
-->

(simulation-appendix)=
## Simulating RNA-Seq data to test batch-correction across experiments

Simulated data can be used to test that methodologies are applicable to new data types. 
Since simulated data has a well-defined ground truth, we can test the performance and accuracy of a methodology using it. 
As long as the real data is similar to the simulated data, we can assume that methodologies will perform similarly on the real data.

In order to test whether it is feasible to use batch correction to adjust the RNA-Seq experiments chosen (considering the unbalanced design), I want to create a simulated data set of tissue-specific batch-affected gene expression data. 
This appendix contains some preliminary work towards this goal, in estimating parameters from the combined data set that will be useful in creating the data set.


## Parameters for simulation
In order to create simulated data that is similar to the real thing, decisions must be made about how to parameterise the distribution of counts per sample and how these relate to tissue specific effects and batch effects.

The `polyester` R package{cite}`Frazee2015-kg` can be used to simulate RNA-seq count data with the same design of tissues, samples, and experiments as in the combined data set, particularly the `create_read_numbers` function, which requires a model matrix that specifies the experimental design and a matrix of coefficients $\beta$ that specify the sample-specific effects.

### Count parameters
For gene expression count data, a zero-truncated negative binomial distribution is commonly used to represent the underlying gene expression counts
 because the distribution is always positive, does not assume mean and variance are equal, and can be tuned to have many zero counts as we see in real data. 

The `get_params` function from `polyester` handles the paramerisation of the zero-inflated negative binomial that it uses to simulate count data, using an example data set as input.
I used a cleaned version of the FANTOM5 data as input which was restricted only to genes that are common between all experiments (HDBR, HPA, FANTOM and GTEx), removing all zero rows, and set NaN counts to 0.
Parameters calculated by polyester include means per gene and size, and probability of a zero count per gene. 

### Experimental design of simulated data
I already have "model-matrix", specifying the experimental design of the combined data set, in terms of batch and the 10 more general {ref}`tissue groups<tissue-groups>` that I mapped samples to using Ontolopy.
These more general tissue groups contain the same specificity (and some of the exact same) terms (e.g. brain) that are in the Human Protein Atlas, which was used to parameterise the simulated count data, which is why this model matrix is a better choice than the more specific 129 Uberon terms that the samples also map to.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import pandas as pd 
from myst_nb import glue

design_file = '../c08-combining/data/design.csv'
design = pd.read_csv(design_file, sep=',' ,index_col=0,
                     usecols=['Sample ID','Experiment','Tissue (UBERON)'])

tissue_groups_df = pd.read_csv('../c08-combining/data/tissues_groups.csv', index_col=0)

design['Group name'] = design['Tissue (UBERON)'].map(tissue_groups_df['Group name'])

tissue_groups = list(design['Group name'].dropna().unique())
mod = pd.DataFrame(index = design.index)
for tissue_group in tissue_groups:
    # Note: zeros correspond to a normal fold change of 1 (as mod contains logfold changes)
    mod[tissue_group] = (design['Group name']==tissue_group).astype('int')

overall_design = mod.copy()
overall_design['Experiment'] = design['Experiment']
overall_design = overall_design.groupby('Experiment').sum()
overall_design['Samples per experiment'] = overall_design.sum(axis=1)
overall_design.loc['Total'] = overall_design.sum(axis=0)

percentage = overall_design.sum(axis=0)/float(overall_design.loc['Total', 'Samples per experiment'])
tissue_groups_to_discard = percentage.index[percentage<0.01]
overall_design.drop(columns=tissue_groups_to_discard, inplace=True)
mod.drop(columns=tissue_groups_to_discard, inplace=True)
tissue_groups.remove(tissue_groups_to_discard)
```

(estimating-coexpression)=
### Estimating co-expression between genes

[//]: # (TODO: Cite other packages)

The `polyester` package does not include gene co-expression (a.k.a. co-occurrance): the correlation between genes of expression values, which is due to genes working together in the same networks, although some other packages do have this functionality.

In order to introduce this correlation to some extent, I used FANTOM data to estimate the correlation between gene expression and used this correlation matrix to create the tissue-specific effects over genes.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import numpy as np

fantom_exp = pd.read_csv('../c08-combining/data/experiments/fantom_gene_expression.tsv', sep='\t', index_col=0)
random_seed = 14042003
num_genes_to_simulate = 1000

# Calculate gene covariances to include in model data for RNA-seq simulations
sampled = fantom_exp.sample(num_genes_to_simulate, random_state=random_seed)
corrcoef_genes = np.corrcoef(sampled)
assert(corrcoef_genes.shape == (num_genes_to_simulate, num_genes_to_simulate))
corrcoef_genes = pd.DataFrame(corrcoef_genes, index=sampled.index, columns=sampled.index)
# display(corrcoef_genes.head())

# Not exactly 1 due to the linear alg. Set to 1.
for gene in corrcoef_genes.columns:
    corrcoef_genes.loc[gene, gene] = 1

# all-NaNs due to all-zero genes in FANTOM. Set to zeros.
for gene in corrcoef_genes.loc[gene][corrcoef_genes.loc[gene].isna()].index:
    corrcoef_genes.loc[gene, :] = np.zeros(num_genes_to_simulate) 
    corrcoef_genes.loc[:, gene] = np.zeros(num_genes_to_simulate) 
assert(len((corrcoef_genes.loc[gene][corrcoef_genes.loc[gene].isna()]))==0)  # No more NaNs

# Save:
with open('../c08-combining/data/simulated/corrcoef_matrix_genes.csv', 'w') as f:
    f.write(f'# corrcoef matrix for {num_genes_to_simulate} randomly sampled genes from FANTOM gene expression file `fantom_gene_expression.tsv`, seed = {random_seed}.\n')
    corrcoef_genes.to_csv(f, sep='\t')
    
glue('average-correlation-fantom', np.mean(corrcoef_genes.values))
```

```{code-cell} ipython3
:tags: [hide-input]

import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.spatial.distance import pdist, squareform

data_array = corrcoef_genes.values
labels = corrcoef_genes.columns

# Code for dendogram and heatmap adapted from plotly examples: https://plotly.com/python/dendrogram/
# Initialize figure by creating upper dendrogram
fig = ff.create_dendrogram(data_array, orientation='bottom', labels=labels, )
for i in range(len(fig['data'])):
    fig['data'][i]['yaxis'] = 'y2'

# Create Side Dendrogram
dendro_side = ff.create_dendrogram(data_array, orientation='right')
for i in range(len(dendro_side['data'])):
    dendro_side['data'][i]['xaxis'] = 'x2'

# Add Side Dendrogram Data to Figure
for data in dendro_side['data']:
    fig.add_trace(data,)

# Create Heatmap
dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
dendro_leaves = list(map(int, dendro_leaves))
heat_data = data_array[dendro_leaves,:]
heat_data = heat_data[:,dendro_leaves]

heatmap = [
    go.Heatmap(
        x = dendro_leaves,
        y = dendro_leaves,
        z = heat_data,
        colorscale = 'Blues',
        name = 'Correlation'
    )
]

heatmap[0]['x'] = fig['layout']['xaxis']['tickvals']
heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

# Add Heatmap Data to Figure
for data in heatmap:
    fig.add_trace(data)

# Edit Layout
fig.update_layout({'width':600, 'height':600,
                         'showlegend':False, 'hovermode': 'closest',
                         })
# Edit xaxis
fig.update_layout(xaxis={'domain': [.15, 1],
                                  'mirror': False,
                                  'showgrid': False,
                                  'showline': False,
                                  'zeroline': False,
                                'showticklabels': False,

                                  'ticks':""})
# Edit xaxis2
fig.update_layout(xaxis2={'domain': [0, .15],
                                   'mirror': False,
                                   'showgrid': False,
                                   'showline': False,
                                   'zeroline': False,
                                   'showticklabels': False,
                                   'ticks':""})

# Edit yaxis
fig.update_layout(yaxis={'domain': [0, .85],
                                  'mirror': False,
                                  'showgrid': False,
                                  'showline': False,
                                  'zeroline': False,
                                  'showticklabels': False,
                                  'ticks': ""
                        })
# Edit yaxis2
fig.update_layout(yaxis2={'domain':[.825, .975],
                                   'mirror': False,
                                   'showgrid': False,
                                   'showline': False,
                                   'zeroline': False,
                                   'showticklabels': False,
                                   'ticks':""})

# Plot!
fig.show()
```

```{figure} ../images/blank.png
---
width: 1
name: heatmap-correlations
---
Heatmap showing the correlation coefficients between the randomly sampled 1000 genes in the FANTOM5 data set.
```

The correlations between genes, which could be used to create the coefficient matrix $\beta$ are shown in {numref}`heatmap-correlations`. 

### Distribution of fold-changes for tissue specific genes

The expected log2-fold change due to tissue-specific effects per gene and per sample (matrix $\beta$) must be pre-decided in order to simulate the data set. 
The size of the effect and number genes affected were estimated using data from the Human Protein Atlas (HPA) - available [here](https://www.proteinatlas.org/download/proteinatlas.tsv.zip) -  which contains for each tissue-specific gene, the transcripts per million (TPM) for tissues that were found to be tissue-enriched (at least a 5 fold change, compared to all other tissues), group-enriched (at least a 5 fold change between the group of 2-7 tissues compared to all other tissues) or tissue enhanced (at least a 5 fold change between the tissue and the average of all other tissues), and the transcripts per million of the most highly expressed tissues that were not. 
Taken together (tissue-enriched, group-enriched and tissue-enhanced), we here refer to these genes/tissues as tissue-specific.
An excerpt of the file can be seen in {numref}`protein-atlas-view-tbl`.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import powerlaw

df = pd.read_csv('../c08-combining/data/proteinatlas.tsv', index_col=0, sep='\t',
                 usecols= ['Gene','RNA tissue category', 'RNA TS', 'RNA TS TPM', 'TPM max in non-specific'])
glue('protein-atlas-view', df.head())
```

```{glue:figure} protein-atlas-view
:name: protein-atlas-view-tbl

The Human protein atlas provides a csv file of TPM values for tissues with >5 fold change. This table was used to parameterise the matrix of coefficients $\beta$.
```

Since the HPA data does not include fold-changes of less than 5, I had no information about these changes, and decided to model the distribution of unaffected genes separately to the affected genes.

(lognormal-estimates)=
**Estimating parameters of lognormal distribution of log2-fold change per gene:** 
For any of these tissue-specific genes/tissues, the log2-fold change per tissue per gene was calculated. 
I first checked that each of the tissues had some tissue-specific genes according to the HPA data; this was the case.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# First check that all tissues have some tissue-specific effects according to HPA (5fold(TPM) changes)
non_spec_tissues = set([])
spec_tissues = set([])
for gene, row in df.iterrows():
    for non_spec_tissue in [x.split(":")[0] for x in str(row.loc['RNA TS TPM']).replace(',',';').split(';')]: 
        non_spec_tissues.add(non_spec_tissue)
    for spec_tissue in [x.split(":")[0] for x in row.loc['TPM max in non-specific'].split(',')]:
        spec_tissues.add(spec_tissue)
        
# remove strings we don't care about:
spec_tissues.remove('all non-specific tissues')  # denotes genes that are only expressed in specific tissues
non_spec_tissues.remove('nan')  # denotes genes that are not tissue-specific

assert(non_spec_tissues==spec_tissues) # => yes all tissues are tissue-specific of these 37
```

I then extracted the multipliers from the data, and converted them to log2-fold format (expected by `polyester`).
Since the distribution was long-tailed, I compared the distribution to an exponential, log-normal and power-law distribution using the python `powerlaw` package{cite}`Alstott2014-qq`. 
Comparative tests showed that lognormal was the best fit (with extremely low p-values, see code output below); {numref}`powerlaw-multipliers-fit` visualises this.

```{code-cell} ipython3
:tags: [hide-input]

import numpy as np
#Extract the data of the TPM multipliers
multipliers = []
for gene, row in df.iterrows():
    if pd.isna(row.loc['RNA TS TPM']):
        continue
    biggest_ts = max([float(x.split(':')[1].strip()) for x in row.loc['RNA TS TPM'].split(';')])
    biggest_non_ts = float(row.loc['TPM max in non-specific'].split(':')[1].strip())
    if biggest_non_ts == 0:
        continue 
    if np.log2(biggest_ts/float(biggest_non_ts)) == 0:
        continue
    multipliers.append(np.log2(biggest_ts/float(biggest_non_ts)))
    
#Fit distribitions to the TPM multipliers
fit = powerlaw.Fit(multipliers, xmin=1, discrete=True)
compare1 = ['lognormal', 'power_law']
R, p = fit.distribution_compare(*compare1)
if  p < 0.05:
    print(f"{compare1[0]} distribution is a better fit than {compare1[1]} distribution with p-value={p}")

compare2 = ['lognormal', 'exponential']
R, p = fit.distribution_compare(*compare2)
if p < 0.05:
    print(f"{compare1[0]} distribution is a better fit than {compare1[1]} distribution with p-value={p}")
    
# Parameters for log2-fold coefficients of tissue-specific expression over genes:
mu_ts = fit.lognormal.mu
sigma_ts = fit.lognormal.sigma
glue('mu-lognormal-ts', f'{mu_ts:.2f}', False)
glue('sigma-lognormal-ts', f'{sigma_ts:.2f}', False)
```

```{code-cell} ipython3
:tags: [hide-input]

bin_edges, probs = fit.pdf(list(np.arange(0, 20, 0.1)))
bin_centres = 0.5 * (bin_edges[:-1] + bin_edges[1:])
xlim = max(bin_edges)
x = list(np.arange(0, xlim, 0.1))

lognormal = fit.lognormal.pdf(x)
exponential = fit.exponential.pdf(x)
power_law = fit.power_law.pdf(x)


fig = go.Figure()
fig.add_trace(go.Scatter(x=bin_centres, y=probs, name='HPA data',  fill='tozeroy'))

fig.add_trace(go.Scatter(x=x, y=lognormal,
                    mode='lines', name='lognormal', line=dict(color='darkorange', width=2,
                              dash='dot')))

fig.add_trace(go.Scatter(x=x, y=exponential,
                    mode='lines', name='exponential', line=dict(color='darkmagenta', width=2,
                              dash='dot')))

fig.add_trace(go.Scatter(x=x, y=power_law,
                    mode='lines', name='power law', line=dict(color='green', width=2,
                              dash='dot')))

fig.update_layout(xaxis_title='Log<sub>2</sub>-fold multipliers tissue-specific gene.',
                 yaxis_title='Probability density', height=400, width=600)
fig.update_xaxes(range=[0, max(bin_centres)])
# fig.update_yaxes(range=[0, 0.008])

fig.show()
```

```{figure} ../images/blank.png
---
width: 1
name: powerlaw-multipliers-fit
---
The distribution of tissue-specific fold-change over all tissue-specific gene-sample pairs from HPA, fitted to lognormal, powerlaw, and exponential distributions, showing the lognormal as the best fit.
```

The log-normal distribution was the best fit to the data, see {numref}`powerlaw-multipliers-fit`). 
The parameters fitting the log2-fold changes to the log-normal distribution were estimated as $\mu=${glue:text}`mu-lognormal-ts` $\sigma=${glue:text}`sigma-lognormal-ts`. 
Visual inspection of {numref}`powerlaw-multipliers-fit` reveals that the data simulated from these parameters appears to fit the data reasonably well, although it may be better parameterised by two overlapping distributions.

+++

**Number of tissue-specific genes per tissue:** 
The number of tissue-specific genes per tissue was also calculated from the HPA data.
Again, the data was most similar to a lognormal, still with very small p-values (see code output below), but the fit (see {numref}`genes-per-tissue`) was less convincing, probably due to the small number of tissues: 37.
The distribution was parameterised with $\mu=${glue:text}`mu-lognormal-num-ts-genes` $\sigma=${glue:text}`sigma-lognormal-num-ts-genes`.

```{code-cell} ipython3
:tags: [hide-input]

#Extract the data of genes per sample
df.dropna(subset=['RNA TS TPM']).head()
count_dict = {}
for gene, row in df.dropna(subset=['RNA TS TPM']).iterrows():
    tissue_names = [x.split(':')[0] for x in row.loc['RNA TS TPM'].split(';')]
    for tissue in tissue_names:
        try:
            count_dict[tissue]+=1
        except:
            count_dict[tissue]=1

genes_per_tissue = [x for x in count_dict.values()]

# Fit powerlaw
min_fold_change = np.log2(5)
fit = powerlaw.Fit(genes_per_tissue, xmin=min_fold_change, discrete=True)
R, p = fit.distribution_compare(*compare1)
if  p < 0.05:
    print(f"{compare1[0]} distribution is a better fit than {compare1[1]} distribution with p-value={p}")

fit.distribution_compare(*compare2)
if p < 0.05:
    print(f"{compare1[0]} distribution is a better fit than {compare1[1]} distribution with p-value={p}")

# Parameters for number of genes affected by tissues:
mu_ngenes = fit.lognormal.mu
sigma_ngenes = fit.lognormal.sigma
glue('mu-lognormal-num-ts-genes', f'{mu_ngenes:.2f}', False)
glue('sigma-lognormal-num-ts-genes', f'{sigma_ngenes:.2f}', False)
```

```{code-cell} ipython3
:tags: [hide-input]

bin_edges, probs = fit.pdf(list(np.arange(0, 20, 0.1)))
bin_centres = 0.5 * (bin_edges[:-1] + bin_edges[1:])
xlim = max(bin_edges)
x = list(np.arange(0, xlim, 0.1))

lognormal = fit.lognormal.pdf(x)
exponential = fit.exponential.pdf(x)
power_law = fit.power_law.pdf(x)


fig = go.Figure()
fig.add_trace(go.Scatter(x=bin_centres, y=probs, name='HPA data',  fill='tozeroy'))

fig.add_trace(go.Scatter(x=x, y=lognormal,
                    mode='lines', name='lognormal', line=dict(color='darkorange', width=2,
                              dash='dot')))

fig.add_trace(go.Scatter(x=x, y=exponential,
                    mode='lines', name='exponential', line=dict(color='darkmagenta', width=2,
                              dash='dot')))

fig.add_trace(go.Scatter(x=x, y=power_law,
                    mode='lines', name='power law', line=dict(color='green', width=2,
                              dash='dot')))

fig.update_layout(xaxis_title='Numbers of tissue-specific genes per tissue',
                 yaxis_title='Probability density', height=400, width=600)
fig.update_xaxes(range=[0, max(bin_centres)])
fig.update_yaxes(range=[0, 0.006])

fig.show()
```

```{figure} ../images/blank.png
---
width: 1
name: genes-per-tissue
---
The distribution of the number of tissue-specific genes per tissue from HPA, fitted to lognormal, powerlaw, and exponential distributions, showing the lognormal as the best fit.
```

## Simulating tissue-specific RNA-Seq counts

Counts can then be simulated using `polyester` (using {download}`this script<../c08-combining/helper_c05/create-base-simulated-counts.R>`) or an alternative tool.

The simulated data set is given by: $C_{ijk}\propto Negative Binomal (mean=\mu_{jk},size=r_{jk})$ for replicate $i$, gene $j$, and sample $k$, where:
- the means are given by $\mu_{jk}=\mu'_j+\beta_{jk} \cdot mod$ 
- $\mu'_j$ are the estimated base means per gene
- $\beta_{jk}$ are the generated matrix of log-fold changes in matrix format, including both batch and tissue effects (`coeffs_batch.csv`)
- $mod$ is the model design matrix. 
- the dispersion parameter (size), $r_{jk}$ is calculated based on $\mu_{jk}$ and the fit between mean and size (estimated from the FANTOM5 data).

## Next Steps
Next steps will be to perform batch-correction on these simulated data sets, e.g. ComBat, ComBat-Seq, and Mutual Nearest Neighbours, and performing differential expression analyses, using the input $\beta$ matrix to test for ground truths.

```{code-cell} ipython3

```
