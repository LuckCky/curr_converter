import unittest

from currency_converter import create_parser, converter, check_input, main
from config import test_rate


class CommandLineTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = create_parser()
        cls.parser = parser


class ConverterTestCase(CommandLineTestCase):
    def test_with_empty_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--amount", "--input_currency", "--output_currency"])

    def test_with_three_args(self):
        args = self.parser.parse_args(["--amount", '10', "--input_currency", 'USD', "--output_currency", 'EUR'])
        # result = converter(args.amount, args.input_currency, args.output_currency, test_rate)
        result = converter(10, 'USD', 'EUR', test_rate)

        self.assertIsNotNone(result)

    def test_with_two_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--input_currency", '$', "--output_currency", 'EUR'])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--amount", '10', "--output_currency", 'EUR'])

    def test_with_one_arg(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--amount"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--input_currency"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--output_currency"])

    def test_input_negative_amount(self):
        self.assertEqual(check_input(-1, None, None),
                         '{"input": "error! Input currency amount cannot be negative or zero"}')

    def test_input_zero_amount(self):
        self.assertEqual(check_input(0, None, None),
                         '{"input": "error! Input currency amount cannot be negative or zero"}')

    def test_no_input_currency(self):
        self.assertEqual(check_input(10, None, None),
                         '{"input": "error! No input currency provided"}')

    def test_input_wrong_currency(self):
        self.assertEqual(check_input(10, 'WRONG_CURRENCY', test_rate),
                         '{"input": "error! Unknown input currency provided"}')


if __name__ == '__main__':
    unittest.main()
