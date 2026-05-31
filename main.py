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
        "trailing_pe": stock_daily_data.trailing_pe,
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

class CashFlowInsert(BaseModel):
    ticker: str
    date_time: str
    free_cash_flow: int
    operating_cash_flow: int
    capex: int
    net_income: int
    stock_based_comp: int
    depreciation_amortization: int
    change_working_capital: int
    dividends_paid: int
    share_bybacks: int
    share_issuance: int
    debt_issuance: int
    debt_rapayment: int
    end_cash_position: int
    changes_in_cash: int

@app.post("/internal/insert_cash_flow")
async def insert_cash_flow(cash_flow_data: CashFlowInsert):
    cash_flow_dict = {
        "ticker": cash_flow_data.ticker,
        "date_time": cash_flow_data.date_time,
        "free_cash_flow": cash_flow_data.free_cash_flow,
        "operating_cash_flow": cash_flow_data.operating_cash_flow,
        "capex": cash_flow_data.capex,
        "net_income": cash_flow_data.net_income,
        "stock_based_comp": cash_flow_data.stock_based_comp,
        "depreciation_amortization": cash_flow_data.depreciation_amortization,
        "change_working_capital": cash_flow_data.change_working_capital,
        "dividends_paid": cash_flow_data.dividends_paid,
        "share_bybacks": cash_flow_data.share_bybacks,
        "share_issuance": cash_flow_data.share_issuance,
        "debt_issuance": cash_flow_data.debt_issuance,
        "debt_rapayment": cash_flow_data.debt_rapayment,
        "end_cash_position": cash_flow_data.end_cash_position,
        "changes_in_cash": cash_flow_data.changes_in_cash
    }
    dbm = utils.get_dbm()
    dbm.insert_cash_flow(cash_flow_dict)
    dbm.close_connection()

class IncomeStatementInsert(BaseModel):
    ticker: str
    date_time: str
    total_revenue: int
    cost_of_revenue: int
    gross_profit: int
    operating_expense: int
    research_and_development: int
    selling_general_and_administration: int
    operating_income: int
    ebit: int
    ebitda: int
    interest_expense: int
    interest_income: int
    pretax_income: int
    tax_provision: int
    net_income: int
    diluted_eps: float
    diluted_average_shares: int

@app.post("/internal/insert_income_statement")
async def insert_income_statement(income_statement_data: IncomeStatementInsert):
    income_statement_dict = {
        "ticker": income_statement_data.ticker,
        "date_time": income_statement_data.date_time,
        "total_revenue": income_statement_data.total_revenue,
        "cost_of_revenue": income_statement_data.cost_of_revenue,
        "gross_profit": income_statement_data.gross_profit,
        "operating_expense": income_statement_data.operating_expense,
        "research_and_development": income_statement_data.research_and_development,
        "selling_general_and_administration": income_statement_data.selling_general_and_administration,
        "operating_income": income_statement_data.operating_income,
        "ebit": income_statement_data.ebit,
        "ebitda": income_statement_data.ebitda,
        "interest_expense": income_statement_data.interest_expense,
        "interest_income": income_statement_data.interest_income,
        "pretax_income": income_statement_data.pretax_income,
        "tax_provision": income_statement_data.tax_provision,
        "net_income": income_statement_data.net_income,
        "diluted_eps": income_statement_data.diluted_eps,
        "diluted_average_shares": income_statement_data.diluted_average_shares
    }
    dbm = utils.get_dbm()
    dbm.insert_income_statement(income_statement_dict)
    dbm.close_connection()

class BalanceSheetInsert(BaseModel):
    ticker: str
    date_time: str
    total_assets: int
    total_liabilities_net_minority_interest: int
    stockholders_equity: int
    current_assets: int
    current_liabilities: int
    cash_and_cash_equivalents: int
    receivables: int
    inventory: int
    total_debt: int
    net_debt: int
    long_term_debt: int
    current_debt: int
    net_ppe: int
    investments_and_advances: int
    retained_earnings: int
    common_stock_equity: int
    shares_issued: int

@app.post("/internal/insert_balance_sheet")
async def insert_balance_sheet(balance_sheet_data: BalanceSheetInsert):
    balance_sheet_dict = {
        "ticker": balance_sheet_data.ticker,
        "date_time": balance_sheet_data.date_time,
        "total_assets": balance_sheet_data.total_assets,
        "total_liabilities_net_minority_interest": balance_sheet_data.total_liabilities_net_minority_interest,
        "stockholders_equity": balance_sheet_data.stockholders_equity,
        "current_assets": balance_sheet_data.current_assets,
        "current_liabilities": balance_sheet_data.current_liabilities,
        "cash_and_cash_equivalents": balance_sheet_data.cash_and_cash_equivalents,
        "receivables": balance_sheet_data.receivables,
        "inventory": balance_sheet_data.inventory,
        "total_debt": balance_sheet_data.total_debt,
        "net_debt": balance_sheet_data.net_debt,
        "long_term_debt": balance_sheet_data.long_term_debt,
        "current_debt": balance_sheet_data.current_debt,
        "net_ppe": balance_sheet_data.net_ppe,
        "investments_and_advances": balance_sheet_data.investments_and_advances,
        "retained_earnings": balance_sheet_data.retained_earnings,
        "common_stock_equity": balance_sheet_data.common_stock_equity,
        "shares_issued": balance_sheet_data.shares_issued
    }
    dbm = utils.get_dbm()
    dbm.insert_balance_sheet(balance_sheet_dict)
    dbm.close_connection()