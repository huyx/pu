# -*- coding: utf-8 -*-
import unittest

from pu.aio.protocols.basic import LineReceiver


class LineReceiverTest(unittest.TestCase):
    def setUp(self):
        self.lines = []
        self.line_receiver = LineReceiver()
        self.line_receiver.line_received = self.lines.append

    def test_crlf(self):
        self.line_receiver.data_received(b'a\r\nb\r\nc')
        self.assertEqual(self.lines, [b'a', b'b'])
        self.assertEqual(self.line_receiver._buffer, b'c')

    def test_cr(self):
        self.line_receiver.data_received(b'a\rb\rc')
        self.assertEqual(self.lines, [b'a', b'b'])
        self.assertEqual(self.line_receiver._buffer, b'c')

    def test_lf(self):
        self.line_receiver.data_received(b'a\nb\nc')
        self.assertEqual(self.lines, [b'a', b'b'])
        self.assertEqual(self.line_receiver._buffer, b'c')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
