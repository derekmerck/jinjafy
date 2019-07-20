import re, io
from pprint import pformat
from typing import Union, IO
import jinja2
from .jinja2_filters import *
from .ruamel_include import yaml


class YmdReader(object):

    @classmethod
    def read(cls, doc: Union[str, io.IOBase]) -> (str, map):
        """

        Reads a annotated yaml-markdown (ymd) doc and pre-process vars with Jinja:

        input: '''
        ---
        var1=10
        ...
        var1 is equal to {{var1}}
        '''

        output: '''
        var1 is equal to 10
        '''

        Returns both the processed md string and the metadata

        """

        logger = logging.getLogger("read_ymd")

        logger.debug(type(doc))
        if isinstance(doc, io.TextIOBase):

            if doc.name.endswith("yaml"):
                metadata = yaml.load(doc)
                return metadata, None

            doc = doc.read()

        yaml_pattern = re.compile(r"^---$.*?^\.\.\.$", re.M | re.DOTALL )


        nonyaml_part = re.sub(yaml_pattern, "", doc)
        content = None
        if nonyaml_part:
            content = "".join(nonyaml_part)
        logger.debug(content)

        yaml_part = re.findall(yaml_pattern, doc)
        metadata = None
        if yaml_part:
            _yaml_part = []
            for _part in yaml_part:
                # pprint(_part)
                _part = re.sub(r"^---\n", "", _part)
                _part = re.sub(r"\n...$", "", _part)
                if _part:
                    _yaml_part.append(_part)
                # pprint(_part)
            yaml_part = "\n".join(_yaml_part)

            metadata = yaml.load(yaml_part)
            # logger.debug(pformat(metadata))

        if content and metadata:
            # Setup env
            env = jinja2.Environment()

            env.filters['sortcsl'] = j2_sortcsl
            env.globals['zip'] = zip
            env.globals['list'] = list
            env.filters['bystart'] = j2_bystart

            _template = env.from_string(content)
            content = _template.render(metadata)

        return metadata, content


