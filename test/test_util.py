# -*- coding: utf-8 -*-
import functools
import unittest

from pu import util


class Test(unittest.TestCase):
    def test_shorten(self):
        s = 'Hi, this is shorter than orignal message ...'
        self.assertEqual(len(util.shorten(s, 30)), 30)
        self.assertEqual(len(util.shorten(s, 10)), 10)

    def test_shorten_cn(self):
        s = '有时候中文的宽度是个问题，字符数、显示所占宽度，以及编码后的字节数……'
        self.assertEqual(len(util.shorten(s, 30)), 30)
        self.assertEqual(len(util.shorten(s, 10)), 10)

    def test_bytes_fromhex(self):
        s = 'aa\tbb\ncc\rdd ee'
        self.assertRaises(ValueError, functools.partial(bytes.fromhex, s))
        self.assertEqual(util.bytes_fromhex(s), b'\xaa\xbb\xcc\xdd\xee')

    def test_format_time(self):
        # 由于时区问题，下面的测试在 Travis CI 中出现错误
        # self.assertEqual(util.format_time(1416469808), '2014-11-20 15:50:08')
        pass


class IterattrsTest(unittest.TestCase):
    class C(object):
        pass

    def setUp(self):
        self.o = IterattrsTest.C()
        self.o.a = 'a'
        self.o._a = '_a'

    def test_iterattrs(self):
        result = tuple(util.iterattrs(self.o))
        self.assertEqual(result, (('a', 'a'),))

    def test_iterattrs_with_filter(self):
        result = tuple(util.iterattrs(self.o, True))
        self.assertEqual(result, (('_a', '_a'), ('a', 'a')))


class CodecTest(unittest.TestCase):
    def setUp(self):
        self.string = ([{'1': 1}],)
        self.binary = ([{b'1': 1}],)

    def test_deep_encode(self):
        self.assertEqual(util.deep_encode(self.string), self.binary)

    def test_deep_decode(self):
        self.assertEqual(util.deep_decode(self.binary), self.string)


class GetSetFieldTest(unittest.TestCase):
    def setUp(self):
        class O: pass
        self.o = O()
        self.o.d = {}
        self.o.d['o'] = O()
        self.o.d['o'].l = [0, 1]
        self.o.a = 'a'

    def test_get_field(self):
        self.assertEqual(util.get_field(self.o, '.a'), 'a')
        self.assertEqual(util.get_field(self.o, '.d:o.l#1'), 1)

    def test_set_field(self):
        util.set_field(self.o, '.a', 'A')
        self.assertEqual(util.get_field(self.o, '.a'), 'A')
        util.set_field(self.o, '.d:o.l#1', 'hello')
        self.assertEqual(util.get_field(self.o, '.d:o.l#1'), 'hello')


if __name__ == "__main__":
    unittest.main()
