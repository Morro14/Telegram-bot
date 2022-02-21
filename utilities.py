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


class Converter:
    currency_all = get_all_currencies()

    @staticmethod
    def convert(quote: str, base: str, amount: str):
        quote, base = str.lower(quote), str.lower(base)
        if quote == base:
            raise ConvertException('Валюты не должны совпадать.')

        try:
            quote_ = keys[quote]
        except KeyError:
            if Converter.currency_all[str.upper(quote)]:
                quote_ = str.upper(quote)
            else:
                raise ConvertException(f'Не удалось обработать "{quote}".')

        try:
            base_ = keys[base]
        except KeyError:
            if Converter.currency_all[str.upper(base)]:
                base_ = str.upper(base)
            else:
                raise ConvertException(f'Не удалось обработать "{base}".')

        try:
            amount_ = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество"{amount}".')
        else:
            r = requests.get(
                f"https://free.currconv.com/api/v7/convert?q={base_}_{quote_}&compact=ultra&apiKey={api_key}")
            rate = float(json.loads(r.content)[base_ + '_' + quote_])
            value = round(amount_ / rate, 6)
            return value
