These are the relations and their columns in the database:

stockplatform.stocks:
    stock_id SERIAL
    ticker VARCHAR(6)
    long_name VARCHAR(50)
    description TEXT
    sector VARCHAR(50)
    industry VARCHAR(50)
    full_time_employees INTEGER
    exchange VARCHAR(10)
    currency VARCHAR(5)
    country VARCHAR(20)
    last_updated TIMESTAMP

stockplatform.stocks_daily
    stock_daily_id SERIAL
    stock_id INTEGER
    date_time TIMESTAMP
    trailing_pe FLOAT
    forward_pe FLOAT
    trailing_peg_ratio FLOAT
    beta FLOAT
    market_cap BIGINT
    enterprise_value BIGINT
    price_to_sales_trailing_12m FLOAT
    price_to_book FLOAT
    enterprise_to_revenue FLOAT
    enterprise_to_ebitda FLOAT
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id)

stocks_daily is populated daily.

stockplatform.history:
    history_id SERIAL
    stock_id INTEGER
    date_time TIMESTAMP
    open FLOAT
    close FLOAT
    low FLOAT
    high FLOAT
    volume INTEGER
    dividends FLOAT
    stock_splits FLOAT
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id)

history is updated hourly.

stockplatform.articles:
    article_id SERIAL
    date_time TIMESTAMP
    title TEXT UNIQUE
    summary TEXT
    link TEXT UNIQUE
    sa_label VARCHAR(10)
    sa_score FLOAT

articles are updated daily.

stockplatform.cash_flows:
    cash_flow_id SERIAL
    stock_id INTEGER
    date_time TIMESTAMP
    free_cash_flow FLOAT
    operating_cash_flow FLOAT
    capex FLOAT
    net_income FLOAT
    stock_based_comp FLOAT
    depreciation_amortization FLOAT
    change_working_capital FLOAT
    dividends_paid FLOAT
    share_buybacks FLOAT
    share_issuance FLOAT
    debt_issuance FLOAT
    debt_repayment FLOAT
    end_cash_position FLOAT
    changes_in_cash FLOAT
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id)

cash_flows are updated yearly.

stockplatform.income_statements:
    income_statement_id SERIAL
    stock_id BIGINT
    date_time TIMESTAMP
    total_revenue FLOAT
    cost_of_revenue FLOAT
    gross_profit FLOAT
    operating_expense FLOAT
    research_and_development FLOAT
    selling_general_and_administration FLOAT
    operating_income FLOAT
    ebit FLOAT
    ebitda FLOAT
    interest_expense FLOAT
    interest_income FLOAT
    pretax_income FLOAT
    tax_provision FLOAT
    net_income FLOAT
    diluted_eps FLOAT
    diluted_average_shares BIGINT
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id)

income_statements are updated yearly.

stockplatform.balance_sheets:
    balance_sheet_id SERIAL
    stock_id INT
    date_time TIMESTAMP
    total_assets FLOAT
    total_liabilities_net_minority_interest FLOAT
    stockholders_equity FLOAT
    current_assets FLOAT
    current_liabilities FLOAT
    cash_and_cash_equivalents FLOAT
    receivables FLOAT
    inventory FLOAT
    total_debt FLOAT
    net_debt FLOAT
    long_term_debt FLOAT
    current_debt FLOAT
    net_ppe FLOAT
    investments_and_advances FLOAT
    retained_earnings FLOAT
    common_stock_equity FLOAT
    shares_issued BIGINT
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id)

balance_sheets are updated yearly.