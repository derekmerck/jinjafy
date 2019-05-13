import logging
from pathlib import Path
from io import StringIO
# from ruamel import yaml
from jinjafy import yaml
from pprint import pformat


def test_yaml_loader():

    here = Path(__file__).parent
    fp = here / "resources" / "include.yml"
    res = yaml.load(fp)

    logging.debug(pformat(res))

    assert(res == {'bar': ['foo', 'fooo', 'foooo'], 'foo': ['foo', 'fooo', 'foooo']})

    s = \
"""
foo: !include inc_foo.yml
bar: !include inc_bar.yml
"""
    stio = StringIO(s)
    stio.name = Path(__file__) / "resources"
    res = yaml.load(stio)

    logging.debug(pformat(res))

    assert(res == {'bar': ['foo', 'fooo', 'foooo'], 'foo': ['foo', 'fooo', 'foooo']})


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    test_yaml_loader()
