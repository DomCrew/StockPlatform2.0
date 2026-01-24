import { useEffect, useState } from "react";
import { getBalanceSheets } from "../services/api";

export default function BalanceSheetTable({ ticker }) {
  const [balanceSheets, setBalanceSheets] = useState(null);

  useEffect(() => {
    async function fetchBalanceSheets() {
      const balanceSheets = await getBalanceSheets(ticker);
      setBalanceSheets(balanceSheets);
    }

    fetchBalanceSheets();
  }, [ticker]);

  if (balanceSheets == null) return <h3>Fetching ...</h3>;

  return (
  <div>
    <table>
      <thead>
        <tr>
          <th>Category</th>
          {balanceSheets.map(bs => (
            <th key={bs.date_time}>
              {new Date(bs.date_time).getFullYear()}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {Object.keys(balanceSheets[0])
          .filter(
            key =>
              !["balance_sheet_id", "stock_id", "date_time"].includes(key)
          )
          .map(category => (
            <tr key={category}>
              <td>{category.replaceAll("_", " ")}</td>
              {balanceSheets.map(bs => (
                <td key={bs.date_time}>
                  {bs[category] !== null
                    ? bs[category].toLocaleString()
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