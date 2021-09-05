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


<!--

The "base" batch effect was then multiplied by a strength per experiment, with experiment strength multipliers as shown in {numref}`batch-strengths`

```{list-table}
:header-rows: 1
:name: batch-strengths

* - Experiment
  - Strength multiplier
* - *HDBR*
  - {glue:text}`hdbr-strength`
* - *FANTOM5*
  - {glue:text}`fantom5-strength`
* - *HPA*
  - {glue:text}`hpa-strength`
* - *GTEx*
  - {glue:text}`gtex-strength`
```
-->

<!--
python code:
# experiment_multipliers = {'HDBR':0.5, 'FANTOM5':1, 'GTEx':0.25, 'HPA':2}
# for e in experiment_multipliers.keys():
#     glue(f"{e.lower()}-strength", f"{experiment_multipliers[e]:.2f}")
-->

### Combining, data wrangling
````{admonition} Code to harmonise meta-data for GxA data sets
:class: dropdown

```python

# CREAT EXP DESIGN FILES: GXA
import pandas as pd
import numpy as np
from uberon_py import obo 
from helper_c05 import clean
from myst_nb import glue

uberon_obo_file = 'data/uberonext_obo.txt'
uberon_obo = obo.Obo(uberon_obo_file,['UBERON','CL'])

#HPA E-MTAB-2836
col_data_hpa_file = 'data/experiments/hpa/E-MTAB-2836_colData.tsv'
col_data_hpa = pd.read_csv(col_data_hpa_file,delimiter='\t', quotechar ='"')
col_data_hpa[col_data_hpa=='  '] = None  # make empty elements None

tissue_map_hpa = uberon_obo.map_tissue_name_to_uberon(col_data_hpa, 'organism_part')
assert(len(tissue_map_hpa[tissue_map_hpa.UBERON.isna()]['name matched on'].unique()) == 0)

# Make HPA experimental file:
lines = []
for index, row in col_data_hpa.iterrows():
    lines.append([
        index,
        'HPA',
        np.nan, #HPA doesn't have individual IDs
        np.nan, #HPA doesn't have individual age
        np.nan, #HPA doesn't have age ranges
        row['developmental_stage'],
        clean.clean_sex(row['sex']),
        clean.clean_tissue(tissue_map_hpa.loc[index,'UBERON']),
        'tissues - donor',
        clean.clean_techrep(row['technical_replicate_group'],'HPA'),
        np.nan, #HPA doesn't have Bio Reps or individual, so can't even try to calc
    ])
hpa_experimental_design = pd.DataFrame(lines,columns = experimental_design_columns)
hpa_experimental_design.set_index('Sample ID',inplace=True)
hpa_experimental_design.to_csv('data/experiments/hpa/hpa_experimental_design.csv')

# GTEx
col_data_gtex_file = 'data/experiments/gtex/E-MTAB-5214_colData.tsv'
col_data_gtex = pd.read_csv(col_data_gtex_file,delimiter=',', quotechar ='"')
col_data_gtex = col_data_gtex.rename(columns = {'Unnamed: 0':'Sample ID'})
col_data_gtex.set_index('Sample ID',inplace=True)

col_data_gtex[col_data_gtex=='  '] = None  #make empty elements None
assert(set(col_data_gtex.disease.unique()) == set(['normal']))
assert(set(col_data_gtex.clinical_information.unique()) == set([None,'not sun exposed', 'sun exposed']))

tissue_map_gtex = uberon_obo.map_tissue_name_to_uberon(col_data_gtex,'organism_part')
#Manually map the GTEx names that don't automatically map
manual_mapping_gtex = {
    'transformed skin fibroblast': None, #Alternative: ? 'UBERON:0002097',#skin of body
    'ebv-transformed lymphocyte': None,  #Alternative: ? 'UBERON:0000178', #blood
    'suprapubic skin': 'UBERON:0001415', #Alternative: ? 'UBERON:0002097',#skin of body
}

for index, row in tissue_map_gtex.iterrows():
    if row['UBERON'] == None:
        uberon_term = manual_mapping_gtex[row['name matched on']]
        tissue_map_gtex.loc[index,'UBERON'] = uberon_term
        
num_excluded_samples = tissue_map_gtex[tissue_map_gtex.UBERON.isna()].shape[0]  # excluded because transformed cell 
glue("Number of excluded GTEx samples", num_excluded_samples)
samples_to_exclude = list(tissue_map_gtex[tissue_map_gtex.UBERON.isna()].index)

#Use additional file to add age information
gtex_additional_info = pd.read_csv('data/experiments/gtex/GTEx_v7_Annotations_SubjectPhenotypesDS.txt',sep='\t')
gtex_additional_info = gtex_additional_info.rename(columns={'SUBJID':'individual','AGE':'age_range'})

col_data_gtex = col_data_gtex.merge(gtex_additional_info[['age_range','individual']],on='individual',how="left").set_index(col_data_gtex.index)

# Make gtex experimental file:
lines = []
for index, row in col_data_gtex.iterrows():
    lines.append([
        index,
        'GTEx',
        row['individual'],
        np.nan,#GTEx doesn't have individual age
        row['age_range'],
        'adult',
        clean_sex(row['sex']),
        clean_tissue(tissue_map_gtex.loc[index,'UBERON']),
        'tissues - donor',
        clean_techrep(row['technical_replicate_group'],'GTEx'),
        np.nan, #TODO: Try to calculate bio reps based on same individual + tissue, but different tech rep?
    ])
gtex_experimental_design = pd.DataFrame(lines,columns = experimental_design_columns)
gtex_experimental_design.set_index('Sample ID',inplace=True)
gtex_experimental_design.to_csv('data/experiments/gtex/gtex_experimental_design.csv')

# HDBR
col_data_hdbr_file = 'data/experiments/hdbr/E-MTAB-4840_colData.tsv'
col_data_hdbr = pd.read_csv(col_data_hdbr_file, delimiter='\t')

# tissue mapping:
tissue_map_hdbr = uberon_obo.map_tissue_name_to_uberon(col_data_hdbr,'organism_part')
for index in tissue_map_hdbr[tissue_map_hdbr.UBERON.isna()]['name matched on'].index:
    tissue_map_hdbr.loc[index,'UBERON'] = 'UBERON:0000955' # Brain
assert(tissue_map_hdbr[tissue_map_hdbr.UBERON.isna()].shape[0]==0)

# clean age and sex metadata:
col_data_hdbr['age'] = col_data_hdbr['developmental_stage'].map(clean.MapHDBR.age)
col_data_hdbr['sex'] = col_data_hdbr['karyotype'].map(clean.MapHDBR.sex)

# Make experimental file:
lines = []
for index, row in col_data_hdbr.iterrows():
    lines.append([
        index,
        'HDBR',
        'HDBR-'+str(row['individual']),
        row['age'],
        np.nan,#HDBR doesn't have age ranges
        'fetus',
        row['sex'],
        clean_tissue(tissue_map_hdbr.loc[index,'UBERON']),
        'tissues - donor',
        np.nan, # TODO:? Calculate based on "block"
        np.nan, # TODO:? Define from individual and tissue IDs different "block"
    ])
hdbr_experimental_design = pd.DataFrame(lines,columns = experimental_design_columns)
hdbr_experimental_design.set_index('Sample ID',inplace=True)
hdbr_experimental_design.to_csv('data/experiments/hdbr/hdbr_experimental_design.csv')
```

