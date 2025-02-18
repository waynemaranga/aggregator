from sources import (
    fetch_alphavantage_data,
    fetch_finnhub_data,
    fetch_fmp_data,
    fetch_eodhd_data,
)

# Normalise the data from the different sources into a common format

def normalise_finnhub_data(data: dict = fetch_finnhub_data()) -> dict:
    return {
        "open": data.get("o", 0),
        "high": data.get("h", 0),
        "low": data.get("l", 0),
        "close": data.get("c", 0),
        "previous_close": data.get("pc", 0),
    }


def normalise_alphavantage_data(data: dict = fetch_alphavantage_data()) -> dict:
    payload = data.get("Global Quote", {})
    return {
        "open": payload.get("02. open", 0),
        "high": payload.get("03. high", 0),
        "low": payload.get("04. low", 0),
        "close": payload.get("05. price", 0),
        "previous_close": payload.get("08. previous close", 0),
    }


def normalise_fmp_data(data: dict = fetch_fmp_data()) -> dict:
    payload = data[0]
    return {
        "open": payload.get("open", 0),
        "high": payload.get("dayHigh", 0),
        "low": payload.get("dayLow", 0),
        "close": payload.get("price", 0),
        "previous_close": payload.get("previousClose", 0),
    }


def normalise_eodhd_data(data: dict = fetch_eodhd_data()) -> dict:
    return {
        "open": data.get("open", 0),
        "high": data.get("high", 0),
        "low": data.get("low", 0),
        "close": data.get("close", 0),
        "previous_close": data.get("previousClose", 0),
    }


if __name__ == "__main__":
    # print(fetch_finnhub_data())
    print(normalise_finnhub_data())
    # print(fetch_alphavantage_data())
    print(normalise_alphavantage_data())
    # print(fetch_fmp_data())
    print(normalise_fmp_data())
    # print(fetch_eodhd_data())
    print(normalise_eodhd_data())

    print("🐬")
