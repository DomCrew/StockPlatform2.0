import os

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

from database import database_utils


class DatabaseManager:
    def __init__(self):
        self.connection = database_utils.get_connection()

    def setup_db(self) -> None:
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/schema.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/stocks_table.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/stocks_daily_table.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/history_table.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/articles_table.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/article_stock_assignments_table.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/cash_flows_table.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/income_statements_table.sql')
        database_utils.execute_sql_file(
            self.connection, 'database/sql/schema/balance_sheets_table.sql')

        for path in os.listdir('database/sql/functions'):
            database_utils.execute_sql_file(
                self.connection, f'database/sql/functions/{path}')

    def reset_db(self) -> None:
        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("DROP SCHEMA IF EXISTS stockplatform CASCADE")

        self.setup_db()

    def insert_stock(self, ticker: str, info: dict) -> None:
        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_stock(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (ticker,
                              info["shortName"],
                              info["longBusinessSummary"],
                              info["sector"],
                              info["industry"],
                              info["fullTimeEmployees"],
                              info["currency"],
                              info["fullExchangeName"],
                              info["country"]))

        self.connection.commit()

    def insert_stock_daily(self, ticker: str, info: dict) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)

        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_stock_daily(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (stock_id,
                              info['trailingPE'],
                              info['forwardPE'],
                              info['trailingPegRatio'],
                              info['beta'],
                              info['marketCap'],
                              info['enterpriseValue'],
                              info['priceToSalesTrailing12Months'],
                              info['priceToBook'],
                              info['enterpriseToRevenue'],
                              info['enterpriseToEbitda']))
        self.connection.commit()

    def get_stock_id_from_ticker(self, ticker: str) -> str:
        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                    "SELECT stock_id FROM stockplatform.stocks WHERE ticker = %s", (ticker,))
                stock_id = curs.fetchall()[0]['stock_id']

        return stock_id

    def insert_history(self, ticker: str, history: pd.DataFrame) -> None:
        history.columns = ['date_time', 'open', 'high', 'low',
                           'close', 'volume', 'dividends', 'stock_splits']
        history['stock_id'] = self.get_stock_id_from_ticker(ticker)
        history.to_sql(
            name="history",
            schema="stockplatform",
            con=database_utils.get_engine(),
            if_exists="append",
            index=False,
            method="multi"
        )
        self.connection.commit()

    def insert_article(self, ticker: str, title: str, summary: str, link: str, datetime: str, sa_label: str, sa_score: float) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)

        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_article(%s, %s, %s, %s, %s, %s, %s)",
                             (stock_id, title, summary, link, datetime, sa_label, sa_score))
        self.connection.commit()

    def insert_articles(self, ticker: str, articles: list) -> None:
        for article in articles:
            self.insert_article(
                ticker,
                article['title'],
                article['summary'],
                article['link'],
                article['date_time'],
                article['sa_label'],
                article['sa_score']
            )

    def insert_cash_flows(self, ticker: str, cash_flow_df: pd.DataFrame) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)
        cash_flow_df['stock_id'] = stock_id
        cash_flow_df.to_sql(
            name="cash_flows",
            schema="stockplatform",
            con=database_utils.get_engine(),
            if_exists="append",
            index=False,
            method="multi"
        )
        self.connection.commit()

    def insert_income_statements(self, ticker: str, income_statement_df: pd.DataFrame) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)
        income_statement_df['stock_id'] = stock_id
        income_statement_df.to_sql(
            name="income_statements",
            schema="stockplatform",
            con=database_utils.get_engine(),
            if_exists="append",
            index=False,
            method="multi"
        )
        self.connection.commit()

    def insert_balance_sheets(self, ticker: str, balance_sheet_df: pd.DataFrame) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)
        balance_sheet_df['stock_id'] = stock_id
        balance_sheet_df.to_sql(
            name="balance_sheets",
            schema="stockplatform",
            con=database_utils.get_engine(),
            if_exists="append",
            index=False,
            method="multi"
        )
        self.connection.commit()

    def get_articles(self, ticker: str, limit: int) -> list:
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.get_articles(%s, %s)"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id, limit))

    def get_prices(self, ticker: str, period: str):
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.get_prices(%s, %s)"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id, period))

    def get_typical_prices(self, ticker: str, period: str):
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.get_typical_prices(%s, %s)"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id, period))

    def get_volumes(self, ticker: str, period: str):
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.get_volumes(%s, %s)"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id, period))

    def get_previous_close(self, ticker: str) -> float:
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.get_previous_close(%s)"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id,))[0]["close_p"]

    def get_info(self, ticker: str) -> dict:
        sql_query = "SELECT * FROM stockplatform.stocks WHERE ticker = %s"
        return database_utils.execute_sql_query(self.connection, sql_query, (ticker,))[0]

    def get_stock_daily(self, ticker: str) -> list:
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.stocks_daily WHERE stock_id = %s ORDER BY date_time DESC"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id,))

    def get_cash_flows(self, ticker: str) -> list:
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.cash_flows WHERE stock_id = %s ORDER BY date_time DESC LIMIT 4"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id,))

    def get_income_statements(self, ticker: str) -> list:
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.income_statements WHERE stock_id = %s ORDER BY date_time DESC LIMIT 4"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id,))

    def get_balance_sheets(self, ticker: str) -> list:
        stock_id = self.get_stock_id_from_ticker(ticker)
        sql_query = "SELECT * FROM stockplatform.balance_sheets WHERE stock_id = %s ORDER BY date_time DESC LIMIT 4"
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id,))

    def get_tickers(self) -> list:
        """Returns a list of all tickers in the stocks table"""
        sql_query = "SELECT ticker FROM stockplatform.stocks"
        return [row["ticker"] for row in database_utils.execute_sql_query(self.connection, sql_query, ())]

    def close_connection(self) -> None:
        self.connection.close()
