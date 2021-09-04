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

(creating-snowflake-inputs)=
# Creating `snowflake` inputs

[//]: # (TODO: Have I already explained VCF format? Link or explain here. Cite the version of the format we use. Explain that there are different versions.)
[//]: # (TODO: Make sure that I haven't confused `create_data` and creating snowflake inputs)

This section describes the sources and pipelines for creating inputs to Snowflake, including necessary files that are packaged alongside it.

[//]: # (TODO: Add any other necessary input files, the three listed here are ones that might need creating to use snowflake)
[//]: # (TODO: Make sure that I've explained the scripts that convert 23andMe to VCF)
[//]: # (TODO: Make this into a table describing the purpose of each part)

There are four main inputs required by Snowflake which must be created:
1. dcGO phenotype mapping file: high-quality mappings between protein (supra)domains and phenotype terms from 16 biomedical ontologies - provided as part of `snowflake` 
2. Background cohort: genetic data of diverse individuals (`.vcf`, VCF format) - default human option provided as part of `snowflake`
3. Consequence file: deleteriousness scores per SNP (`.Consequence`, format specific to `snowflake`) - default human option provided as part of `snowflake` 
4. Input cohort: genetic data of person or people of interest (`.vcf`, VCF format) - provided by user

The dcGO mapping file works for all organisms and only needs remaking if dcGO or SUPERFAMILY have significant updates.
Alternatively, a slimmed version can be created that contains only the ontologies of interest to a specific organism which reduces `snowflake`'s running time, and here I explain how I made a slimmed version of this file for ontologies of interest to humans. 
The background cohort and consequence file must be created once for each organism/genome build. 
Here, since I have only used Snowflake in predicting human phenotypes, I walk through the creation of the human background cohort and consequence file.
Lastly, the input cohort file must be created per input cohort. 
Here I run through the creation of a VCF file from 23andMe genotype files.

```{admonition} Consequences of input cohort SNPs
:class: info
:name: consequences-input-cohort
It is possible to create a consequence file for any cohort VCF file, i.e. it would be possible to make an input cohort consequence file.
However, since `snowflake` can only cluster our input cohort against the background for SNPs which overlap between the two cohorts, we only need to create one such file for either the input or the background. 
Here I've chosen to do it for the background cohort since then this file can be reused for many different input cohorts.
```

(dcgo-input)=
## DcGO phenotype mapping file (human)

It is simple to create the dcGO mapping file since dcGO provides the required files for download on the [SUPERFAMILY website](https://supfam.mrc-lmb.cam.ac.uk/SUPERFAMILY/cgi-bin/dcdownload.cgi).
The website provides 2 files of {ref}`high-coverage<high-coverage-dcGO>` mappings for each ontology supported by dcGO: one that maps between SCOP domains and ontology terms, and another that maps between SCOP {abbr}`supradomains (combinations of domains)` and ontology terms.
Currently, `snowflake` does not support the inclusion of dcGO supra-domain assignments.

```{admonition} High-coverage versus high-quality
:class: info
:name: high-coverage-dcGO

DcGO provides two versions of it's GO mappings: high-coverage and high-quality. The high-quality mapping contains only those associations between domains and phenotypes that are supported by single-domain proteins, while the high-coverage version contains some associations that have been inferred from known associations to multi-domain proteins. The high-coverage mapping contains roughly 10 times as many GO terms and 10 times as many protein domains compared to the high-quality version.
 
For all other (non-GO) ontologies, dcGO provides only the high-coverage version.

The high-coverage mappings were used in `snowflake` to increase the coverage of the phenotype predictions, i.e. so that more SNPs could be included and more phenotypes. 
```

```{margin} Incusion of the Mammalian Phenotype ontology
:name: choosing-dcGO-ontologies

The Mamalian Phenotype (MP) ontology{cite}`Smith2005-ug` is based on phenotypes seen in mice. While mice do have many anatomical and phenotypic similarities to humans, and are thus often used as models for human diseases, there are of course differences and some terms don't directly translate or are likely to be defined differently for humans (e.g. `MP:0001933` *abnormal litter size* or `MP:0002068` *abnormal parental behaviour*) and have different mechanisms behind them.
There are also many terms which do make sense for humans (e.g. `MP:0002166` *altered tumour susceptibility* or `MP:0011117` *abnormal susceptibility to weight gain*) and may represent interesting results. The suitability of MP terms must be considered term-by-term, but the terms were included in the human phenotype mapping file to increase coverage of both proteins and phenotypes.

```

The ontologies that contain interpretable phenotype terms for humans are: 
- Disease Ontology{cite}`Schriml2012-dz` (DO)
- Human Phenotype Ontology{cite}`Kohler2021-oy` (HP)
- Gene Ontology{cite}`Ashburner2000-cr` (GO), specifically terms from the `biological_process` subontology.
- MEdical Subject Headings{cite}`Lowe1994-jx`, (MESH) - on the dcGO website this is found under CTD diseases
- Mammalian Phenotype Ontology{cite}`Smith2005-ug` (MP) 

Some of these ontologies aren't designed only (or even primarily) for humans, but since they {ref}`contain terms which are relevant to humans<choosing-dcGO-ontologies>` and the associations are made based on protein domains found in human proteins, these ontologies were chosen.
While dcGO supports many other ontologies (e.g. Zebrafish and Xenopus ontologies) based on protein domains that can be found in humans, I made the decision that the trade-off between the additional time needed to run the phenotype predictor and sift through the results of these ontology terms was not worth the increase in coverage gained from whichever of these terms were meaningful.

To create the `snowflake` input for humans, files for the five relevant ontologies were downladed (for [DO](https://supfam.org/SUPERFAMILY/Domain2GO/Domain2DO.txt), [HP](https://supfam.org/SUPERFAMILY/Domain2GO/Domain2HP.txt), [GO](https://supfam.org/SUPERFAMILY/Domain2GO/Domain2GO_supported_only_by_all.txt), [MESH](https://supfam.org/SUPERFAMILY/Domain2GO/Domain2CD.txt), and [MP](https://supfam.mrc-lmb.cam.ac.uk/SUPERFAMILY/Domain2GO/Domain2MP.txt)), then concatenated, and the GO cellular component and GO molecular function terms were removed (these term identifiers were extracted from the `GO_subontologies` field of the `Domain2GO_supported_only_by_all.txt` file).

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import pandas as pd
import os
from myst_nb import glue

notebook_name = '3-creating-inputs.ipynb' # __file__ doesn't work in a jupyter notebook

input_dir = 'data/dcGO_input/downloaded'
HP_loc = os.path.join(input_dir, 'Domain2HP.txt')
MESH_loc = os.path.join(input_dir, 'Domain2CD.txt')
DO_loc = os.path.join(input_dir, 'Domain2DO.txt')
GO_loc = os.path.join(input_dir, 'Domain2GO_supported_only_by_all.txt') # high coverage
MP_loc = os.path.join(input_dir, 'Domain2MP.txt')

new_col_names = ['domain_type', 
                 'domain_sunid', 
                 'ont_term_id', 
                 'ont_term_name', 
                 'ont_subontologies', 
                 'information_content', 
                 'annotation_origin_1direct_0inherited']

hp = pd.read_csv(HP_loc, sep='\t', comment= '#')
hp.columns = new_col_names
hp['ont_id'] = 'HP'

mesh = pd.read_csv(MESH_loc, sep='\t', comment= '#')
mesh.columns = new_col_names
mesh['ont_id'] = 'MESH'

do = pd.read_csv(DO_loc, sep='\t', comment= '#')
do.columns = new_col_names
do['ont_id'] = 'DO'

go = pd.read_csv(GO_loc, sep='\t', comment= '#')
go.columns = new_col_names
go = go[go['ont_subontologies'] == 'biological_process']
go['ont_id'] = 'GO_BP'

mp = pd.read_csv(MP_loc, sep='\t', comment= '#')
mp.columns = new_col_names
mp['ont_id'] = 'MP'

all_onts = pd.concat([hp, mesh, do, go, mp], ignore_index=True)
outfile = 'data/dcGO_input/created/human_po.txt'
with open(outfile, 'w') as f:
    f.write(f'# file created at {pd.Timestamp.now()} by {notebook_name}.\n')
    f.write('# file contains high coverage mappings for HP, MESH (CD), DO, and GOBP.\n')
    all_onts.to_csv(f, index=False)
    
display(all_onts.head())

def glue_counts_dcGO(df: pd.DataFrame, identifier: str):
    """
    Expects a DataFrame df that contains only ontology terms of interest.
    """
    glue(f"{identifier}_assignments", len(df))
    glue(f"{identifier}_terms", len(df['ont_term_id'].unique()))
    glue(f"{identifier}_domains", len(df['domain_sunid'].unique()))
    
    return None
    
glue_counts_dcGO(all_onts[all_onts['ont_id']=='HP'], 'HP')
glue_counts_dcGO(all_onts[all_onts['ont_id']=='MESH'], 'MESH')
glue_counts_dcGO(all_onts[all_onts['ont_id']=='DO'], 'DO')
glue_counts_dcGO(all_onts[all_onts['ont_id']=='GO_BP'], 'GOBP')
glue_counts_dcGO(all_onts[all_onts['ont_id']=='MP'], 'MP')
glue_counts_dcGO(all_onts, 'all')
```

```{code-cell} ipython3
:tags: [hide-input, remove-output]

from IPython.display import HTML 

lines_to_view = [8000,20000,50000]
view = HTML(all_onts.iloc[lines_to_view].to_html(index=False)) 
glue("excerpt-pofile", view)
```

```{glue:figure} excerpt-pofile
:figwidth: 800px
:name: tbl:excerpt-pofile

An excerpt of the dcGO mapping file `human_po.txt`, showing mappings between phenotype terms from a range of ontologies, and SCOP sun IDs.
```

{numref}`tbl:excerpt-pofile` shows the type of content inside the phenotype ontology file. 
the `information_content` field is a measure of how specific the phenotype term is, for example *Pathological Conditions, Signs and Symptoms* is a very general term, while *Abnormality of the vertebral column* is more specific and *phosphatidylserine metabolic process* is the most specific shown.

```{list-table} Summary statistics of the coverage of human-related phenotype terms.
:name: dcgo-po-stats
:header-rows: 1

* - Ontology
  - Number of dcGO assignments
  - Number of unique terms assigned
  - Number of unique domain `sunid`s assigned
* - HP: Human phenotype ontology
  - {glue:text}`HP_assignments`
  - {glue:text}`HP_terms`
  - {glue:text}`HP_domains`
* - MeSH: Medical Subject headings
  - {glue:text}`MESH_assignments`
  - {glue:text}`MESH_terms`
  - {glue:text}`MESH_domains`
* - DO: Disease ontology
  - {glue:text}`DO_assignments`
  - {glue:text}`DO_terms`
  - {glue:text}`DO_domains`
* - GOBP: Gene ontology, biological process
  - {glue:text}`GOBP_assignments`
  - {glue:text}`GOBP_terms`
  - {glue:text}`GOBP_domains`
* - MP: Mammalian phenotype ontology
  - {glue:text}`MP_assignments`
  - {glue:text}`MP_terms`
  - {glue:text}`MP_domains`
* - Total (all included ontologies)
  - {glue:text}`all_assignments`
  - {glue:text}`all_terms`
  - {glue:text}`all_domains`
```

{numref}`dcgo-po-stats` shows the number of assignments, unique phenotype terms, and unique domains covered in the dcGO phenotype mapping per ontology and in total. 
The file contains {glue:text}`all_assignments` assignments, {glue:text}`all_terms` unique ontology terms, and {glue:text}`all_domains` unique domains. 
This constrains the proteins and phenotypes which `snowflake` can make predictions about.

+++

(bg-cohort-input)=
## Background cohort 

As described in the overview, Snowflake requires genetic "background" data to compare the individuals we are interested in against, i.e. so that meaningful clustering can take place. 
Although Snowflake has the functionality to be run with any background data set, the choice of data set is constrained since it must contain representative genetic data from from the entire population.

(acquire-1000G)=
### Data acquisition: the 1000 Genomes project
[//]: # (TODO: cross ref to whole genome sequencing)
The 1000 Genomes project{cite}`Consortium2015-ci,1000_Genomes_Project_Consortium2012-ek` ran from 2008 to 2015, with the aim of comprehensively mapping common human genetic variation across diverse populations. 
The project sequenced individuals whole genomes, and released data in two main phases:
- Phase 1: 37.9 million variants, in 1092 individuals, across 14 populations
- Phase 3: 84.4 million variants, in 2504 individuals, across 26 populations

```{margin} VCF
:name: vcf-format
When individual humans have their whole genomes sequenced, this is compared to the human reference genome. 
The alleles at each location are commonly stored in Variant Call Format (VCF) files; a much more compact format compared to storing the entire genome. 
VCF files describe the locations on the genome of variations between individuals, given by chromosome, position, variant identifiers (e.g. rsID), and then the calls at those locations for each individual.
```

Data from the 1000 Genomes project are always used for the background cohort to `snowflake`, with data from the 1000 Genomes project Phase 3{cite}`Consortium2015-ci` used as a default, and earlier experiments using data from Phase 1{cite}`1000_Genomes_Project_Consortium2012-ek`. 
Here I describe the process of creating the phase 1 {ref}`VCF<vcf-format>` file (`1000G.vcf`), but the same process is followed to create the larger phase 3 VCF file (`2500G.vcf`).

For both phases of the 1000 Genomes project, data are provided as VCF files for each chromosome. 
Both data sets are available through the [International Genome Sequencing Resource](https://www.internationalgenome.org/data){cite}`Fairley2020-hp` (IGSR); phase 1 VCFs (GRCh37) can be downloaded via FTP at `ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase1/analysis_results/integrated_call_sets/`, and phase 3 VCFs (GRCh37) can be downloaded at `ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/`.

After downloading these files, the per-chromosome VCF files were combined into one large VCF file (for all chromosomes).
The {ref}`consequence<creating-consequence-file>` file must be created at this stage, before the final input VCF can be created.

(final-bg-vcf)=
### Create final input VCF
In order to create the final input VCF, we must remove SNPs from the VCF file that are not in the consequence file. 
This reduces the file size dramatically, since many recorded SNPs are either synonymous, nonsense, non-coding or multi-allelic.
The VCF file is then [Tabix](http://www.htslib.org/doc/tabix.html)-indexed{cite}`Li2011-sl`, which increases the speed of Snowflake.

[//]: # (TODO: Summary statistics and name of VCF file here, also excerpt of file?)

+++

(creating-consequence-file)=
## Consequence file
[//]: # (TODO: Cite + cross-ref VEP, FATHMM and SUPERFAMILY)
[//]: # (TODO: Add image of consequence constituent bits)

The consequence file contains the "consequences" of one amino acid being changed to another, which is used to weight which SNPs are the more important dimensions for clustering a phenotype. 
It also contains the mapping between SNPs and proteins, and SNPs and domain architecture.

This file is generated using:
- Ensembl's {abbr}`VEP (Variant Effect Predictor)` tool to map from chromosomes and locations to SNP type (e.g. missense/nonsense/nonsynonymous), and to protein ID
- FATHMM for scoring the deleteriousness of {ref}`missense<missense>` mutatations
- SUPERFAMILY for mapping from protein IDs given by VEP to their domain architectures (SCOP family/superfamily)

(run-vep)=
### Run the Variant Effect Predictor tool
In order to get a list of SNPs to input to FATHMM, we must first determine which SNPs in the background data are missense SNPs.
This can be done using Ensembl's {abbr}`VEP (Variant Effect Predictor)` [web tool](https://www.ensembl.org/info/docs/tools/vep/index.html){cite}`McLaren2016-di`, which takes a VCF as input.
This first 10 columns of the combined VCF file is used as input to VEP since only these columns are needed, and making the file smaller reduces processing time.

(query-fathmm)=
### Query FATHMM and SUPERFAMILY for the SNPs of interest
[//]: # (TODO: Write, cite, cross-reference)
To get the consequence file, VEP output was first filtered to contain only biallelic missense SNPs, and was then used as input to query the FATHMM and SUPERFAMILY databases for the unweighted conservation scores and the domain assignments.

(consequence-summary)=
### Summary
[//]: # (TODO: Consequence file excerpt, explain fields and what is used)

```{code-cell} ipython3
:tags: [remove-cell]

import tabix
import os
import numpy as np

# Read in background and make a note of which calls are thre
background_loc = 'data/background.vcf'
bg_df = pd.read_csv(background_loc, 
                    usecols=['#CHROM', 'POS', 'REF', 'ALT'],
                    dtype={"#CHROM":str, 'POS':int, 'REF':str, 'ALT':str},
                    sep='\t', 
                    index_col=['#CHROM', 'POS'])
display(bg_df)

consequence_loc = 'data/consequences.tsv'
c_columns = ['#CHROM', 'POS', 'calls', 'snp_id', 'ENSP_id', 'prot_sub', 'HMM', 'position', 'ref_prob', 'mut_prob', 'SUPERFAMILY', 'Sup_e_val', 'FAMILY', 'Fam_e_val']

# TODO: Get combined 23andMe (v2 chip) and CAGI6 list
c_tb = tabix.open(f"{consequence_loc}.gz")
flipped_count = 0
selected_rows = []
for chrom, pos in bg_df.index.unique():
    results = c_tb.query(chrom, pos-1, pos)    
    ref, alt = bg_df.loc[(chrom, pos)]
    
    for result in results:
        call = result[2]
        if call == f"{ref}/{alt}":
            selected_rows.append(result)
        elif call == f"{alt}/{ref}":
            selected_rows.append(result)
            flipped_count+=1
print(flipped_count)
            
c_df = pd.DataFrame(selected_rows, columns=c_columns)
# Some versions of snowflake keep in information about proteins that don't have domain assignments (this removes those rows)
c_df = c_df.replace(r'^\s*$', np.nan, regex=True).dropna(subset=['FAMILY','SUPERFAMILY'])
c_df.to_csv('data/consequences_2500G.tsv', index=False)

c_df.set_index(['#CHROM', 'POS'], inplace=True)
```

```{code-cell} ipython3
:tags: [remove-output, hide-input]

glue('consequence-rows', len(c_df.index))
glue('consequence-unique-snps', len(c_df.index.unique()))
glue('consequence-unique-proteins', len(c_df['ENSP_id'].unique())) 
glue('consequence-unique-families', len(c_df['FAMILY'].unique())) 
glue('consequence-unique-supfam', len(c_df['SUPERFAMILY'].unique()))

regs_snp = c_df.iloc[0].name
multi_family_snp = False
multi_supfam_snp = False
for chrom, pos in c_df[c_df.index.duplicated(keep=False)].index.unique():
    families_per_snp = len(c_df.loc[(chrom, pos)]['FAMILY'].unique())
    superfamilies_per_snp = len(c_df.loc[(chrom, pos)]['SUPERFAMILY'].unique())
    if families_per_snp > 1 and superfamilies_per_snp == 1:
        multi_family_snp = (chrom, pos)
    elif superfamilies_per_snp > 1:
        multi_supfam_snp = (chrom, pos)
        
    if multi_family_snp and multi_supfam_snp:
        break

index_to_view = [regs_snp, multi_family_snp, multi_supfam_snp]
glue("excerpt-consequence", c_df.loc[index_to_view])
```

[//]: # (TODO: Table not displaying properly in PDF)
[//]: # (TODO: Probabilities > 1?!)

```{glue:figure} excerpt-consequence
:figwidth: 800px
:name: tbl:excerpt-consequence

An excerpt of the consequence file `2500G.consequence`, showing mappings between SNPs, protein IDs, mutant and reference probabilities from FATHMM, and SCOP sun IDs (via SUPERFAMILY).
```

[//]: # (TODO: Check reasoning: is it because multiple proteins or is because if a protein has multiple domains we include it for that SNP)

As we can see in {ref}`tbl:excerpt-consequence`, the consequence file can contain multiple rows for the same SNPs since the SNP may appear in multiple proteins, since proteins can have overlapping reading frames. 
Less frequently, SNPs that fall in multiple proteins may also fall in more than one domain families or even superfamilies.

[//]: # (TODO: Give number of SNPs in consequence file in this next paragraph:)
The output `.consequence` file defines the upper limit of the number of SNPs `snowflake` can make phenotype predictions based on.
In practice, this will often be a much smaller number as for SNPs to be used they must be:
- measured in the input cohort (which is often genotyped, and therefore contains far fewer variants)
- within protein domains that exist in the dcGO mapping file in addition to the consequence file.
- a SNP where there is some variation between the background and input

[//]: # (TODO: Show distribution of abs ref-mut probs, i.e. deleteriousness score)
Like the VCF file, the Consequence file is the indexed with Tabix{cite}`Li2011-sl` to increase Snowflake's speed.

```{code-cell} ipython3
:tags: [remove-cell]

# TODO: tabix consequence file
# TODO: filter background VCF file
display(c_df.loc[index_to_view])
# TODO: tabix VCF file
```

(input-cohort)=
## Input cohort

(23andme-input)=
###  23andMe file formats
[//]: # (TODO: cite different 23andme chips, maybe have excerpt of table of different numbers)

The SNPs which are measured in a genotyping experiment depends on the chip used.
Since launch, 23andMe have used a number of different Illumina chips for their genotyping service. 
These chips capture information for different SNPs, and vastly different numbers of SNPs.
This means that in order to combine data from different chips, many loci can not be used.

23andMe have their own file formats, which must be convered to VCF in order to use `snowflake`. 
One of these formats is tab separated and very similar to VCF, but for their API, 23andMe also stored genotype data in long strings (~1 million characters, twice the number of loci on the chip) of the form `AAAACCTTTT__CC__`, where every 2 nucleotides corresponds to a given SNP on the 23andMe chip with a rsID, chromosome and position.
To convert this compressed format to VCF, 23andMe provided a genotype snp map file (`snps.data`), which is different for each 23andMe chip, that gives rsIDs, chromosome and position for each index, which looks like:

```
# index is a key for the /genomes/ endpoint (2 base pairs per index).
# strand is always +1.
index   snp     chromosome      chromosome_position
0       rs41362547      MT      10044
1       rs28358280      MT      10550
2       rs3915952       MT      11251
```

So, according to this file, the first two characters of the genotype string correspond to `rs41362547`, then the next two correspond to `rs28358280`.

The `create_data` function of snowflake contains the functionality to create a VCF file from 23andMe API string formats, for three different chips. 

(genome-builds)=
### Genome builds
```{margin} Position and BED formats       
:name: position-bed-format
The positions of the variants (SNPs) that are recorded can vary in format: essentially this comes down to a change in formatting, the fact that sometimes counting starts at 0, and sometimes it starts at 1, and sometimes ranges are closed on one side e.g. `chr1 127140000 127140001` in BED format is equivalent to `chr1:127140001-127140001` in "Position" format{cite}`Tyner2016-er`.
```

The files currently generated for snowflake use the GRC37 (hg19) human genome build. 
This is the version that is currently supported by FATHMM, 23andMe, and phase 1 of 1000G. 

[//]: # (TODO: Write about importance of using the same genome build, explain 1000G, fathmm, and 23andMe use 37)

<!--
### Filtering
If the VCF is purely for the purpose of running Snowflake, then it makes sense to filter it to contain only the SNPs in the Consequence file.


#### Example: ALSPAC
[//]: # (TODO: show how many SNPs are removed for commonality with 1000G)


### CAGI
[//]: # (TODO: Write)

+++

### Data Pipelines

+++

#### Pipeline for creating VCF files from 23andMe data
The CAGI, Athletes, and ALSPAC datasets were all genotyped using 23andMe, so the following applies to all of these datasets.

+++


+++

#### CAGI
[//]: # (TODO: Possibly delete this section)

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was CAGI data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**

[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**

[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for CAGI. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Mapping phenotypes to CAGI measurements
[//]: # (TODO: Write)

+++

#### Athletes
[//]: # (TODO: Possibly delete this section)

##### Creating VCF files
[//]: # (TODO: Cross-ref to Pipeline for creating VCF files above)
[//]: # (TODO: What settings was CAGI data set created with using VCF files)

**Missing values**
[//]: # (TODO: write - or possibly move to results section)

**Distribution of SNPs per phenotype**
[//]: # (TODO: Distribution of number of SNPs per phenotype for ALSPAC, showing overall and highlighting phenotypes with ground truth information)

**Distribution of SNP scores within phenotypes**
[//]: # (TODO: Distribution of number SNP scores within phenotypes - violin plot with some examples - for CAGI. Known phenotypes included, dotted lines showing max scores for any SNP.)

##### Mapping phenotypes to CAGI measurements
[//]: # (TODO: Write)
-->
