import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("📈 Indian Stock Screener with Buy/Sell Alerts")

# Sidebar settings
st.sidebar.header("Filter Settings")
rsi_threshold = st.sidebar.slider("RSI Buy Threshold", 50, 80, 55)
volume_multiplier = st.sidebar.slider("Volume Multiplier", 1.0, 3.0, 1.5)
timeframe = st.sidebar.selectbox("Timeframe", ["1d", "1h", "15m"], index=0)
period_map = {"1d": "3mo", "1h": "30d", "15m": "5d"}
period = period_map[timeframe]

# List of tickers
tickers = {
    "RELIANCE.NS": "Reliance",
    "TCS.NS": "TCS",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "SBI",
    "AXISBANK.NS": "Axis Bank",
    "LT.NS": "L&T"
}

results = []

for symbol, name in tickers.items():
    try:
        df = yf.download(symbol, interval=timeframe, period=period)
        if df.empty or "Close" not in df.columns:
            continue

        close = df["Close"]
        volume = df["Volume"]

        df["EMA50"] = ta.trend.ema_indicator(close=close, window=50).ema_indicator()
        df["EMA200"] = ta.trend.ema_indicator(close=close, window=200).ema_indicator()
        df["RSI"] = ta.momentum.RSIIndicator(close=close, window=14).rsi()
        df["VolumeSMA"] = volume.rolling(window=20).mean()
        df.dropna(inplace=True)

        last = df.iloc[-1]

        is_buy = (
            last["Close"] > last["EMA50"] > last["EMA200"]
            and last["RSI"] > rsi_threshold
            and last["Volume"] > last["VolumeSMA"] * volume_multiplier
        )

        is_sell = (
            last["Close"] < last["EMA50"] < last["EMA200"]
            and last["RSI"] < 40
        )

        signal = "Buy 📈" if is_buy else "Sell 📉" if is_sell else ""

        if signal:
            results.append({
                "Stock": name,
                "Symbol": symbol,
                "Close": round(last["Close"], 2),
                "RSI": round(last["RSI"], 2),
                "Volume": int(last["Volume"]),
                "Signal": signal
            })

    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")

st.subheader("📋 Screener Results")
if results:
    df_result = pd.DataFrame(results)
    st.dataframe(df_result)
    st.download_button("Download Results as CSV", df_result.to_csv(index=False), "screener_results.csv")
else:
    st.info("No stocks matched the current filter criteria.")
