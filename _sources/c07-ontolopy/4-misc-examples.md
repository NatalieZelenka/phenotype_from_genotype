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

(ontolopy-examples-2)=
# Example uses: mapping samples to diseases or phenotypes

There are a number of potential uses for Ontolopy. 
In this section, I show two simple examples to demonstrate this usefulness. 
These show how Ontolopy can be used to:
1. {ref}`Find disease-related samples<opydiseaseexample>`
2. {ref}`Find samples of pluripotent stem cells<opycelldifferentiation>` (cells that can turn into different tissue types)

Then in {ref}`the next section<ontolopy-mapping-example>` I give the more detailed and complex example of creating a mapping between samples and tissues (which is what Ontolopy was created for specifically), and how this was used to {ref}`find inconsistencies in the FANTOM5 data<FANTOM5-inconsistencies-example>`.

(ontolopy-example-inputs)=
## Inputs
The examples of using Ontolopy in this Chapter use input files from FANTOM5{cite}`Lizio2015-ph` (for samples) and Uberon{cite}`Mungall2012-nc` (the cross-species anatomy ontology).

```{margin} Choosing ont_ids
When we read in ontologies using Ontolopy, if you do not provide `ont_ids`, Ontolopy will keep all ontology term identifiers of the form `LETTERS:NUMBERS`, but often there are many external reference terms (`xref`s) that make the ontology object larger for no gain, so it's recommended to provide them.

When providing `ont_ids`, it's important that you keep all terms that you're interested in, as everything else is discarded.
```

```{code-cell} ipython3
:tags: [hide-input, remove-output]

import ontolopy as opy
import pandas as pd 
from myst_nb import glue
import time

# Read in files:
# -------------
fantom_obo_file = '../c08-combining/data/experiments/fantom/ff-phase2-170801.obo.txt'
fantom_samples_info_file = '../c08-combining/data/experiments/fantom/fantom_humanSamples2.0.csv'
uberon_obo_file = '../c08-combining/data/uberon_ext_210321.obo' 

# Uberon OBO:
uberon_obo = opy.load_obo(
    file_loc=uberon_obo_file, 
    ont_ids=['GO', 'UBERON','CL'], 
)

# FANTOM OBO:
fantom_obo = opy.load_obo(
    file_loc=fantom_obo_file, 
    ont_ids=['CL', 'FF', 'GO', 'UBERON', 'DOID'],
)

# FANTOM Samples Info file:
fantom_samples_info = pd.read_csv(fantom_samples_info_file, index_col=1)


# Glue Samples Info excerpt:
# --------------------------
indices = [1,9,11]  # choose rows for variety
display(fantom_samples_info.iloc[indices])
glue("fantom-samples-info-excerpt", fantom_samples_info.iloc[indices], display=False)
```

(opy-fantom5)=
### FANTOM5 

