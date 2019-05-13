import io
from glob import glob
from pathlib import Path
from typing import Union
from enum import Enum
from pprint import pformat
import attr
import jinja2
from . import Pandoc, YmdReader
from .jinja2_filters import *


class Format(Enum):

    MARKDOWN = "md"
    REVEAL_JS = "revealjs"
    WORD = "docx"
    HTML = "html"


@attr.s
class Jinjafier(object):

    template = attr.ib()

    boilerplate = attr.ib(default=None)
    output = attr.ib(default=None)
    target_format = attr.ib(default=Format.MARKDOWN)
    extra_args = attr.ib(factory=list)
    bibliography = attr.ib(default=None)

    env = attr.ib(init=False)
    _template = attr.ib(init=False)
    _boilerplate = attr.ib(init=False)

    @env.default
    def make_env(self):
        # Setup env
        env = jinja2.Environment()

        env.filters['sortcsl'] = j2_sortcsl
        env.globals['zip'] = zip
        env.globals['list'] = list
        env.filters['bystart'] = j2_bystart

        # def render_block(block, level=1):
        #     return Pandoc.render_block(block, level)
        #
        # def render_bp(block_key, level=1):
        #     block = self._boilerplate.get(block_key)
        #     if block:
        #         return Pandoc.render_block(block, level)

        env.filters['render_block'] = Pandoc.render_block
        # env.filters['render_bp'] = render_bp

        return env


    @_template.default
    def set_template(self):
        if not self.template:
            return
        if isinstance(self.template, io.TextIOBase):
            logging.debug("Found filelike template")
            _val = self.template.read()
            return self.env.from_string(_val)
        elif isinstance(self.template, str):
            templates = Path(__file__).parent / "templates"
            logging.debug( templates / Path(self.template))
            logging.debug(Path.exists( templates / Path(self.template)) )
            if Path.exists(templates / Path(self.template)):
                logging.debug("Found builtin template")
                self.env.loader = jinja2.loaders.FileSystemLoader(str(templates))
                return self.env.get_template(self.template)
            else:
                logging.debug("Found str template")
                return self.env.from_string(self.template)
        else:
            raise TypeError("Not builtin, filelike, or str")

    @_boilerplate.default
    def set_boilerplate(self):

        if not self.boilerplate:
            return

        logging.debug("Checking for boilerplate")
        logging.debug(self.boilerplate / "*.ymd")

        bp = {}
        fns = glob( str( self.boilerplate / "*.ymd" ) )
        for fn in fns:
            logging.debug(fn)
            with open(fn) as f:
                _meta, _content = YmdReader.read(f)
                _blocks = Pandoc.get_blocks(_content)
                bp = {**bp, **_blocks}
        if bp:
            logging.debug(bp)
            return bp

    @classmethod
    def get_meta(cls, meta):

        if isinstance(meta, dict):
            logging.debug("Found dict meta")
            return meta
        elif isinstance(meta, io.TextIOBase):
            logging.debug("Found filelike meta")
            _meta, _content = YmdReader.read(meta)
            _blocks = Pandoc.get_blocks(_content)
            return {**_meta, "blocks": _blocks}
        else:
            raise TypeError("Not filelike or dict")

    def render(self, meta):
        meta = self.get_meta(meta)
        if self._boilerplate:
            meta["blocks"] = {**meta.get("blocks", {}), **self._boilerplate}
        content = self._template.render(meta)

        return content
