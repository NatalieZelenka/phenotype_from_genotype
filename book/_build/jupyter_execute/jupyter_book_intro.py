# Start Here

[//]: # (TODO: Check Thesis title)
[//]: # (TODO: Check links)
[//]: # (TODO: Check reference to chapters)

You're looking at Natalie Thurlby's thesis <!-- TODO: Thesis title--> as a [jupyter book](https://jupyterbook.org/intro.html). 

## What is a Jupyter Book?

This jupyter book thesis is made up of markdown files and jupyter notebooks, which are kept in [this](link-to-github) GitHub repo. The code for all graphs in <!--chapters X, Y and Z of--> this thesis are available there (as jupyter notebooks), which you can run for yourself using [binder](link-to-binder) if you like. This jupyter book thesis is therefore as up-to-date and as reproducible as possible.

### Contents and navigation
You can use the sidebar on the left to navigate to a chapter or section, while the sidebar on the right navigates more finely within a "page" of the book. If you'd like an overview of the whole book, you can look at [the table of contents](link-to-full-table-of-contents). 

At the bottom of each page are buttons which let you go to the previous or next sections.

### Viewing code
Where code is used to collect data, perform an analysis, or create a graph that is shown or mentioned in the book, you can see the code used to create it, by clicking on the "Click to show" arrow like the one here:

print("How did I make this output?")
# This is how

### References
References for each page are given at the end of the page, but there is also a [separate bibliography](link-bib) for the full book.

## Give me the PDF 
Alternatively, you can download the thesis as a PDF [here](link-to-download). 

[link-to-download]: <!-- -->
[link-to-full-table-of-contents]: <!-- -->
[link-to-github]: <!-- -->
[link-to-binder]: <!-- -->
[link-bib]: <!-- -->



```{toctree}
:hidden:
:titlesonly:
:caption: Front Matter

Title Page <front-matter/title-page>
front-matter/list-of-figures
front-matter/list-of-tables
front-matter/full-table-of-contents
front-matter/acknowledgements
front-matter/abstract
front-matter/declaration
```


```{toctree}
:hidden:
:titlesonly:
:numbered: 
:caption: Main book

c01-introduction/intro
c02-biology-background/0-bg-biology
c03-compbio-background/0-compbio-bg
c04-snowflake/0-index
c05-combining/0-index
c06-filter/0-index
c07-conclusion/0-conclusion
```


```{toctree}
:hidden:
:titlesonly:
:caption: End Matter

Bibliography <end-matter/reference>
```