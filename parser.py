import requests
from bs4 import BeautifulSoup
from pycbrf.toolbox import ExchangeRates
import consts
from logger import Logger


class Parser:
    def __init__(self):
        self.url = consts.PRICE_URL
        self.headers = consts.PARSER_HEADERS
        self.logger = Logger("parser logger")

    def get_commodity_prices(self, commodity_name):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            self.logger.info(f"Успешный запрос к {self.url}")
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find("table", class_="table-heatmap")

            if table:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    # Если есть ячейки и их достаточно для обработки
                    if len(cells) > 1:
                        # Извлекаем информацию о котировках для заданного товара
                        if commodity_name.lower() in cells[0].text.lower():
                            commodity_price = cells[1].text.strip()
                            return commodity_price

                # Если товар не найден
                return None

            else:
                self.logger.error(f"Не удалось выполнить запрос к {self.url}, статус код: {response.status_code}")
                return None

        else:
            return None

    def get_currency_rate(self, currency_code):
        rates = ExchangeRates()
        try:
            rate = rates[currency_code]
            self.logger.info(f"Получен курс валюты {currency_code}: {rate.rate}")
            return rate.rate
        except KeyError:
            self.logger.error(f"Не удалось получить курс валюты {currency_code}")
            return None