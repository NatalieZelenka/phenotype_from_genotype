## The `uberon-py` package
[//]: # (TODO: Make Uberon-py a website and link to it)
[//]: # (TODO: Make a Zenodo for uberon-py and reference it here)

In order to map between Uberon tissues, CL cells, and named tissues from sample information, I created a small Python Package -  `uberon-py`, which is [available to install]([https://pypi.org/project/uberon-py/]) via the Python Package Index, with code [available on GitHub](https://github.com/NatalieThurlby/uberon-py).

## Functionality
[//]: # (TODO: Explain what can be downloaded in more detail)

This package allows users to use Python to:
1. **Download useful Uberon ontology files** a selection of Uberon ontology `.obo` files.
2. **Load `.obo` ontology files**, either your own, separately downloaded, or those obtained in (1).
3. **Mapping via name:** Map from sample-to-tissue via informal tissue names given in experimental design information (e.g. “eye stalk”) to an Uberon term (UBERON:0010326, Optic Pedicel).
4. **Mapping via ontology:** Map from CL cell types (e.g. `CL:0000235`, Macrophage), sample ontology term to Uberon tissues (e.g. `UBERON:0002405`, Immune system). Or from sample ontology terms (like FANTOM terms, such as FF:10048-101G3, Smooth Muscle, Adult, Pool1) to Uberon terms (`UBERON:0001135`, Smooth Muscle Tissue). Returns relationships between source term and Uberon term.
5. **Create sample-to-tissue mappings** based on (3) and (4)
6. **Find disagreements in mappings** based on (3) and (4), which my indicate errors in sample metadata or ontologies.

### Mapping by name

Informal tissue names are mapped Uberon term identifiers by checking for exact name matches to Uberon term names and their synonyms in the extended Uberon ontology.

### Mapping by term

A mapping between a provided term (e.g. a FANTOM sample identifier or CL identifier) associated with a sample and an Uberon term is created by:

* Finding all relationships of interest (e.g. `is_a`, `related_to`, `part_of`, `derives_from`, `intersection_of`, `union_of`) to any other sample, cell or Uberon term.
* Propagate any relationships found using the same list of relationships, until either an Uberon term is found, or no new relationships are found, or you reach the root terms of the ontology. 

In this way, some mappings can be made via the cell ontology, which cannot be made through Uberon alone, for example: Macrophage - monocyte derived, donor3 `is_a` Human macrophage sample `derives_from` Macrophage `is_a` Monocyte `is_a` Leukocyte `part_of` Immune System, e.g. this sample is related to the immune system.

### Using disagreements between mappings to improve biological ontologies

The uberon_py package has two methods of mapping to tissues. Where both can be ran, disagreements between these mappings can be checked. For the FANTOM5 data, this was possible, and disagreements between these mappings revealed problems in the biological ontologies and experiment metadata that were provided to the package in order to create the mappings. These could then be fed back to the maintainers of these ontologies and datasets in order to improve/correct them. 

Disagreements between the tissue-sample mappings created through the (FANTOM, CL and Uberon) ontologies and those created using human annotation illuminates what may be a lack of specificity, incompleteness in, or disagreement between FANTOM, CL, or Uberon annotations, either in creating ontologies or annotating tissues to samples. The process of mapping FANTOM to Uberon tissues found twenty-two such disagreements, of which FANTOM, Uberon, and CL where appropriate have been informed via GitHub issues, some of which have already sparked changes in the ontologies. 

Three different types of example are described below, to give an idea of how multiple mappings may be used to improve annotation.

#### Missing Uberon annotation: `Bronchus part_of some Lung`
For example, sample `FF:11511-119G8` (Bronchial Epithelial Cell, donor1) is mapped by name to `UBERON:0002048` Lung, but by ontology to `UBERON:0002185` Bronchus, and these two Uberon terms are not straightforwardly related by any formal relation in the Uberon ontology although the description text for Bronchus says “the upper conducting airways of the lung”. 

Similar missing annotations were discovered between Aorta and Artery, and Hair follicle and Dermal papilla.

#### Mislabelled FANTOM sample: `FF:11590-120G6` should be labelled _Alveolar Epithelial Cells_ not _Renal Glomerular Endothelial Cells_ 
The FANTOM sample ontology contains two samples named Renal Glomerular Endothelial Cells, donor2; `FF:11590-120G6` and `FF:11594-120H1`. One of these is a mislabelled sample, which is actually an Alveolar Epithelial Cell sample.

#### Imprecise FANTOM annotation to tissue
Several FANTOM tissues are labelled by name colloquially, rather than precisely. For example, both Nucleus pulpopus and Vertebra are labelled Spinal cord (although the spinal cord itself is considered disjoint from these entities, both by definition, and in the Uberon ontology). It’s for this reason that the ontology mapping is preferred over the labelled sample name in creating the overall FANTOM sample-to-tissue mapping.
