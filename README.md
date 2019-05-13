Jinjafy
==================

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Source: <https://www.github.com/derekmerck/jinjafy>


Overview
----------------

Data-driven document templating and format conversion using Jinja2 and Pandoc.


Setup
----------------

```bash
$ pip install https://github.com/derekmerck/jinjafy
```

CLI Usage
----------------

Generate a static data-driven [revealjs][] presentation.

[revealjs]: https://revealjs.com/#/

```bash
$ jinjafy revealjs_2d example/sample_presentation.yaml -t revealjs --theme moon
```

Generate a data-driven cv.

```bash
$ jinjafy cv example/sample_cv.yaml -t docx --bibliography=example/sample_bib.csl.yaml
```

When working with references, it can be convenient to setup your bibliography file using an environment variable:

```bash
$ export JINJAFY_BIBLIOGRAPHY="/path/to/my_bib.csl.yaml"
```

REST Server Usage
----------------

Serve a dynamically generated data-driven revealjs presentation.

```bash
$ jinjafy-rest
$ curl http://localhost:8080/render/revealjs_2d?source=example%2Fsample_presentation.yaml&theme=moon
```

Source may be a URL or a relative path to the server for locally installed content.


Dependencies
----------------

- [Jinja2][]
- [Pandoc][] and `pandoc-citeproc`
- [Click][]
- [Connexion][]

[Jinja2]: http://jinja.pocoo.org
[Pandoc]: https://pandoc.org
[Click]: https://palletsprojects.com/p/click/
[Connexion]: https://connexion.readthedocs.io/en/latest/


License
----------------
MIT
