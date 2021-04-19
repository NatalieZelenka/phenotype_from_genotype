# Discussion

(quality-coverage)=
## Mapping quality and coverage
[//]: # (TODO: Write)

Of course we don't have a gold standard to compare to.

### Disagreements

[//]: # (TODO: Write - how many agreements versus disagreements? Also Qualitatively describe.)

### Coverage

[//]: # (TODO: Write - sensitive to inclusion of the correct data, e.g. CL)


## Speed 

## Limitations

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

### Weird choices?
relation strings

### Name mapping slow
[//]: # (TODO: Write)

## Fit-for-purpose
[//]: # (TODO: Write)