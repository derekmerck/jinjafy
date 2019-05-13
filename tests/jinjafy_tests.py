import logging, os
from pathlib import Path
from jinjafy import Jinjafier

template = """
# {{ title }}

{{ author }}

{{ content }}
"""

meta = {'title': "My title", 'author': "Author, My", "content": "Lorem ipsum ..."}


def simple_test():

    j = Jinjafier(template)
    output = j.render(meta)
    assert("# My title" in output)


def file_test():

    here = Path(__file__).parent
    template_fn = here / "resources" / "template.md"
    meta_fn = here / "resources" / "meta.ymd"
    with open(template_fn) as f, open(meta_fn) as g:
        j = Jinjafier(f)
        output = j.render(g)

    assert("# My title" in output)


def builtin_test():

    j = Jinjafier("simple.md")
    output = j.render(meta)
    assert("# My title" in output)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    simple_test()
    file_test()
    builtin_test()
