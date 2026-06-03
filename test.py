from collection.finance import get_history, get_income_statement, get_info, get_cash_flow, get_balance_sheet, get_news
# from collection.sentiment_analysis import get_news_and_sentiment
from database.database import DatabaseManager
from dotenv import load_dotenv

TEST_TICKERS = ["amzn", "aapl", "dis", "jpm"]

def insert_test_data(dbm: DatabaseManager, ticker: str):
    info = get_info(ticker)
    dbm.insert_stock(ticker, info)
    info['ticker'] = ticker
    dbm.insert_stock_daily(info)

    history = get_history(ticker)
    dbm.insert_history(ticker, history)

def insert_sheets(dbm: DatabaseManager, ticker: str):
    cash_flows = get_cash_flow(ticker)
    dbm.insert_cash_flows(ticker, cash_flows)

    income_statement = get_income_statement(ticker)
    dbm.insert_income_statements(ticker, income_statement)

    balance_sheet = get_balance_sheet(ticker)
    dbm.insert_balance_sheets(ticker, balance_sheet)

if __name__ == "__main__":
    load_dotenv()
    dbm = DatabaseManager()
    dbm.reset_db()
    dbm.close_connection()
