import { useEffect, useState } from "react";
import { getLatestPrice } from "../services/api";

export default function LatestPrice({ ticker }) {
  const [latestPrice, setLatestPrice] = useState(null);
  const [colour, setColour] = useState(null);
  const [time, setTime] = useState(null);
  const [percentChange, setPercentChange] = useState(null);
  const [actualChange, setActualChange] = useState(null);

  useEffect(() => {
    async function fetchPrice() {
      const price = await getLatestPrice(ticker);
      setLatestPrice(price.latest_price);
      setColour(price.colour);
      setTime(price.time);
      setPercentChange(price.diff.percentage);
      setActualChange(price.diff.actual);
    }

    fetchPrice();
  }, [ticker]);

  if (latestPrice == null) return <h3>Fetching ...</h3>;

  return (
    <div style={{ paddingRight: "4px", paddingBottom: "0px", paddingTop: "0px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", width: "100%", padding: "0px" }}>
        <p style={{ color: "var(--orange)", fontSize: "36px", padding: "0px" }}>${latestPrice.toFixed(2)}</p>
        <div style={{ textAlign: "center", padding: "0px" }}>
          <p style={{ color: colour, fontSize: "16px", padding: "0px" }}>{percentChange.toFixed(2)}%</p>
          <p style={{ color: colour, fontSize: "16px", padding: "0px" }}>{actualChange.toFixed(2)}</p>
        </div>
      </div>
      <p>{new Date(time).toISOString()}</p>
    </div>
  );
}