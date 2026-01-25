import { useState } from "react";
import CandleChart from "./components/Charts/CandleChart";
import VolumeChart from "./components/Charts/VolumeChart";
import TickerSearch from "./components/TickerSearch";
import LatestPrice from "./components/LatestPrice";
import InfoTable from "./components/InfoTable";
import DailyTable from "./components/DailyTable";
import ArticlesTable from "./components/ArticlesTable";
import CashFlowTable from "./components/FinanceTables/CashFlowTable";
import IncomeStatementTable from "./components/FinanceTables/IncomeStatementTable";
import BalanceSheetTable from "./components/FinanceTables/BalanceSheetTable";
import CCIChart from "./components/Charts/CCIChart";
import MACDChart from "./components/Charts/MACDChart";
import OBVChart from "./components/Charts/OBVChart";
import ATRChart from "./components/Charts/ATRChart";

export default function App() {
  const [ticker, setTicker] = useState("amzn");
  const [period, setPeriod] = useState("daily");
  const [chart, setChart] = useState("stock");
  const [financeTab, setFinanceTab] = useState("cash_flow");

  return (
    <div className="app-container">
      <div class="header-card">
        <div>
          <h1>StockPlatform2 - {ticker}</h1>
          <TickerSearch onSubmit={setTicker} />
        </div>
        <LatestPrice ticker={ticker} />
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", width: "100%"}}>
        <div>
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
        </div>

        <div>
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
        </div>
      </div>

      {chart === "stock" && (
        <CandleChart
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

      <DailyTable
        ticker={ticker}
      />

      <ArticlesTable
        ticker={ticker}
      />

      <InfoTable
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
