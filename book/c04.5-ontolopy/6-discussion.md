# Discussion

## Usage

(quality-coverage)=
## Mapping quality and coverage
[//]: # (TODO: Write)

Of course we don't have a gold standard to compare to.

### Disagreements

[//]: # (TODO: Write - how many agreements versus disagreements? Also Qualitatively describe.)

### Coverage

[//]: # (TODO: Write - sensitive to inclusion of the correct data, e.g. CL)


## Speed 

### Ontology mapping
As we saw in the {ref}`examples<ontolopy-examples-2>`, Ontolopy runs quickly for most uses involving operations on or queries to ontology objects (typically less than half a second). 
The time taken depends on the size of the ontology, the number of the chosen relations, and the popularity of those relations within the ontology.
However, making a query with a large number of relations to check can inflate how long a query takes to run.

### Name mapping slow
[//]: # (TODO: Write)


## Limitations

### It's difficult to make complex queries
[//]: # (TODO: Write)
For example, if we want to find out which samples are made of precursor cells, we have to find *in vivo* samples which are or are derived from stem cell samples.
In this particular case, the difficulty is partly because `derives_from` means "extracted from", or "extracted from and then had lots of things done to it", which can change the meaning.



### Ontologies don't always capture the directionality of relationships that we are interested in
[//]: # (TODO: Check if child-mapping still exists)
Ontology structures are directed and acyclic, and we depend on the directionality of the relationships in order to infer new relationships from these graphs. 
These are very well thought out, but very general, so they don't always simply suit our use case. 

In terms of mapping tissues, this was noticeable in terms of the `develops_from` relationship.
For example `CL:0008002` *skeletal muscle fiber* `develops_from` `CL:0000515` *skeletal muscle myoblast*. 
The acylic nature of ontologies, means that if `develops_from` is captured per term, then `develops_into` isn't.
If we look for parent terms only, we will not find that *skeletal muscle myoblast* develops into skeletal muscle fiber, and therefore we will not find that it develops into a part of *skeletal muscle tissue* (`UBERON:0001134`). 
But, currently, we would need to write a specific script if we wanted to capture these kinds of relationships. 
This would likely need more complex logic than simply turning on `child-mapping=TRUE`, because for example, we might only want to capture `develops_into` relationships where the cell of interest is a single-fate stem cell or a pre-cursor cell, so that we don't end up with too much broad and meaningless mapping, or for example we might only be interested in cell types that are found in adults.

In order to do something like this, we would need to have something more like a query language (e.g. SPARQL) for interacting with the ontology, which is beyond this scope of this package.

### Only maps to one tissue
When mapping by ontology or name, multiple mappings can be retrieved, but when finding an overall mapping, only one (per method) is chosen. 
An good example of this is leukocytes, which are part of the blood and the immune system.

### Weird choices in implementation
[//]: # (TODO: Write)
- relation strings
- not matching up with existing tools: (+s a small number of very well maintained dependencies, it's not clear how well-used these tools are anyway)

## Fit-for-purpose
[//]: # (TODO: Write)