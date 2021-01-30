(uberon-py)=
# The `uberon-py` package
[//]: # (TODO: Make Uberon-py a website and link to it)
[//]: # (TODO: Make a Zenodo for uberon-py and reference it here)
[//]: # (TODO: Explain Research Software Engineering approach)
[//]: # (TODO: Signpost this section)
[//]: # (TODO: make sure I am consistent about uberon-py/uberon_py)
[//]: # (TODO: Write roadmap/future work for this section, e.g. make the example public)
[//]: # (TODO: Link to documentation)

In order to map between Uberon tissues, CL cells, and named tissues from sample information, I created a small Open Source Python Package -  `uberon-py`, which is [available to install via the Python Package Index]([https://pypi.org/project/uberon-py/]), with code [available on GitHub](https://github.com/NatalieThurlby/uberon-py).

## Functionality
[//]: # (TODO: Explain what can be downloaded in more detail)

This package allows users to use Python to:
1. **Download useful Uberon ontology files** a selection of Uberon ontology `.obo` files.
2. **Load `.obo` ontology files**, either your own, separately downloaded, or those obtained in (1).
3. **{ref}`Mapping via name<mapping-by-name>`:** Map from sample-to-tissue via informal tissue names given in experimental design information (e.g. “eye stalk”) to an Uberon term (`UBERON:0010326`, Optic Pedicel).
4. **{ref}`Mapping via ontology term<mapping-by-term>`:** Map from CL cell types (e.g. `CL:0000235`, Macrophage), sample ontology term to Uberon tissues (e.g. `UBERON:0002405`, Immune system). Or from sample ontology terms (like FANTOM terms, such as FF:10048-101G3, Smooth Muscle, Adult, Pool1) to Uberon terms (`UBERON:0001135`, Smooth Muscle Tissue). Returns relationships between source term and Uberon term.
5. **Create sample-to-tissue mappings** based on (3) and (4)
6. **{ref}`Find disagreements in mappings<disagreement-finding>`** based on (3) and (4), which my indicate errors in sample metadata or ontologies.

The less self-explanatory aspects of this functionality are explained below:

(mapping-by-name)=
**Mapping by name:**

Informal tissue names are mapped Uberon term identifiers by checking for exact name matches to Uberon term names and their synonyms in the extended Uberon ontology.

(mapping-by-term)=
**Mapping by term:**

A mapping between a provided term (e.g. a FANTOM sample identifier or CL identifier) associated with a sample and an Uberon term is created by:
* Finding all relationships of interest (e.g. `is_a`, `related_to`, `part_of`, `derives_from`, `intersection_of`, `union_of`) to any other sample, cell or Uberon term.
* Propagate any relationships found using the same list of relationships, until either an Uberon term is found, or no new relationships are found, or you reach the root terms of the ontology. 

In this way, some mappings can be made via the cell ontology, which cannot be made through Uberon alone, for example: Macrophage - monocyte derived, donor3 `is_a` Human macrophage sample `derives_from` Macrophage `is_a` Monocyte `is_a` Leukocyte `part_of` Immune System, e.g. this sample is related to the immune system.

(disagreement-finding)=
**Using disagreements between mappings to improve biological ontologies:**

As described, the `uberon_py` package has two methods of mapping to tissues. 
Where both can be ran, disagreements between these mappings can be checked. 
When these two methods disagree, logical inconsistencies in either the mappings or the ontologies is revealed. 
See the {ref}`example<FANTOM5-inconsistencies-example>` of how this worked for the FANTOM5 data set.

## Example usage
 
### Example 1: creation of gene expression data set
{numref}`c05.3-data-wrangling` shows an example of how this package can be used to create a sample to tissue mapping for four different gene expression data sets.

(FANTOM5-inconsistencies-example)=
### Example 2: finding inconsistencies in the FANTOM5 data
For the FANTOM5 data, disagreements between these mappings revealed problems in the biological ontologies and experiment metadata that were provided to the package in order to create the mappings. 
These could then be fed back to the maintainers of these ontologies and datasets in order to improve/correct them. 

Disagreements between the tissue-sample mappings created through the (FANTOM, CL and Uberon) ontologies and those created using human annotation illuminates what may be a lack of specificity, incompleteness in, or disagreement between FANTOM, CL, or Uberon annotations, either in creating ontologies or annotating tissues to samples. 
The process of mapping FANTOM to Uberon tissues found twenty-two such disagreements, of which FANTOM, Uberon, and CL where appropriate have been informed via GitHub issues, some of which have already sparked changes in the ontologies. 

Three different types of example are described below, to give an idea of how multiple mappings may be used to improve annotation.

#### Missing Uberon annotation
**Example: `Bronchus part_of some Lung`**

One type of problem that can be revealed is a missing link in an ontology.

An example of this that was found using the FANTOM data set was that there was no formal relationin the Uberon ontology between *Bronchus* and *Lung*, despite the fact that the description text for Bronchus says “the upper conducting airways of the lung”.

This was found because the sample `FF:11511-119G8` (Bronchial Epithelial Cell, donor1) is mapped by name to `UBERON:0002048` Lung, but by ontology to `UBERON:0002185` Bronchus. 
This was flagged as inconsistent because there are no relation in the Uberon ontology between these terms.

Similar missing annotations were discovered between Aorta and Artery, and Hair follicle and Dermal papilla.

#### Mislabelled sample
**Example: `FF:11590-120G6` should be labelled _Alveolar Epithelial Cells_ not _Renal Glomerular Endothelial Cells_**

Sometimes samples are simply mislabelled.
In this case the mistake was revealed by testing the agreement between annotations because the mistake is only for the name, but not tissue annotation.

[//]: # (TODO: Link to other person who found this on researchgate/wherever)
The FANTOM sample ontology contains two samples named Renal Glomerular Endothelial Cells, donor2: `FF:11590-120G6` and `FF:11594-120H1`. 
One of these is a mislabelled sample, and it is actually an Alveolar Epithelial Cell sample.

#### Imprecise annotation to tissue
__Example: *Nucleus pulpopus* as *Spinal cord*__

Several FANTOM tissues are labelled by name colloquially, rather than precisely. 
For example, both *Nucleus pulpopus* and *Vertebra* are labelled *Spinal cord* (although the spinal cord itself is considered disjoint from these entities, both by definition, and in the Uberon ontology).
It’s for this reason that the ontology mapping is preferred over the labelled sample name in creating the overall FANTOM sample-to-tissue mapping.