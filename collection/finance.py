import yfinance as yf
import pandas as pd
import numpy as np
import math

def get_history(ticker: str) -> pd.DataFrame:
    """ Returns historical prices for a given ticker """
    history = yf.Ticker(ticker).history(interval="1h",period="2y")
    return history.reset_index()

def get_info(ticker: str) -> dict:
    """ Returns company info for a given ticker """
    return yf.Ticker(ticker).info

def get_latest_price(ticker: str) -> float:
    """ Returns current price of the stock """
    return round(yf.Ticker(ticker).fast_info["lastPrice"], 2)

def get_news(ticker: str, count: int) -> list:
    """ Returns latest news for a given ticker """
    news = yf.Ticker(ticker).get_news(count, "news")
    return [{
        "title": item["content"].get("title"),
        "summary": item["content"].get("summary"),
        "link": item["content"]["canonicalUrl"].get("url"),
        "date_time": item["content"].get("pubDate")
    } for item in news]

def get_balance_sheet(ticker: str) -> pd.DataFrame:
    """ Returns balance sheet for a given ticker """
    balance_sheet = yf.Ticker(ticker).balance_sheet
    rows_to_keep = {
        "Total Assets": "total_assets",
        "Total Liabilities Net Minority Interest": "total_liabilities_net_minority_interest",
        "Stockholders Equity": "stockholders_equity",
        "Current Assets": "current_assets",
        "Current Liabilities": "current_liabilities",
        "Cash And Cash Equivalents": "cash_and_cash_equivalents",
        "Receivables": "receivables",
        "Inventory": "inventory",
        "Total Debt": "total_debt",
        "Net Debt": "net_debt",
        "Long Term Debt": "long_term_debt",
        "Current Debt": "current_debt",
        "Net PPE": "net_ppe",
        "Investments And Advances": "investments_and_advances",
        "Retained Earnings": "retained_earnings",
        "Common Stock Equity": "common_stock_equity",
        "Shares Issued": "shares_issued"
    }
    balance_sheet = balance_sheet.loc[
        balance_sheet.index.intersection(rows_to_keep.keys())
    ].T.reset_index()


    new_columns = [rows_to_keep[row] for row in balance_sheet.columns[1:]]
    balance_sheet.columns = ["date_time"] + new_columns
    return balance_sheet

def get_income_statement(ticker: str) -> pd.DataFrame:
    """ Returns income statement for a given ticker """
    income_statement = yf.Ticker(ticker).income_stmt
    rows_to_keep = {
        "Total Revenue": "total_revenue",
        "Cost of Revenue": "cost_of_revenue",
        "Gross Profit": "gross_profit",
        "Operating Expense": "operating_expense",
        "Research Development": "research_and_development",
        "Selling General Administrative": "selling_general_and_administration",
        "Operating Income": "operating_income",
        "EBIT": "ebit",
        "EBITDA": "ebitda",
        "Interest Expense": "interest_expense",
        "Interest Income": "interest_income",
        "Pretax Income": "pretax_income",
        "Tax Provision": "tax_provision",
        "Net Income": "net_income",
        "Diluted EPS": "diluted_eps",
        "Diluted Average Shares": "diluted_average_shares"
    }

    income_statement = income_statement.loc[
        income_statement.index.intersection(rows_to_keep.keys())
    ].T.reset_index()

    new_columns = [rows_to_keep[row] for row in income_statement.columns[1:]]
    income_statement.columns = ["date_time"] + new_columns

    return income_statement

def get_cash_flow(ticker: str) -> pd.DataFrame:
    """ Returns cash flow statement for a given ticker """
    cash_flow = yf.Ticker(ticker).cashflow
    rows_to_keep = {
        "Free Cash Flow": "free_cash_flow",
        "Operating Cash Flow": "operating_cash_flow",
        "Capital Expenditure": "capex",
        "Net Income From Continuing Operations": "net_income",
        "Stock Based Compensation": "stock_based_comp",
        "Depreciation And Amortization": "depreciation_amortization",
        "Change In Working Capital": "change_working_capital",
        "Cash Dividends Paid": "dividends_paid",
        "Repurchase Of Capital Stock": "share_buybacks",
        "Issuance Of Capital Stock": "share_issuance",
        "Issuance Of Debt": "debt_issuance",
        "Repayment Of Debt": "debt_repayment",
        "End Cash Position": "end_cash_position",
        "Changes In Cash": "changes_in_cash"
    }

    cash_flow = cash_flow.loc[
        cash_flow.index.intersection(rows_to_keep.keys())
    ].T.reset_index()

    new_columns = [rows_to_keep[row] for row in cash_flow.columns[1:]]
    cash_flow.columns = ["date_time"] + new_columns
    return cash_flow

