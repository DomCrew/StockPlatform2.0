import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getVolumes } from "../../services/api";
import { baseChartOptions, chartHeight } from "./ChartDefaults";

export default function VolumeChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const volumes = await getVolumes(ticker, period);
      const volumesData = volumes.map(p => ({
        x: p.date,
        y: p.volume
      }));

      setSeries([
        {
            name: "Volume",
            type: "bar",
            data: volumesData,
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
      type: "bar"
    },
    dataLabels: {
      enabled: false
    }
  };

  if (loading) return <div>Loading chart...</div>;

  return (
    <div className="chart-card">
      <h2>Volume Chart - {period}</h2>
      <Chart
        options={options}
        series={series}
        type="bar"
        height={chartHeight}
      />
    </div>
  );
}