DROP FUNCTION IF EXISTS stockplatform.get_articles;

CREATE OR REPLACE FUNCTION stockplatform.get_articles(
    p_stock_id BIGINT,
    p_limit INTEGER
)
RETURNS TABLE (
    date_time TIMESTAMP,
    title TEXT,
    link TEXT,
    sa_label VARCHAR(10),
    sa_score FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.date_time,
        a.title,
        a.link,
        a.sa_label,
        a.sa_score
    FROM
        stockplatform.articles a
    JOIN
        stockplatform.article_stock_assignments asa ON a.article_id = asa.article_id
    WHERE
        asa.stock_id = p_stock_id
    ORDER BY
        a.date_time DESC
    LIMIT p_limit;
END;
$$;