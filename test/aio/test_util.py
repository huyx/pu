# -*- coding: utf-8 -*-
from pu.aio.util import file_get_contents
import asyncio
import os.path
import unittest


def setUpModule():
    global loop
    loop = asyncio.get_event_loop()


class Test(unittest.TestCase):
    def test_file_get_contents(self):
        filename = os.path.abspath(__file__)
        content = loop.run_until_complete(file_get_contents(filename))
        self.assertIn('test_file_get_contents', content.decode('utf_8'))

    def test_file_get_contents_http(self):
        url = 'http://www.baidu.com/'
        content = loop.run_until_complete(file_get_contents(url))
        self.assertIn('baidu', content.decode('utf_8'))

