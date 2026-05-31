DROP FUNCTION  IF EXISTS stockplatform.insert_income_statement;

CREATE OR REPLACE FUNCTION stockplatform.insert_income_statement (
    stock_id_p INTEGER,
    date_time_p TIMESTAMP,
    total_revenue_p FLOAT,
    cost_of_revenue_p FLOAT,
    gross_profit_p FLOAT,
    operating_expense_p FLOAT,
    research_and_development_p FLOAT,
    selling_general_and_administration_p FLOAT,
    operating_income_p FLOAT,
    ebit_p FLOAT,
    ebitda_p FLOAT,
    interest_expense_p FLOAT,
    interest_income_p FLOAT,
    pretax_income_p FLOAT,
    tax_provision_p FLOAT,
    net_income_p FLOAT,
    diluted_eps_p FLOAT,
    diluted_average_shares_p FLOAT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO stockplatform.income_statements (
        stock_id,
        date_time,
        total_revenue,
        cost_of_revenue,
        gross_profit,
        operating_expense,
        research_and_development,
        selling_general_and_administration,
        operating_income,
        ebit,
        ebitda,
        interest_expense,
        interest_income,
        pretax_income,
        tax_provision,
        net_income,
        diluted_eps,
        diluted_average_shares
    )
    VALUES (
        stock_id_p,
        date_time_p,
        total_revenue_p,
        cost_of_revenue_p,
        gross_profit_p,
        operating_expense_p,
        research_and_development_p,
        selling_general_and_administration_p,
        operating_income_p,
        ebit_p,
        ebitda_p,
        interest_expense_p,
        interest_income_p,
        pretax_income_p,
        tax_provision_p,
        net_income_p,
        diluted_eps_p,
        diluted_average_shares_p
    );
END;
$$;