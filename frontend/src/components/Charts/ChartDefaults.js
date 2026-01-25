export const annotationStyle = {
  color: "var(--orange)",
  background: "var(--background-colour)",
  fontSize: "11px",
  fontFamily: "var(--font-family)"
}

export const baseChartOptions = {
  grid: {
    show: true,
    borderColor: "var(--text-colour)",
    strokeDashArray: 3
  },
  xaxis: {
    tooltip: {
      enabled: false
    },
    axisBorder: {
      color: "var(--text-colour)"
    },
    axisTicks: {
      show: false
    },
    type: "category",
    tickAmount: 12,
    labels: {
      rotate: 0,
      style: {
        colors: "var(--text-colour)",
        fontFamily: "var(--font-family)"
      },
      formatter: value => {
        const d = new Date(value);
        return d.toLocaleString("en-US", {
          month: "short",
          year: "2-digit"
        }).replace(" ", " '");
      }
    }
  },
  yaxis: {
    forceNiceScale: true,
    decimalsInFloat: 0,
    labels: {
      style: {
        colors: "var(--text-colour)",
        fontFamily: "var(--font-family)"
      }
    }
  },
  tooltip: {
    marker: { show: false },
    theme: false,
    shared: true,
    intersect: false,
    style: {
      fontFamily: "var(--font-family)",
      fontSize: "11px"
    },
    x: {
      formatter: value =>
        new Date(value).toISOString()
    },
    y: {
      formatter: value =>
        Intl.NumberFormat().format(value)
    },
    marker: {
      show: false
    },
    fillSeriesColor: false
  },
  legend: {
    position: "top",
    horizontalAlign: "left",
    fontSize: "11px",
    fontFamily: "var(--font-family)",
    labels: {
      colors: "var(--white)"
    },
    markers: {
      width: 12,
      height: 12,
      radius: 3,
      strokeColor: "var(--text-colour)",
      fillColors: undefined
    },
    itemMargin: {
      horizontal: 10,
      vertical: 5
    },
    onItemClick: {
      toggleDataSeries: true
    },
    onItemHover: {
      highlightDataSeries: true
    }
  }
};

export const chartHeight = 350;