````


````{admonition} FANTOM5 data pipeline code
:class: dropdown

This code makes use of the {download}`fantom.py helper script<./helper_c05/fantom.py>`.

```python

# General:
import pandas as pd
import numpy as np
import sys
import time
import os
from ontolopy import obo # my package

# My helper functions:
from helper_c05 import fantom

#load ontologies
fantom_obo_file = 'data/experiments/fantom/ff-phase2-170801.obo.txt'
uberon_obo_file = 'data/uberonext_obo.txt'
fantom_obo_root_terms = ['FF:0000001','EFO:0000001']

fantom_obo = obo.Obo(fantom_obo_file, ['FF','CL','UBERON'], fantom_obo_root_terms)
uberon_obo = obo.Obo(uberon_obo_file, ['UBERON','CL'], fantom_obo_root_terms)

#load and process fantom counts data 
fantom_count_file_loc = 'data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_counts_ann.osc.txt'
ensg_mapping_loc = 'data/experiments/fantom/biomart_ensg_hgnc.txt'
samples_info_file = 'data/experiments/fantom/fantom_humanSamples2.0.csv'
fantom_counts = fantom.Fantom(fantom_count_file_loc,
                              ensg_mapping_loc, 
                              fantom_obo, 
                              uberon_obo, 
                              samples_info_file)

fantom_counts.gene_expression.to_csv('data/experiments/fantom/fantom_gene_expression.tsv', sep='\t')

pd.DataFrame(fantom_counts.funnel_plot_samples.items(), columns=['Sample Data Stage', 'Number of samples']).to_csv('data/experiments/fantom/funnel_plot_samples.tsv', index=False, sep='\t')

pd.DataFrame(fantom_counts.funnel_plot_transcripts.items(), columns=['Transcript Data Stage', 'Number of transcripts']).to_csv('data/experiments/fantom/funnel_plot_transcripts.tsv', index=False, sep='\t')
```

