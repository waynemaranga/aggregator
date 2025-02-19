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

## AWS Lambda
1. `uv pip freeze > requirements.txt`
2. `pip install -r requirements.txt -t dependencies/`
3. `zip -r dependencies-layer.zip dependencies/`
4. Upload the zip file as a Lambda layer

## Workflow
1. Create the Lambda
2. EventBridge/CloudWatch Events triggers/runs Lambda at fixed/given interval and rate (other variables). The rule runs on a schedule, not an event. TODO: try to run on event e.g client triggers etc. from frontend
   - Rule type: Schedule
   - Create rule (TODO: try Event Bridge Scheduler)
   - Schedule runs at regular/fixed rate i.e every 90 minutes.
   - Target type: AWS service (TODO: try EventBridge targets e.g event bus, API destination)
   - Target: Lambda function -> enter function ARN or select from dropdown (+ version and alias)
   - (Optional) consider using dead letter queue (DLQ) for failed invocations
   - **SUMMARY** -> RULE DETAIL -> BUILD SCHEDULE -> TARGET(S) -> TAGS -> REVIEW -> CREATE RULE
3. Create the message queue
   - Create queue: Use **Standard** type
   - Left configs at default
   - Disabled server side encryption
   - Define access policy with IAM/etc on basic or json
   - (Optional) dead letter queue, tags, redrive allow policy
   - redo the queue with sufficient lambda/sql integration IAM and test
