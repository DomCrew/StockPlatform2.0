from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from database import DatabaseManager
from sentiment_analysis import get_news_and_sentiment
from finance import get_info
import utils


def daily_pipeline(ticker: str) -> str:
    dbm = DatabaseManager()
    try:
        articles = get_news_and_sentiment(ticker, 7)
        info = get_info(ticker)
        dbm.insert_articles(ticker, articles)
        dbm.insert_stock_daily(ticker, info)
        return f"{ticker} pipeline finished"
    finally:
        dbm.close_connection()


if __name__ == "__main__":
    load_dotenv()
    dbm = DatabaseManager()
    tickers = utils.make_get_request("stocks/")
    dbm.close_connection()

    print("Starting daily pipeline")

    with ThreadPoolExecutor(max_workers=4) as e:
        futures = [e.submit(daily_pipeline, t) for t in tickers]

        for future in as_completed(futures):
            print(future.result())
