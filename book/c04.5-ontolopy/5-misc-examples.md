(ontolopy-examples-2)=
# More example uses

(FANTOM5-inconsistencies-example)=
## Example 1: finding inconsistencies in the FANTOM5 data
[//]: # (TODO: Add a table here of all the inconsistencies: medium priority)
For the FANTOM5 data, disagreements between these mappings revealed problems in the biological ontologies and experiment metadata that were provided to the package in order to create the mappings. 
These could then be fed back to the maintainers of these ontologies and datasets in order to improve/correct them. 

Disagreements between the tissue-sample mappings created through the (FANTOM, CL and Uberon) ontologies and those created using human annotation illuminates what may be a lack of specificity, incompleteness in, or disagreement between FANTOM, CL, or Uberon annotations, either in creating ontologies or annotating tissues to samples. 
The process of mapping FANTOM to Uberon tissues found twenty-two such disagreements, of which FANTOM, Uberon, and CL where appropriate have been informed via GitHub issues, some of which have already sparked changes in the ontologies. 

Three different types of example are described below, to give an idea of how multiple mappings may be used to improve annotation.

### Finding samples that are missing annotations to tissues
[//]: # (TODO: output list of fantom terms to annotate to c+ t-cell)

### Missing Uberon or CL annotation
**Example: `Bronchus part_of some Lung`**

One type of problem that can be revealed is a missing link in an ontology.

An example of this that was found using the FANTOM data set was that there was no formal relationin the Uberon ontology between *Bronchus* and *Lung*, despite the fact that the description text for Bronchus says “the upper conducting airways of the lung”.

This was found because the sample `FF:11511-119G8` (Bronchial Epithelial Cell, donor1) is mapped by name to `UBERON:0002048` Lung, but by ontology to `UBERON:0002185` Bronchus. 
This was flagged as inconsistent because there are no relation in the Uberon ontology between these terms.

Similar missing annotations were discovered between *Aorta* and *Artery*, *Hair follicle* and *Dermal papilla*, and *Skeletal muscle myoblast* and *Skeletal muscle fiber*.

#### Mislabelled sample
**Example: `FF:11590-120G6` should be labelled _Alveolar Epithelial Cells_ not _Renal Glomerular Endothelial Cells_**

Sometimes samples are simply mislabelled.
In this case the mistake was revealed by testing the agreement between annotations because the mistake is only for the name, but not tissue annotation.

[//]: # (TODO: Link to other person who found this on researchgate/wherever)
The FANTOM sample ontology contains two samples named Renal Glomerular Endothelial Cells, donor2: `FF:11590-120G6` and `FF:11594-120H1`. 
One of these is a mislabelled sample, and it is actually an Alveolar Epithelial Cell sample.

#### Imprecise annotation to tissue
[//]: # (TODO: should prefer more precise mapping whichever way around it is? Or not... Need to think.)
There are two types of disagreements that arise from imprecise annotation: those that cause a disagreement between mappings, and those that can be resolved automatically by choosing the more precise term, but still reveal a better possible mapping.

__Example: *Nucleus pulpopus* as *Spinal cord*__
Several FANTOM tissues are labelled by name colloquially, rather than precisely. 
For example, both *Nucleus pulpopus* and *Vertebra* are labelled *Spinal cord* (although the spinal cord itself is considered disjoint from these entities by definition, and in the Uberon ontology).
It’s for this reason that the ontology mapping is preferred over the labelled sample name in creating the overall FANTOM sample-to-tissue mapping.

__Example2: `FF:11423-118G1 is_a` *dermal melanocyte*__
Sometimes the text in the samples information file can help us to reach better mappings in the sample ontology file. 
For example sample `FF:11423-118G1` (and five other similar samples) are mapped to `CL:0000148` (*melanocyte*), which is a cell that can come from many different parts of the body (skin, heart, eyes, etc), so `uberon-py` can only map this tissue to several tissues (some of which this cell will not have come from) if the {ref}`child mapping<child-mapping>` functionality used.
However, since the sample was labelled as coming from the "skin", it's clear that this sample would have been better annotated to `CL:0002482` (*dermal melanocyte*).


## Example 2: Finding disease-related samples
[//]: # (TODO: Open as ipynb and bring over mapping bits and pieces from c05-filter)
You can choose what kinds of samples you want to find, by restricting the types of relations that you are interested in.