def get_smas(history_df: pd.DataFrame) -> pd.DataFrame:
    """ Returns simple moving averages of close prices """
    sma_df = pd.DataFrame({
        "date": history_df["datetime"],
        "sma20": history_df["close_p"].rolling(20).mean(),
        "sma50": history_df["close_p"].rolling(50).mean(),
        "sma100": history_df["close_p"].rolling(100).mean()
    })
    sma_df = sma_df.replace({np.nan: None})
    return sma_df.to_dict(orient="records")

def get_ccis(typical_prices: list) -> list:
    tp_df = pd.DataFrame(typical_prices)
    calc_df = pd.DataFrame({
        "date_time": tp_df["date_time"],
        "TP": tp_df["typical_price"],
        "20DaySMAofTP": tp_df["typical_price"].rolling(20).mean(),
        "20DayMeanDevofTP": tp_df["typical_price"].rolling(20).apply(
            lambda x: np.mean(np.abs(x - np.mean(x))), raw=True
        )
    })

    calc_df["CCI"] = (calc_df["TP"] - calc_df["20DaySMAofTP"]) / (0.015 * calc_df["20DayMeanDevofTP"])
    return calc_df.dropna().to_dict(orient="records")

def get_macds(history: list) -> list:
    cp_df = pd.DataFrame({
        "date_time": [item["datetime"] for item in history],
        "close": [item["close_p"] for item in history]
    })

    exp1 = cp_df["close"].ewm(span=12, adjust=False).mean()
    exp2 = cp_df["close"].ewm(span=26, adjust=False).mean()
    
    macd_df = pd.DataFrame({
        "date_time": cp_df["date_time"],
        "macd_line": exp1 - exp2
    })

    macd_df["signal_line"] = macd_df["macd_line"].ewm(span=9, adjust=False).mean()
    macd_df["histogram"] = macd_df["macd_line"] - macd_df["signal_line"]

    return macd_df.to_dict(orient="records")

def obv_map_function(row, prev_obv):
    if row["close_p"] > row["open_p"]:
        return prev_obv + row["volume_q"]
    elif row["close_p"] < row["open_p"]:
        return prev_obv - row["volume_q"]
    else:
        return prev_obv

def true_range_map_function(row, prev_close):
    high_low = row["high_p"] - row["low_p"]
    high_prev_close = abs(row["high_p"] - prev_close)
    low_prev_close = abs(row["low_p"] - prev_close)
    return max(high_low, high_prev_close, low_prev_close)

def get_obvs(history: list) -> list:
    obv_list = []
    prev_obv = 0
    for row in history:
        current_obv = obv_map_function(row, prev_obv)
        obv_list.append({
            "date_time": row["datetime"],
            "obv": current_obv
        })
        prev_obv = current_obv
    return obv_list

def get_atrs(prices: list) -> list:
    trs = [{
        "date_time": prices[0]["datetime"],
        "tr": prices[0]["high_p"] - prices[0]["low_p"]
    }]

    for i in range(1, len(prices)):
        tr = true_range_map_function(prices[i], prices[i-1]["close_p"])
        trs.append({
            "date_time": prices[i]["datetime"],
            "tr": tr
        })

    atrs = [{
        "date_time": trs[0]["date_time"],
        "atr": (sum([trs[i]["tr"] for i in range(14)]) / 14)
    }]
    for i, tr in enumerate(trs[1:]):
        prev_atr = atrs[i-1]["atr"]
        atr = ((prev_atr * 13) + tr["tr"]) / 14
        atrs.append({
            "date_time": tr["date_time"],
            "atr": atr
        })
    
    return atrs

if __name__ == "__main__":
    print(get_news("AAPL", 1))