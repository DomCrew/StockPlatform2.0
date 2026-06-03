from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from database.database import DatabaseManager
from sentiment_analysis import get_news_and_sentiment
from finance import get_info, get_news
import collection_utils


def daily_pipeline(ticker: str) -> str:
    dbm = DatabaseManager()
    try:
        news = get_news(ticker, 5)
        #news = get_news_and_sentiment(news)
        #remove late
        for article in news:
            article["sa_label"] = "Positive"
            article["sa_score"] = 0.5
        info = get_info(ticker)
        dbm.insert_stock_daily(info)
        dbm.insert_articles(ticker, news)
        return f"{ticker} pipeline finished"
    finally:
        dbm.close_connection()


if __name__ == "__main__":
    load_dotenv()
    #tickers = collection_utils.make_get_request("stocks/")
    tickers = ["amzn", "aapl", "dis", "jpm"]

    print("Starting daily pipeline")

    for ticker in tickers:
        daily_pipeline(ticker)

    # with ThreadPoolExecutor(max_workers=len(tickers)) as executor:
    #     for result in executor.map(daily_pipeline, tickers):
    #         print(result)
