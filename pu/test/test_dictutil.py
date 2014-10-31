# -*- coding: utf-8 -*-
from functools import partial
from pu.dictutil import repr_dict, DotDict, DotOrderedDict, Dot, OrderedDict
import unittest


class Test(unittest.TestCase):
    def test_repr_dict(self):
        d = dict(a=4, b=3, c=2, d=1)
        repr_dict(d)
        self.assertEqual(repr_dict(d, sorted), 'dict(a=4, b=3, c=2, d=1)')
        self.assertEqual(repr_dict(d, partial(sorted, reverse=True)), 'dict(d=1, c=2, b=3, a=4)')

    def test_dotdict_getitem(self):
        d = DotDict(a=1)
        self.assertEqual(d.a, 1)

    def test_dotdict_setitem(self):
        d = DotDict()
        d.b = 2
        self.assertEqual(d['b'], 2)

    def test_dotdict_non_exists(self):
        d = DotDict()
        try:
            assert d.c
        except AttributeError:
            pass
    
    def test_dotordereddict(self):
        d = DotOrderedDict(a=1)
        d.b = 2
        assert d.a == 1
        assert d['b'] == 2
        assert list(d.keys()) == ['a', 'b']
        try:
            assert d.c
        except AttributeError:
            pass
    
    def test_dotit(self):
        adict = dict(a=1, b=2)
        d = Dot(adict)
        assert d.a == 1
        assert d['a'] == 1
        assert d.b == 2
        try:
            assert d.c
        except AttributeError:
            pass

    def test_dotit_nest_dict(self):
        adict = dict(a=dict(aa=1, ab=2), b=2)
        d = Dot(adict)
        assert d.a.aa == 1
        assert d.a.ab == 2

    def test_dotit_ordered_dict(self):
        adict = OrderedDict([
            ('a', OrderedDict([
                ('aa', 1),
                ('ab', 2),
                ])),
            ('b', 2),
            ])
        d = Dot(adict)
        assert d.a.aa == 1
        assert d.a.ab == 2

    def test_dotit_repr(self):
        adict = dict(a=dict(aa=1, ab=2), b=2)
        d = Dot(adict)
        self.assertEqual(repr(adict), repr(d))
