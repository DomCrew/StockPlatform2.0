CREATE TABLE IF NOT EXISTS stockplatform.stocks(
    stock_id SERIAL PRIMARY KEY,
    ticker VARCHAR(4) UNIQUE NOT NULL,
    long_name VARCHAR(50),
    description TEXT,
    sector VARCHAR(20),
    industry VARCHAR(20),
    full_time_employees INTEGER,
    exchange VARCHAR(10),
    currency VARCHAR(5),
    country VARCHAR(20),
    last_updated TIMESTAMP
);