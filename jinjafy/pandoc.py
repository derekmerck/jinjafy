import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Mapping
import pypandoc
# import attr


# @attr.s
class Pandoc(object):

    pd_api = None

    @classmethod
    def convert(cls,
                _input: Mapping,
                target_format: str = "md",
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
            tmpfiles.append(f.name)

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

    @classmethod
    def get_blocks(cls, content: str) -> map:
        # Separates out top-level blocks for use with templates
        pd = pypandoc.convert_text(source=content,
                                   format='md',
                                   to="json")
        cd = json.loads(pd)
        cls.pd_api = cd.get('pandoc-api-version')
        pd_blocks = {}

        for b in cd.get('blocks'):
            if b['t'] == "Header" and b['c'][0] == 1:
                if b['c'][1][1]:
                    key = b['c'][1][1][0]
                else:
                    key = b['c'][1][0]
                    # logging.debug(key)
                pd_blocks[key] = []
            pd_blocks[key].append(b)
        return pd_blocks

    @classmethod
    def render_block(cls, block: list, level=1) -> str:

        def offset_headers(block, offset):
            for b in block:
                if b['t'] == "Header":
                    b['c'][0] = b['c'][0] + offset
            return block

        logging.debug(block)

        offset = 0
        if block[0]['t'] == "Header":
            cardinal_level = block[0]['c'][0]
            offset = level - cardinal_level

        if offset != 0:
            block = offset_headers(block, offset)

        input_ = {u'blocks': block,
                  u'meta': {},
                  u'pandoc-api-version': cls.pd_api}
        input = json.dumps(input_)

        pd = pypandoc.convert_text(source=input,
                                   format='json',
                                   to="md")
        return pd