````

```{admonition} Code: combine experimental design
:class: dropdown

```python
import pandas as pd
from myst_nb import glue

# read in experimental design files:
hdbr_experimental_design=pd.read_csv(
    'data/experiments/hdbr/hdbr_experimental_design.csv', 
    index_col='Sample ID')
fantom_experimental_design=pd.read_csv(
    'data/experiments/fantom/fantom_experimental_design.csv', 
    index_col='Sample ID')
hpa_experimental_design=pd.read_csv(
    'data/experiments/hpa/hpa_experimental_design.csv', 
    index_col='Sample ID')
gtex_experimental_design=pd.read_csv(
    'data/experiments/gtex/gtex_experimental_design.csv', 
    index_col='Sample ID')

# combine:
combined_design =  pd.concat([hdbr_experimental_design, fantom_experimental_design, hpa_experimental_design, gtex_experimental_design])

# drop non-tissue-specific:
combined_design.dropna(subset =['Tissue (UBERON)'], inplace=True)
assert(combined_design[combined_design['Tissue (UBERON)'].isna()].shape[0] == 0)

# save
combined_design.to_csv('data/combined/combined_experimental_design.csv')
```

````

```{code-cell} ipython3
:tags: [hide-input]

# # load combined_design + add tissue groups info and save/print.

# # glue
# glue('number of samples in combined data set', combined_design.shape[0])
# glue('number of Uberon tissue types in combined data set', combined_design['Tissue (UBERON)'].unique().shape[0])
# glue('number of individuals in combined data set', combined_design['Individual ID'].unique().shape[0]-1)

# print('sex breakdown (of samples):\n',combined_design['Sex'].value_counts())
# print('sample type breakdown:\n',combined_design['Sample Type'].value_counts())
# print('experiment breakdown:\n',combined_design['Experiment'].value_counts())
```


```{code-cell} ipython3
# from plotly.subplots import make_subplots

def get_mu(mean, sigma=1):
    return np.log(mean)-(sigma*sigma)/2.0
    

def get_sigma(mean):
    return np.sqrt(2*np.log(mean))

def create_batch_effects(probs, batch_means, num_genes=1000):
    # Get base lognormal
    batches = list(batch_means.keys())
    num_batches = len(batches)
    
    batch_base_multipliers = {}
    batch_base_multiplier = np.random.lognormal(
#         [0]*num_batches, 
#         [get_sigma(batch_means[x]) for x in batch_means.keys()], 
        [get_mu(batch_means[x]) for x in batches]
        [1]*num_batches,
        size=(num_genes, num_batches))

    for i, p0 in enumerate(probs):
        batch_base_multipliers[p0] = pd.DataFrame(
            one_truncate(p0, batch_base_multiplier, num_genes),
            columns = batches,
            index = range(1, num_genes+1),
        )
        
    return batch_base_multipliers

def one_truncate(p0, batch_base, num_genes=1000):
    """
    Removes 1-prob_batch proportion of batch_base
    p0 = probability of 0 count
    """
    batch_base_copy = batch_base.copy()
    for i in range(batch_base.shape[1]):
        ones=np.random.binomial(1, p0, size=num_genes)
        batch_base_copy[ones==1, i] = 1
    
    return batch_base_copy 

