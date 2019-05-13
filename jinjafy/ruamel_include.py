from pathlib import Path
import logging
from ruamel.yaml import YAML

yaml = YAML(typ='safe', pure=True)
yaml.default_flow_style = False


def my_compose_document(self):
    self.parser.get_event()
    node = self.compose_node(None, None)
    self.parser.get_event()
    # self.anchors = {}    # <<<< commented out
    return node


yaml.Composer.compose_document = my_compose_document


# adapted from http://code.activestate.com/recipes/577613-yaml-include-support/
def yaml_include(loader, node):
    global yaml
    # logging.debug(yaml.reader.stream.name)
    here = Path(yaml.reader.stream.name).parent
    # logging.debug(here)
    y = loader.loader
    yaml = YAML(typ=y.typ, pure=y.pure)  # same values as including YAML
    yaml.composer.anchors = loader.composer.anchors
    return yaml.load( here / node.value )


yaml.Constructor.add_constructor("!include", yaml_include)
