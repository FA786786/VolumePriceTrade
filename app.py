import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# Sample list of stocks
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

st.title("📊 Indian Stock Screener with Buy/Sell Alerts")

# Filters
rsi_threshold = st.sidebar.slider("RSI Buy Threshold", 50, 80, 60)
volume_multiplier = st.sidebar.slider("Volume Multiplier", 1.0, 3.0, 1.5)
timeframe = st.sidebar.selectbox("Timeframe", ["1d", "1h", "15m"])

def fetch_data(ticker, interval="1d"):
    try:
        df = yf.download(ticker, period="90d", interval=interval)
        if df.empty:
            return None
        df["RSI"] = ta.rsi(df["Close"], length=14)
        df["VolumeAvg"] = df["Volume"].rolling(window=20).mean()
        return df
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

results = []

for stock in stocks:
    df = fetch_data(stock, interval=timeframe)
    if df is None or df.empty:
        continue
    latest = df.iloc[-1]
    if latest["RSI"] < rsi_threshold and latest["Volume"] > volume_multiplier * latest["VolumeAvg"]:
        results.append({
            "Stock": stock,
            "RSI": round(latest["RSI"], 2),
            "Volume": int(latest["Volume"]),
            "VolumeAvg": int(latest["VolumeAvg"])
        })

# Display results
if results:
    st.subheader("📈 Screener Results")
    st.dataframe(pd.DataFrame(results))
else:
    st.info("No matching stocks found with current filters.")
