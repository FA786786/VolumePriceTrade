import streamlit as st
import yfinance as yf
import pandas as pd
import ta  # This is the 'ta' library, not pandas_ta

# Title
st.title("📊 Indian Stock Screener (RSI + Volume)")

# Stock List
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS"]

# Sidebar controls
rsi_buy_threshold = st.sidebar.slider("RSI Buy Threshold", 50, 80, 60)
volume_ratio = st.sidebar.slider("Volume > x times average", 1.0, 3.0, 1.5)
interval = st.sidebar.selectbox("Interval", ["1d", "1h", "15m"])
period = st.sidebar.selectbox("Period", ["7d", "30d", "60d", "90d"], index=1)

@st.cache_data
def fetch_data(ticker, interval, period):
    df = yf.download(ticker, interval=interval, period=period)
    if df.empty:
        return None
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    df["Vol_Avg"] = df["Volume"].rolling(20).mean()
    return df

results = []

for stock in stocks:
    df = fetch_data(stock, interval, period)
    if df is not None and not df.empty:
        last = df.iloc[-1]
        if (
            last["RSI"] < rsi_buy_threshold and
            last["Volume"] > volume_ratio * last["Vol_Avg"]
        ):
            results.append({
                "Stock": stock,
                "RSI": round(last["RSI"], 2),
                "Volume": int(last["Volume"]),
                "Avg Volume": int(last["Vol_Avg"])
            })

# Display results
if results:
    st.subheader("📈 Stocks Matching Criteria")
    st.dataframe(pd.DataFrame(results))
else:
    st.info("No stocks matched the current filters.")
