# -*- coding: utf-8 -*-
from .. import util
import unittest


class Test(unittest.TestCase):
    def test_shorten(self):
        s = 'Hi, this is shorter than orignal message ...'
        self.assertEqual(len(util.shorten(s, 30)), 30)
        self.assertEqual(len(util.shorten(s, 10)), 10)

    def test_shorten_cn(self):
        s = '有时候中文的宽度是个问题，字符数、显示所占宽度，以及编码后的字节数……'
        self.assertEqual(len(util.shorten(s, 30)), 30)
        self.assertEqual(len(util.shorten(s, 10)), 10)


if __name__ == "__main__":
    unittest.main()
