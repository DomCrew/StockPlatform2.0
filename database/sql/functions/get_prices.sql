DROP FUNCTION IF EXISTS stockplatform.get_prices;

CREATE FUNCTION stockplatform.get_prices (
    p_stock_id INTEGER,
    p_period TEXT
)
RETURNS TABLE (
    datetime TIMESTAMP,
    open_p FLOAT,
    close_p FLOAT,
    high_p FLOAT,
    low_p FLOAT
)
LANGUAGE plpgsql
AS $$
DECLARE
    start_date TIMESTAMP;
    end_date TIMESTAMP := now();
    date_bucket TEXT;
BEGIN
    IF p_period = 'intraday' THEN
        start_date := end_date - INTERVAL '1 month';
    ELSIF p_period = 'daily' THEN
        start_date := end_date - INTERVAL '1 year';
        date_bucket := 'day';
    ELSIF p_period = 'weekly' THEN
        start_date := end_date - INTERVAL '2 years';
        date_bucket := 'week';
    ELSIF p_period = 'monthly' THEN
        start_date := end_date - INTERVAL '2 years';
        date_bucket := 'month';
    END IF;

    IF p_period = 'intraday' THEN
        RETURN QUERY
        SELECT
            date_time, open, close, high, low
        FROM
            stockplatform.history
        WHERE
            stock_id = p_stock_id AND
            date_time >= start_date AND
            date_time <= end_date
        ORDER BY date_time;
    END IF;

    IF p_period != 'intraday' THEN
        RETURN QUERY
        SELECT
            date_trunc(date_bucket, date_time) AS date_time,
            (array_agg(open  ORDER BY date_time ASC))[1] AS open,
            (array_agg(close ORDER BY date_time DESC))[1] AS close,
            MAX(high) AS high,
            MIN(low)  AS low
        FROM
            stockplatform.history
        WHERE
            stock_id = p_stock_id AND
            date_time >= start_date AND
            date_time <= end_date
        GROUP BY
            date_trunc(date_bucket, date_time)
        ORDER BY
            date_time;
    END IF;

END;
$$;