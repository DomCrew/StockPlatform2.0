import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import { getPrices, getSMAs } from "../../services/api";
import { baseChartOptions, chartHeight } from "./ChartDefaults";

export default function CandleChart({ ticker, period }) {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);

      // Fetch OHLC prices
      const prices = await getPrices(ticker, period);
      const candlestickData = prices.map(p => ({
        x: p.date,
        y: [p.open, p.high, p.low, p.close]
      }));

      // Fetch smas
      const smas = await getSMAs(ticker, period);
      const smas20Data = smas.map(p => ({
        x: p.date,
        y: p.sma20
      }));

      const smas50Data = smas.map(p => ({
        x: p.date,
        y: p.sma50
      }));

      const smas100Data = smas.map(p => ({
        x: p.date,
        y: p.sma100
      }));

      setSeries([
        {
            name: "Candlestick",
            type: "candlestick",
            data: candlestickData
        },
        {
            name: `SMA 20`,
            type: "line",
            data: smas20Data,
            color: 'var(--orange)',
            tooltip: { enabled: false }
        },
        {
            name: `SMA 50`,
            type: "line",
            data: smas50Data,
            color: 'var(--link-colour)',
            tooltip: { enabled: false }
        },
        {
            name: `SMA 100`,
            type: "line",
            data: smas100Data,
            color: 'var(--purple)',
            tooltip: { enabled: false }
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
      type: "candlestick",
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: 'var(--green)',
          downward: 'var(--pink)'
        }
      }
    },
    tooltip: {
      shared: true,
      intersect: false,
      custom: ({ series, seriesIndex, dataPointIndex, w }) => {
        const date = w.globals.labels[dataPointIndex];
        const o = w.globals.seriesCandleO[0][dataPointIndex];
        const h = w.globals.seriesCandleH[0][dataPointIndex];
        const l = w.globals.seriesCandleL[0][dataPointIndex];
        const c = w.globals.seriesCandleC[0][dataPointIndex];

        const sma20 = w.globals.series[1][dataPointIndex];
        const sma50 = w.globals.series[2][dataPointIndex];
        const sma100 = w.globals.series[3][dataPointIndex];

        return `
          <div style="background: var(--background-colour); color: var(--text-colour); padding: 4px; font-size: 11px; font-family: var(--font-family);">
            <div class="apexcharts-tooltip-title" style="padding: 0px; font-size: 11px;">
              <p>${new Date(date).toISOString()}</p>
            </div>
            <div>
              <p>Open: ${Intl.NumberFormat().format(o)}</p>
              <p>High: ${Intl.NumberFormat().format(h)}</p>
              <p>Low: ${Intl.NumberFormat().format(l)}<p>
              <p>Close: ${Intl.NumberFormat().format(c)}</p>
            </div>
            <div style="color: var(--orange);">
              <p>SMA20: ${Intl.NumberFormat().format(sma20)}</p>
              <p>SMA50: ${Intl.NumberFormat().format(sma50)}</p>
              <p>SMA100: ${Intl.NumberFormat().format(sma100)}</p>
            </div>
          </div>
        `;
      }
    }
  };

  if (loading) return <div>Loading chart...</div>;

  return (
    <div className="chart-card">
      <h2>Candle Chart - {period}</h2>
      <Chart
        options={options}
        series={series}
        type="candlestick"
        height={chartHeight}
      />
    </div>
  );
}