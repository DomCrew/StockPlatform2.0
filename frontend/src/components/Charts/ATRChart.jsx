import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getATRs } from "../../services/api";
import { baseChartOptions, chartHeight } from "./ChartDefaults";

export default function ATRChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const atrs = await getATRs(ticker, period);
      const atrsData = atrs.map(p => ({
        x: p.date_time,
        y: p.atr
      }));

      setSeries([
        {
            name: "ATR",
            type: "line",
            data: atrsData,
            color: "var(--link-colour)"
        }
      ]);

      setLoading(false);
    }

    fetchData();
  }, [ticker, period]);

  const options = {
    ...baseChartOptions,
    chart: {
      animations: {
        enabled: false
      },
      type: "line"
    }
  };

  if (loading) return <div>Loading chart...</div>;

  return (
    <div className="chart-card">
      <h2>ATR Chart - {period}</h2>
      <Chart
        options={options}
        series={series}
        type="line"
        height={chartHeight}
      />
    </div>
  );
}