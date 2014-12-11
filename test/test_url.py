# -*- coding: utf-8 -*-
import unittest
from urllib import parse

from pu.url import parse_url, Netloc


class TestParseUrl(unittest.TestCase):
    def test_host_only(self):
        result = parse_url('hostname')
        self.assertEqual(result.hostname, 'hostname')
        self.assertEqual(result.port, None)

    def test_port_only(self):
        result = parse_url('9999', default_host='localhost')
        self.assertEqual(result.hostname, 'localhost')
        self.assertEqual(result.port, 9999)

    def test_hostport(self):
        result = parse_url('hostname:9999')
        self.assertEqual(result.hostname, 'hostname')
        self.assertEqual(result.port, 9999)

    def test_path_query(self):
        result = parse_url('hostname/path?x=1&y=2')
        self.assertEqual(parse.parse_qsl(result.query), [('x', '1'), ('y', '2')])

    def test_params(self):
        result = parse_url('hostname/path;params is here')
        self.assertEqual(result.path, '/path;params is here')
        self.assertEqual(result.params, '')
        result = parse_url('hostname/path;params is here', parse_params=True)
        self.assertEqual(result.params, 'params is here')

    def test_misc(self):
        result = parse_url('http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baidu&bar=&wd=parse_url')
        self.assertIn(('wd', 'parse_url'), parse.parse_qsl(result.query))


class TestNetloc(unittest.TestCase):
    def test_netloc(self):
        result = Netloc('9999', default_host='localhost')

        self.assertEqual(result.hostname, 'localhost')
        self.assertEqual(result.port, 9999)
