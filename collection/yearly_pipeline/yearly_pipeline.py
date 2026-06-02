"""Yearly pipeline script for data that rarely updates"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from database.database import DatabaseManager
from finance import get_info, get_income_statement, get_cash_flow, get_balance_sheet
import collection_utils


def yearly_pipeline(ticker: str) -> str:
    dbm = DatabaseManager()
    try:
        info = get_info(ticker)
        dbm.insert_stock(ticker, info)

        bs = get_balance_sheet(ticker)
        ist = get_income_statement(ticker)
        cf = get_cash_flow(ticker)
        dbm.insert_balance_sheets(ticker, bs)
        dbm.insert_income_statements(ticker, ist)
        dbm.insert_cash_flows(ticker, cf)

        return f"{ticker} pipeline finished"
    finally:
        dbm.close_connection()


if __name__ == "__main__":
    load_dotenv()
    dbm = DatabaseManager()
    tickers = collection_utils.make_get_request("stocks/")
    dbm.close_connection()

    print("Starting yearly pipeline")

    with ThreadPoolExecutor(max_workers=4) as e:
        futures = [e.submit(yearly_pipeline, t) for t in tickers]

        for future in as_completed(futures):
            print(future.result())
