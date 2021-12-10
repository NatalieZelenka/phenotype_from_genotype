# phenotype_from_genotype
Repo for tracking my thesis' conversion to jupyter book.

## Website:
To build html:
`jupyter-book build book`

For interactive images:
Replace the `img` tags with an `iframe` tag pointing to the standalone html (which must be copied into `_build/html/_images`). (Not ideal. Hopefully they will fix.). I.e. Copy in the following:
```html
<!--
<a class="reference internal image-reference" href="../_images/combining_funnel_interactive.html"><img alt="../_images/combining_funnel_interactive.html" src="../_images/combining_funnel_interactive.html" style="height: 150px;" /></a> -->
<iframe src="../_images/combining_funnel_interactive.html" width="600px" height="300px" style="border:none;"></iframe>
```

To view/check:
`open book/_build/html/index.html`

## To build PDF
<!--
`jupyter-book build book --builder pdfhtml`
`jupyter-book build book --builder pdflatex` <- fails
-->

<!--
First build latex:
`jupyter-book build book --builder latex`

Next edit `_build/latex/thesis.tex`:
- Delete the jupyter-book intro
- Delete the biography (auto-generated, so there will be two)
- Make sure anything don't want numbered has a * after it e.g. `\chapter*{Glossary}` 
- Delete everything to do with `\index`
- Interactive figures: add in the static versions
- Code blocks: remove/link to website.

Finally, move to the `latex` directory and run `make`.
-->

` jupyter-book build . --builder pdfhtml`
