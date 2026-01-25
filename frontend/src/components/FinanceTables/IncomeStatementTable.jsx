import { useEffect, useState } from "react";
import { getIncomeStatements } from "../../services/api";

export default function IncomeStatementTable({ ticker }) {
  const [incomeStatements, setIncomeStatements] = useState(null);

  useEffect(() => {
    async function fetchIncomeStatements() {
      const incomeStatements = await getIncomeStatements(ticker);
      setIncomeStatements(incomeStatements);
    }

    fetchIncomeStatements();
  }, [ticker]);

  if (incomeStatements == null) return <h3>Fetching ...</h3>;

  return (
  <div class="table-card">
    <h2>Income Statement</h2>
    <table>
      <thead>
        <tr>
          <th>Category</th>
          {incomeStatements.map(is => (
            <th key={is.date_time}>
              {new Date(is.date_time).getFullYear()}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {Object.keys(incomeStatements[0])
          .filter(
            key =>
              !["income_statement_id", "stock_id", "date_time"].includes(key)
          )
          .map(category => (
            <tr key={category}>
              <td>{category.replaceAll("_", " ")}</td>
              {incomeStatements.map(is => (
                <td key={is.date_time}>
                  {is[category] !== null
                    ? is[category].toLocaleString()
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