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


def stencil(template, meta, target_format=None, theme=None):

    here = Path(__file__).parent

    _meta = yaml.safe_load(meta)

    if theme and target_format:
        fn = "{}_themes.yaml".format(target_format)
        with open(here / 'extras' / fn) as f:
            themes = yaml.safe_load(f)
            _meta["theme"] = themes.get(theme)

    loader = jinja2.FileSystemLoader([here / "templates", "."])
    env = jinja2.Environment(loader=loader)

    # Check for includes
    here = Path(__file__).parent
    templates = glob( os.path.join( here, "templates", "{}*".format(template) ) )

    _output = {}
    for t in templates:
        t = os.path.basename(t)
        _template = env.get_template(t)
        _output[t] = _template.render(_meta)

    return _output


def convert(input, _format, target_format,
            inc_header,
            inc_pre_body,
            inc_post_body,
            theme=None,
            extra_args=None):
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

    def add_include_str(_str, arg_name):
        if not _str:
            return
        nonlocal extra_args, tmpfiles
        f = tempfile.NamedTemporaryFile("w+", delete=False)
        f.write(_str)
        f.close()
        extra_args += ['{}'.format(arg_name), f.name]
        tmpfiles.append( f.name )

    add_include_str(inc_header, "-H")
    add_include_str(inc_pre_body, "-B")
    add_include_str(inc_post_body, "-A")

    _output = pypandoc.convert_text(input,
                                    target_format,
                                    format=_format,
                                    extra_args=extra_args)

    for fn in tmpfiles:
        # logging.debug(tmpfiles)
        os.remove(fn)

    # logging.debug(_output)
    return _output


def jinjafy(template, meta, to=None, theme=None, extra_args=None) -> str:

    _output = stencil(template, meta, target_format=to, theme=theme)

    # logging.debug(pformat(_output))

    # find base and includes
    base = inc_pre_body = inc_header = inc_post_body = None

    R = re.compile(r"{}\.([^.]*)\.([^.]*)".format(template))

    for k, v in _output.items():
        match = R.match(k)

        if match:
            if match.groups()[0].lower().startswith("h"):
                inc_header = v
            elif match.groups()[0].lower().startswith("b"):
                inc_pre_body = v
            elif match.groups()[0].lower().startswith("p"):
                inc_post_body = v
        else:
            base = v
            _format = os.path.splitext(k)[1][1:]

    if to and (_format != to):
        _output = convert(base, _format, target_format=to,
                          inc_header=inc_header,
                          inc_pre_body=inc_pre_body,
                          inc_post_body=inc_post_body,
                          theme=theme,
                          extra_args=extra_args)

    return _output
