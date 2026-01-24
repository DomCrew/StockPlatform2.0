DROP FUNCTION IF EXISTS stockplatform.get_previous_close;

CREATE FUNCTION stockplatform.get_previous_close (
    p_stock_id INTEGER
)
RETURNS TABLE (
    datetime TIMESTAMP,
    close_p FLOAT
)
LANGUAGE plpgsql
AS $$
DECLARE
    today_date DATE := now()::DATE;
BEGIN
    RETURN QUERY
    SELECT
        date_time as datetime,
        close as close_p
    FROM
        stockplatform.history
    WHERE
        stock_id = p_stock_id AND
        date_time < today_date
    ORDER BY date_time DESC
    LIMIT 1;
END;
$$;