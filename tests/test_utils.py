import unittest

from utils import parse_currency_args, parse_rate


class TestCurrency(unittest.TestCase):
    def test_parse_currency_args(self):
        self.assertEqual(parse_currency_args('$'), 'USD')
        self.assertEqual(parse_currency_args('€'), 'EUR')
        self.assertEqual(parse_currency_args('¥'), 'JPY')
        self.assertEqual(parse_currency_args('Ұ'), 'CNY')
        self.assertEqual(parse_currency_args('GBP'), 'GBP')
        self.assertEqual(parse_currency_args('RUR'), 'RUR')
        self.assertEqual(parse_currency_args(''), '')
        self.assertEqual(parse_currency_args(None), None)

    def test_parse_rate(self):
        self.assertIsInstance(parse_rate(), dict)
        self.assertEqual(parse_rate()['EUR'], 1)
        self.assertIsInstance(parse_rate()['EUR'], float)
        self.assertIsInstance(parse_rate()['USD'], float)

if __name__ == '__main__':
    unittest.main()
