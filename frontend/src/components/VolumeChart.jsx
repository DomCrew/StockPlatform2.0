import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getVolumes } from "../services/api";

export default function VolumeChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const volumes = await getVolumes(ticker, period);
      const volumesData = volumes.map(p => ({
        x: new Date(p.date),
        y: [p.volume]
      }));

      setSeries([
        {
            name: "Volume",
            type: "bar",
            data: volumesData
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
      type: "bar",
      height: 400
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
      type="bar"
      height={400}
    />
  </div>
);
}