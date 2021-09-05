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

# Simulation

<!--
Simulated data can be used to test that methodologies are applicable to new data types. 
Since simulated data has a well-defined ground truth, we can test the performance and accuracy of a methodology using it. 
As long as the real data is similar to the simulated data, we can assume that methodologies will perform similarly on the real data.

In order to test whether it is feasible to use batch correction to combine the RNA-Seq experiments chosen (considering the unbalanced design), a simulated data set of tissue-specific batch-affected gene expression data was created. 

Data can be simulated based on its expected distribution and the parameters for the simulated distribution for each gene can be chosen based on estimates from existing data sets. 
Any number of samples can be simulated in this manner.
Additional effects (e.g. noise) can be added to this base level of gene expression and pre-decided fold changes for differences between samples (e.g. differential expression of tissue-specific genes, or batch effects) can be achieved by multiplying (or adding to) the simulated data. 


## Experimental design of simulated data
One aspect of the simulated data that I kept identical to the real data was number of samples in each experiment and tissue-group.

I focused on tissue-specific expression for samples within the 10 more general {ref}`tissue groups<tissue-groups>` that I mapped samples to using Ontolopy, rather than the more specific 129 Uberon terms that the samples map to.
These more general tissue groups contain the same specificity (and some of the exact same) terms (e.g. brain) that are in the Human Protein Atlas, which was used to parameterise the simulated count data.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import pandas as pd 
from myst_nb import glue

design_file = 'data/design.csv'
design = pd.read_csv(design_file, sep=',' ,index_col=0,
                     usecols=['Sample ID','Experiment','Tissue (UBERON)'])

tissue_groups_df = pd.read_csv('data/tissues_groups.csv', index_col=0)

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

glue('design-balance', overall_design)
glue('mod-head', mod.head())

mod.to_csv('data/simulated/group_mod.csv')
```




(estimating-coexpression)=
### Estimating co-expression between genes
[//]: # (TODO: Cite other packages)
The `polyester` package does not include gene co-expression (a.k.a. co-occurrance): the correlation between genes of expression values, which is due to genes working together in the same networks.
Although some other packages do have this functionality, they are created for scRNA-Seq data and would not be suitable for this purpose.

In order to introduce this correlation to some extent, I used FANTOM data to estimate the correlation between gene expression and used this correlation matrix to create the tissue-specific effects over genes.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import numpy as np

fantom_exp = pd.read_csv('data/experiments/fantom_gene_expression.tsv', sep='\t', index_col=0)
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
with open('data/simulated/corrcoef_matrix_genes.csv', 'w') as f:
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

The correlations between genes, which are used to {ref}`create the coefficient matrix<creating-coefficient-matrix>` are shown in {numref}`heatmap-correlations`. 


### Distribution of fold-changes for tissue specific genes

The expected log2-fold change due to tissue-specific effects per gene and per sample (matrix $\beta$) must be pre-decided in order to simulate the data set. 
The size of the effect and number genes affected were estimated using data from the Human Protein Atlas (HPA) - available [here](https://www.proteinatlas.org/download/proteinatlas.tsv.zip) -  which contains for each tissue-specific gene, the transcripts per million (TPM) for tissues that were found to be tissue-enriched (at least a 5 fold change, compared to all other tissues), group-enriched (at least a 5 fold change between the group of 2-7 tissues compared to all other tissues) or tissue enhanced (at least a 5 fold change between the tissue and the average of all other tissues), and the transcripts per million of the most highly expressed tissues that were not. 
Taken together (tissue-enriched, group-enriched and tissue-enhanced), we here refer to these genes/tissues as tissue-specific.
An excerpt of the file can be seen in {numref}`protein-atlas-view-tbl`.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import powerlaw

df = pd.read_csv('data/proteinatlas.tsv', index_col=0, sep='\t',
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
Comparative tests showed that lognormal was the best fit (with extremely low p-values, see code output below);  {numref}`powerlaw-multipliers` visualises this.

```{code-cell} ipython3
:tags: [hide-input]

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
                 yaxis_title='Probability density', height=400)
fig.update_xaxes(range=[0, max(bin_centres)])
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
Visually inspection of {numref}`multipliers-fit` reveals that the data simulated from these parameters appears to fit the data reasonably well, although it may be better parameterised by two overlapping distributions.

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
                 yaxis_title='Probability density', height=400)
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

