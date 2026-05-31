DROP FUNCTION IF EXISTS stockplatform.insert_cash_flow;

CREATE OR REPLACE FUNCTION stockplatform.insert_cash_flow (
    stock_id_p INTEGER,
    date_time_p TIMESTAMP,
    free_cash_flow_p FLOAT,
    operating_cash_flow_p FLOAT,
    capex_p FLOAT,
    net_income_p FLOAT,
    stock_based_comp_p FLOAT,
    depreciation_amortization_p FLOAT,
    change_working_capital_p FLOAT,
    dividends_paid_p FLOAT,
    share_buybacks_p FLOAT,
    share_issuance_p FLOAT,
    debt_issuance_p FLOAT,
    debt_repayment_p FLOAT,
    end_cash_position_p FLOAT,
    changes_in_cash_p FLOAT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO stockplatform.cash_flows (
        stock_id,
        date_time,
        free_cash_flow,
        operating_cash_flow,
        capex,
        net_income,
        stock_based_comp,
        depreciation_amortization,
        change_working_capital,
        dividends_paid,
        share_buybacks,
        share_issuance,
        debt_issuance,
        debt_repayment,
        end_cash_position,
        changes_in_cash
    )
    VALUES (
        stock_id_p,
        date_time_p,
        free_cash_flow_p,
        operating_cash_flow_p,
        capex_p,
        net_income_p,
        stock_based_comp_p,
        depreciation_amortization_p,
        change_working_capital_p,
        dividends_paid_p,
        share_buybacks_p,
        share_issuance_p,
        debt_issuance_p,
        debt_repayment_p,
        end_cash_position_p,
        changes_in_cash_p
    );
END;
$$;