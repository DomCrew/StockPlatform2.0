# STOCKPLATFORM2

The purpose of this project was to create an improved version of my university capstone project, a platform for analysing stocks. There are two parts, a Python/SQL backend and a React frontend.

## GETTING STARTED

To run the backend, you will need [Python](https://www.python.org/downloads/) (I used 3.13.9 whilst creating this) and access to a [PostgreSQL](https://www.postgresql.org/download/windows/) database. For the frontend, you will need [node.js](https://nodejs.org/en/download).

### BACKEND

In the root directory, create a file ```.env``` and enter your database credentials like so:
```
DB_USER=[db username]
DB_NAME=[db name]
DB_PORT=[db port]
DB_PASSWORD=[db password]
DB_HOST=[db_host]
```

Create a virtual environment and install dependencies:
```
python -m -venv .venv
.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Then, to run the backend do ```fastapi dev```

### FRONTEND

```
cd frontend
npm install react-apexcharts apexcharts
```

Then, to run the frontend do ```npm start```

## API ENDPOINTS

```/stocks/[ticker e.g. amzn]/endpoint```

### Stock Info

```http://127.0.0.1:8000/stocks/[ticker e.g. amzn]/info```
Returns a dictionary of static information in the format:
```
{
  "stock_id": 1,
  "ticker": "amzn",
  "long_name": "Amazon.com, Inc.",
  "description": "Long business summary",
  "sector": "Consumer Cyclical",
  "industry": "Internet Retail",
  "full_time_employees": 1578000,
  "exchange": "NasdaqGS",
  "currency": "USD",
  "country": "United States",
  "last_updated": "2026-01-20T18:16:18.009058"
}
```

### Chart data

These endpoints all take a parameter ```period```, which can be one of ```"intraday"```, ```"daily"```, ```"weekly"``` or ```"monthly"```. This determines the intervals between each data point as well as how far back in time to fetch data for. For example, ```"weekly"``` will fetch weekly values for a period of 2 years. If a period is not provided, it defaults to ```"weekly"```.

For OHLC data, there is a ```prices``` endpoint. ```http://127.0.0.1:8000/stocks/ticker/prices``` returns a list of dictionaries with OHLC data, in order of date.
```
[{
    "date": "2024-01-15T00:00:00",
    "open": 151.179992675781,
    "close": 155.320007324219,
    "high": 155.759994506836,
    "low": 151.175003051758
  }, ...]
```

For volumes ```http://127.0.0.1:8000/stocks/ticker/volumes``` will returns a list of volumes in the format:
```
[{
    "date": "2024-01-15T00:00:00",
    "volume": 15123
  }, ...]
```

For simple moving averages, ```http://127.0.0.1:8000/stocks/ticker/volumes``` returns a list of simple moving average dictionaries in the format:
```
[{
    "date": "2025-12-22T00:00:00",
    "sma20": 228.272476196289,
    "sma50": 216.994674987793,
    "sma100": 202.954708709717
  }, ...]
```

For on balance volume, ```http://127.0.0.1:8000/stocks/ticker/obvs``` returns a list of on balance volume figures like so:
```
[{
    "date_time": "2024-01-22T00:00:00",
    "obv": 64663492
  }, ...]
```

For average true range, ```http://127.0.0.1:8000/stocks/ticker/obvs``` returns a list of average true range data in the format:
```
[
  {
    "date_time": "2024-01-22T00:00:00",
    "atr": 9.11776406424386
  }, ...]
```

For commodity channel index, ```http://127.0.0.1:8000/stocks/ticker/ccis``` returns a list of commodity channel index figures:
```
[{
    "date_time": "2024-06-03T00:00:00",
    "CCI": 59.1266205811448,
    ...
  }, ...]
```

For moving average convergence divergence, ```http://127.0.0.1:8000/stocks/ticker/macd``` returns the macd line, signal line and histogram information like so:
```
[{
    "date_time": "2024-01-22T00:00:00",
    "macd_line": 0,
    "signal_line": 0,
    "histogram": 0
  }, ...]
```

### Other

```http://127.0.0.1:8000/stocks/[ticker e.g. amzn/latestprice```
Returns the latest price and the time of the request:
```
{
  "latest_price": 239.16,
  "time": "2026-01-25T16:13:12.385629",
  "diff": {
    "actual": -0.0300024414062534,
    "previous": 239.190002441406,
    "percentage": -0.01
  }
}
```

For a list of recent articles, there is an endpoint ```articles```, which also takes a ```limit``` parameter. This: ```http://127.0.0.1:8000/stocks/amzn/articles?limit=5``` returns the five most recent articles for amzn in order of date:
```
[{
    "date_time": "2026-01-22T14:34:43",
    "title": "Apple and amazon launch new product",
    ...
  }, ...]
```

There are three endpoints for finance tables, ```cashflows```, ```balancesheets``` and ```incomestatements```. For example, ```http://127.0.0.1:8000/stocks/amzn/cashflows``` will return a list of cashflow dictionaries in order of date:
```
[{
    "cash_flow_id": 1,
    "stock_id": 1,
    "date_time": "2024-12-31T00:00:00",
    "free_cash_flow": 32878000000,
    ...
  }, ...]
```