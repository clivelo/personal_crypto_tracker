import re
import requests
from bs4 import BeautifulSoup
from locale import atof, Error as localeError


class CurrencyConverter:

    url_prefix = "https://www.marketwatch.com/investing/currency/"
    price_html_class = "intraday__price"

    def get_rate(self, from_curr, to_curr):
        """Fetch data from url"""
        try:
            page = requests.get(f"{self.url_prefix}{from_curr}{to_curr}")
        except requests.ConnectionError:
            print("Err#300: Network problem, connection error.")
        except requests.HTTPError as e:
            print(f"Err#301: HTTPError {e}.")
        except requests.Timeout as e:
            print(f"Err#302: Connection timeout. {e}")
        except requests.TooManyRedirects:
            print("Err#303: Too many redirects.")
        except Exception as e:
            print(f"{e}\nErr#399: Something went terribly wrong.")
        data = BeautifulSoup(page.content, "html.parser")

        price = self.parse_price(data)
        return price

    def parse_price(self, data):
        """Parse current price"""
        try:
            price = data.find_all(class_=self.price_html_class)
        except Exception as e:
            print(f"{e}\nErr#321: Could not parse current price.")
        if not price:
            raise Exception("Err#321: Could not parse current price.")

        try:
            # Regex for looking between value"> and </span
            price = atof(re.search(r"(?<=>)(.*?)(?=</bg-quote)", str(price))
                         .group(0))
        except localeError:
            print("Err#323: Locale error")
        except Exception as e:
            print(f"{e}\nErr#322: This is why I hate regex.")

        return price
