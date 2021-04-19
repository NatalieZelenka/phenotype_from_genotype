# How `Ontolopy` works

This section briefly describes the tools and practices that `Ontolopy` is built upon.

[//]: # (TODO: cte everything)

## Practices
### Development philosophy

(continuous-integration)=
```{margin} Continuous Integration
Continuous integration, delivery, and deployment enable running tests and updating packaging frequently by automatically doing these things when changes are made to a version-controlled repository{cite}`The_Turing_Way_Community2019-xk`.
```

`Ontolopy` aspires to Research Software Engineering best practice, including:
 - automated testing with [pytest](https://docs.pytest.org/en/stable/) which are {ref}`continuously integrated<continuous-integration>` with [GitHub Actions](https://github.com/features/actions).
 - [Semantic Versioning](https://semver.org/) to make the package versions informative and useful for others. 
 - thorough [documentation](https://nataliethurlby.github.io/ontolopy), which is versioned (meaning that you can always reach the documentation corresponding to the version of the software you are using).
 
It is also Open Source (with an MIT license), and available on [GitHub](https://github.com/NatalieThurlby/ontolopy), and distributed via the [Python Package Index](https://pypi.org/project/ontolopy/).

### Style

## Tools
## Packaging
twine


### Testing
- GitHub Actions
    - PyTest

### Dependencies
`Ontolopy` has a small number of dependencies: `numpy`{cite}`harris2020array` and `pandas`{cite}`reback2020pandas` for general data manipulation, and `validators` (for validating URLs) 

### Logging
in-built `logging` module, 

### Documentation
- Versioning
-  Sphinx, sphinx.ext.autosummary, GitHub pages
pydata-sphinx-theme

[//]: # (TODO: Fill in website address, link/cite gitpython and pygithub)
(sphinx-extension)=
The versioned documentation (accessible e.g. at `/{tagged_version}`) was created using a local sphinx extension, which uses gitpython and pygithub.


