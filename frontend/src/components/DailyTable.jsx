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
    <div>
      <p><strong>Trailing PE</strong> {daily[0].trailing_pe}</p>
      <p><strong>Forward PE</strong> {daily[0].forward_pe}</p>
      <p><strong>Trailing PEG Ratio</strong> {daily[0].trailing_peg_ratio}</p>
      <p><strong>Beta</strong> {daily[0].beta}</p>
      <p><strong>Market Cap</strong> {daily[0].market_cap}</p>
      <p><strong>Enterprise Value</strong> {daily[0].enterprise_value}</p>
      <p><strong>Price to Sales Trailing 12M</strong> {daily[0].price_to_sales_trailing_12m}</p>
      <p><strong>Price to Book</strong> {daily[0].price_to_book}</p>
      <p><strong>Enterprise to Revenue</strong> {daily[0].enterprise_to_revenue}</p>
      <p><strong>Enterprise to EBITDA</strong> {daily[0].enterprise_to_ebitda}</p>
    </div>
  );
}