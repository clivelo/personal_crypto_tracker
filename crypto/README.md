## CSV formatting
Two CSV files are needed (`crypto.csv` and `deposits.csv`) and must be placed inside the `crypto/` directory. They must follow the required format below.

### crypto.csv
- The `Coin` column must must hold strings that allow access to `https://coinmarketcap.com/currencies/<coin>`.
- The `Symbol` column holds strings that is only for display.
- The `Holdings` column must be a numeric value that can be cast to `float`. Commas in numbers can be parsed (e.g., 1,000).

| Coin | Symbol | Holdings |
| -- | -- | -- |
| Bitcoin | BTC | 0.013 |
| Ethereum | ETH | 0.16 |

### deposits.csv
- The `Date` column is currently unused, its use may be implemented in the future.
- The `Amount` column must hold numeric values that can be cast to `float`. Commas in numbers can be parsed (e.g., 1,000).
- The `Currency` column must hold strings that abide to the ISO 4217 currency codes.

| Date | Amount | Currency |
| -- | -- | -- |
| Jan 1, 2022 | 1000 | USD |
| Jan 2, 2022 | 200 | EUR |
