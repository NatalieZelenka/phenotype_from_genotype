# Future Work
I keep an updated [roadmap for `Ontolopy`](https://nataliethurlby.github.io/ontolopy/contents/roadmap.html) on the documentation website and a detailed list of [issues on GitHub](https://github.com/NatalieThurlby/ontolopy/issues).

## v2.0.0
The main priority for Ontolopy is reaching a stable version for release, user-testing, and publishing the work.
You can see the full list of features for the [v2.0.0 Milestone](https://github.com/NatalieThurlby/ontolopy/milestone/1) on GitHub, but to summarise:
- Finish tutorials for all functions/methods
- Reach 80% test coverage
- User-testing

## Other potential improvements to Ontolopy
### Text-mining
[//]: # (TODO: Add text-mining part to uberon-py and test on different data sets)
[//]: # (TODO: fix/write)
- Speeding up
- Improve existing basic text-mining by using {ref}`TF-IDF<tf-idf>`, and then creates a similarity measure based on cooccurance, e.g. “mental” and “brain” have high similarity since they often appear in the same document  (documents are term descriptions).

(pronto-integration)=
### Integration with Pronto
Test integration with Pronto to investigate how it would effect how the speed of the current implementation.

### `opy.Go`
The `opy.Uberon` class adds functionality specifically for the Uberon ontology.
We could imagine similar functionality for the Gene Ontology, and perhaps integration with GOATools{cite}`Klopfenstein2018-eh`.

### Ontology validity
[//]: # (TODO: Write/cite ROBOT)
Since it is possible with `Ontolopy` to add new terms and relationships, to merge OBO files, and to build ontologies from scratch, it might be useful for `Ontolopy` to have some functionality for checking the validity of the OBO object automatically.
This could include for example checking for cyclic relationships, or checking if there is any missing information such as ontology version numbers, or required attributes for terms. 
This could use some of the same approaches as ROBOT.

## Miscellaneous
Although it is not really an output of `Ontolopy`, I also hope to be able to release the {ref}`sphinx extension<sphinx-extension>` that I used to create versioned documentation soon.
