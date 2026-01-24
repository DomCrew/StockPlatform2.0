CREATE TABLE IF NOT EXISTS stockplatform.history(
    history_id SERIAL PRIMARY KEY,
    stock_id INTEGER NOT NULL,
    date_time TIMESTAMP NOT NULL,
    open FLOAT NOT NULL,
    close FLOAT NOT NULL,
    low FLOAT NOT NULL,
    high FLOAT NOT NULL,
    volume INTEGER NOT NULL,
    dividends FLOAT,
    stock_splits FLOAT,
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id)
);