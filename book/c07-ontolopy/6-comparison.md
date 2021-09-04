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

<!--
# Comparison to SPARQL with Owlready2
Compare lengths of time to load, and query Uberon using SPARQL and owlready2

+++

## Loading the ontology

### Code compactness

### Speed

### OWL versus OBO

```{code-cell} ipython3
import owlready2
import time
from myst_nb import glue

start = time.time()
uberon = owlready2.get_ontology("http://purl.obolibrary.org/obo/uberon.owl")
ont = uberon.load()
print(uberon)
glue('load-time-owlready',f"{time.time()-start:.2f} seconds")
```

```{code-cell} ipython3
sparql_query = """
select ?x WHERE { 
    ?x :is_a obo:UBERON_0002050 
}
"""
```

```{code-cell} ipython3
print(len(list(owlready2.default_world.sparql("""

SELECT ?x WHERE { 
    ?x uberon:BFO_0000050 uberon:UBERON_0000358 
}
"""))))
```

## Querying the ontology


### Generalisability
Must choose the maximum length of the path

### Code compactness
Gets bigger for larger length of relation path
And this is a compact form of this code (i.e. we are not [using SPARQL's BIND command for readability](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial#BIND,_BOUND,_IF))

### Speed

### Found relations

```{code-cell} ipython3
go = owlready2.get_ontology("http://purl.obolibrary.org/obo/go.owl").load()

# Get the number of OWL Class in GO
list(default_world.sparql("""
           SELECT (COUNT(?x) AS ?nb)
           { ?x a owl:Class . }
    """))
```

```{code-cell} ipython3
list(go.sparql("""
           SELECT (COUNT(?x) AS ?nb)
           { ?x a owl:Class . }
    """))
```

```{code-cell} ipython3

```
-->