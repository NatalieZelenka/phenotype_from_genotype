# phenotype_from_genotype
Repo for tracking my thesis' conversion to jupyter book.

To build:
`cd ~/phd/jupyter_books_etc/jekyll-version/phenotype_from_genotype/book`
`jupyter-book build .`

To view/check:
`open _build/html/index.html`

# Notes on Rmd
At the moment, I am using `jupytext c05-combining/3-data-wrangling.Rmd --to md:myst` to convert from Rmarkdown to Myst. (Not properly tested). The reason I want to use Rmd is the ability to use R and Python in one notebook. I'm not sure if this will work in Myst/Jupyter Book. The alternative, is that I will have to split up chapters into things that only use one format, i.e. move the data downloading into the 'data' chapter (as an R ipynb) and then have the 'data wrangling' chapter be a python ipynb.