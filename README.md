# Personal Crypto Tracker
A simple tracker for your cryptocurrency investments. Input your deposits and crypto holdings in the CSV files, this app will display all the prices of the cryptos you own on the terminal and calculate the net value of your investments. It's always a good idea to keep track of your investments using a spreadsheet, this app encourages you as you will need to input your data into a CSV file and also serves to provide concise summary of your investments.

## Dependencies
App written in `python 3.10.1`, other versions may or may not work.
- requests
- bs4
- colorama
- google-currency

## Install and run app
1. Clone this repository
2. Open terminal/command line
3. Change directory `cd` to this app
4. Execute `python3 tracker.py`

## CSV formatting
Two CSV files are needed (`crypto.csv` and `deposits.csv`) and must be placed inside the `crypto/` directory. They must follow the required format below.

### crypto.csv
- The `Coin` column must must hold strings that allow access to `https://coinmarketcap.com/currencies/<coin>`.
- The `Symbol` column holds strings that are only for display.
- The `Holdings` column must be a numeric value that can be cast to `float`. Commas in numbers can be parsed (e.g., 1,000).

| Coin | Symbol | Holdings |
| -- | -- | -- |
| Bitcoin | BTC | 0.013 |
| Ethereum | ETH | 0.16 |

### deposits.csv
- The `Date` column is currently unused, its use may be implemented in the future.
- The `Amount` column must hold numeric values that can be cast to `float`. Commas in numbers can be parsed (e.g., 1,000). DO NOT include currency symbols (e.g., $).
- The `Currency` column must hold strings that abide to the ISO 4217 currency codes.

| Date | Amount | Currency |
| -- | -- | -- |
| Jan 1, 2022 | 1000 | USD |
| Jan 2, 2022 | 200 | EUR |

## Future plans
I am planning to add a GUI to this tracker for more data visualization.
