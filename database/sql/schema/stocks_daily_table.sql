CREATE TABLE IF NOT EXISTS stockplatform.stocks_daily(
    stock_daily_id SERIAL PRIMARY KEY,
    stock_id INTEGER NOT NULL,
    date_time TIMESTAMP NOT NULL,
    trailing_pe FLOAT,
    forward_pe FLOAT,
    trailing_peg_ratio FLOAT,
    beta FLOAT,
    market_cap BIGINT,
    enterprise_value BIGINT,
    price_to_sales_trailing_12m FLOAT,
    price_to_book FLOAT,
    enterprise_to_revenue FLOAT,
    enterprise_to_ebitda FLOAT,
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id)
);