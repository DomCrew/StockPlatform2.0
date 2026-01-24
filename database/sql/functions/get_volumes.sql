DROP FUNCTION IF EXISTS stockplatform.get_volumes;

CREATE FUNCTION stockplatform.get_volumes (
    p_stock_id INTEGER,
    p_period TEXT
)
RETURNS TABLE (
    datetime TIMESTAMP,
    volume_q BIGINT
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
            date_time, volume::BIGINT
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
            (SUM(volume  ORDER BY date_time ASC)) AS volume
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