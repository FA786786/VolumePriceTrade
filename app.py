import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# Title
st.title("📊 Indian Stock Screener: RSI + Volume Strategy")

# Stock List
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS"]

# Sidebar inputs
rsi_buy_threshold = st.sidebar.slider("RSI Buy Threshold", 50, 80, 60)
volume_ratio = st.sidebar.slider("Volume > x times average", 1.0, 3.0, 1.5)
interval = st.sidebar.selectbox("Interval", ["1d", "1h", "15m"])
period = st.sidebar.selectbox("Period", ["7d", "30d", "60d", "90d"], index=1)

# Function to fetch and process data
@st.cache_data
def fetch_data(ticker, interval, period):
    df = yf.download(ticker, interval=interval, period=period)
    if df.empty or len(df) < 20:
        return None  # Not enough data
    try:
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
        df["Vol_Avg"] = df["Volume"].rolling(20).mean()
    except Exception:
        return None
    return df

# Screen stocks
results = []

for stock in stocks:
    df = fetch_data(stock, interval, period)
    if df is None or df.empty or df["RSI"].isna().all():
        continue
    last = df.iloc[-1]
    if (
        last["RSI"] < rsi_buy_threshold
        and last["Volume"] > volume_ratio * last["Vol_Avg"]
    ):
        results.append({
            "Stock": stock.replace(".NS", ""),
            "RSI": round(last["RSI"], 2),
            "Volume": int(last["Volume"]),
            "Avg Volume": int(last["Vol_Avg"]),
            "Signal": "🔔 Buy"
        })

# Output
st.subheader("📈 Screener Results")
if results:
    st.dataframe(pd.DataFrame(results))
else:
    st.warning("No stocks matched the criteria.")
