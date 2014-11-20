import unittest

from pu import minimist


class Test(unittest.TestCase):
    def test_abc_1(self):
        self.assertEqual(
            minimist.parse('a b c'),
            dict(_=['a', 'b', 'c']))

    def test_abc_2(self):
        self.assertEqual(
            minimist.parse('-a -b -c'),
            dict(_=[], a=True, b=True, c=True))

    def test_abc_3(self):
        self.assertEqual(
            minimist.parse('-abc'),
            dict(_=[], a=True, b=True, c=True))

    def test_arg_eq_value(self):
        self.assertEqual(
            minimist.parse('--arg long-option -a short-option'),
            dict(_=[], arg='long-option', a='short-option'))

    def test_list(self):
        self.assertEqual(
            minimist.parse('-a a -b b -b', lists=['a']),
            dict(_=[], a=['a'], b=['b', True]))

    def test_number(self):
        self.assertEqual(
            minimist.parse('--pi 3.14 -r 10'),
            dict(_=[], pi=3.14, r=10))

    def test_strings(self):
        self.assertEqual(
            minimist.parse('--pi 3.14 -r 10', strings=['pi', 'r']),
            dict(_=[], pi='3.14', r='10'))

    def test_bool_arg(self):
        self.assertEqual(
            minimist.parse('--arg. -a.'),
            dict(_=[], arg=True, a=True))

    def test_more_value_1(self):
        self.assertEqual(
            minimist.parse('-a 1,2,3 -b 3e4'),
            dict(_=[], a=(1, 2, 3), b=3e4))

    def test_more_value_2(self):
        self.assertEqual(
            minimist.parse('-a "{1,2,3}"'),
            dict(_=[], a={1, 2, 3}))

    def test_defaults(self):
        self.assertEqual(
            minimist.parse('--pi 3.14 -r 10', defaults=dict(type='cycle', r=1)),
            dict(_=[], pi=3.14, r=10, type='cycle'))

    def test_extra_args(self):
        self.assertEqual(
            minimist.parse('a b c -- -d --e f'),
            dict(_=['a', 'b', 'c'], **{ '--':  ['-d', '--e', 'f']}))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
