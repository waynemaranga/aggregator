# Aggregator

## Python 🐍

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Get API keys/tokens:
Here’s the information in a table format:  

| #   | Service                 | Link                                                              |
| --- | ----------------------- | ----------------------------------------------------------------- |
| 1   | Alpha Vantage           | <https://www.alphavantage.co/support/#api-key>                    |
| 2   | Polygon.io              | <https://polygon.io/dashboard/keys>                               |
| 3   | Finnhub                 | <https://finnhub.io/dashboard>                                    |
| 4   | Financial Modeling Prep | <https://site.financialmodelingprep.com/developer/docs/dashboard> |
| 5   | EOD Historical Data     | <https://eodhd.com/cp/dashboard>                                  |

This should make it easier to read and use. 🚀
5. Create `.env` from `.env.example` and fill in the keys/tokens
6. Run `sources.py` or `normalise.py`

## Docker 🐋

1. `docker build --tag aggimg .`
2. `docker run aggimg`
