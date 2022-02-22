from config import keys, api_key
import requests
import json


class ConvertException(Exception):
    pass


def get_all_currencies():
    """Return a dictionary with all available currencies"""
    r = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey={api_key}')
    all_currencies = json.loads(r.content)['results']
    return all_currencies


currency_all = get_all_currencies()


class Converter:

    @staticmethod
    def convert(quote: str, base: str, amount: float):
        if quote == base:
            raise ConvertException('Валюты не должны совпадать.')
        try:
            quote_ = keys[quote]
        except KeyError:
            if currency_all[quote]:
                quote_ = quote
            else:
                raise ConvertException(f'Не удалось обработать "{quote}".')
        try:
            base_ = keys[base]
        except KeyError:
            if currency_all[base]:
                base_ = base
            else:
                raise ConvertException(f'Не удалось обработать "{base}".')

        r = requests.get(
            f"https://free.currconv.com/api/v7/convert?q={base_}_{quote_}&compact=ultra&apiKey={api_key}")
        rate = float(json.loads(r.content)[base_ + '_' + quote_])
        value = round(amount / rate, 5)
        return value

    @staticmethod
    def format_strings(quote, base, amount):
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество"{amount}".')
        if quote.lower() in keys:
            quote = quote.lower()
        else:
            quote = quote.upper()
        if base.lower() in keys:
            base = base.lower()
        else:
            base = base.upper()
        return quote, base, amount
