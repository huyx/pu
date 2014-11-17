# -*- coding: utf-8 -*-
import unittest

from pu.manager import Manager


class Test(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()

    def test_register_with_name(self):
        self.manager.register(1, 'ONE')
        self.assertEqual(self.manager.get('ONE'), 1)

    def test_register_function(self):
        @self.manager.register
        def f(): pass
        self.assertEqual(self.manager.get('f'), f)

    def test_register_class(self):
        @self.manager.register
        class C(): pass
        self.assertEqual(self.manager.get('C'), C)

    def test_named(self):
        self.manager.named('one', 'ONE')(1)
        self.assertEqual(self.manager.get('one'), 1)
        self.assertEqual(self.manager.get('ONE'), 1)

    def test_named_function(self):
        @self.manager.named('funcf', 'FUNCF')
        def f(): pass
        self.assertEqual(self.manager.get('funcf'), f)
        self.assertEqual(self.manager.get('FUNCF'), f)

    def test_named_class(self):
        @self.manager.named('clsc', 'CLSC')
        class C(): pass
        self.assertEqual(self.manager.get('clsc'), C)
        self.assertEqual(self.manager.get('CLSC'), C)

    def test_duplicate(self):
        self.manager.register(1, 'ONE')
        self.assertRaises(AssertionError,
            self.manager.register, '1', 'ONE')
