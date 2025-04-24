import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Indian Futures Stock Screener", layout="wide")

st.title("📈 Indian Futures Stock Screener")
st.markdown("By FA786786 • Powered by yfinance + ta")

# User Inputs
tickers = st.multiselect("Select Stocks", options=["RELIANCE.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "HDFCBANK.NS"], default=["RELIANCE.NS"])
timeframe = st.selectbox("Timeframe", options=["1m", "5m", "15m", "1h", "1d"], index=2)
period = st.selectbox("Period", options=["1d", "5d", "1mo", "3mo", "6mo", "1y"], index=1)
rsi_thresh = st.slider("RSI Threshold", 50, 80, 55)
volume_multiplier = st.slider("Volume Multiplier", 1.0, 3.0, 1.5, step=0.1)

st.divider()

results = []

for ticker in tickers:
    try:
        df = yf.download(ticker, period=period, interval=timeframe)
        if df.empty or len(df) < 50:
            continue

        # Fix: Use squeeze() to ensure 1D series
        df['EMA50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator().squeeze()
        df['EMA200'] = ta.trend.EMAIndicator(df['Close'], window=200).ema_indicator().squeeze()
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi().squeeze()
        df['VolumeSMA'] = df['Volume'].rolling(20).mean()

        latest = df.iloc[-1]

        if latest['RSI'] > rsi_thresh and latest['Volume'] > volume_multiplier * latest['VolumeSMA']:
            results.append(ticker)
    except Exception as e:
        st.warning(f"{ticker} error: {e}")

# Display results
st.subheader("📊 Screener Results")
if results:
    st.success("Matching stocks found:")
    for r in results:
        st.write(f"✅ {r}")
else:
    st.info("No matching stocks found with current filters.")