(creating-coefficient-matrix)=
### Simulating coefficients for log-fold change
To simulate the matrix of coefficients of log2-fold change for input to `polyester`, I first created lognormally distributed (with parameters {ref}`estimated<lognormal-estimates>` from Human Protein Atlas data) and correlated (according to the {ref}`gene correlations<estimating-coexpression>` calculated earlier) coefficients.

Instead of creating log fold coefficients per tissue, I create them per row.
This is equivalent and allows me to use `numpy.random`'s `multivariate_normal` function, which I then transform to a lognormal distribution.

I then set a proportion of these coefficients to zero, based on the lognormal relationship for the number of tissue-specific genes per tissue.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

from copy import deepcopy
mus  = num_genes_to_simulate*[mu_ts]
sigmas = num_genes_to_simulate*[sigma_ts]

cov = deepcopy(corrcoef_genes.values)
for row in range(len(corrcoef_genes.values)):
    for col in range(len(corrcoef_genes.values)):
        cov[row][col] = corrcoef_genes.values[row][col] * sigmas[row] * sigmas[col]

mvn = np.random.multivariate_normal(mus, cov, size=len(tissue_groups)) 
sim = pd.DataFrame(np.exp(mvn), columns=corrcoef_genes.columns, index=tissue_groups)

display(np.transpose(sim).head())

for tissue in sim.index:
    num_genes_affected = min(int(np.random.lognormal(mu_ngenes, sigma_ngenes)), num_genes_to_simulate) 
    print(num_genes_affected)
    
    genes_to_set_to_zero = list(sim.columns)
    np.random.shuffle(genes_to_set_to_zero)
    genes_to_set_to_zero = genes_to_set_to_zero[:num_genes_affected]
    sim.loc[tissue, genes_to_set_to_zero] = 0

display(np.transpose(sim).head())
glue('correlation-coefficients', np.mean(np.corrcoef(np.transpose(sim))))
np.transpose(sim).to_csv('data/simulated/genes_1000/group_coeffs.csv')
```

## Simulating tissue-specific RNA-Seq counts

I simulated batch effects separately from the "base" read counts to facilitate comparison between them.

I first simulated the base read counts were simulated using `polyester` (using {download}`this script<helper_c05/create-base-simulated-counts.R>`).
The simulated data set is given by: $C_{ijk}\propto Negative Binomal (mean=\mu_{jk},size=r_{jk})$ for replicate $i$, gene $j$, and sample $k$, where:
- the means are given by $\mu_{jk}=\mu'_j+\beta_{jk} \cdot mod$ 
- $\mu'_j$ are the estimated base means per gene
- $\beta_{jk}$ are the generated matrix of log-fold changes in matrix format, including both batch and tissue effects (`coeffs_batch.csv`)
- $mod$ is the model design matrix. 
- the dispersion parameter (size), $r_{jk}$ is calculated based on $\mu_{jk}$ and the fit between mean and size (estimated from the FANTOM5 data).


```{code-cell} ipython3
# load in base counts
base_counts = pd.read_csv('data/simulated/genes_1000/simulated.csv', index_col=0) 
base_counts.index.names = ['Genes']
batches = pd.Series(pd.Categorical(design['Experiment']), index=base_counts.columns)

# Create mod batch
mod_batch = pd.DataFrame(index = design.index)
for exp in design['Experiment'].unique():
    mod_batch[exp] = (design['Experiment']==exp).astype('int')
mod_batch.index = base_counts.columns

