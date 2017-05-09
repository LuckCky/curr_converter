import requests
import xml.etree.ElementTree as ET

from config import ecb_url, cube, symbols


def parse_currency_args(currency):
    if currency and len(currency) < 3:
        currency = next((element['cc'] for element in symbols if element['symbol'] == currency), currency)
    return currency


def parse_rate():
    try:
        response = requests.get(ecb_url)
    except Exception as e:
        return {"error": "error occurred while accessing www.ecb.europa.eu: {}".format(e)}
    else:
        currency_xml = response.content.decode()
    root = ET.fromstring(currency_xml)
    currencies_list = [currency.attrib.get('currency') for currency in root.iter(cube) if currency.attrib.get('currency')]
    rates_list = [float(currency.attrib.get('rate')) for currency in root.iter(cube) if currency.attrib.get('rate')]
    result = dict(zip(currencies_list, rates_list))
    result['EUR'] = float(1)
    return result
