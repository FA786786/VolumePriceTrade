import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import talib

st.set_page_config(page_title="Indian Stock Screener", layout="wide")

st.markdown("""
    <h1 style='text-align: center;'>📊 Indian Stock Screener with Buy/Sell Alerts</h1>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filter Settings")
rsi_buy_threshold = st.sidebar.slider("RSI Buy Threshold", 50, 80, 60)
volume_multiplier = st.sidebar.slider("Volume Multiplier", 1.0, 3.0, 1.5)
timeframe = st.sidebar.selectbox("Timeframe", ["1d", "1h", "15m"])

# List of stock tickers
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS"]

results = []

st.markdown("### Screener Results")

for ticker in tickers:
    try:
        df = yf.download(ticker, period="6mo", interval=timeframe)
        if df.empty:
            st.error(f"No data for {ticker}")
            continue

        df.dropna(inplace=True)

        close = df['Close'].values
        volume = df['Volume'].values

        # Flatten the arrays for indicators
        rsi = talib.RSI(close).flatten()
        avg_volume = pd.Series(volume).rolling(window=14).mean().values.flatten()

        latest_rsi = rsi[-1]
        latest_volume = volume[-1]
        avg_volume_14 = avg_volume[-1]

        signal = ""
        if latest_rsi < rsi_buy_threshold and latest_volume > avg_volume_14 * volume_multiplier:
            signal = "BUY"

        results.append({
            "Ticker": ticker,
            "RSI": round(latest_rsi, 2),
            "Volume": int(latest_volume),
            "Avg Volume (14d)": int(avg_volume_14),
            "Signal": signal
        })

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")

# Convert results to dataframe
results_df = pd.DataFrame(results)

if not results_df.empty:
    st.dataframe(results_df)
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Results as CSV", csv, "screener_results.csv", "text/csv")
else:
    st.info("No matching stocks found with current filters.")
