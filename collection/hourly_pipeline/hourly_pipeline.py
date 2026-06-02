"""Hourly pipeline script for OHLC data, volume, dividends and stock splits"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from database.database import DatabaseManager
from finance import get_history
import collection_utils


def hourly_pipeline(ticker: str) -> str:
    dbm = DatabaseManager()
    try:
        history = get_history(ticker)
        dbm.insert_history(ticker, history)
        return f"{ticker} pipeline finished"
    finally:
        dbm.close_connection()


if __name__ == "__main__":
    load_dotenv()
    dbm = DatabaseManager()
    tickers = collection_utils.make_get_request("stocks/")
    dbm.close_connection()

    print("Starting hourly pipeline")

    with ThreadPoolExecutor(max_workers=4) as e:
        futures = [e.submit(hourly_pipeline, t) for t in tickers]

        for future in as_completed(futures):
            print(future.result())
