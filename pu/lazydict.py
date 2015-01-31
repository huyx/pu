# -*- coding: utf-8 -*-
'''lazydict
lazy 在这里有两个意思：

1. setdefault 时可以选择延迟生成对象
2. 提供一些方便地方法访问对象

d = lazydict()
d.setdefault('list', factory=list)
'''
from collections import Mapping, Sequence, MutableSequence, MutableMapping


def _smart_get(ob, key, default=None):
    if isinstance(ob, Sequence):
        return ob[int(key)]
    elif isinstance(ob, Mapping):
        return ob.get(key, default)
    else:
        return getattr(ob, key, default)


def smart_get(ob, key, default=None):
    if '.' not in key:
        return _smart_get(ob, key, default)

    first, _, other = key.partition('.')
    child = _smart_get(ob, first)

    assert child is not None, '{} 没有 {}.'.format(ob, first)

    return smart_get(child, other, default)


def _smart_set(ob, key, value):
    if isinstance(ob, MutableSequence):
        ob[int(key)] = value
    elif isinstance(ob, MutableMapping):
        ob[key] = value
    else:
        setattr(ob, key, value)


def smart_set(ob, key, value):
    if '.' not in key:
        return _smart_set(ob, key, value)

    first, _, other = key.partition('.')
    child = _smart_get(ob, first)

    assert child is not None, '{} 没有 {}.'.format(ob, first)

    return smart_set(child, other, value)


class lazydict(dict):
    def setdefault(self, key, default=None, *, factory=None):
        if key in self:
            return self[key]
        if factory:
            default = factory()
        return dict.setdefault(self, key, default)

    # 绑定 smart_get, smart_set
    smart_get = smart_get
    smart_set = smart_set
