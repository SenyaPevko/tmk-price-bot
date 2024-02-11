from pycbrf.toolbox import ExchangeRates
from logger import Logger


class CurrencyRater:
    def __init__(self):
        self.logger = Logger("currency rater logger")

    def get_currency_rate(self, currency_code):
        rates = ExchangeRates()
        try:
            rate = rates[currency_code]
            self.logger.info(f"Получен курс валюты {currency_code}: {rate.rate}")
            return rate.rate
        except KeyError:
            self.logger.error(f"Не удалось получить курс валюты {currency_code}")
            return None
