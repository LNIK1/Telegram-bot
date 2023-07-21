import requests
import json
from config import value_keys


class APIException(Exception):
    pass


class ValueException(Exception):
    pass


class Conversion:

    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException('Базовая и конвертируемая валюты должны отличаться.')

        try:
            base_ticker = value_keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}.\n'
                               f'Для просмотра доступного списка валют введите команду /values')

        try:
            quote_ticker = value_keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}.\n'
                               f'Для просмотра доступного списка валют введите команду /values')

        try:
            amount_value = float(amount)
        except ValueError:
            raise APIException(f'Количество конвертируемой валюты должно быть числом.')

        r = requests.get(f'https://api.coingate.com/v2/rates/merchant/{base_ticker}/{quote_ticker}')
        request_total = json.loads(r.content)

        try:
            total_value = float(request_total)
        except ValueError:
            raise ValueException(f'Не удалось обработать полученное значение валюты.')

        result = amount_value * total_value

        return result