def create_batch_hist(batch_bases):
    probs = batch_bases.keys()
    # Note: hist shows open range on lefthand side, and includes righthandside as this more easily illustrates the additional zeros. Zeros are no longer there, I got confused. Muliply by 1 to get no effect.
    fig = make_subplots(rows=2, cols=int((len(probs)/2)), 
                        subplot_titles=[f"p<sub>0</sub> = {prob}" for prob in probs],
                        shared_yaxes=True,
                        shared_xaxes=True,
                        x_title ='Base multiplicative batch-effects (log2-fold)',
                        y_title='Number of<br>genes')
        
    nbins = 50
    max_ = round(np.log2(batch_bases[0]).max().max())
    step = max_/float(nbins)
    tiny_bit = 0.0001
    print(max_, step)
    bin_edges = np.arange(-1 + tiny_bit, max_+tiny_bit, step)
    bin_edges_rounded= [round(x, 2) for x in bin_edges]
    num_graphs = len(probs)-1

    for i, p0 in enumerate(probs):
        if i == num_graphs:
            continue
            # No need to visualise a bar with 1000 genes at 1
        batch_base = np.log2(batch_bases[p0]+1)['HPA'] # Just visualise the first batch - they should all have the same distribution
        counts, bins = np.histogram(batch_base, bins=bin_edges)
        bins = 0.5 * (bins[:-1] + bins[1:])
        df = pd.DataFrame({'bin min':bin_edges_rounded[:-1], 'bin max': bin_edges_rounded[1:], 'bin_centers':bins, 'counts':counts })
        
        fig.add_trace(
            go.Bar(x=df['bin_centers'], y=df['counts']),
            row=1+int((i)/(num_graphs/2.0)), col=int(np.mod(i,num_graphs/2.0))+1,
        )
    fig.update_layout(bargap=0, bargroupgap=0, height=400, width=700, showlegend=False)
    fig.update_yaxes(range=[0, 1000])

#     fig.show()
    return fig

# fig, base_batch_multipliers = create_batch_hist(probs, batch_base)

#----------------
probs= [0, 0.3, 0.5, 0.7, 1.0]
batch_means = {'HDBR':164, 'FANTOM5':1.1, 'GTEx':164, 'HPA':22}
batch_m = create_batch_effects(probs, batch_means, num_genes=1000)
# max(batch_bases[0][:, 0])
create_batch_hist(batch_m)
# batch_bases[0]
# batch_bases[0.3]
# print(probs)
#----------------
# batch_base_multipliers = create_batch_effects(probs, num_genes=1000, num_batches=4)
# fig = create_batch_hist(batch_base_multipliers)
#----------------
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
#----------------
# Create final simulated data sets including batch:
batch_dfs = {probs[-1]: base_counts}
zero_mask = (base_counts != 0).astype(int)

for i, p in enumerate(probs[:-1]):
    # mod_m = batch effect per sample measurement
#     mod_m = np.array(batches.map(experiment_multipliers)).reshape(1,len(batches.map(experiment_multipliers)))
    
    # beta_j = batch effect per gene (for this batch strength)
#     beta_j = np.array(base_batch_multipliers[i]).reshape(1,len(base_batch_multipliers[i]))
    beta_jb = batch_m[p]
        
    # A_mj = additive batch effect per measurement + gene (for this batch strength
#     A_mj = mod_m*np.transpose(additive[p])
#     A_mj = mod_batch.dot(additive[p]).transpose().values
    
#     batch_df = base_counts + zero_mask*A_mj
#     batch_df[batch_df<0] = 0
    batch_df = (base_counts.multiply(batch_m[0].values.dot(mod_batch.transpose().values))).astype(int)
#     batch_df = base_counts.multiply(mod_m.transpose().dot(beta_jb).transpose()).astype(int) #+ A_mj
#     batch_df.to_csv(f"data/simulated/genes_1000/simulated_batch_{str(p).replace('.', '_')}.csv")
#     batch_df.to_csv(f"data/simulated/genes_1000/simulated_additive_batch_{str(p).replace('.', '_')}.csv")

    batch_dfs[p] = pd.DataFrame(batch_df, columns=base_counts.columns, index=base_counts.index)
#----------------

def density(a, npts=100, bw_adjust=1):
    kde = gaussian_kde(a, bw_adjust)
    min_ = a.min()
    max_ = a.max()
    range_ = max_ - min_
    low = min_ - range_ * 0.1
    high = max_ + range_ * 0.1
    x = np.linspace(low, high, npts)
    y = kde(x)
    return x, y

    
#----------------

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
#----------------

