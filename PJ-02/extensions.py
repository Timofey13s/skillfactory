import requests
import json
from config import code_cur

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):

        if not base in code_cur:
            raise APIException(f'Не найдена валюта {base}')
        if not quote in code_cur:
            raise APIException(f'Не найдена валюта {quote}')
        if base == quote:
            raise APIException('Невозможно перевести одинаковые валюты')
        try:
            amount_sum = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        if amount_sum <= 0:
            raise APIException(f'Количество должно быть больше нуля')

        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = json.loads(r.content)

        if base != 'рубль':
            base_rub = float(data['Valute'][code_cur[base]]['Value'])
        else:
            base_rub = 1
        if quote != 'рубль':
            if not quote in code_cur:
                raise APIException(f'Не найдена валюта {quote}')
            quote_rub = float(data['Valute'][code_cur[quote]]['Value'])
        else:
            quote_rub = 1

        return round(base_rub / quote_rub * amount_sum, 2)
