DROP FUNCTION IF EXISTS stockplatform.insert_article;

CREATE OR REPLACE FUNCTION stockplatform.insert_article(
    p_stock_id BIGINT,
    p_title TEXT,
    p_summary TEXT,
    p_link TEXT,
    p_date_time TIMESTAMP,
    p_sa_label VARCHAR(10),
    p_sa_score FLOAT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    v_article_id BIGINT;
BEGIN
    INSERT INTO stockplatform.articles (
        title,
        summary,
        link,
        date_time,
        sa_label,
        sa_score
    )
    VALUES (
        p_title,
        p_summary,
        p_link,
        p_date_time,
        p_sa_label,
        p_sa_score
    )
    ON CONFLICT (title) DO UPDATE
    SET link = EXCLUDED.link
    RETURNING article_id INTO v_article_id;

    INSERT INTO stockplatform.article_stock_assignments (
        stock_id,
        article_id
    )
    VALUES (
        p_stock_id,
        v_article_id
    );
END;
$$;