from datetime import datetime
import os

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

def execute_sql_file(connection, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    with connection as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
        conn.commit()

def execute_sql_query(connection, query: str, params: tuple = None) -> list:
    with connection as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(query, params)
            results = curs.fetchall()

    return results

def none_to_missing(obj) -> float:
    if obj is None:
        return -0.001
    return obj

def get_today() -> str:
    """ Return today's date string """
    return datetime.today().strftime("%Y-%m-%d")