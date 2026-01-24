import { useEffect, useState } from "react";
import { getLatestPrice } from "../services/api";

export default function LatestPrice({ ticker }) {
  const [latestPrice, setLatestPrice] = useState(null);

  useEffect(() => {
    async function fetchPrice() {
      const price = await getLatestPrice(ticker);
      setLatestPrice(price);
    }

    fetchPrice();
  }, [ticker]);

  if (latestPrice == null) return <h3>Fetching ...</h3>;

  return <h3>${latestPrice.toFixed(2)}</h3>;
}