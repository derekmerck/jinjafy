# -*- coding: utf-8 -*-
"""
From https://davidchall.github.io/yaml-includes.html with minor modifications**

** result += ... to result.append()

```
education:    !include education.yaml

activities:   !include [schools.yaml, conferences.yaml, workshops.yaml]

publications: !include {peer_reviewed: publications/peer_reviewed.yaml, internal: publications/internal.yaml}
```

```
with open('document.yaml', 'r') as f:
    data = yaml.load(f, Loader=IncludeLoader)
```
"""
import yaml, logging, os.path, codecs
import pprint


class IncludeLoader(yaml.Loader):
    def __init__(self, stream, version="1.0", preserve_quotes=False):
        self._root = os.path.split(stream.name)[0]
        super(IncludeLoader, self).__init__(stream)
        IncludeLoader.add_constructor('!include', IncludeLoader.include)
        IncludeLoader.add_constructor('!import',  IncludeLoader.include)
        IncludeLoader.add_constructor('!include_raw', IncludeLoader.include_raw)

    def include_raw(self, node):
        return self.include(node, func=self.read_raw)

    def include(self, node, func=None):
        if func == None:
            func=self.read_yaml

        if isinstance(node, yaml.ScalarNode):
            return func(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            result = []
            for filename in self.construct_sequence(node):
                result.append(func(filename))
            return result

        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k,v in self.construct_mapping(node).iteritems():
                result[k] = func(v)
            return result

        else:
            logging.error("Unrecognised node type in !include statement")
            raise yaml.constructor.ConstructorError

    def read_yaml(self, filename):
        filepath = os.path.join(self._root, filename)
#        with codecs.open(filepath, encoding="utf-8") as f:
        with open(filepath, 'r') as f:
            return yaml.load(f, IncludeLoader)

    def read_raw(self, filename):
        filepath = os.path.join(self._root, filename)
#        with codecs.open(filepath, encoding="utf-8") as f:
        with open(filepath, 'r') as f:
            return f.read()
