import json
import requests
from config import keys


class ValueException(Exception):
    pass


class ValueConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: float):

        if base == quote:
            raise ValueException(f'{quote} это {quote}\nЯ так понимаю вы просто хотите увидеть число {amount}).')

        try:
            keys[base]
        except KeyError:
            raise ValueException(f'Не удалось найти валюту {base}.')

        try:
            keys[quote]
        except KeyError:
            raise ValueException(f'Не удалось найти валюту {quote}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ValueException(f'Не удалось обработать количество {amount}, для дробных чисел используйте точку.')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/09eb62f135f78a1ebace27b4/latest/{keys[base]}')
        total = json.loads(r.content)["conversion_rates"][f'{keys[quote]}']
        total *= float(amount)
        return round(total, 2)
