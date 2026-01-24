import { useEffect, useState } from "react";
import { getStockInfo } from "../services/api";

export default function InfoTable({ ticker }) {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    async function fetchInfo() {
      const info = await getStockInfo(ticker);
      setInfo(info);
    }

    fetchInfo();
  }, [ticker]);

  if (info == null) return <h3>Fetching ...</h3>;

  return (
    <div>
      <p><strong>Long Name:</strong> {info.long_name}</p>
      <p><strong>Description:</strong> {info.description}</p>
      <p><strong>Sector:</strong> {info.sector}</p>
      <p><strong>Industry:</strong> {info.industry}</p>
      <p><strong>Full Time Employees:</strong> {info.full_time_employees}</p>
      <p><strong>Currency:</strong> {info.currency}</p>
      <p><strong>Exchange:</strong> {info.exchange}</p>
      <p><strong>Country:</strong> {info.country}</p>
    </div>
  );
}