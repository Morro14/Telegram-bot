from config import keys
import requests
import json
from lxml import etree


class ConvertException(Exception):
    pass


def get_all_currencies():
    """Return a dictionary with all currencies from cl-currencies-select-option.txt"""
    all_currencies = {}
    tree = etree.parse('cl-currencies-select-option.txt')
    opt = tree.findall('/option')
    for o in opt:
        value = o.get('value')
        title = o.get('title')
        all_currencies.update({value: title})
    return all_currencies


class Converter:
    currency_all = get_all_currencies()

    @staticmethod
    def convert(quote: str, base: str, amount:str):
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
            amount_ = amount.replace(',', '.')
            amount_ = float(amount_)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество"{amount}".')

        if base_ != 'USD':
            base_to_usd = requests.post(
                f"http://api.currencylayer.com/live?access_key=5f3f8678366e5935dd728319e90bc512&currencies={base_},USD")
            quote_to_usd = requests.get(
                f"https://free.currconv.com/api/v7/convert?q=USD_{quote_}&compact=ultra&apiKey=ec0d89548ad9ff4620ad")
            print(quote_to_usd.content)
            quote_to_usd = float(json.loads(quote_to_usd.content)['USD_' + quote_])
            base_to_usd = float(json.loads(base_to_usd.content)['quotes']['USD' + base_])
            quote_to_base = quote_to_usd / base_to_usd
            value = round(amount_ / quote_to_base, 6)
            return value
        else:
            r = requests.post(
                f"http://api.currencylayer.com/live?access_key=5f3f8678366e5935dd728319e90bc512&currencies={quote_},{base_}")
            value = round(amount_ / float(json.loads(r.content)['quotes'][base_ + quote_]), 6)
            return value

    @staticmethod
    def add_currency(name, code, keys_dict=keys):
        """Adds a {name: code} into the dictionary"""
        code = str.upper(code)
        if name in keys:
            raise ConvertException(f'Имя "{name}" уже есть. Введите другое имя. ')
        if code not in Converter.currency_all:
            raise ConvertException(f'Код {code} не поддерживается.')
        else:
            keys_dict.update({name: code})

