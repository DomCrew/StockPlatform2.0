import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getPrices, getSMAs } from "../services/api";

export default function StockChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      // Fetch OHLC prices
      const prices = await getPrices(ticker, period);
      const candlestickData = prices.map(p => ({
        x: new Date(p.date),
        y: [p.open, p.high, p.low, p.close]
      }));

      // Fetch smas
      const smas = await getSMAs(ticker, period);
      const smas20Data = smas.map(p => ({
        x: new Date(p.date),
        y: [p.sma20]
      }));

      const smas50Data = smas.map(p => ({
        x: new Date(p.date),
        y: [p.sma50]
      }));

      const smas100Data = smas.map(p => ({
        x: new Date(p.date),
        y: [p.sma100]
      }));

      setSeries([
        {
            name: "Candlestick",
            type: "candlestick",
            data: candlestickData
        },
        {
            name: `SMA 20`,
            type: "line",
            data: smas20Data
        },
        {
            name: `SMA 50`,
            type: "line",
            data: smas50Data
        },
        {
            name: `SMA 100`,
            type: "line",
            data: smas100Data
        }
      ]);

      setLoading(false);
    }

    fetchData();
  }, [ticker, period]);

  const options = {
    chart: {
      animations: {
        enabled: false
      },
      type: "candlestick",
      height: 400
    },
    xaxis: {
      type: "category"
    },
    yaxis: {
      tooltip: { enabled: true }
    },
    tooltip: {
      enabled: true
    }
  };

  if (loading) return <div>Loading chart...</div>;

  return (
  <div className="chart-card">
    <Chart
      options={options}
      series={series}
      type="candlestick"
      height={400}
    />
  </div>
);
}