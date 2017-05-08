import unittest

from currency_converter import create_parser, converter


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
        args = self.parser.parse_args(["--amount", '10', "--input_currency", '$', "--output_currency", 'EUR'])
        result = converter(args.amount, args.input_currency, args.output_currency)
        self.assertIsNotNone(result)

    def test_with_two_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--input_currency", '$', "--output_currency", 'EUR'])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--amount", '10', "--output_currency", 'EUR'])

        args = self.parser.parse_args(["--amount", '10', "--input_currency", '$'])
        result = converter(args.amount, args.input_currency, args.output_currency)
        self.assertIsNotNone(result)

    def test_with_one_arg(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--amount"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--input_currency"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--output_currency"])

    def test_with_minus_amount(self):
        args = self.parser.parse_args(["--amount", '-10', "--input_currency", '$', "--output_currency", 'EUR'])
        result = converter(args.amount, args.input_currency, args.output_currency)
        self.assertIsNotNone(result)

    def test_with_wrong_currency(self):
        args = self.parser.parse_args(["--amount", '10', "--input_currency", 'WRONG_CURRENCY'])
        result = converter(args.amount, args.input_currency, args.output_currency)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
