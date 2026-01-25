import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getOBVs } from "../../services/api";
import { baseChartOptions, chartHeight } from "./ChartDefaults";

export default function OBVChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const obv = await getOBVs(ticker, period);
      const obvLineData = obv.map(p => ({
        x: p.date_time,
        y: p.obv
      }));

      setSeries([
        {
            name: "OBV",
            type: "line",
            data: obvLineData,
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
      <h2>OBV CHART - {period}</h2>
      <Chart
        options={options}
        series={series}
        type="line"
        height={chartHeight}
      />
    </div>
  );
}