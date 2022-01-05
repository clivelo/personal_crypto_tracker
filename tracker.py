import os
import sys
import csv
import time
from locale import setlocale, LC_NUMERIC
from crypto import Crypto


def read_crypto_file(file_name):
    """
    Read crypto.csv and returns a list of crypto objects
    """
    crypto_list = []

    try:
        with open(file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar="|")
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                crypto_list.append(Crypto(row[0], row[1]))
    except IOError:
        print("Err#100: CSV file for crypto not found.")
    except Exception as e:
        print(f"{e}\nErr#109: Something went terribly wrong.")

    return crypto_list


def read_deposits_file(file_name):
    """
    Read deposits.csv and returns a list deposits in dict
    """
    deposits_list = []

    try:
        with open(file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                deposits_list.append({"Date": row[0],
                                      "Amount": row[1],
                                      "Currency": row[2]})
    except IOError:
        print("Err#110: CSV file for crypto not found.")
    except Exception as e:
        print(f"{e}\nErr#119: Something went terribly wrong.")

    return deposits_list


def clearConsole(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


def main():
    crypto_list = read_crypto_file("crypto/crypto.csv")
    deposits_list = read_deposits_file("crypto/deposits.csv")

    start_time = time.time()
    while True:
        clearConsole()
        for cryp in crypto_list:
            cryp.fetch_data()
            cryp.parse_rank()
            cryp.parse_price()
            cryp.parse_price_change_24h()
            print(cryp)
        time.sleep(60 - (time.time() - start_time) % 60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    setlocale(LC_NUMERIC, "en_US.ISO8859-1")
    clearConsole()
    main()
