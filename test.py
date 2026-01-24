from collection.finance import get_history, get_income_statement, get_info, get_cash_flow, get_balance_sheet
from collection.sentiment_analysis import get_news_and_sentiment
from database.database import DatabaseManager
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    dbm = DatabaseManager()
    dbm.reset_db()

    info = get_info("amzn")
    dbm.insert_stock("amzn", info)
    dbm.insert_stock_daily("amzn", info)

    history = get_history("amzn")
    dbm.insert_history("amzn", history)

    info = get_info("aapl")
    dbm.insert_stock("aapl", info)
    dbm.insert_stock_daily("aapl", info)


    history = get_history("aapl")
    dbm.insert_history("aapl", history)

    articles = get_news_and_sentiment("amzn", 10)
    dbm.insert_articles("amzn", articles)

    articles = get_news_and_sentiment("aapl", 10)
    dbm.insert_articles("aapl", articles)

    cash_flows = get_cash_flow("amzn")
    dbm.insert_cash_flows("amzn", cash_flows)

    income_statement = get_income_statement("amzn")
    dbm.insert_income_statements("amzn", income_statement)

    balance_sheet = get_balance_sheet("amzn")
    dbm.insert_balance_sheets("amzn", balance_sheet)

    cash_flows = get_cash_flow("aapl")
    dbm.insert_cash_flows("aapl", cash_flows)

    income_statement = get_income_statement("aapl")
    dbm.insert_income_statements("aapl", income_statement)

    balance_sheet = get_balance_sheet("aapl")
    dbm.insert_balance_sheets("aapl", balance_sheet)

    dbm.close_connection()