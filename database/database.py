import os

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

from database import database_utils


def normalize_value(value):
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if isinstance(value, (str, bytes)):
        if isinstance(value, bytes):
            value = value.decode('utf-8', errors='ignore')
        if value.strip().lower() in {"nat", "nan", "none", "null", "na", "n/a"}:
            return None
    return value


def clean_dict_values(d: dict) -> dict:
    return {key: normalize_value(value) for key, value in d.items()}


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
                              info.get("shortName", None),
                              info.get("longBusinessSummary", None),
                              info.get("sector", None),
                              info.get("industry", None),
                              info.get("fullTimeEmployees", None),
                              info.get("currency", None),
                              info.get("fullExchangeName", None),
                              info.get("country", None)))

        self.connection.commit()

    def insert_stock_daily(self, info: dict) -> None:
        stock_id = self.get_stock_id_from_ticker(info["ticker"])

        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_stock_daily(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (stock_id,
                              info.get('trailingPE', None),
                              info.get('forwardPE', None),
                              info.get('trailingPegRatio', None),
                              info.get('beta', None),
                              info.get('marketCap', None),
                              info.get('enterpriseValue', None),
                              info.get('priceToSalesTrailing12Months', None),
                              info.get('priceToBook', None),
                              info.get('enterpriseToRevenue', None),
                              info.get('enterpriseToEbitda', None)))

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

    def insert_article(self, article_dict: dict) -> None:
        stock_id = self.get_stock_id_from_ticker(article_dict["ticker"])

        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_article(%s, %s, %s, %s, %s, %s, %s)",
                             (stock_id,
                              article_dict.get("title", None),
                              article_dict.get("summary", None),
                              article_dict.get("link", None),
                              article_dict.get("date_time", None),
                              article_dict.get("sa_label", None),
                              article_dict.get("sa_score", None)))
        self.connection.commit()

    def insert_articles(self, ticker: str, articles: list) -> None:
        for article in articles:
            article["ticker"] = ticker
            self.insert_article(
                article
            )

    def insert_cash_flow(self, ticker: str, cash_flow_dict: dict) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)
        cash_flow_dict = clean_dict_values(cash_flow_dict)

        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_cash_flow(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (stock_id,
                              cash_flow_dict.get("date_time", None),
                              cash_flow_dict.get("free_cash_flow", None),
                              cash_flow_dict.get("operating_cash_flow", None),
                              cash_flow_dict.get("capex", None),
                              cash_flow_dict.get("net_income", None),
                              cash_flow_dict.get("stock_based_comp", None),
                              cash_flow_dict.get("depreciation_amortization", None),
                              cash_flow_dict.get("change_working_capital", None),
                              cash_flow_dict.get("dividends_paid", None),
                              cash_flow_dict.get("share_buybacks", None),
                              cash_flow_dict.get("share_issuance", None),
                              cash_flow_dict.get("debt_issuance", None),
                              cash_flow_dict.get("debt_repayment", None),
                              cash_flow_dict.get("end_cash_position", None),
                              cash_flow_dict.get("changes_in_cash", None)))
        self.connection.commit()

    def insert_cash_flows(self, ticker: str, cash_flow_df: pd.DataFrame) -> None:
        for _, row in cash_flow_df.iterrows():
            cash_flow_dict = row.to_dict()
            self.insert_cash_flow(ticker, cash_flow_dict)

    def insert_income_statement(self, ticker: str, income_statement_dict: dict) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)
        income_statement_dict = clean_dict_values(income_statement_dict)

        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_income_statement(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (stock_id,
                              income_statement_dict.get("date_time", None),
                              income_statement_dict.get("total_revenue", None),
                              income_statement_dict.get("cost_of_revenue", None),
                              income_statement_dict.get("gross_profit", None),
                              income_statement_dict.get("operating_expense", None),
                              income_statement_dict.get("research_and_development", None),
                              income_statement_dict.get("selling_general_and_administration", None),
                              income_statement_dict.get("operating_income", None),
                              income_statement_dict.get("ebit", None),
                              income_statement_dict.get("ebitda", None),
                              income_statement_dict.get("interest_expense", None),
                              income_statement_dict.get("interest_income", None),
                              income_statement_dict.get("pretax_income", None),
                              income_statement_dict.get("tax_provision", None),
                              income_statement_dict.get("net_income", None),
                              income_statement_dict.get("diluted_eps", None),
                              income_statement_dict.get("diluted_average_shares", None)))

        self.connection.commit()

    def insert_income_statements(self, ticker: str, income_statement_df: pd.DataFrame) -> None:
        for _, row in income_statement_df.iterrows():
            income_statement_dict = row.to_dict()
            self.insert_income_statement(ticker, income_statement_dict)

    def insert_balance_sheet(self, ticker: str, balance_sheet_dict: dict) -> None:
        stock_id = self.get_stock_id_from_ticker(ticker)
        balance_sheet_dict = clean_dict_values(balance_sheet_dict)

        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT * FROM stockplatform.insert_balance_sheet(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (stock_id,
                              balance_sheet_dict.get("date_time", None),
                              balance_sheet_dict.get("total_assets", None),
                              balance_sheet_dict.get("total_liabilities_net_minority_interest", None),
                              balance_sheet_dict.get("stockholders_equity", None),
                              balance_sheet_dict.get("current_assets", None),
                              balance_sheet_dict.get("current_liabilities", None),
                              balance_sheet_dict.get("cash_and_cash_equivalents", None),
                              balance_sheet_dict.get("receivables", None),
                              balance_sheet_dict.get("inventory", None),
                              balance_sheet_dict.get("total_debt", None),
                              balance_sheet_dict.get("net_debt", None),
                              balance_sheet_dict.get("long_term_debt", None),
                              balance_sheet_dict.get("current_debt", None),
                              balance_sheet_dict.get("net_ppe", None),
                              balance_sheet_dict.get("investments_and_advances", None),
                              balance_sheet_dict.get("retained_earnings", None),
                              balance_sheet_dict.get("common_stock_equity", None),
                              balance_sheet_dict.get("shares_issued", None)))

        self.connection.commit()

    def insert_balance_sheets(self, ticker: str, balance_sheet_df: pd.DataFrame) -> None:
        for _, row in balance_sheet_df.iterrows():
            balance_sheet_dict = row.to_dict()
            self.insert_balance_sheet(ticker, balance_sheet_dict)

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
        return database_utils.execute_sql_query(self.connection, sql_query, (stock_id,))[0]

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
