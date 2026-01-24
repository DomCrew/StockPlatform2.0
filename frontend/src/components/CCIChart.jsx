import React, { useState, useEffect, lazy } from "react";
import Chart from "react-apexcharts";
import { getCCIs } from "../services/api";

export default function CCIChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const ccis = await getCCIs(ticker, period);
      const ccisData = ccis.map(p => ({
        x: new Date(p.date_time),
        y: [p.CCI]
      }));

      setSeries([
        {
            name: "CCI",
            type: "line",
            data: ccisData
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
    },
    annotations: {
        yaxis: [
      {
        y: 100,
        strokeDashArray: 4,
        label: {
          text: "+100",
        }
      },
      {
        y: -100,
        strokeDashArray: 4,
        label: {
          text: "-100",
        }
      }
    ]
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