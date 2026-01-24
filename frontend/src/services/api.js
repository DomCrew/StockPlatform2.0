const BASE_URL = "http://localhost:8000";

export async function getPrices(ticker, period) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/prices?period=${period}`
  );
  return res.json();
}

export async function getSMAs(ticker, period) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/smas?period=${period}`
  );
  return res.json();
}

export async function getVolumes(ticker, period) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/volumes?period=${period}`
  );
  return res.json();
}

export async function getCCIs(ticker, period) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/ccis?period=${period}`
  );
  return res.json();
}

export async function getMACD(ticker, period) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/macd?period=${period}`
  );
  return res.json();
}

export async function getLatestPrice(ticker) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/latestprice`
  );
  const data = await res.json()
  return data.latest_price;
}

export async function getStockInfo(ticker) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/info`
  );
  return res.json();
}

export async function getStockDaily(ticker) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/daily`
  );
  return res.json();
}

export async function getArticles(ticker, limit=10) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/articles?limit=${limit}`
  );
  const articles = await res.json();
  for (let i = 0; i < articles.length; i++) {
    articles[i].colour = articles[i].sa_label === "positive" ? "green" : (articles[i].sa_label === "negative" ? "red" : "orange");
  }
  return articles;
}

export async function getCashFlows(ticker) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/cashflows`
  );
  return res.json();
}

export async function getIncomeStatements(ticker) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/incomestatements`
  );
  return res.json();
}

export async function getBalanceSheets(ticker) {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/balancesheets`
  );
  return res.json();
}

export async function getOBVs(ticker, period="weekly") {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/obvs?period=${period}`
  );
  return res.json();
}

export async function getATRs(ticker, period="weekly") {
  const res = await fetch(
    `${BASE_URL}/stocks/${ticker}/atrs?period=${period}`
  );
  return res.json();
}