[//]: # (TODO: Check display of all tables in this section, potentially link to website version for full excerpt)

Large experiments sometimes include an ontology of samples instead of or (more frequently) in addition to a samples information file.
The data from the FANTOM5 experiment{cite}`Lizio2015-ph` is one such example of this.
I {ref}`have already explained the FANTOM5 data in more detail<fantom5-expression-data>` but for now the only things we need to keep in mind are that:
1. The FANTOM5 experiment measures transcript expression in a wide variety of samples, across many tissue and cell types.
2. FANTOM5 provide an [ontology of samples](https://fantom.gsc.riken.jp/5/datafiles/latest/extra/Ontology/ff-phase2-170801.obo.txt) as well as a [sample information file](https://fantom.gsc.riken.jp/5/datafiles/reprocessed/hg38_latest/basic/HumanSamples2.0.sdrf.xlsx) (containing short text descriptions of samples).

```{glue:figure} fantom-samples-info-excerpt
:figwidth: 800px
:name: fantom-samples-info-excerpt

An excerpt of the FANTOM sample info file, showing sources of text-based information, e.g. "heart, adult, pool1" in the *Charateristics [description]* field, and mapping to ontology term in the index (`FF:10016-101C7`).
```

{numref}`fantom-samples-info-excerpt` shows an excerpt of the FANTOM Samples Information file. 
This kind of file is typical of transcription experiments: a csv file containing hand-entered text-based information, using non-specific lay terms for samples e.g. "heart".

The FANTOM ontology file links specific FANTOM samples to more general types of FANTOM samples and to Uberon tissues and CL cell types. 

(fantom-obo-excerpt)=
For example an excerpt of the FANTOM ontology OBO file is:
```
[Term]
id: FF:0000076
name: hepatic sinusoidal endothelial cell sample
namespace: FANTOM5
synonym: "hepatic sinusoidal endothelial cell" EXACT []
is_a: FF:0000002 ! in vivo cell sample
intersection_of: FF:0000002 ! in vivo cell sample
intersection_of: derives_from CL:1000398 ! endothelial cell of hepatic sinusoid
intersection_of: derives_from UBERON:0001281 ! hepatic sinusoid
relationship: derives_from CL:1000398 ! endothelial cell of hepatic sinusoid
relationship: derives_from UBERON:0001281 ! hepatic sinusoid
created_by: tmeehan
creation_date: 2011-03-01T04:51:50Z
```

(opyuberondata)=
### Uberon
As I mentioned in {numref}`Section %s<uberon-is>`, Uberon is a cross-species anatomy ontology with excellent linkage to other ontologies. 
As we can see above, the FANTOM5 ontology links FANTOM samples to Uberon.
This means that the Uberon{cite}`Mungall2012-nc` [extended ontology OBO file](http://purl.obolibrary.org/obo/uberon/ext.obo) can then be used to further link the samples to human disease or gene ontology terms.

For example, here is an excerpt of the Uberon extended OBO file (non-consecutive lines for brevity), showing how the Uberon extended ontology could be used to link a FANTOM sample to a GO term:

```
[Term]
id: UBERON:0001281
name: hepatic sinusoid
alt_id: UBERON:0003275
def: "Wide thin-walled blood vessels in the liver. In mammals they have neither veinous or arterial markers." [http://en.wikipedia.org/wiki/Hepatic_sinusoid, ZFIN:curator]
synonym: "hepatic sinusoids" RELATED []
synonym: "liver hepatic sinusoids" EXACT [EHDAA2:0000999]
synonym: "liver sinusoid" EXACT []
intersection_of: part_of UBERON:0002107 ! liver
relationship: part_of UBERON:0004647 ! liver lobule
relationship: part_of UBERON:0006877 {source="https://github.com/obophenotype/uberon/wiki/Inferring-part-of-relationships"} ! vasculature of liver
property_value: homology_notes "(...) the amphibian liver has characteristics in common with both fish and terrestrial vertebrates. (...) The histological structure of the liver is similar to that in other vertebrates, with hepatocytes arranged in clusters and cords separated by a meshwork of sinusoids and the presence of the traditional triad of portal venule, hepatic arteriole, and bile duct.[well established][VHOG]" xsd:string {date_retrieved="2012-09-17", external_class="VHOG:0000708", ontology="VHOG", source="http://bgee.unil.ch/", source="DOI:10.1053/ax.2000.7133 Crawshaw GJ, Weinkle TK, Clinical and pathological aspects of the amphibian liver. Seminars in Avian and Exotic Pet Medicine (2000)"}

[Term]
id: UBERON:0002107
name: liver
def: "An exocrine gland which secretes bile and functions in metabolism of protein and carbohydrate and fat, synthesizes substances involved in the clotting of the blood, synthesizes vitamin A, detoxifies poisonous substances, stores glycogen, and breaks down worn-out erythrocytes[GO]." [BTO:0000759, http://en.wikipedia.org/wiki/Liver]
synonym: "iecur" RELATED LATIN [http://en.wikipedia.org/wiki/Liver]
is_a: UBERON:0002365 {source="BTO", source="EHDAA2", source="GO-def"} ! exocrine gland
is_a: UBERON:0004119 ! endoderm-derived structure
is_a: UBERON:0005172 ! abdomen element
is_a: UBERON:0006925 ! digestive system gland
disjoint_from: UBERON:0010264 ! hepatopancreas
relationship: contributes_to_morphology_of UBERON:0002423 ! hepatobiliary system
relationship: produces UBERON:0001970 ! bile
relationship: site_of GO:0002384 ! hepatic immune response
relationship: site_of GO:0005978 ! glycogen biosynthetic process
relationship: site_of GO:0005980 ! glycogen catabolic process
property_value: external_definition "Organ which secretes bile and participates in formation of certain blood proteins.[AAO]" xsd:string {date_retrieved="2012-06-20", external_class="AAO:0010111", ontology="AAO", source="AAO:BJB"}
property_value: function_notes "secretes bile and functions in metabolism of protein and carbohydrate and fat, synthesizes substances involved in the clotting of the blood, synthesizes vitamin A, detoxifies poisonous substances, stores glycogen, and breaks down worn-out erythrocytes[GO]." xsd:string
```

These excerpts show how `FF:0000076` (*hepatic sinusoidal endothelial cell sample*s) are `derived_from` the *hepatic sinusoid* which is `part_of` *the liver* the `site_of` *hepatic immune response*, *glycogen biosynthetic process* and *glycogen catabolic process*. 
There are many such relationships in these files: Ontolopy provides an easy way of extracting these.

```{admonition} Warning: not all relationships are easy to interpret
:name: ontolopy-relationship-interpretation
:class: warning

In this case, we do not have enough information to infer that *hepatic sinusoidal endothelial cell sample*s are a `site_of` (for example) the *hepatic immune response* because it could be another, disjoint, part of the liver that is the site of this. 
We can also not rule it out: a more specific annotation in the future might enable us to find this out with these files.

However, this information could still be useful in Computational Biology. If we don't know exactly where a process takes place, we may want to cast a wider net and look at all samples which are part of a larger tissue we know exhibits the process we are interested in.  

This is something to be aware of in general when using Ontolopy: if you are only interested in straight-forward relationships, then you often need to think carefully about the types of relationships that you ask for: `part_of` relationships need particular care.
```

(opydiseaseexample)=
## Example 1: Finding disease-related samples
[//]: # (TODO: cite disease ontology)
This first example shows a simple use-case of Ontolopy, where we are looking for relationships to any term in an ontology: in this case any relation to a Disease Ontology term (representing human diseases). 
This Ontolopy query can be done with only the FANTOM ontology.

As {ref}`we just saw<ontolopy-relationship-interpretation>`, to extract relationships from ontologies (whether using Ontolopy or with any other method), you have to think about the types of relations that you are interested in. 
For example, if we are interested in finding samples which are models for `DOID` disease terms, then we want to ask for `DOID` targets only, and `is_a` and `is_model_for` relationships only.

[//]: # (TODO: change widths of columns to improve formatting of table)

```{code-cell} ipython3
:tags: [hide-input]

def get_disease_related_samples(samples, ont):
    disease_relations_of_interest = ['is_a','is_model_for']
    disease_related = opy.Relations(
        allowed_relations=disease_relations_of_interest, 
        sources=list(samples),
        targets=['DOID'],
        ont=ont,
    )
    return disease_related

start = time.time()
disease_related = get_disease_related_samples(fantom_samples_info.index, ont=fantom_obo).dropna(subset=['to'])
time_taken = time.time()-start
print(f"Finds {disease_related.shape[0]} disease relations in {time_taken:.3f} seconds")
```

```{code-cell} ipython3
:tags: [remove-cell]

# Styling table for thesis
# ========================
disease_related['relation_text'] = disease_related['relation_text'].str.wrap(50)
disease_related['relation_path'] = disease_related['relation_path'].str.wrap(48)
to_display = disease_related.head(5).style.set_properties(**{
    'white-space': 'pre-wrap',
})
display(to_display)
glue("disease-relations-found", to_display, display=False)
```

Ontolopy can quickly (less than half a second) retrieve this information, very compactly (in one line of code if we wanted).
We can see an excerpt of the output in {numref}`disease-relations-found`.
This would be useful for example if we wanted to remove disease samples from the samples we were looking at.

```{glue:figure} disease-relations-found
:figwidth: 800px
:name: disease-relations-found

The top 5 lines of the disease-related FANTOM samples that Ontolopy found.
```

+++

(opycelldifferentiation)=
## Example 2: Find tissues that are capable of cell differentiation

[//]: # (TODO: Explain cell differentiation == stem cell)

````{margin}
```{admonition} The difference between "derives from" and "develops from"
:class: info
The Uberon extended ontology contains relations [`derives_from`](http://www.ontobee.org/ontology/RO?iri=http://purl.obolibrary.org/obo/RO_0001000): a very general term that just means one comes from the other in some sense and [`develops_from`](http://www.ontobee.org/ontology/RO?iri=http://purl.obolibrary.org/obo/RO_0002202) which means that the two are developmentally connected, i.e. `CL:0000005` *fibroblast neural crest derived* cell `develops_from CL:0000008` *migratory cranial neural crest cell*, but `FF:0100003` *intestinal cell line sample* `derives_from` `UBERON:0000160` *intestine*.
```
````

This second example showcases a different and slightly more complex example where:
1. __We want to look for relations to a specific term__ rather than a general one: in this case `GO:0030154` *cell differentiation*. 
2. __We need to use an external ontology__ (Uberon), so we use the `merge` function.
3. __We need to chain two queries and stick them together__. The `derives_from` relation in the context of the FANTOM5 ontology can mean "extracted from" or "extracted from and then do lots of things to it". To rule out the latter type of samples we only want to ask for *in vivo* samples (`is_a` *in vivo sample* `FF:0000002`) that `derives_from` cell types that are `capable_of` *cell differentiation* (`GO:0030154`).

```{code-cell} ipython3
:tags: [hide-input]

def get_differentiable_samples(samples, ont):
    in_vivo = 'FF:0000002'
    in_vivo_samples = opy.Relations(
        allowed_relations=['is_a'], 
        sources=list(samples), 
        targets=[in_vivo], 
        ont=ont,
    ).dropna(subset=['to'])
    
    differentiable = 'GO:0030154'
    differentiable_samples = opy.Relations(
        allowed_relations=['is_a', 'derives_from', 'capable_of'],
        sources=list(in_vivo_samples.index),
        targets=[differentiable],
        ont=ont,
    )
    return differentiable_samples

# merge ontology:
merged = uberon_obo.merge(fantom_obo)

# get differentiable cell samples:
start = time.time()
differentiable_samples = get_differentiable_samples(fantom_samples_info.index, ont=merged).dropna(subset=['to'])
time_taken = time.time()-start
print(f"Finds {differentiable_samples.shape[0]} relations to cell differentiation in {time_taken:.3f} seconds")
```

```{code-cell} ipython3
:tags: [remove-cell]

# Styling table for thesis
# ========================
differentiable_samples['relation_text'] = differentiable_samples['relation_text'].str.wrap(50)
differentiable_samples['relation_path'] = differentiable_samples['relation_path'].str.wrap(48)
to_display = differentiable_samples.iloc[[0,4,5,7,8]].style.set_properties(**{
    'white-space': 'pre-wrap',
})
display(to_display)
glue("differentiable-relations-found", to_display, display=False)
```

```{glue:figure} differentiable-relations-found
:figwidth: 800px
:name: differentiable-relations-found

An excerpt of the output of Ontolopy's found FANTOM samples that are or derive from cells that are `capable_of` cell differentiation (`GO:0030154`).
```

Again Ontolopy can retrieve this information compactly (2 lines of code), and in less than half a second.
An excerpt of the output is shown in {numref}`differentiable-relations-found`.
This would be useful if we wanted to look at expression in tissues that are capable of cell differentiation, for example.
