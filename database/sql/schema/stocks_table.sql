CREATE TABLE IF NOT EXISTS stockplatform.stocks(
    stock_id SERIAL PRIMARY KEY,
    ticker VARCHAR(6) UNIQUE NOT NULL,
    long_name VARCHAR(50),
    description TEXT,
    sector VARCHAR(50),
    industry VARCHAR(50),
    full_time_employees INTEGER,
    exchange VARCHAR(10),
    currency VARCHAR(5),
    country VARCHAR(20),
    last_updated TIMESTAMP
);

INSERT INTO stockplatform.stocks (ticker) VALUES ('amzn'),
('aapl'),
('jpm'),
('dis');
