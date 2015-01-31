# -*- coding: utf-8 -*-
import unittest

from pu.lazydict import lazydict


class TestLazydict(unittest.TestCase):
    def setUp(self):
        self.d = lazydict()

    def test_setdefault(self):
        self.d.setdefault('a', 1000)
        self.assertEqual(self.d['a'], 1000)

    def test_setdefault_lazy(self):
        self.d.setdefault('a', factory=lambda: 1000)
        self.assertEqual(self.d['a'], 1000)

    def test_smart_get(self):
        self.d['a'] = {'b': [lazydict]}
        lazydict_name = self.d.smart_get('a.b.0.__name__')
        self.assertEqual(lazydict_name, 'lazydict')

    def test_smart_get_default(self):
        self.d['a'] = {'b': [lazydict]}
        value = 'Default!'
        new_value = self.d.smart_get('a.b.0.xxxx', value)
        self.assertEqual(new_value, value)

    def test_smart_get_exception(self):
        self.d['a'] = {'b': [lazydict]}
        with self.assertRaises(ValueError):
            self.d.smart_get('a.b.xxxx')

    def test_smart_set_dict(self):
        self.d['a'] = {}
        value = 'Yeah!'
        self.d.smart_set('a.b', value)
        new_value = self.d.smart_get('a.b')
        self.assertEqual(new_value, value)

    def test_smart_set_attr(self):
        self.d['a'] = {'b': [lazydict]}
        value = 'Yeah!'
        self.d.smart_set('a.b.0.newattr', value)
        new_value = self.d.smart_get('a.b.0.newattr')
        self.assertEqual(new_value, value)


if __name__ == '__main__':
    unittest.main()
