# -*- coding: utf-8 -*-
import unittest
from pu import rcp


class Test(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(
            rcp.encode(rcp.Notify('hello', ['tom', 'bob'], {})),
            ['N', 'hello', ['tom', 'bob'], {}])

        self.assertEqual(
            rcp.encode(rcp.Call(99, 'add', (1, 2), {})),
            ['C', 99, 'add', (1, 2), {}])

        self.assertEqual(
            rcp.encode(rcp.Return(99, 3)),
            ['R', 99, 3])

        self.assertEqual(
            rcp.encode(rcp.Error(99, 101, '协议错误', None)),
            ['E', 99, 101, '协议错误', None])

    def test_decode(self):
        self.assertEqual(
            rcp.decode(['N', 'hello', ['tom', 'bob'], {}]),
            rcp.Notify('hello', ['tom', 'bob'], {}))

        self.assertEqual(
            rcp.decode(['C', 99, 'add', (1, 2), {}]),
            rcp.Call(99, 'add', (1, 2), {}))

        self.assertEqual(
            rcp.decode(['R', 99, 3]),
            rcp.Return(99, 3))

        self.assertEqual(
            rcp.decode(['E', 99, 101, '协议错误', None]),
            rcp.Error(99, 101, '协议错误', None))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
