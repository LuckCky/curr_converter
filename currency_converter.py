import argparse
import json
import requests
import xml.etree.ElementTree as ET

from config import ecb_url, cube, symbols


parser = argparse.ArgumentParser()
parser.add_argument("--amount", type=float,
                    help="amount which we want to convert")
parser.add_argument("--input_currency", type=str,
                    help="3 letters name or currency symbol")
parser.add_argument("--output_currency", type=str,
                    help="3 letters name or currency symbol")
args = parser.parse_args()


def parse_currency_args(currency):
    if currency and len(currency) < 3:
        currency = next((element['cc'] for element in symbols if element['symbol'] == currency), currency)
    return currency


def parse_rate():
    currency_xml = requests.get(ecb_url).content.decode()
    root = ET.fromstring(currency_xml)
    currencies_list = [currency.attrib.get('currency') for currency in root.iter(cube) if currency.attrib.get('currency')]
    rates_list = [float(currency.attrib.get('rate')) for currency in root.iter(cube) if currency.attrib.get('rate')]
    result = dict(zip(currencies_list, rates_list))
    result['EUR'] = 1
    return result


def main():
    input_amount = args.amount
    input_currency = args.input_currency
    output_currency = args.output_currency

    input_currency = parse_currency_args(input_currency)
    output_currency = parse_currency_args(output_currency)
    rate = parse_rate()
    result = {}
    try:
        eur_rate = rate[input_currency]
    except KeyError:
        result = {"input": "error! No currency provided"}
        print(json.dumps(result))
        return json.dumps(result)
    try:
        curr_rate = rate[output_currency]
        output_amount = input_amount / eur_rate * curr_rate
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
            output_amount = input_amount / eur_rate * curr_rate
            all_currencies[key] = output_amount
        result["input"] = {"amount": input_amount}
        result["input"]["currency"] = input_currency
        result["output"] = all_currencies
    print(json.dumps(result))
    return json.dumps(result)

if __name__ == '__main__':
    main()
