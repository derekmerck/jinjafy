import logging, os
from pathlib import Path
from jinjafy import Jinjafier

template = """
{{ blocks["my-title"] | render_block }}

{{ blocks["my-title"] | render_block(2) }}

"""


def file_test():

    here = Path(__file__).parent
    meta_fn = here / "resources" / "meta.ymd"
    j = Jinjafier(template)
    with open(meta_fn) as g:
        output = j.render(g)

    logging.debug(output)

    assert( "My title\n==" in output )
    assert( "Subheadings\n--" in output)
    assert( "My title\n--" in output )
    assert( "### Subheadings" in output)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    file_test()
