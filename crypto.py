import re
import requests
from bs4 import BeautifulSoup
from locale import atof, Error as localeError


class Crypto:
    """
    Crypto(coin, holding, goal_rate=None, currency="USD")
        Arguments:
        - coin (str): Name of cryptocurrency. Must be a working URL to
          https://coinmarketcap.com/currencies/<coin>
        - holding (float): Amount of coin holding
        - goal_rate (float) (default: None): Price goal for crypto
        - currency (str) (default: USD): Currency that goal_rate operates with.
          Must comply to ISO 4217 names.
    """

    url_prefix = "https://coinmarketcap.com/currencies/"
    rank_html_class = "namePill namePillPrimary"
    price_html_class = "priceValue"
    price_change_24h_up_html_class = "sc-15yy2pl-0 gEePkg"
    price_change_24h_down_html_class = "sc-15yy2pl-0 feeyND"

    def __init__(self, coin, holding, goal_rate=None, currency="USD"):
        self.coin = coin
        self.holding = holding
        self.goal_rate = goal_rate
        self.currency = currency
        self.url = f"{self.url_prefix}{self.coin}"
        self.isUp = True
        self.fetch_data()
        self.parse_rank()
        self.parse_price()
        self.parse_price_change_24h()

    def fetch_data(self):
        try:
            self.page = requests.get(self.url)
        except requests.ConnectionError:
            print("Err#200: Network problem, connection error.")
        except requests.HTTPError as e:
            print(f"Err#201: HTTPError {e}.")
        except requests.Timeout as e:
            print(f"Err#202: Connection timeout. {e}")
        except requests.TooManyRedirects:
            print("Err#203: Too many redirects.")
        except Exception as e:
            print(f"{e}\nErr#299: Something went terribly wrong.")
        self.data = BeautifulSoup(self.page.content, "html.parser")

    def parse_rank(self):
        """Parse coin rank"""
        try:
            rank = self.data.find_all(class_=self.rank_html_class)
        except Exception as e:
            print(f"{e}\nErr#210: Could not parse rank.")
        if not rank:
            raise Exception("Err#210: Could not parse rank.")

        try:
            # Regex for looking between # and <
            self.rank = int(re.search(r"(?<=#)(.*?)(?=<)", str(rank)).group(0))
        except Exception:
            print("Err#211: This is why I hate regex.")

    def parse_price(self):
        """Parse current price"""
        try:
            price = self.data.find_all(class_=self.price_html_class)
        except Exception as e:
            print(f"{e}\nErr#221: Could not parse current price.")
        if not price:
            raise Exception("Err#221: Could not parse current price.")

        try:
            # Regex for looking between $ and <
            self.price = atof(re.search(r"(?<=\$)(.*?)(?=<)", str(price))
                              .group(0))
        except localeError:
            print("Err#223: Locale error")
        except Exception as e:
            print(f"{e}\nErr#222: This is why I hate regex.")

    def parse_price_change_24h(self):
        """Parse price change last 24-hour"""
        try:
            price_change_24h = self.data.find_all(
                class_=self.price_change_24h_up_html_class)
            self.isUp = True
            if not price_change_24h:
                price_change_24h = self.data.find_all(
                    class_=self.price_change_24h_down_html_class)
                self.isUp = False
        except Exception as e:
            print(f"{e}\nErr#231: Could not parse price change last 24-hour.")
        if not price_change_24h:
            raise Exception(
                "Err#231: Could not parse price change last 24-hour.")

        try:
            # Regex for looking between $ and <
            self.price_change_24h = atof(re.search(
                r"(?<=span>)(.*?)(?=<\!)", str(price_change_24h[0])).group(0))
            if not self.isUp:
                self.price_change_24h *= -1
        except localeError:
            print("Err#233: Locale error")
        except Exception as e:
            print(f"{e}\nErr#232: This is why I hate regex.")

    def __repr__(self):
        return f"Crypto({self.coin}, {self.holding},\
                        goal_rate={self.goal_rate},\
                        currency={self.currency})"

    def __str__(self):
        return f"{self.coin}: ${self.price} {self.price_change_24h}% {self.holding}"
