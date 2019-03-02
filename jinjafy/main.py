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


def stencil(template: str,
            meta: Mapping,
            target_format: str = None,
            theme: str = None):

    here = Path(__file__).parent

    # Check for extra meta
    if target_format:
        extras = glob(os.path.join(here, "extras", "{}*".format(target_format)))
        for e in extras:
            with open(e) as f:
                _extras = yaml.safe_load(f)
                meta = {**meta, **_extras}

    if theme and meta.get("themes") and meta["themes"].get(theme):
        meta["theme"] = meta["themes"].get(theme)

    # Setup env
    loader = jinja2.FileSystemLoader([here / "templates", "."])
    env = jinja2.Environment(loader=loader)

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
            extra_args: str = None):
    """
    Wrappper for pypandoc that supports includes as strings and provides
    some target_format-specific defaults
    """

    if not extra_args:
        extra_args = []

    if target_format == "revealjs":
        extra_args += ["-s",
                       "-V", "revealjs-url=https://revealjs.com",
                       "--slide-level=3"]

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

    for k,a in sections:
        if _input.get(k):
            add_file_arg(_input[k]["content"], a)

    _output = pypandoc.convert_text(_input['body']['content'],
                                    target_format,
                                    format=_input['body']['format'],
                                    extra_args=extra_args)

    for fn in tmpfiles:
        # logging.debug(tmpfiles)
        os.remove(fn)

    # logging.debug(_output)
    return _output


def jinjafy(template: str, meta: Mapping, to: str = None, theme: str = None,
            extra_args: list = None) -> str:

    _output = stencil(template, meta, target_format=to, theme=theme)

    if to:
        _output = convert(_output, target_format=to,
                          theme=theme,
                          extra_args=extra_args)

    return _output
