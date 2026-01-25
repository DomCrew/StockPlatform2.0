import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getCCIs } from "../../services/api";
import { annotationStyle, baseChartOptions, chartHeight } from "./ChartDefaults";

export default function CCIChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      const ccis = await getCCIs(ticker, period);
      const ccisData = ccis.map(p => ({
        x: p.date_time,
        y: p.CCI
      }));

      setSeries([
        {
            name: "CCI",
            type: "line",
            data: ccisData,
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
    },
    annotations: {
      yaxis: [
        {
          y: 100,
          strokeDashArray: 4,
          borderColor: "var(--green)",
          label: {
            text: "+100",
            style: annotationStyle
          }
        },
        {
          y: -100,
          strokeDashArray: 4,
          borderColor: "var(--pink)",
          label: {
            text: "-100",
            style: annotationStyle
          }
        }
      ]
    }
  };

  if (loading) return <div>Loading chart...</div>;

  return (
    <div className="chart-card">
      <h2>CCI Chart - {period}</h2>
      <Chart
        options={options}
        series={series}
        type="line"
        height={chartHeight}
      />
    </div>
  );
}