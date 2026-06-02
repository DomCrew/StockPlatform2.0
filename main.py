from typing import Union
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd
from pydantic import BaseModel

from collection.finance import get_atrs, get_obvs, get_smas, get_latest_price, get_ccis, get_macds
from database.database import DatabaseManager
import utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# e.g. http://127.0.0.1:8000/stocks/


@app.get("/stocks")
def read_root():
    dbm = utils.get_dbm()
    tickers = dbm.get_tickers()
    dbm.close_connection()
    return tickers

# e.g. http://127.0.0.1:8000/stocks/amzn/latestprice


@app.get("/stocks/{ticker}/latestprice")
def read_item(ticker: str):
    latest = get_latest_price(ticker)
    return {"latest_price": latest,
            "time": datetime.today(),
            "diff": utils.get_price_change_from_previous(ticker, latest)}

# e.g. http://127.0.0.1:8000/stocks/amzn/info


@app.get("/stocks/{ticker}/info")
def read_item(ticker: str):
    dbm = utils.get_dbm()
    info = dbm.get_info(ticker)
    dbm.close_connection()
    return utils.none_to_missing_dict(info)

# e.g. http://127.0.0.1:8000/stocks/amzn/daily


@app.get("/stocks/{ticker}/daily")
def read_item(ticker: str):
    dbm = utils.get_dbm()
    daily = dbm.get_stock_daily(ticker)
    dbm.close_connection()
    return utils.none_to_missing_dict(daily)

# e.g. http://127.0.0.1:8000/stocks/amzn/articles?limit=5


@app.get("/stocks/{ticker}/articles")
def read_item(ticker: str, limit: Union[int, None] = 10):
    dbm = utils.get_dbm()
    articles = dbm.get_articles(ticker, limit)
    dbm.close_connection()
    return articles

# Finance tables

# http://127.0.0.1:8000/stocks/amzn/cashflows


@app.get("/stocks/{ticker}/cashflows")
def read_item(ticker: str):
    dbm = utils.get_dbm()
    cash_flows = dbm.get_cash_flows(ticker)
    dbm.close_connection()
    return cash_flows

# http://127.0.0.1:8000/stocks/amzn/incomestatements


@app.get("/stocks/{ticker}/incomestatements")
def read_item(ticker: str):
    dbm = utils.get_dbm()
    income_statement = dbm.get_income_statements(ticker)
    dbm.close_connection()
    return income_statement

# http://127.0.0.1:8000/stocks/amzn/balancesheets


@app.get("/stocks/{ticker}/balancesheets")
def read_item(ticker: str):
    dbm = utils.get_dbm()
    balance_sheet = dbm.get_balance_sheets(ticker)
    dbm.close_connection()
    return balance_sheet

# Chart data

# e.g. http://127.0.0.1:8000/stocks/amzn/prices?period=weekly


@app.get("/stocks/{ticker}/prices")
def read_item(ticker: str, period: Union[str, None] = "weekly"):
    dbm = utils.get_dbm()
    prices = dbm.get_prices(ticker, period)
    dbm.close_connection()
    prices = utils.rename_keys_in_dict_list(
        prices, ["date", "open", "close", "high", "low"])
    return prices

# e.g. http://127.0.0.1:8000/stocks/amzn/smas?period=weekly


@app.get("/stocks/{ticker}/smas")
def read_item(ticker: str, period: Union[str, None] = "weekly"):
    dbm = utils.get_dbm()
    prices = dbm.get_prices(ticker, period)
    dbm.close_connection()
    smas = get_smas(pd.DataFrame(prices))
    return smas

# e.g. http://127.0.0.1:8000/stocks/amzn/volumes?period=weekly


@app.get("/stocks/{ticker}/volumes")
def read_item(ticker: str, period: Union[str, None] = "weekly"):
    dbm = utils.get_dbm()
    volumes = dbm.get_volumes(ticker, period)
    dbm.close_connection()
    volumes = utils.rename_keys_in_dict_list(volumes, ["date", "volume"])
    return volumes

# http://127.0.0.1:8000/stocks/amzn/ccis?period=weekly


@app.get("/stocks/{ticker}/ccis")
def read_item(ticker: str, period: Union[str, None] = "weekly"):
    dbm = utils.get_dbm()
    typical_prices = dbm.get_typical_prices(ticker, period)
    cci_values = get_ccis(typical_prices)
    dbm.close_connection()
    return cci_values

# http://127.0.0.1:8000/stocks/amzn/macd?period=weekly


@app.get("/stocks/{ticker}/macd")
def read_item(ticker: str, period: Union[str, None] = "weekly"):
    dbm = utils.get_dbm()
    prices = dbm.get_prices(ticker, period)
    dbm.close_connection()
    return get_macds(prices)

# http://127.0.0.1:8000/stocks/amzn/obvs?period=weekly


@app.get("/stocks/{ticker}/obvs")
def read_item(ticker: str, period: Union[str, None] = "weekly"):
    dbm = utils.get_dbm()
    volume = dbm.get_volumes(ticker, period)
    prices = dbm.get_prices(ticker, period)
    history = utils.merge_lists_by_date_time(prices, volume)
    dbm.close_connection()
    return get_obvs(history)

# http://127.0.0.1:8000/stocks/amzn/atrs?period=weekly


@app.get("/stocks/{ticker}/atrs")
def read_item(ticker: str, period: Union[str, None] = "weekly"):
    dbm = utils.get_dbm()
    prices = dbm.get_prices(ticker, period)
    dbm.close_connection()
    return get_atrs(prices)
