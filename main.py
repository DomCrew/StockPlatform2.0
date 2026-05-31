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


class HistoryInsert(BaseModel):
    ticker: str
    date_time: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float
    stock_splits: float


@app.post("/internal/insert_history/")
async def insert_history(history_data: HistoryInsert):
    history_df = pd.DataFrame({
        "date_time": [history_data.date_time],
        "open": [history_data.open],
        "high": [history_data.high],
        "low": [history_data.low],
        "close": [history_data.close],
        "volume": [history_data.volume],
        "dividends": [history_data.dividends],
        "stock_splits": [history_data.stock_splits]
    })
    dbm = utils.get_dbm()
    dbm.insert_history(history_data.ticker, history_df)
    dbm.close_connection()


class ArticleInsert(BaseModel):
    ticker: str
    date_time: str
    title: str
    summary: str
    link: str
    sa_label: str
    sa_score: float


@app.post("/internal/insert_article")
async def insert_article(article_data: ArticleInsert):
    article_dict = {
        "ticker": article_data.ticker,
        "date_time": article_data.date_time,
        "title": article_data.title,
        "summary": article_data.summary,
        "link": article_data.link,
        "sa_label": article_data.sa_label,
        "sa_score": article_data.sa_score
    }
    dbm = utils.get_dbm()
    dbm.insert_article(article_dict)
    dbm.close_connection()


class StockDailyInsert(BaseModel):
    ticker: str
    date_time: str
    trailing_pe: float
    forward_pe: float
    trailing_peg_ratio: float
    beta: float
    market_cap: int
    enterprise_value: int
    price_to_sales_trailing_12m: float
    price_to_book: float
    enterprise_to_revenue: float
    enterprise_to_ebitda: float

@app.post("/internal/insert_stock_daily")
async def insert_stock_daily(stock_daily_data: StockDailyInsert):
    stock_daily_dict = {
        "ticker": stock_daily_data.ticker,
        "date_time": stock_daily_data.date_time,
        "trailing_pe": stock_daily_data.float,
        "forward_pe": stock_daily_data.forward_pe,
        "trailing_peg_ratio": stock_daily_data.trailing_peg_ratio,
        "beta": stock_daily_data.beta,
        "market_cap": stock_daily_data.market_cap,
        "enterprise_value": stock_daily_data.enterprise_value,
        "price_to_sales_trailing_12m": stock_daily_data.price_to_sales_trailing_12m,
        "price_to_book": stock_daily_data.price_to_book,
        "enterprise_to_revenue": stock_daily_data.enterprise_to_revenue,
        "enterprise_to_ebitda": stock_daily_data.enterprise_to_ebitda,
    }
    dbm = utils.get_dbm()
    dbm.insert_article(stock_daily_dict)
    dbm.close_connection()


#cash flow, balance sheet, income statement inserts