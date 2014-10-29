# -*- coding: utf-8 -*-
"""Load YAML file

Feature:

- support !include tag to include another YAML file
"""
from __future__ import print_function
from yaml.constructor import Constructor, ConstructorError
import os.path
import yaml


INCLUDE_TAG = '!include'


def load(filename, encoding='utf-8'):
    dirname = os.path.dirname(filename)

    def include(loader, node):
        try:
            filename = loader.construct_scalar(node)
        except:
            try:
                filename, nodename = loader.construct_sequence(node)
            except:
                raise ConstructorError(None, None,
                    'expected a string or sequence(2 elements), but found %s' % node.id,
                    node.start_mark)
        else:
            nodename = None

        with open(os.path.join(dirname, filename), encoding=encoding) as f:
            document = yaml.load(f)

        if nodename:
            return document[nodename]

        return document

    Constructor.add_constructor(INCLUDE_TAG, include)

    with open(filename, encoding=encoding) as f:
        data = yaml.load(f)

    del Constructor.yaml_constructors[INCLUDE_TAG]

    return data
