import os
import csv
import time
from locale import setlocale, atof, LC_ALL
from forex_python.converter import CurrencyRates
from crypto import Crypto


def read_crypto_file(file_name):
    """
    Read crypto.csv and returns a list of crypto objects
    """
    print("Loading crypto...")
    crypto_list = []

    try:
        with open(file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar="|")
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                crypto_list.append(Crypto(row[0], row[1], atof(row[2])))
    except IOError:
        print("Err#100: CSV file for crypto not found.")
    except Exception as e:
        print(f"{e}\nErr#109: Something went terribly wrong.")

    return crypto_list


def read_deposits_file(file_name):
    """
    Read deposits.csv and returns a list deposits in dict
    """
    print("Loading deposits...")
    deposits_list = []

    try:
        with open(file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                deposits_list.append({"Date": row[0],
                                      "Amount": atof(row[1]),
                                      "Currency": row[2]})
    except IOError:
        print("Err#110: CSV file for crypto not found.")
    except Exception as e:
        print(f"{e}\nErr#119: Something went terribly wrong.")

    return deposits_list


def clear_console(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


def display_on_console(crypto_list, deposits_list):
    total_deposits = sum([depos["Amount"] for depos in deposits_list])
    print(f"Total deposits: {total_deposits:.2f} USD\n")

    print(Crypto.header)
    print("-" * 90)
    for cryp in crypto_list:
        cryp.fetch_data()
        cryp.parse_rank()
        cryp.parse_price()
        cryp.parse_price_change_24h()
        cryp.update_holding()
        print(cryp)

    try:
        total_holdings = sum([cryp.holding_fiat for cryp in crypto_list])
        print(f"\nTotal holdings\t| {total_holdings:.2f}")
        print(f"Total deposits\t| {total_deposits:.2f}")
        print(f"Net (USD)\t| {total_holdings - total_deposits:.2f}")
        print(
            f"Net (%)\t\t| {(total_holdings - total_deposits) / total_deposits * 100:.2f}%")
    except ZeroDivisionError:
        print("Err#120: 0 deposits, division by zero error.")

    print(
        f"\nLast updated time:\t{time.strftime('%H:%M:%S', time.localtime())}")


def main():
    crypto_list = read_crypto_file("crypto/crypto.csv")
    deposits_list = read_deposits_file("crypto/deposits.csv")

    c = CurrencyRates()
    for depos in deposits_list:
        rate = c.get_rate(depos["Currency"], "USD")
        depos["Amount"] *= rate

    start_time = time.time()
    while True:
        clear_console()
        display_on_console(crypto_list, deposits_list)
        time.sleep(180 - (time.time() - start_time) % 180)


if __name__ == "__main__":
    # os.chdir(os.path.dirname(__file__))
    try:
        setlocale(LC_ALL, "en_US.utf8")
    except Exception:
        try:
            setlocale(LC_ALL, "en_US.UTF-8")
        except Exception as e:
            print(f"{e}\nErr#000: locale error.")
    clear_console()
    main()
