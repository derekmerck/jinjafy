import logging
from pathlib import Path
from io import StringIO
from jinjafy import YmdReader, Pandoc

doc = """
---
title: My title
author: Author, My
content: |-
  ** Emphatic content **
...
# {{title}}

{{ author }}

{{content*key2}}

---
key2: 2
...
## Subheadings

Subinfo

"""

def str_test():

    meta, content = YmdReader.read(doc)
    assert( "# My title" in content )


def file_test():

    logging.debug(__file__)
    here = Path(__file__).parent
    fp = here / "resources" / "meta.ymd"

    with open(fp) as f:
        meta, content = YmdReader.read(f)

        assert ("# My title" in content)


def filelike_test():

    s = StringIO(doc)

    meta, content = YmdReader.read(s)

    assert( "# My title" in content )


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    str_test()
    file_test()
    filelike_test()

