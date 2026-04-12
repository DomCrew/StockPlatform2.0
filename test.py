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

    for ticker in TEST_TICKERS:
        insert_test_data(dbm, ticker)

    # news = get_news("aapl", 10)
    # articles = get_news_and_sentiment("amzn", 10, news)
    # dbm.insert_articles("amzn", articles)

    # news = get_news("aapl", 10)
    # articles = get_news_and_sentiment("aapl", 10, news)
    # dbm.insert_articles("aapl", articles)

    a1 = {
        "ticker": "amzn",
        "title": "Test example headline",
        "summary": "Example Summary",
        "link": "https:www.example.co.uk",
        "date_time": "2023-12-12 10:11:12",
        "sa_label": "Positive",
        "sa_score": "0.3456789"
    }

    a2 = {
        "ticker": "aapl",
        "title": "Test example headline",
        "summary": "Example Summary",
        "link": "https:www.example.co.uk",
        "date_time": "2023-12-12 10:11:12",
        "sa_label": "Positive",
        "sa_score": "0.3456789"
    }

    a3 = {
        "ticker": "dis",
        "title": "Disney hires Hyunji",
        "summary": "Example Summary",
        "link": "https:www.example2.co.uk",
        "date_time": "2023-12-12 10:11:12",
        "sa_label": "Positive",
        "sa_score": "0.3456789"
    }

    a4 = {
        "ticker": "jpm",
        "title": "JPMorgan Chase reports earnings",
        "summary": "Example Summary",
        "link": "https:www.example3.co.uk",
        "date_time": "2023-12-12 10:11:12",
        "sa_label": "Positive",
        "sa_score": "0.3456789"
    }

    dbm.insert_article(a1)
    dbm.insert_article(a2)
    dbm.insert_article(a3)
    dbm.insert_article(a4)

    for ticker in TEST_TICKERS:
        insert_sheets(dbm, ticker)

    dbm.close_connection()
