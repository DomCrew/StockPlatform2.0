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

```http://127.0.0.1:8000/stocks/[ticker e.g. amzn]/prices?period=[one of 'intraday','daily','weekly','monthly']```
Returns a list of OCHL data in the format:
```
[{
    "date": "2024-01-15T00:00:00",
    "open": 151.179992675781,
    "close": 155.320007324219,
    "high": 155.759994506836,
    "low": 151.175003051758
  }]
```

```http://127.0.0.1:8000/stocks/[ticker e.g. amzn]/volumes?period=[one of 'intraday','daily','weekly','monthly']```
Returns a list of volume in the format:
```
[{
    "date": "2024-01-15T00:00:00",
    "volume": 15123
  }]
```

```http://127.0.0.1:8000/stocks/[ticker e.g. amzn]/smas?period=[one of 'intraday','daily','weekly','monthly']```
Returns a list of simple moving averages in the format:
```
[{
    "date": "2025-12-22T00:00:00",
    "sma20": 228.272476196289,
    "sma50": 216.994674987793,
    "sma100": 202.954708709717
  }]
```

```http://127.0.0.1:8000/stocks/[ticker e.g. amzn/latestprice```
Returns the latest price and the time of the request:
```
{
  "latest_price": 239.12,
  "time": "2026-01-19T18:02:48.407917"
}
```

```http://127.0.0.1:8000/stocks/amzn/articles?limit=5```
Returns a list of articles with sentiment analysis scores in the format:
```
[{
    "date_time": "2026-01-22T14:34:43",
    "title": "Apple and amazon launch new product",
    "link": "https://example.com/amazon-product",
    "sa_label": "positive",
    "sa_score": 0.8
  }]
```

```http://127.0.0.1:8000/stocks/amzn/cashflows```
Returns a list of cashflow information in the format:
```
[{
    "cash_flow_id": 1,
    "stock_id": 1,
    "date_time": "2024-12-31T00:00:00",
    "free_cash_flow": 32878000000,
    "operating_cash_flow": 115877000000,
    "capex": -82999000000,
    "net_income": 59248000000,
    "stock_based_comp": 22011000000,
    "depreciation_amortization": 52795000000,
    "change_working_capital": -15541000000,
    "dividends_paid": null,
    "share_buybacks": 0,
    "share_issuance": null,
    "debt_issuance": 5142000000,
    "debt_repayment": -16954000000,
    "end_cash_position": 82312000000,
    "changes_in_cash": 9723000000
  }]
```

```http://127.0.0.1:8000/stocks/amzn/incomestatements```
Returns a list of income statement information in the format:
```
[{
    "date_time": "2024-12-31T00:00:00",
    "ebitda": 123815000000,
    "ebit": 71020000000,
    "interest_expense": 2406000000,
    "interest_income": 4677000000,
    "diluted_average_shares": 10721000000,
    "diluted_eps": 5.53,
    "net_income": 59248000000,
    "tax_provision": 9265000000,
    "pretax_income": 68614000000,
    "operating_income": 68593000000,
    "operating_expense": 243078000000,
    "gross_profit": 311671000000,
    "total_revenue": 637959000000,
    "stock_id": 1
  }]
```