import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getOBVs } from "../services/api";

export default function OBVChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const obv = await getOBVs(ticker, period);
      const obvLineData = obv.map(p => ({
        x: new Date(p.date_time),
        y: [p.obv]
      }));

      setSeries([
        {
            name: "OBV",
            type: "line",
            data: obvLineData
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