import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(layout="wide")
st.title("📊 Volume, Price, Trade Screener")

# Filters
rsi_threshold = st.slider("RSI Threshold", 50, 80, 55)
volume_multiplier = st.slider("Volume Multiplier", 1.0, 3.0, 1.5)

# List of stocks to screen
nifty_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS"]

results = []

for ticker in nifty_stocks:
    try:
        df = yf.download(ticker, period="6mo", interval="1d")
        if df.empty:
            continue

        df.dropna(inplace=True)

        # Calculate indicators
        df['EMA50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator().squeeze()
        df['EMA200'] = ta.trend.EMAIndicator(df['Close'], window=200).ema_indicator().squeeze()
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi().squeeze()
        df['VolumeSMA'] = df['Volume'].rolling(window=20).mean()

        # Latest row
        latest = df.iloc[-1]

        # Conditions
        price_above_ema50 = latest['Close'] > latest['EMA50']
        price_above_ema200 = latest['Close'] > latest['EMA200']
        rsi_ok = latest['RSI'] > rsi_threshold
        volume_ok = latest['Volume'] > (latest['VolumeSMA'] * volume_multiplier)

        if all([price_above_ema50, price_above_ema200, rsi_ok, volume_ok]):
            results.append({
                "Ticker": ticker,
                "Close": round(latest['Close'], 2),
                "RSI": round(latest['RSI'], 2),
                "Volume": int(latest['Volume']),
                "VolumeSMA": int(latest['VolumeSMA']),
            })

    except Exception as e:
        st.warning(f"{ticker} error: {e}")

# Display results
st.markdown("## 📈 Screener Results")
if results:
    st.dataframe(pd.DataFrame(results))
else:
    st.info("No matching stocks found with current filters.")