# Load in real data
real = pd.read_csv('data/combined/combined_subset.csv', index_col=0) # shuffled using gshuf
real.head()
```

## Assessing suitability of simulated data
To assess the suitability of the simulated data as a test of batch effect removal, I compared PCA plots and distributions of the real and simulated data, after performingh the normalisation steps that precede batch correction. These steps include:
- Removing poorly expressed genes (


### Distributions
To determine which value of $p_0$ was the closest match to the data, I visualised the distributions of the real and simulated data across experiments.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

from scipy.stats import gaussian_kde

def remove_low_expression_genes(df, expression_cutoff = 200, absent_pc_sample = 0.8):
    """
    
    :param expression_cutoff: cut off for counts below which it counts as absent
    :absent_pc_sample: percentage of samples that have to be less than expression cutoff for a gene to be discarded
    """
    
    always_zero = len(df.index[df.sum(axis=1) == 0])  # Num all-0 genes
    print('genes sum 0:', always_zero ) 

    low_expression_genes = df.index[(df <= expression_cutoff).sum(axis=1)/len(df.columns) > absent_pc_sample]
    print('more than 80% genes equal to 0:', len(low_expression_genes)) 
    
    return low_expression_genes

def create_exp_matrix(df, design):
    """Create a matrix with a row per count observation, and a column for experiment."""
    exp_df = pd.DataFrame(data=[])
    for x in design['Experiment'].unique():
        expression = df[design[design['Experiment']==x].index].stack()
        labels = pd.Series([x]*len(expression))
        gene_ids = pd.Series(expression.index.codes[0])
        exp_df = exp_df.append(
            pd.DataFrame(data = {
                'Expression': expression.values,
                'Experiment': labels.values, 
                'Gene': gene_ids.values
            }))
    return exp_df
```

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# probs_to_plot = [0, 0.5, 1.0]
probs_to_plot = [0, 0.5, 1.0]

plots = ['real'] + [f"p<sub>0</sub> = {p}" for p in probs_to_plot]
num_graphs = len(plots)

step = 1
tiny_bit = 0.0001
bin_edges = np.arange(-1+tiny_bit, 20+tiny_bit, step)
# bin_edges_rounded= [round(x, 2) for x in bin_edges]

# TODO: Make the exp data object wider with more
x_y = {}
for i, to_plot in enumerate(plots):    
    if i == 0:
        data = real.copy()
    else:
        data = batch_dfs[probs_to_plot[i-1]].copy()
        data.columns = real.columns

    low_exp = remove_low_expression_genes(data)
    data = data.drop(index=low_exp)
    exp_data = create_exp_matrix(data, design)
    exp_data['Log expression'] = np.log2(exp_data['Expression'] + 1)
    for j, experiment_name in enumerate(design['Experiment'].unique()):
        print(to_plot, experiment_name)
        dat = exp_data[exp_data['Experiment']==experiment_name]['Log expression']
#         dat = exp_data[exp_data['Experiment']==experiment_name]['Expression']

        x_y[(to_plot, experiment_name)] = np.histogram(dat, bins=bin_edges, density=True)
#         x_y[(to_plot, experiment_name)] = density(dat, bw_adjust=0.08)


fig = make_subplots(
    rows=1, cols=num_graphs, 
    subplot_titles=plots,
    shared_yaxes=True,
    shared_xaxes=True,
    x_title ='Log expression',
    y_title='Density',
)

colours = ['skyblue', 'limegreen', 'rgb(208, 32, 144)', 'darkorange']
for i, to_plot in enumerate(plots):
    for j, experiment_name in enumerate(design['Experiment'].unique()):
        # data too chunky to use plotly's built in density plot as it tries to display every piece of data separately
        # so, I calculate separately
        show_leg = False
        if i == 0:
            show_leg = True
        
        hist_y = x_y[(to_plot, experiment_name)][0]
        bin_edges = x_y[(to_plot, experiment_name)][1]
        bin_centres = 0.5 * (bin_edges[:-1] + bin_edges[1:])


        dens_x, dens_y = x_y[(to_plot, experiment_name)]
        
        fig.add_trace(
            go.Scatter(x=bin_centres, y=hist_y, 

#             go.Scatter(x=dens_x, y=dens_y, 
                       mode='lines', 
                       legendgroup=experiment_name,
                       name=experiment_name,
                       line=dict(color=colours[j]),
                       showlegend=show_leg,
                      ),
            row=1, col=int(i+1),
         )
fig.update_layout(height=400, width=700)
fig.show()
```

```{code-cell} ipython3
:tags: [hide-input]

fig = make_subplots(
    rows=1, cols=num_graphs, 
    subplot_titles=plots,
    shared_yaxes=True,
    shared_xaxes=True,
    x_title ='Log expression',
    y_title='Density',
)

