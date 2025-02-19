import os
import json
from datetime import datetime
import requests
from typing import Any, Optional
import random
import boto3

# AWS SDK
sqs = boto3.client("sqs")
SQS_QUEUE_URL: Optional[str] = os.environ.get("AWS_SQS_QUEUE_URL")

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


def fetch_financial_data(api_keys: dict[str, Optional[str]] = get_api_keys(), symbol: str = DEFAULT_TICKER) -> dict[str, Any]:
    """Fetch financial data from multiple sources"""
    results = {}
    api_keys = get_api_keys()

    # AlphaVantage
    if api_keys["ALPHAVANTAGE_API_KEY"]:
        try:
            url: str = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_keys['ALPHAVANTAGE_API_KEY']}"
            response: requests.Response = requests.get(url)
            results["alphavantage"] = response.json()

        except Exception as e:
            print(f"AlphaVantage API error: {str(e)}")
            results["alphavantage"] = None

    # Polygon.io
    if api_keys["POLYGONIO_API_KEY"]:
        try:
            url: str = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={api_keys['POLYGONIO_API_KEY']}"
            response: requests.Response = requests.get(url)
            results["polygonio"] = response.json()

        except Exception as e:
            print(f"Polygon.io API error: {str(e)}")
            results["polygonio"] = None

    # Finnhub
    if api_keys["FINNHUB_API_KEY"]:
        try:
            url: str = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_keys['FINNHUB_API_KEY']}"
            response: requests.Response = requests.get(url)
            results["finnhub"] = response.json()

        except Exception as e:
            print(f"Finnhub API error: {str(e)}")
            results["finnhub"] = None

    # Financial Modeling Prep
    if api_keys["FMP_API_KEY"]:
        try:
            url: str = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_keys['FMP_API_KEY']}"
            response: requests.Response = requests.get(url)
            results["fmp"] = response.json()

        except Exception as e:
            print(f"Financial Modeling Prep API error: {str(e)}")
            results["fmp"] = None

    # EOD Historical Data
    if api_keys["EODHD_API_TOKEN"]:
        try:
            url: str = f"https://eodhd.com/api/real-time/{symbol}.US?api_token={api_keys['EODHD_API_TOKEN']}&fmt=json"
            response: requests.Response = requests.get(url)
            results["eodhd"] = response.json()

        except Exception as e:
            print(f"EOD Historical Data API error: {str(e)}")
            results["eodhd"] = None

    return results


def lambda_handler(event, context):
    print(f"Starting financial data check at {event.get('time', datetime.now())}...")

    try:
        # Get symbol from event or use default
        symbol = event.get("symbol", "AAPL")

        results: dict[str, Any] = fetch_financial_data(symbol=symbol)
        sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(results))
        return {"statusCode": 200,"body": f"Sent to SQS at {datetime.now().isoformat()}"}

    except Exception as e:
        print(f"Check failed: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e), "timestamp": str(datetime.now())}),
        }

    finally:
        print(f"Check complete at {str(datetime.now())}")
