Jinjafy
==================

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Source: <https://www.github.com/derekmerck/jinjafy>



Overview
----------------

Stand-alone document templating and format conversion using Jinja2 and Pandoc.


CLI Usage
----------------

Generate a static data-driven revealjs presentation.

```bash
$ pip install https://github.com/derekmerck/jinjafy
$ jinjafy revealjs_2d examples/sample_data.yaml -t revealjs --theme moon
```

See `jinjafy --help` for details.


Server Usage
----------------

Serve a dynamic data-driven revealjs presentation.

```bash
$ jinjafy-rest
$ curl http://localhost:8080/render/revealjs_2d?source=example%2Fsample_presentation.yaml&theme=moon
```

Source may be a URL or relative path to the server for local content.


Dependencies
----------------

- [Jinja2][]
- [Pandoc][]
- [Click][]

[Jinja2]: http://jinja.pocoo.org
[Pandoc]: https://pandoc.org
[Click]: https://palletsprojects.com/p/click/


License
----------------
MIT