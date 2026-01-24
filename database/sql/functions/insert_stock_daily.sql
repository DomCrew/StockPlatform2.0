DROP FUNCTION IF EXISTS stockplatform.insert_stock_daily;

CREATE OR REPLACE FUNCTION stockplatform.insert_stock_daily (
    stock_id_p INTEGER,
    trailing_pe_p FLOAT,
    forward_pe_p FLOAT,
    trailing_peg_ratio_p FLOAT,
    beta_p FLOAT,
    market_cap_p BIGINT,
    enterprise_value_p BIGINT,
    price_to_sales_trailing_12m_p FLOAT,
    price_to_book_p FLOAT,
    enterprise_to_revenue_p FLOAT,
    enterprise_to_ebitda_p FLOAT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO
    stockplatform.stocks_daily (
        stock_id,
        date_time,
        trailing_pe,
        forward_pe,
        trailing_peg_ratio,
        beta,
        market_cap,
        enterprise_value,
        price_to_sales_trailing_12m,
        price_to_book,
        enterprise_to_revenue,
        enterprise_to_ebitda
    )
    VALUES (
        stock_id_p,
        NOW(),
        trailing_pe_p,
        forward_pe_p,
        trailing_peg_ratio_p,
        beta_p,
        market_cap_p,
        enterprise_value_p,
        price_to_sales_trailing_12m_p,
        price_to_book_p,
        enterprise_to_revenue_p,
        enterprise_to_ebitda_p
    );
END;
$$;