colours = ['skyblue', 'limegreen', 'rgb(208, 32, 144)', 'darkorange']
for i, to_plot in enumerate(plots):
    for j, experiment_name in enumerate(design['Experiment'].unique()):
        # data too chunky to use plotly's built in density plot as it tries to display every piece of data separately
        # so, I calculate separately
        show_leg = False
        if i == 0:
            show_leg = True
        
        hist_y = x_y[(to_plot, experiment_name)][0]
        bin_edges = x_y[(to_plot, experiment_name)][1]
        bin_centres = 0.5 * (bin_edges[:-1] + bin_edges[1:])


        dens_x, dens_y = x_y[(to_plot, experiment_name)]
        
        fig.add_trace(
            go.Scatter(x=bin_centres, y=hist_y, 

#             go.Scatter(x=dens_x, y=dens_y, 
                       mode='lines', 
                       legendgroup=experiment_name,
                       name=experiment_name,
                       line=dict(color=colours[j]),
                       showlegend=show_leg,
                      ),
            row=1, col=int(i+1),
         )
fig.update_layout(height=400, width=700)
fig.show()
```

```{figure} ../images/blank.png
---
width: 1
name: density-sim
---
Density plots for the real (leftmost) and simulated data for varying probability of zero batch-effect $p_{0}$. As $p_{0}$ increases...
```

[//]: # (TODO: Write caption)
[//]: # (TODO: Glue best p0)

The density plots in {numref}` density-sim` shows that the simulated data has comparable distributions to the true data, with $p_{0}=${glue:text}`best-p0` appearing to show the closest resemblance to the data. 
PCA (figure {numref}`pca-sim`) reveals that batch effects are visible in the simulated data, as they are in the real data.

### PCA
[//]: # (TODO: Add PCA)

I also visualised prinicipal components analysis for the simulated data, with and without batch effect. 
We would expect to see the data clustering by tissue for the simulated data with no batch effect, and by batch for the simulated batch-effected data, which is the case (see {numref}`pca-simulations`).

[//]: # (TODO: Write)
I followed a standard data pipeline for PCA:
1. removing low-expression genes (less than 100 counts in more than 80% of samples)
2. feature scaling
3.

```{code-cell} ipython3
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
```

## Limitations of simulations

**Negative Binomial**
Although the negative binomial distribution is often used to model count data, count data do not always fit the distribution very well{cite}`Hawinkel2020-fz`, and I did not check that the 4 experiments used here do so.

Number of genes with tissue-specific effects measured over 37 tissues (all are in my data set), and 20,000 genes... Need PROPORTION OF genes.
**Estimated from HPA TPM summaries**
- only counts data with log2-fold changes of > 5 TPM, don't get a good estimate of smaller changes
- estimates are made from TPM data but applied to counts data

**Co-expression not accurately modelled**
[//]: # (TODO: Image for co-expression in real and simulated data)

Although I use gene expression data to ensure that the coefficients for genes are correlated across samples, this does not ensure that the resulting dataset shows this coexpression accurately (although it does improve it substantially, see {numref}`correlations-coexpression`).
One result of this is that Principal Components Analysis plots for simulated data are not as informative for simulated data since the explained variance of the first two components is lower.
This should not impact the interpretation of the simultations, since if anything it will be more difficult to estimate batch effects with more variance over genes.
[//]: # (TODO: Write)

These correlations are very sensitive to the number of zeros in the coefficient matrix.

[//]: # (TODO: Glue all numbers and write about them)

```{list-table} Table showing correlations between genes for real and simulated count data, and $\beta$ matrix.
:header-rows: 1
:name: correlations-coexpression

* - FANTOM5 data
  - Coefficients matrix for tissue-specific expression, $\beta$
  - Simulated count (no co-expression between coefficients)
  - Simulated count data (with co-expression between coefficients)
* - {glue:text}`average-correlation-fantom`
  - {glue:text}`correlation-coefficients`
  - 0.05
  - ?
```

**Batch effects**
A good indication of the relative size or extent of batch effects was not readily available. 
Batch effects (log-fold changes - and proportion of genes affected by them) were chosen such that the simulated distributions most closely (according to visual inspection of PCA and box-plots).

The simulated data set is read counts and the fold changes are calculated from TPM data, however the simulated data does not include effects due to gene length or library size.

[//]: # (TODO: write: multiplicative batch effect?)
I combined multiplicative and additive batch effects: not sure if there are more nonlinear effects, or whether it was necessary to include multiplicative effects, etc.
Looking at the real data, the number of zero counts is clearly quite different per experiment and this is not well-modelled by the simulated data set.
A multiplicative batch effect that included multiplying some genes by zero might have been a good idea to simulate this, or potentially, a multiplicative batch effect which had more small values (much below 1), which would potentially reduce small counts to zero counts.

-->