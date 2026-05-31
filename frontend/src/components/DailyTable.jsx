import { useEffect, useState } from "react";
import { getStockDaily } from "../services/api";

export default function DailyTable({ ticker }) {
  const [daily, setDaily] = useState(null);

  useEffect(() => {
    async function fetchDaily() {
      const daily = await getStockDaily(ticker);
      setDaily(daily);
    }

    fetchDaily();
  }, [ticker]);

  if (daily == null) return <h3>Fetching ...</h3>;

  return (
    <div class="table-card">
      <p><strong>Trailing PE</strong> - {daily.trailing_pe}</p>
      <p><strong>Forward PE</strong> - {daily.forward_pe}</p>
      <p><strong>Trailing PEG Ratio</strong> - {daily.trailing_peg_ratio}</p>
      <p><strong>Beta</strong> - {daily.beta}</p>
      <p><strong>Market Cap</strong> - {daily.market_cap}</p>
      <p><strong>Enterprise Value</strong> - {daily.enterprise_value}</p>
      <p><strong>Price to Sales Trailing 12M</strong> - {daily.price_to_sales_trailing_12m}</p>
      <p><strong>Price to Book</strong> - {daily.price_to_book}</p>
      <p><strong>Enterprise to Revenue</strong> - {daily.enterprise_to_revenue}</p>
      <p><strong>Enterprise to EBITDA</strong> - {daily.enterprise_to_ebitda}</p>
    </div>
  );
}