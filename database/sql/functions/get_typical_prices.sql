CREATE OR REPLACE FUNCTION stockplatform.get_typical_prices(
    p_stock_id INTEGER,
    p_period TEXT
)
RETURNS TABLE (
    date_time TIMESTAMP,
    typical_price FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        h.datetime,
        (h.high_p + h.low_p + h.close_p) / 3 AS typical_price
    FROM
        (SELECT * FROM stockplatform.get_prices(p_stock_id, p_period)) AS h
    ORDER BY
        h.datetime;
END;
$$;