(ont-fw)=
# Future Work
I keep an updated [roadmap for Ontolopy](https://nataliethurlby.github.io/ontolopy/contents/roadmap.html) on the documentation website and a detailed list of [issues on GitHub](https://github.com/NatalieThurlby/ontolopy/issues).

(opyv2)=
## v2.0.0
The main priority for Ontolopy is reaching a stable version for release, user-testing, and publishing the work.

You can see the full list of features for the [v2.0.0 Milestone](https://github.com/NatalieThurlby/ontolopy/milestone/1) on GitHub, but to summarise:
- Finish tutorials for all functions/methods
- Reach 80% test coverage
- User-testing
- Benchmark speed against OWL reasoning

<!--If this proved useful, then allowing R-users to use Ontolopy by creating a wrapper to R using [`reticulate`](https://rstudio.github.io/reticulate/).-->

(opyadditional)=
## Other potential improvements to Ontolopy

In addition to the barebones necessities for v2.0.0 above, there are a number of more ambitious pieces of functionality which would improve its' usefulness.

(text-search-ont)=
### Text-search and fuzzy-matching
The `Uberon.map_by_name` function currently implements a slow search of names in ontologies, but this search could be both much quicker and more general (e.g. able to use wild cards, or search in any field to create mappings), i.e. similar in fuctionality to [OwlReady2](https://pypi.org/project/Owlready2/){cite}`Lamy2017-hv`'s [`search` function](https://owlready2.readthedocs.io/en/v0.32/). 
Fuzzy-matching then expand this functionality to help capture misspelled information.

(complex-queries-ont)=
### Functionality for more complex queries
Ontolopy doesn't contain tools for making complex queries. 
For example, if we want to find out which samples are made of precursor cells, we have to find *in vivo* samples which are or are derived from stem cell samples.
In this particular case, the difficulty is partly because `derives_from` means "extracted from", or "extracted from and then had lots of things done to it", which can change the meaning.

If we want to do this at the moment, we have to make two queries to Ontolopy separately and then combine them (as in {ref}`this example<can-have-human-part-define>`), which is clearly not very user-friendly.

(opygo)=
### `opy.Go`
The `opy.Uberon` class adds functionality specifically for the Uberon ontology, helping users to map between samples (or other entities) and tissues for their specific area of interest.
We could imagine similar functionality for the Gene Ontology, and perhaps integration with GOATools{cite}`Klopfenstein2018-eh`.

(pronto-integration)=
### Integration with Pronto
Test integration with Pronto to investigate how it would effect how the speed of the current implementation.

(opyvalidity)=
### Ontology validity
[//]: # (TODO: Write/cite ROBOT)
Since it is possible with Ontolopy to add new terms and relationships, to merge OBO files, and to build ontologies from scratch, it might be useful for Ontolopy to have some functionality for checking the validity of the OBO object automatically.
This could include for example checking for cyclic relationships, or checking if there is any missing information such as ontology version numbers, or required attributes for terms. 
This could use some of the same approaches as ROBOT.

(opymiscfw)=
## Miscellaneous
- **NLP similarity measures**: An earlier version of Ontolopy included text-mining to find similar terms using a {ref}`TF-IDF<tf-idf>` like measure to create a similarity measure based on co-occurance, e.g. “mental” and “brain” have high similarity since they often appear in the same document (documents being term descriptions). This functionality is not currently in Ontolopy, and doesn't really align with the core functionality of the module, but it could be released separately to find potential missing ontology links.
- **Versioned docs sphinx extension:** Although it is not really an output of Ontolopy, I also hope to be able to release the {ref}`sphinx extension<sphinx-extension>` that I used to create versioned documentation soon.
