# How Ontolopy works

This section briefly describes the tools and practices that Ontolopy is built upon.

[//]: # (TODO: cite everything, validators, semvar, twine pytest sphinx extensions)
[//]: # (TODO: add version link for Ontolopy)

## Practices
__Development philosophy:__

[//]: # (TODO: Aside: RSEing)

(continuous-integration)=
```{margin} Continuous Integration
Continuous integration, delivery, and deployment enable running tests and updating packaging frequently by automatically doing these things when changes are made to a version-controlled repository{cite}`The_Turing_Way_Community2019-xk`.
```

Ontolopy aspires to [Research Software Engineering](https://society-rse.org/) best practice, including:
 - Automated testing with [pytest](https://docs.pytest.org/en/stable/) which are {ref}`continuously integrated<continuous-integration>` with [GitHub Actions](https://github.com/features/actions).
 - [Semantic Versioning](https://semver.org/) to make the package versions informative and useful for others. 
 - Thorough [documentation](https://nataliethurlby.github.io/ontolopy), which is versioned. This means that you can always reach the documentation corresponding to the version of the software you are using - you can access this at `/versions/{tagged_version}`, e.g. `v1.0.2-beta` is [here](https://nataliethurlby.github.io/ontolopy/versions/1.0.2-beta/).) The documentation is also built automatically using GitHub Actions.
 - Keeping a small number of dependencies, which are: `numpy`{cite}`harris2020array` and `pandas`{cite}`reback2020pandas` for general data manipulation, and `validators` (for validating URLs) 

[//]: # (TODO: Aside about Open Source)

__Open Source:__

Ontolopy is Open Source (with an MIT license), and available on [GitHub](https://github.com/NatalieThurlby/ontolopy).
This means that:
- anyone can contribute to it. I provided [developer guidance](https://nataliethurlby.github.io/ontolopy/contents/develop.html#developer-guidance) and ["good first issues"](https://github.com/NatalieThurlby/ontolopy/labels/good%20first%20issue) to reduce the barrier to this.
- anyone can download, use, reuse, or adapt the source code for their own work. This is made easier by the fact that Ontolopy is distributed via the [Python Package Index](https://pypi.org/project/ontolopy/).

__Style:__

Ontolopy uses consistent programming style and conventions to make it easier for others to work with (these were adapted from the [MetaWards](https://metawards.org/) package developer guide{cite}`Woods_undated-rm`:
- Python-style naming conventions:
    - Packages: lowercase (single word)
    - Classes: CamelCase
    - Methods, Functions, Variables: snake_case
- Functions with leading underscores (e.g. `_extract_source()`)  are meant for internal use only.
- Relative imports should be used at all times, with imports ideally delayed until they are needed.

## Tools
[//]: # (TODO: Aside about Packaging? Where do I first say packaging?)

__Packaging:__

Packaging is carried out automatically using GitHub actions whenever a new version of the software is "tagged" via GitHub. 
This uses the [`twine`](https://twine.readthedocs.io/en/latest/){cite}`Stufft2019-mg` Python Package. 

__Testing:__

Tests are automatically run whenever Ontolopy code is changed on either the GitHub `main` or `dev` (development) branches. 
This is achieved with GitHub Actions and the [`pytest`](https://docs.pytest.org/){cite}`pytestx.y` Python Package.

__Logging:__

Python's in-built [`logging`](https://docs.python.org/3/library/logging.html) module is used to integrate logging messages from dependencies as well as adding useful logging messages for Ontolopy users.
This allows informative messages to be printed to the console or to a log file.

[//]: # (TODO: Aside: docstrings)
__Documentation:__

Ontolopy's documentation is hosted on GitHub pages [here](https://nataliethurlby.github.io/ontolopy/), and built using [`Sphinx`](https://www.sphinx-doc.org/) with the [`pydata-sphinx-theme`](https://pydata-sphinx-theme.readthedocs.io/) theme{cite}`PyData_Community2019-rw`, and it is automatically built using GitHub Actions whenever there are changes to the development branch or when there is a new release.
It also makes use of following tools:
- [`peaceiris`'s GitHub pages action](https://github.com/peaceiris/actions-gh-pages) - to automatically update a GitHub pages site in a GitHub Action.
- [`sphinx.ext.autosummary`](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) - to automatically build an API Reference from docstrings in code. 

(sphinx-extension)=
In addition to the above tools which were built by others, I wrote a small local sphinx extension to create the versioned documentation.
This, in turn, uses [gitpython](https://gitpython.readthedocs.io/) and [pygithub](https://pygithub.readthedocs.io/). 