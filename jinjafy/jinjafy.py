from typing import Mapping
import logging
import tempfile
import os
import re
from glob import glob
from pathlib import Path
from pprint import pformat
import yaml
import jinja2

from .pandoc import Pandoc
from .jinja2_filters import *
from .pyyaml_include import IncludeLoader


def stencil(template: str,
            meta: Mapping,
            target_format: str = None,
            theme: str = None,
            bibliography: str = None):

    here = Path(__file__).parent

    if bibliography:
        with open(bibliography) as f:
            meta['bibliography'] = yaml.safe_load(f)

    # Check for extra meta
    if target_format:
        extras = glob(os.path.join(here, "extras", "{}*".format(target_format)))
        for e in extras:
            with open(e) as f:
                _extras = yaml.load(f, Loader=IncludeLoader)
                meta = {**meta, **_extras}

    if theme and meta.get("themes") and meta["themes"].get(theme):
        meta["theme"] = meta["themes"].get(theme)

    # Setup env
    loader = jinja2.FileSystemLoader([here / "templates", os.curdir])
    env = jinja2.Environment(loader=loader)

    env.filters['sortcsl'] = j2_sortcsl
    env.globals['zip'] = zip
    env.globals['list'] = list
    env.filters['bystart'] = j2_bystart

    _output = {}
    _format = None

    # Find templates
    templates = glob( os.path.join( here, "templates", "{}*".format(template) ) )
    R = re.compile(r"^{}\.(?P<tmpl>[hbp]*)\.?(?P<format>[^.]*)$".format(template))
    _map = {
        'h': 'header',
        '':  'body',
        'b': 'pre_body',
        'p': 'post_body'
    }
    for t in templates:
        t = os.path.basename(t)
        _template = env.get_template(t)
        content = _template.render(meta)

        m = R.match(t)

        if not m:
            raise ValueError("Unknown template include type ({})".format(t))

        k = _map.get(m.group('tmpl'))
        _output[k] = {"content": content,
                      "format":  m.group('format')}

    logging.debug(pformat(_output))
    return _output


def jinjafy(template: str, meta: Mapping, to: str = None,
            theme: str = None, bibliography: str = None,
            extra_args: list = None, outfile: str = None) -> str:

    _output = stencil(template, meta, target_format=to,
                      theme=theme, bibliography=bibliography)

    if to:
        _output = Pandoc.convert(_output, target_format=to,
                          theme=theme,
                          bibliography=bibliography,
                          extra_args=extra_args,
                          outfile=outfile)

    return _output
