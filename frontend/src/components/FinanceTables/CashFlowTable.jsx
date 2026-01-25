import { useEffect, useState } from "react";
import { getCashFlows } from "../../services/api";

export default function CashFlowTable({ ticker }) {
  const [cashFlows, setCashFlows] = useState(null);

  useEffect(() => {
    async function fetchCashFlows() {
      const cashFlows = await getCashFlows(ticker);
      setCashFlows(cashFlows);
    }

    fetchCashFlows();
  }, [ticker]);

  if (cashFlows == null) return <h3>Fetching ...</h3>;

  return (
  <div class="table-card">
    <h2>Cash Flow</h2>
    <table>
      <thead>
        <tr>
          <th>Category</th>
          {cashFlows.map(cf => (
            <th key={cf.date_time}>
              {new Date(cf.date_time).getFullYear()}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {Object.keys(cashFlows[0])
          .filter(
            key =>
              !["cash_flow_id", "stock_id", "date_time"].includes(key)
          )
          .map(category => (
            <tr key={category}>
              <td>{category.replaceAll("_", " ")}</td>
              {cashFlows.map(cf => (
                <td key={cf.date_time}>
                  {cf[category] !== null
                    ? cf[category].toLocaleString()
                    : "—"}
                </td>
              ))}
            </tr>
          ))}
      </tbody>
    </table>
  </div>
);
}