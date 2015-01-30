# -*- coding: utf-8 -*-
'''
d = lazydict()
d.setdefault('list', factory=list)
'''

class lazydict(dict):
    def setdefault(self, key, default=None, *, factory=None):
        if key in self:
            return self[key]
        if factory:
            default = factory()
        return dict.setdefault(self, key, default)
