import { useState } from "react";
import StockChart from "./components/StockChart";
import VolumeChart from "./components/VolumeChart";
import TickerSearch from "./components/TickerSearch";
import LatestPrice from "./components/LatestPrice";
import InfoTable from "./components/InfoTable";
import DailyTable from "./components/DailyTable";
import ArticlesTable from "./components/ArticlesTable";
import CashFlowTable from "./components/CashFlowTable";
import IncomeStatementTable from "./components/IncomeStatementTable";
import BalanceSheetTable from "./components/BalanceSheetTable";
import CCIChart from "./components/CCIChart";
import MACDChart from "./components/MACDChart";
import OBVChart from "./components/OBVChart";
import ATRChart from "./components/ATRChart";

export default function App() {
  const [ticker, setTicker] = useState("amzn");
  const [period, setPeriod] = useState("daily");
  const [chart, setChart] = useState("stock");
  const [financeTab, setFinanceTab] = useState("cash_flow");

  return (
    <div className="app-container">
      <h1>StockPlatform2 - {ticker}</h1>
      <LatestPrice ticker={ticker} />

      <TickerSearch onSubmit={setTicker} />
      <button onClick={() => setPeriod("intraday")}>
        Intraday
      </button>
      <button onClick={() => setPeriod("daily")}>
        Daily
      </button>
      <button onClick={() => setPeriod("weekly")}>
        Weekly
      </button>
      <button onClick={() => setPeriod("monthly")}>
        Monthly
      </button>

      <button onClick={() => setChart("stock")}>
        Candlestick Chart
      </button>
      <button onClick={() => setChart("volume")}>
        Volume Chart
      </button>
      <button onClick={() => setChart("macd")}>
        MACD Chart
      </button>
      <button onClick={() => setChart("obv")}>
        OBV Chart
      </button>
      <button onClick={() => setChart("atr")}>
        ATR Chart
      </button>
      <button onClick={() => setChart("cci")}>
        CCI Chart
      </button>

      {chart === "stock" && (
        <StockChart
          ticker={ticker}
          period={period}
        />
      )}
      {chart === "volume" && (
        <VolumeChart
          ticker={ticker}
          period={period}
        />
      )}
      {chart === "macd" && (
        <MACDChart
          ticker={ticker}
          period={period}
        />
      )}
      {chart === "obv" && (
        <OBVChart
          ticker={ticker}
          period={period}
        />
      )}
      {chart === "atr" && (
        <ATRChart
          ticker={ticker}
          period={period}
        />
      )}
      {chart === "cci" && (
        <CCIChart
          ticker={ticker}
          period={period}
        />
      )}

      <InfoTable
        ticker={ticker}
      />

      <DailyTable
        ticker={ticker}
      />

      <ArticlesTable
        ticker={ticker}
      />

      <button onClick={() => setFinanceTab("cash_flow")}>
        Cash Flow
      </button>
      <button onClick={() => setFinanceTab("income_statement")}>
        Income Statement
      </button>
      <button onClick={() => setFinanceTab("balance_sheet")}>
        Balance Sheet
      </button>


      {financeTab === "cash_flow" && (
        <CashFlowTable
          ticker={ticker}
        />
      )}
      {financeTab === "income_statement" && (
        <IncomeStatementTable
          ticker={ticker}
        />
      )}
      {financeTab === "balance_sheet" && (
        <BalanceSheetTable
          ticker={ticker}
        />
      )}
    </div>
  );
}
