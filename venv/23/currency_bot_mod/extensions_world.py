import requests
import json
from get_currencie_world import get_currencie

currencie = get_currencie()

class APIException(Exception):
    pass


class CryptoConverter:

    def all_currency():
        pass

    @staticmethod
    def get_price(quote=str, base=str, amount=str):
        if quote not in currencie.values():
            raise APIException(f'Я не знаю волюту "{quote}"'
                               f'\n\nПопробуй ешё раз\nПример ввода: USD RUB 10')

        if base not in currencie.values():
            raise APIException(f'Я не знаю волюту "{base}" '
                               f'\n\nПопробуй ешё раз\nПример ввода: USD RUB 10')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Мне кажется "{amount}" - это не цифра'
                               f'\n\nПопробуй ешё раз\nПример ввода: USD RUB 10')

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковае валюты {quote}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        total_base = round(json.loads(r.content)[base] * amount, 2)
        return total_base
