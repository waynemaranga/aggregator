# ℹ️ Fetching Open-Close Stock Data from Various APIs

# AWS CDK + OpenAPI & Swagger: https://aws.amazon.com/blogs/devops/deploy-and-manage-openapi-swagger-restful-apis-with-the-aws-cloud-development-kit/
# Swagger Amazon API Gateway Integration: https://swagger.io/blog/api-development/introducing-the-amazon-api-gateway-integration/

import os
import dotenv
from typing import Optional
import requests
from datetime import datetime
import random

dotenv.load_dotenv(".env") # https://github.com/theskumar/python-dotenv?tab=readme-ov-file#getting-started

# API Keys
ALPHAVANTAGE_API_KEY: Optional[str] = os.getenv("ALPHAVANTAGE_API_KEY", "")
POLYGONIO_API_KEY: Optional[str] = os.getenv("POLYGONIO_API_KEY", "")
FINNHUB_API_KEY: Optional[str] = os.getenv("FINNHUB_API_KEY", "")
FMP_API_KEY: Optional[str] = os.getenv("FMP_API_KEY", "")
EODHD_API_TOKEN: Optional[str] = os.getenv("EODHD_API_TOKEN", "")

# Default Values
TODAY: str = datetime.today().strftime("%Y-%m-%d")
DEFAULT_DATE: str = TODAY
TICKERS: list[str] = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA"]
DEFAULT_TICKER: str = random.choice(TICKERS) 
# DEFAULT_TICKER: str = "MSFT" 


# AlphaVantage: https://www.alphavantage.co/documentation/
def fetch_alphavantage_data(ticker: str = DEFAULT_TICKER) -> dict:
    # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo
    try:
        url: str = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}"
        response: requests.Response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# Polygon.io: https://polygon.io/docs/stocks | https://github.com/polygon-io/client-python
def fetch_polygonio_data(ticker: str = DEFAULT_TICKER, date: str = DEFAULT_DATE, adjusted: str = "true") -> dict:
    # https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date
    try:
        #// url: str = f"https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted={adjusted}&apiKey={POLYGONIO_API_KEY}"
        url: str = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted={adjusted}&apiKey={POLYGONIO_API_KEY}"
        response: requests.Response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# Finnhub: https://finnhub.io/docs/api/introduction | https://github.com/Finnhub-Stock-API/finnhub-python
def fetch_finnhub_data(ticker: str = DEFAULT_TICKER) -> dict:
    # https://
    try:
        url: str = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
        response: requests.Response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# Financial Modeling Prep: https://financialmodelingprep.com/developer/docs/
def fetch_fmp_data(ticker: str = DEFAULT_TICKER) -> dict:
    # https://site.financialmodelingprep.com/developer/docs#full-quote-quote
    try:
        url: str = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_API_KEY}"
        response: requests.Response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
# EOD Historical Data: https://eodhistoricaldata.com/financial-apis/
def fetch_eodhd_data(ticker: str = DEFAULT_TICKER, fmt: str = "json") -> dict:
    # 
    try:
        url: str = f"https://eodhd.com/api/real-time/{ticker}.US?api_token={EODHD_API_TOKEN}&fmt={fmt}"
        response: requests.Response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # [print(i) for i in [ALPHAVANTAGE_API_KEY, POLYGONIO_API_KEY, FINNHUB_API_KEY, FMP_API_KEY, EODHD_API_TOKEN]]
    # print(TODAY)
    print(fetch_polygonio_data())
    print(fetch_finnhub_data())
    print(fetch_alphavantage_data())
    print(fetch_fmp_data())
    print(fetch_eodhd_data())

    print("🐬")