[//]: # (TODO: Check kappa + experiment accurate in caption)

```{figure} ../images/blank.png
---
width: 1
name: additive-base-batch
---
An example of the distribution of batch effects per $p_{0}$, probability of zero batch-effect. Experiment shown is HDBR ($\kappa=0.5$). As $p_{0}$ increases, more of the distribution is "0", meaning that the addition has no effect.
```

<!--
For the multiplicative effect, I used multiplicative batch effects that were normally distributed over genes, and batch with $\mu = 1$, $\sigma = 0.1$ as a "base" batch effect, then again simulated data with batch-effects affecting 0% to 100% of genes, in 10% intervals (defined using $p_{0}$ the proportion of genes with zero batch effects), giving distributions of batch effects shown in {numref}`base-batch-dists`. 

The batch effect strengths were increased in additive and multiplicative effects simultaneously.
-->

#----------------

# p0=0.5
# mean_per_gene = 182.5114  # from combat
# mean_batch = 0.1*mean_per_gene
# n_nbinom=5
# p_nbinom = n_nbinom/(n_nbinom + mean_batch)
# print(p_nbinom)
# from scipy.stats import laplace_asymmetric
# # additive_base = np.random.normal(0, 10, size=(num_genes_to_simulate, num_batches)).astype(int)
# print(batch_kappas.values())
# additive_base = laplace_asymmetric.rvs(
#     kappa=[0.5,0.5,1, 1],
#     scale=[scale]*num_batches, 
#     size=(num_genes_to_simulate, num_batches)).astype(int)

# print(additive_base[:, 0])

# batch_kappas = [0.5, 0.5, 2, 2]  # Two batches increased the count on average and 2 decreased it on average
# kappa = 0.5
# scale = 20
# mean, var, skew, kurt = laplace_asymmetric.stats(kappa,scale=scale, moments='mvsk')
# # additive_base = np.random.negative_binomial(5, p_nbinom, size=(num_genes_to_simulate, 1)).astype(int).reshape( num_genes_to_simulate)
# print(mean, var, skew, kurt)
# r = laplace_asymmetric.rvs(kappa, scale=scale, size=1000)
# print(r[r>0].mean())
# # ax.plot(x, , 'k-', lw=2, label='frozen pdf')

# # additive_base = np.random.negative_binomial(1, 0.01, size=(num_genes_to_simulate, num_batches)).astype(int)
# # (additive_base*np.random.binomial(1, 1-p0, (num_genes_to_simulate, num_batches))).reshape(num_batches, num_genes_to_simulate)
# px.histogram(r)
# # print(-1*additive_base)
# # print(additive_base)
#----------------

# ADDITIVE BATCH EFFECTS in terms of ADDING A NEW DISTRIBUTION TO OUR DISTRIBUTION IS A BIT WEIRD - EITHER NEED VERY SPECIFIC DISTRIBUTION THAT I DON'T KNOW HOW TO PARAMETERISE OR END UP WITH NON-CONTINUOUSNESS AROUND START OF DIST

# from plotly.subplots import make_subplots

# # probs =  [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# probs= [0, 0.3, 0.5, 0.7, 1.0]
# num_graphs = len(probs)-1
# fig = make_subplots(
#     rows=2, cols=int(num_graphs/2), 
#     subplot_titles=[f"p<sub>0</sub> = {prob}" for prob in probs],
#     shared_yaxes=True,
#     shared_xaxes=True,
#     x_title ='Base additive batch-effects (counts)',
#     y_title='Number of<br>genes',
# )

# # batch_kappas = {'HDBR':1, 'FANTOM5':1, 'GTEx':2, 'HPA':2}
# # batch_scales = {'HDBR':20, 'FANTOM5':20, 'GTEx':20, 'HPA':20}
# additive = {}

# batch_names = design['Experiment'].unique()
# num_batches = len(batch_names)

# batch_means = {'HDBR':1120, 'FANTOM5':20, 'GTEx':1390, 'HPA':220}

# # batch_loc = {'HDBR':10, 'FANTOM5':20, 'GTEx':20, 'HPA':25}
# # sigma=1.5
# # additive_base = np.random.lognormal(
# #     mean=[np.log2(batch_means[x]) for x in batch_names],
# #     sigma=[sigma]*num_batches,
# #     size=(num_genes_to_simulate, num_batches),    
# # ).astype(int)

# # additive_base = laplace_asymmetric.rvs(
# #     kappa=list(batch_kappas.values()),
# #     loc=list(batch_loc.values()),
# #     scale=list(batch_scales.values()), 
# #     size=(num_genes_to_simulate, num_batches)).astype(int)

# # n = 5
# # batch_p = {'HDBR':0.2, 'FANTOM5':0.5, 'HPA':0.005, 'GTEx':0.006, }

# # additive_base = np.random.negative_binomial(
# #     n=[n]*num_batches, 
# #     p=[batch_p[x] for x in batch_names], 
# #     size=(num_genes_to_simulate, num_batches)
# # ).astype(int)

# # UNIFORM
# batch_means = {'HDBR':1120, 'FANTOM5':20, 'GTEx':1390, 'HPA':220}
# variation_means = {'HDBR':200, 'FANTOM5':200, 'GTEx':200, 'HPA':200}
# additive_base = np.random.uniform(
#     low=[0 for x in batch_names],
#     high=[2*batch_means[x] for x in batch_names], 
#     size=(num_genes_to_simulate, num_batches)
# ).astype(int)

# print(batch_names)
# print(additive_base.mean(axis=0))

# for i, p0 in enumerate(probs):
#     additive[p0] = (additive_base*np.random.binomial(1, 1-p0, (num_genes_to_simulate, num_batches))).transpose()
    
#     if p0 == probs[-1]:
#         # Want to calculate it, but not graph it.
#         continue
#     fig.add_trace(
#         go.Histogram(x=additive[p0][0,:], 
#                      xbins=dict(size=5),
#                     ),
#         row=1+int((i)/(num_graphs/2.0)), col=int(np.mod(i,num_graphs/2.0))+1,
#     )
# fig.update_layout(bargap=0, bargroupgap=0, height=400, width=700, showlegend=False)
# # fig.update_yaxes(range=[0, 30])
# # fig.update_xaxes(range=[-200,200], tickangle=-70)

# fig.show()
#----------------
#----------------
#----------------
#----------------

```


### Batch effects
It coudn't find a convincing general estimate of the size of batch effects in bulk RNA-Seq studies, as it would require someone to do an experiment with a lot of replicates, which isn't usually done.
I modelled batch effects with both multiplicative and additive effect.

<!-- 
TODO: Check math displays
-->

```{margin} Asymmetric Laplace distribution
:name: asymmetric-laplace
The asymmetric Laplace distribution looks like two back-to-back exponential distributions, where each exponential distribution may have unequal scale.

$$
f(x;m,\lambda ,\kappa )={\frac {\lambda }{\kappa +1/\kappa }}{\begin{cases}\exp \left((\lambda /\kappa )(x-m)\right)&{\text{if }}x<m\\[4pt]\exp(-\lambda \kappa (x-m))&{\text{if }}x\geq m\end{cases}}
$$
```

For the additive effect, I used batch effects that were distribution according to an asymmetric Laplace distribution, as this is the distribution that represents the difference between two Negative Binomial distributions{cite}`Seetha_Lekshmi2014-dq`, meaning that that the batch-effected and non-batch effected counts will still follow a zero inflated negative binomial distributon. 
The assymetric Laplace distribution was generated for each batch, with the skew parameter $\kappa$ being set to `0.5` for two of the batches and `2` for the other two batches (as in {numref}`batch-kappas`): meaning that two batches increased the mean of the resulting distribution of counts on average, and two reduced them on average. I also varied the proportion of genes affected (1-$p_{0}$) from 0% to 100% in 10% intervals.
An example of the overall distributions of additive batch efects is shown in {numref}`additive-base-batch`.

The batch-effects were then added to the base read counts per replicate $i$, gene $j$, sample $k$, and proportion of genes affected by batch effects $p$:

$ C_{ijkp} = C_{ijk} A_{ijp}$ where:
- $A_{ijpk} = mod_{batch, ik}*a_{ijp}$ are the additive batch effects on all samples.
- $a_{ijp}$ are the additive batch effects per gene, batch, and $p0$.
- $mod_{batch, ik}$ is a model matrix describing which batch each sample measurement belongs to.

<!--
$ C_{ijkp} = C_{ijk} \circ M_{ijp} + A_{ijp}$ where:
- $M_{ijp} are the multiplicative batch effects.
- $\beta_{batch, jp}$ are the base coefficients of the multiplicative batch effects.
- $mod_{batch, i}$ is a model vector describing which batch each measurement belongs to.
- $A_{ijp}$ are the additive batch effects per gene.
- $\circ$ denotes element-wise multiplication.
-->

I focused on tissue-specific expression for samples within the 10 more general {ref}`tissue groups<tissue-groups>` that I mapped samples to using Ontolopy, rather than the more specific 129 Uberon terms that the samples map to.
These more general tissue groups contain the same specificity (and some of the exact same) terms (e.g. brain) that are in the Human Protein Atlas, which was used to parameterise the simulated count data.



```{glue:figure} mod-head
:name: mod-head-tbl

The first few lines of the model matrix, needed as input to `polyester`.
```

{ref}`mod-head-tbl` shows an excerpt of the model matrix used as input to `polyester` to simulate the data, while {ref}`design-balance-tbl` shows the experimental design of the combined data set, which is also used for the simulated dataset. 

In addition, to make the data set more manageable, the data set was simulated for 1000 genes rather than ~20,000. 