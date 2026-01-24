import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getATRs } from "../services/api";

export default function ATRChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const atrs = await getATRs(ticker, period);
      const atrsData = atrs.map(p => ({
        x: new Date(p.date_time),
        y: [p.atr]
      }));

      setSeries([
        {
            name: "ATR",
            type: "line",
            data: atrsData
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
      type: "line",
      height: 200
    },
    xaxis: {
      type: "datetime"
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
      type="line"
      height={400}
    />
  </div>
);
}