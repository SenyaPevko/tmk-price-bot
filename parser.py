import requests
from bs4 import BeautifulSoup
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
                    # Cells must be enough for parsing
                    if len(cells) > 1:
                        # Fetching info
                        if commodity_name.lower() in cells[0].text.lower():
                            commodity_price = cells[1].text.strip()
                            return commodity_price

                # In case cells not found
                return None

            else:
                self.logger.error(f"Не удалось выполнить запрос к {self.url}, статус код: {response.status_code}")
                return None

        else:
            return None

