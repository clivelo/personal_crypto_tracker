import os
import csv
import time
import json
from locale import setlocale, atof, LC_ALL
from crypto import Crypto, Wallet
from colorama import init, Back, Style
from google_currency import convert


def read_crypto_file(file_name):
    """
    Read crypto.csv and returns a list of crypto objects
    """
    print("Loading crypto...")

    try:
        with open(file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar="|")
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                w.add_coin(Crypto(row[0], row[1], atof(row[2])))
    except IOError:
        raise Exception("Err#100: CSV file for crypto not found.")
    except Exception as e:
        raise Exception(f"{e}\nErr#109: Something went terribly wrong.")


def read_deposits_file(file_name):
    """
    Read deposits.csv and returns a list deposits in dict
    """
    print("Loading deposits...")

    try:
        with open(file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                w.add_deposit({"Date": row[0],
                               "Amount": atof(row[1]),
                               "Currency": row[2]})
    except IOError:
        raise Exception("Err#110: CSV file for crypto not found.")
    except Exception as e:
        raise Exception(f"{e}\nErr#119: Something went terribly wrong.")


def clear_console(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


def display_on_console():
    print(f"Total deposits: {w.total_deposits:.2f} USD\n")

    print(Crypto.header)
    print("-" * 90)
    w.update_rates()
    for cryp in w.wallet:
        print(cryp)

    try:
        print(f"\nTotal holdings\t| {w.total_holdings:.2f}")
        print(f"Total deposits\t| {w.total_deposits:.2f}")
        highlight_color = Back.GREEN if w.total_holdings >= w.total_deposits else Back.RED
        print(f"{highlight_color}Net (USD)\t| {w.total_holdings - w.total_deposits:.2f}")
        print(
            f"{highlight_color}Net (%)\t\t| {(w.total_holdings - w.total_deposits) / w.total_deposits * 100:.2f}%")
    except ZeroDivisionError:
        raise Exception("Err#120: 0 deposits, division by zero error.")
    except Exception as e:
        raise Exception(f"{e}\nErr#129: Something went terribly wrong.")

    print(
        f"\nLast updated time:\t{time.strftime('%H:%M:%S', time.localtime())}")


def main():
    read_crypto_file("crypto/crypto.csv")
    read_deposits_file("crypto/deposits.csv")

    print("Loading currency rates...")
    currency_pairs = {}
    for depos in w.deposits:
        currency_pair = depos["Currency"] + "USD"
        if currency_pair not in currency_pairs.keys():
            for i in range(5):
                currency_converter = json.loads(convert(depos["Currency"], "USD", 1))
                if currency_converter["converted"]:
                    break
                elif i == 4:
                    raise Exception(
                        f"Err#301: two possible errors here\n1. Bad currency code: {depos}\n2. API for converting currency failed 5 times in a row.")
            currency_pairs[currency_pair] = atof(currency_converter["amount"])
        depos["Amount"] *= currency_pairs[currency_pair]
        depos["Currency"] = "USD"
    w.update_total_deposits()

    start_time = time.time()
    while True:
        clear_console()
        display_on_console()
        time.sleep(180 - (time.time() - start_time) % 180)


if __name__ == "__main__":
    # os.chdir(os.path.dirname(__file__))
    try:
        setlocale(LC_ALL, "en_US.utf8")
    except Exception:
        try:
            setlocale(LC_ALL, "en_US.UTF-8")
        except Exception as e:
            raise Exception(f"{e}\nErr#000: locale error.")
    init(autoreset=True)
    clear_console()

    print("Initializing wallet...")
    w = Wallet()

    main()
