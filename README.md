Jinjafy
==================

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Source: <https://www.github.com/derekmerck/jinjafy>



Overview
----------------

Quick stand-alone document templating and format conversion using Jinja2 and Pandoc.


Usage
----------------

```bash
$ pip install https://github.com/derekmerck/jinjafy
$ jinjafy examples/revealjs_template.md sample_data.yaml \
  -o presentation.html -f md -t revealjs
```

See `jinjafy --help` for details.


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