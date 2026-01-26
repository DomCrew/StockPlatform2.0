DROP FUNCTION IF EXISTS stockplatform.insert_stock;

CREATE OR REPLACE FUNCTION stockplatform.insert_stock (
    ticker_p TEXT,
    long_name_p TEXT,
    description_p TEXT,
    sector_p TEXT,
    industry_p TEXT,
    full_time_employees_p INTEGER,
    currency_p TEXT,
    exchange_p TEXT,
    country_p TEXT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO
    stockplatform.stocks (
        ticker,
        long_name,
        description,
        sector,
        industry,
        full_time_employees,
        currency,
        exchange,
        country,
        last_updated
    )
    VALUES (
        ticker_p,
        long_name_p,
        description_p,
        sector_p,
        industry_p,
        full_time_employees_p,
        currency_p,
        exchange_p,
        country_p,
        NOW()
    )
    ON CONFLICT (ticker)
    DO UPDATE SET
        long_name = EXCLUDED.long_name,
        description = EXCLUDED.description,
        sector = EXCLUDED.sector,
        industry = EXCLUDED.industry,
        full_time_employees = EXCLUDED.full_time_employees,
        currency = EXCLUDED.currency,
        exchange = EXCLUDED.exchange,
        country = EXCLUDED.country,
        last_updated = NOW();
END;
$$;