import streamlit as st
import pandas as pd
import yfinance as yf
import ta

# --- Streamlit App Title ---
st.set_page_config(page_title="Indian Futures Stock Screener", layout="centered")
st.title("📈 Indian Futures Stock Screener")
st.caption("By FA786786 • Powered by yfinance + ta")

# --- UI Widgets ---
tickers = st.multiselect(
    "Select Stocks",
    ["RELIANCE.NS", "TCS.NS", "ICICIBANK.NS", "SBIN.NS", "HDFCBANK.NS", "LT.NS", "INFY.NS", "AXISBANK.NS"],
    default=["RELIANCE.NS"]
)

timeframe = st.selectbox("Timeframe", ["5m", "15m", "1h", "1d"])
period = st.selectbox("Period", ["5d", "7d", "30d", "60d"])

rsi_threshold = st.slider("RSI Threshold", 50, 80, 55)
volume_multiplier = st.slider("Volume Multiplier", 1.0, 3.0, 1.5)

# --- Screener Function ---
def screen_stock(ticker):
    try:
        df = yf.download(ticker, interval=timeframe, period=period, progress=False)

        if df.empty or len(df) < 50:
            return None

        df['EMA50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator().squeeze()
        df['EMA200'] = ta.trend.EMAIndicator(df['Close'], window=200).ema_indicator().squeeze()
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi().squeeze()
        df['VolumeSMA'] = df['Volume'].rolling(20).mean().squeeze()

        latest = df.iloc[-1]

        if (
            latest['Close'] > latest['EMA50'] > latest['EMA200']
            and latest['RSI'] > rsi_threshold
            and latest['Volume'] > volume_multiplier * latest['VolumeSMA']
        ):
            return {
                "Ticker": ticker,
                "Close": round(latest['Close'], 2),
                "RSI": round(latest['RSI'], 2),
                "Volume": int(latest['Volume']),
                "Volume Avg": int(latest['VolumeSMA'])
            }

    except Exception as e:
        st.warning(f"{ticker} error: {e}")
        return None

# --- Screener Execution ---
results = []

for ticker in tickers:
    data = screen_stock(ticker)
    if data:
        results.append(data)

# --- Display Results ---
st.subheader("📊 Screener Results")

if results:
    df_result = pd.DataFrame(results)
    st.dataframe(df_result)
else:
    st.info("No matching stocks found with current filters.")
