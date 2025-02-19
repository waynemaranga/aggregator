import os
import json
from datetime import datetime
import http.client
import urllib.parse
from typing import Any, Optional
import random

# Default Values
TODAY: str = datetime.today().strftime("%Y-%m-%d")
DEFAULT_DATE: str = TODAY
TICKERS: list[str] = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA"]
DEFAULT_TICKER: str = random.choice(TICKERS)
# DEFAULT_TICKER: str = "MSFT"


def get_api_keys() -> dict[str, Optional[str]]:
    """Retrieve API keys from Lambda environment variables"""
    return {
        "ALPHAVANTAGE_API_KEY": os.environ.get("ALPHAVANTAGE_API_KEY"),
        "POLYGONIO_API_KEY": os.environ.get("POLYGONIO_API_KEY"),
        "FINNHUB_API_KEY": os.environ.get("FINNHUB_API_KEY"),
        "FMP_API_KEY": os.environ.get("FMP_API_KEY"),
        "EODHD_API_TOKEN": os.environ.get("EODHD_API_TOKEN"),
    }


def fetch_url(base_url: str, endpoint: str):
    """Fetch JSON response from an API using http.client"""
    try:
        parsed_url: urllib.parse.ParseResult = urllib.parse.urlparse(base_url)
        conn = http.client.HTTPSConnection(parsed_url.netloc)

        conn.request("GET", endpoint, headers={"User-Agent": "Mozilla/5.0"})
        response: http.client.HTTPResponse = conn.getresponse()

        if response.status == 200:
            return json.loads(response.read().decode())
        else:
            print(f"Error {response.status}: {response.reason}")
            return None

    except Exception as e:
        print(f"API request error: {str(e)}")
        return None

    finally:
        conn.close()


def fetch_financial_data(
    api_keys: dict[str, Optional[str]] = get_api_keys(), symbol: str = DEFAULT_TICKER
) -> dict[str, Any]:
    """Fetch financial data from multiple sources"""
    results = {}
    api_keys = get_api_keys()

    # AlphaVantage
    if api_keys["ALPHAVANTAGE_API_KEY"]:
        url: str = "https://www.alphavantage.co"
        endpoint: str = f"/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_keys['ALPHAVANTAGE_API_KEY']}"
        results["alphavantage"] = fetch_url(url, endpoint)

    # Polygon.io
    if api_keys["POLYGONIO_API_KEY"]:
        url: str = "https://api.polygon.io"
        endpoint: str = f"/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={api_keys['POLYGONIO_API_KEY']}"
        results["polygonio"] = fetch_url(url, endpoint)

    # Finnhub
    if api_keys["FINNHUB_API_KEY"]:
        url: str = "https://finnhub.io"
        endpoint: str = (
            f"/api/v1/quote?symbol={symbol}&token={api_keys['FINNHUB_API_KEY']}"
        )
        results["finnhub"] = fetch_url(url, endpoint)

    # Financial Modeling Prep
    if api_keys["FMP_API_KEY"]:
        url: str = "https://financialmodelingprep.com"
        endpoint: str = f"/api/v3/quote/{symbol}?apikey={api_keys['FMP_API_KEY']}"
        results["fmp"] = fetch_url(url, endpoint)

    # EOD Historical Data
    if api_keys["EODHD_API_TOKEN"]:
        url: str = "https://eodhd.com"
        endpoint: str = f"/api/real-time/{symbol}.US?api_token={api_keys['EODHD_API_TOKEN']}&fmt=json"
        results["eodhd"] = fetch_url(url, endpoint)

    return results


def lambda_handler(event, context):
    print(f"Starting financial data check at {event.get('time', datetime.now())}...")

    try:
        # Get symbol from event or use default
        symbol = event.get("symbol", "AAPL")

        # Fetch data
        results: dict[str, Any] = fetch_financial_data(symbol=symbol)

        # You might want to store this in S3 or another database
        # For now, we'll just return it
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"timestamp": str(datetime.now()), "symbol": symbol, "data": results}
            ),
        }

    except Exception as e:
        print(f"Check failed: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e), "timestamp": str(datetime.now())}),
        }

    finally:
        print(f"Check complete at {str(datetime.now())}")
