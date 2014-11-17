import unittest

from pu import minimist

_ = minimist.Namespace

class Test(unittest.TestCase):
    def test_abc_1(self):
        self.assertEqual(
            minimist.parse('a b c'),
            _(_=['a', 'b', 'c']))

    def test_abc_2(self):
        self.assertEqual(
            minimist.parse('-a -b -c'),
            _(_=[], a=True, b=True, c=True))

    def test_abc_3(self):
        self.assertEqual(
            minimist.parse('-abc'),
            _(_=[], a=True, b=True, c=True))

    def test_arg_eq_value(self):
        self.assertEqual(
            minimist.parse('--arg long-option -a short-option'),
            _(_=[], arg='long-option', a='short-option'))

    def test_list(self):
        self.assertEqual(
            minimist.parse('-a a -b b -b', lists=['a']),
            _(_=[], a=['a'], b=['b', True]))

    def test_number(self):
        self.assertEqual(
            minimist.parse('--pi 3.14 -r 10'),
            _(_=[], pi=3.14, r=10))

    def test_strings(self):
        self.assertEqual(
            minimist.parse('--pi 3.14 -r 10', strings=['pi', 'r']),
            _(_=[], pi='3.14', r='10'))

    def test_more_value_1(self):
        self.assertEqual(
            minimist.parse('-a 1,2,3 -b 3e4'),
            _(_=[], a=(1, 2, 3), b=3e4))

    def test_more_value_2(self):
        self.assertEqual(
            minimist.parse('-a "{1,2,3}"'),
            _(_=[], a={1, 2, 3}))

    def test_defaults(self):
        self.assertEqual(
            minimist.parse('--pi 3.14 -r 10', defaults=dict(type='cycle', r=1)),
            _(_=[], pi=3.14, r=10, type='cycle'))

    def test_extra_args(self):
        self.assertEqual(
            minimist.parse('a b c -- -d --e f'),
            _(_=['a', 'b', 'c'], **{ '--':  ['-d', '--e', 'f']}))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
