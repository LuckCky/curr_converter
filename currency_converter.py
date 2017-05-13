#!/usr/bin/env python3

import argparse
import json

from utils import parse_currency_args, parse_rate


def create_parser():
    """
    creates parser for arguments
    :return: parser with provided arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=float, required=True,
                        help="amount which we want to convert")
    parser.add_argument("--input_currency", type=str, required=True,
                        help="3 letters name or currency symbol")
    parser.add_argument("--output_currency", type=str, required=False,
                        help="3 letters name or currency symbol")
    return parser


def check_input(input_amount, input_currency, rate):
    """
    various checks for user input
    :param input_amount: amount which we want to convert
    :param input_currency: 3 letters name or currency symbol
    :param rate: currency rates from ECB
    :return: error or False if all checks are good
    """
    if input_amount <= 0:
        result = {"input": "error! Input currency amount cannot be negative or zero"}
        print(json.dumps(result))
        return json.dumps(result)
    elif not input_currency:
        result = {"input": "error! No input currency provided"}
        print(json.dumps(result))
        return json.dumps(result)
    try:
        rate[input_currency]
    except KeyError:
        result = {"input": "error! Unknown input currency provided"}
        print(json.dumps(result))
        return json.dumps(result)
    return False


def converter(input_amount, input_currency, output_currency, rate):
    """
    converts currencies
    :param input_amount: amount which we want to convert
    :param input_currency: 3 letters name or currency symbol
    :param output_currency: 3 letters name or currency symbol
    :param rate: dict with currency rates from ECB
    :return: JSON with converted currencies
    """
    eur_rate = rate[input_currency]
    result = {}
    try:
        curr_rate = rate[output_currency]
        output_amount = round(input_amount / eur_rate * curr_rate, 2)
        result = {
            "input":
                {
                    "amount": input_amount,
                    "currency": input_currency
                },
            "output":
                {
                    output_currency: output_amount
                }
        }
    except KeyError:
        all_currencies = {}
        for key, value in rate.items():
            curr_rate = rate[key]
            output_amount = round(input_amount / eur_rate * curr_rate, 2)
            all_currencies[key] = output_amount
        result["input"] = {"amount": input_amount}
        result["input"]["currency"] = input_currency
        result["output"] = all_currencies
    print(json.dumps(result))
    return json.dumps(result)


def main():
    """
    main func does all the job
    :return: JSON with error if checks are unsuccessful or converted currencies
    """
    parser = create_parser()
    args = parser.parse_args()

    # change symbols for three letter name
    input_currency = parse_currency_args(args.input_currency)
    output_currency = parse_currency_args(args.output_currency)

    input_amount = args.amount

    # get ECB rates
    rate, rate_error = parse_rate()
    if rate_error:
        return rate
    # check input conditions
    input_error = check_input(input_amount, input_currency, rate)
    if input_error:
        return input_error
    return converter(input_amount, input_currency, output_currency, rate)

if __name__ == '__main__':
    main()
