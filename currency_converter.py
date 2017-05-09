import argparse
import json

from utils import parse_currency_args, parse_rate


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=float, required=True,
                        help="amount which we want to convert")
    parser.add_argument("--input_currency", type=str, required=True,
                        help="3 letters name or currency symbol")
    parser.add_argument("--output_currency", type=str, required=False,
                        help="3 letters name or currency symbol")
    return parser


def converter(input_amount, input_currency, output_currency):

    if input_amount <= 0:
        result = {"input": "error! Currency amount cannot be negative or zero"}
        print(json.dumps(result))
        return json.dumps(result)

    input_currency = parse_currency_args(input_currency)
    output_currency = parse_currency_args(output_currency)
    rate = parse_rate()
    try:
        result = {"input": rate["error"]}
        print(json.dumps(result))
        return json.dumps(result)
    except KeyError:
        pass
    result = {}
    try:
        eur_rate = rate[input_currency]
    except KeyError:
        result = {"input": "error! No currency provided"}
        print(json.dumps(result))
        return json.dumps(result)
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
    parser = create_parser()
    args = parser.parse_args()
    converter(args.amount, args.input_currency, args.output_currency)

if __name__ == '__main__':
    main()
