import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getMACD } from "../../services/api";
import { baseChartOptions, chartHeight } from "./ChartDefaults";

export default function MACDChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const macd = await getMACD(ticker, period);
      const macdLineData = macd.map(p => ({
        x: p.date_time,
        y: p.macd_line
      }));

      const signalLineData = macd.map(p => ({
        x: p.date_time,
        y: p.signal_line
      }));

      const histogramData = macd.map(p => ({
        x: p.date_time,
        y: p.histogram
      }));

      setSeries([
        {
            name: "MACD Line",
            type: "line",
            data: macdLineData,
            color: "var(--orange)"
        },
        {
            name: "Signal Line",
            type: "line",
            data: signalLineData,
            color: "var(--pink)"
        },
        {
            name: "Histogram",
            type: "bar",
            data: histogramData,
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
      <h2>MACD Chart - {period}</h2>
      <Chart
        options={options}
        series={series}
        type="line"
        height={chartHeight}
      />
    </div>
  );
}