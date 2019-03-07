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
import pypandoc

from .jinja2_filters import *
from .yaml_extras import IncludeLoader


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


def convert(_input: Mapping, target_format: str,
            theme: str = None,
            bibliography: str = None,
            extra_args: str = None,
            outfile: str = None):
    """
    Wrappper for pypandoc that supports 'includes' as strings and provides
    some target_format-specific defaults
    """

    if not extra_args:
        extra_args = []

    filters = []

    if target_format == "revealjs":
        extra_args += ["-s",
                       "-V", "revealjs-url=https://revealjs.com",
                       "--slide-level=3"]

    here = Path(__file__).parent
    csl_path = here / "extras" / "chicago-syllabus_plus.csl"

    if bibliography:
        extra_args += ["--bibliography={}".format(bibliography),
                       "--csl={}".format(csl_path)]
        filters.append('pandoc-citeproc')
        if target_format == "md" or target_format == "markdown":
            target_format = "markdown-citations"

    if theme:
        extra_args += ["-V", "theme={}".format(theme)]

    tmpfiles = []

    def add_file_arg(_str, arg_name):
        if not _str:
            return
        nonlocal extra_args, tmpfiles
        f = tempfile.NamedTemporaryFile("w+", delete=False)
        f.write(_str)
        f.close()
        extra_args += ['{}'.format(arg_name), f.name]
        tmpfiles.append( f.name )

    sections = [("header", "-H"),
                ("pre-body", "-B"),
                ("post-body", "-A")]

    for k, a in sections:
        if _input.get(k):
            add_file_arg(_input[k]["content"], a)

    _output = pypandoc.convert_text(_input['body']['content'],
                                    target_format,
                                    format=_input['body']['format'],
                                    filters=filters,
                                    extra_args=extra_args,
                                    outputfile=outfile)

    for fn in tmpfiles:
        # logging.debug(tmpfiles)
        os.remove(fn)

    # logging.debug(_output)
    return _output


def jinjafy(template: str, meta: Mapping, to: str = None,
            theme: str = None, bibliography: str = None,
            extra_args: list = None, outfile: str = None) -> str:

    _output = stencil(template, meta, target_format=to,
                      theme=theme, bibliography=bibliography)

    if to:
        _output = convert(_output, target_format=to,
                          theme=theme,
                          bibliography=bibliography,
                          extra_args=extra_args,
                          outfile=outfile)

    return _output
