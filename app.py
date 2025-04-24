import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.title("📊 Indian Stock Screener with Buy/Sell Alerts")

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

# Sidebar filters
rsi_threshold = st.sidebar.slider("RSI Buy Threshold", 50, 80, 60)
volume_multiplier = st.sidebar.slider("Volume Multiplier", 1.0, 3.0, 1.5)
timeframe = st.sidebar.selectbox("Timeframe", ["1d", "1h", "15m"])

@st.cache_data
def fetch_data(ticker, interval):
    df = yf.download(ticker, period="90d", interval=interval)
    if df.empty:
        return None
    df.ta.rsi(length=14, append=True)
    df["VolumeAvg"] = df["Volume"].rolling(window=20).mean()
    return df

results = []

for stock in stocks:
    df = fetch_data(stock, timeframe)
    if df is None or "RSI_14" not in df.columns:
        continue
    latest = df.iloc[-1]
    if latest["RSI_14"] < rsi_threshold and latest["Volume"] > volume_multiplier * latest["VolumeAvg"]:
        results.append({
            "Stock": stock,
            "RSI": round(latest["RSI_14"], 2),
            "Volume": int(latest["Volume"]),
            "VolumeAvg": int(latest["VolumeAvg"])
        })

if results:
    st.subheader("📈 Screener Results")
    st.dataframe(pd.DataFrame(results))
else:
    st.info("No matching stocks found with current filters.")
