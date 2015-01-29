# -*- coding: utf-8 -*-
from pu.util import make_key


class Cache(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        key = make_key(args, kwargs)
        try:
            return self[key]
        except KeyError:
            return self.setdefault(key, self.func(*args, **kwargs))
