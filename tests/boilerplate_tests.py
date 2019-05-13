import logging, os
from pathlib import Path
from jinjafy import Jinjafier

template = """
# {{ title }}

{{ author }}

{{ content }}

{{ blocks["boilerplate-1"] | render_block }}
{{ blocks["boilerplate-2"] | render_block(2) }}
"""

meta = {'title': "My title", 'author': "Author, My", "content": "Lorem ipsum ..."}


def boilerplate_test():

    here = Path(__file__).parent
    j = Jinjafier(template, boilerplate=here/"resources"/"bp")
    output = j.render(meta)

    logging.debug(output)

    assert("Boilerplate 1\n==" in output)
    assert("Subsection 1.1\n--" in output)
    assert("Boilerplate 2\n--" in output)
    assert("### Subsection 2.1" in output)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    boilerplate_test()
