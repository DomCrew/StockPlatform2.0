import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getMACD } from "../services/api";

export default function MACDChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const macd = await getMACD(ticker, period);
      const macdLineData = macd.map(p => ({
        x: new Date(p.date_time),
        y: [p.macd_line]
      }));

      const signalLineData = macd.map(p => ({
        x: new Date(p.date_time),
        y: [p.signal_line]
      }));

      const histogramData = macd.map(p => ({
        x: new Date(p.date_time),
        y: [p.histogram]
      }));

      setSeries([
        {
            name: "MACD Line",
            type: "line",
            data: macdLineData
        },
        {
            name: "Signal Line",
            type: "line",
            data: signalLineData
        },
        {
            name: "Histogram",
            type: "bar",
            data: histogramData
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