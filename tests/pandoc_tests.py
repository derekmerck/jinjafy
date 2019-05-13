import logging
from jinjafy import Pandoc

doc = """
# Title 1

Some content 1

## Subtitle 1.1

Some content 1.1

# Title 2

Some content 2

"""

def test_block_round_trip():

    d = Pandoc.get_blocks(doc)
    o = Pandoc.render_block(d['title-1'], 3)

    assert( "#### Subtitle 1.1" in o )


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    test_block_round_trip()
