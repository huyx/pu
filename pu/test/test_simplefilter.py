# -*- coding: utf-8 -*-
from pu.simplefilter import Filter
import unittest


class FitlerTest(unittest.TestCase):
    def test_equal(self):
        f = Filter('a = A')

        self.assertTrue(f(dict(a='A')))

        self.assertFalse(f(dict()))
        self.assertFalse(f(dict(a='a')))

    def test_not_equal(self):
        f = Filter('a != A')

        self.assertTrue(f(dict(a='a')))

        self.assertTrue(f(dict()))
        self.assertFalse(f(dict(a='A')))

    def test_almost_equal(self):
        f = Filter('a ~= *A*')

        self.assertTrue(f(dict(a='A')))
        self.assertTrue(f(dict(a='--A--')))

        self.assertFalse(f(dict()))
        self.assertFalse(f(dict(a='a')))

    def test_not_almost_equal(self):
        f = Filter('a !~= *A*')

        self.assertFalse(f(dict(a='A')))
        self.assertFalse(f(dict(a='--A--')))

        self.assertTrue(f(dict()))
        self.assertTrue(f(dict(a='a')))

    def test_hex_equal(self):
        f = Filter('a #= AA')

        self.assertTrue(f(dict(a=b'\xAA')))

        self.assertFalse(f(dict()))
        self.assertFalse(f(dict(a=b'a')))

    def test_hex_not_equal(self):
        f = Filter('a #!= AA')

        self.assertTrue(f(dict(a='a')))

        self.assertTrue(f(dict()))
        self.assertFalse(f(dict(a='\xAA')))

    def test_hex_almost_equal(self):
        f = Filter('a #~= *AA*')

        self.assertTrue(f(dict(a='\xAA')))
        self.assertTrue(f(dict(a='--\xAA--')))

        self.assertFalse(f(dict()))
        self.assertFalse(f(dict(a='a')))

    def test_hex_not_almost_equal(self):
        f = Filter('a #!~= *AA*')

        self.assertFalse(f(dict(a='\xAA')))
        self.assertFalse(f(dict(a='--\xAA--')))

        self.assertTrue(f(dict()))
        self.assertTrue(f(dict(a='a')))


# TODO:
class AndFilterGroupTest(unittest.TestCase):
    pass


# TODO:
class OrFilterGroupTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
