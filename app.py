import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.title("📊 Volume, Price, Trade Screener")

rsi_threshold = st.slider("RSI Threshold", 50, 80, 55)
volume_multiplier = st.slider("Volume Multiplier", 1.0, 3.0, 1.5)

stock_list = {
    "RELIANCE.NS": "Reliance",
    "TCS.NS": "TCS",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "SBI",
    "AXISBANK.NS": "Axis Bank"
}

results = []

for ticker, name in stock_list.items():
    try:
        df = yf.download(ticker, period="6mo", interval="1d")
        if df.empty or len(df) < 100:
            continue

        df['EMA50'] = ta.trend.ema_indicator(close=df['Close'], window=50)
        df['EMA200'] = ta.trend.ema_indicator(close=df['Close'], window=200)
        df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
        df['VolumeSMA'] = df['Volume'].rolling(window=20).mean()
        df.dropna(inplace=True)

        latest = df.iloc[-1]

        buy = (
            latest['Close'] > latest['EMA50'] and
            latest['Close'] > latest['EMA200'] and
            latest['RSI'] > rsi_threshold and
            latest['Volume'] > latest['VolumeSMA'] * volume_multiplier
        )

        sell = (
            latest['Close'] < latest['EMA50'] and
            latest['Close'] < latest['EMA200'] and
            latest['RSI'] < 40
        )

        signal = "📈 Buy" if buy else "📉 Sell" if sell else None

        if signal:
            results.append({
                "Stock": name,
                "Symbol": ticker,
                "Close": round(latest['Close'], 2),
                "RSI": round(latest['RSI'], 2),
                "Volume": int(latest['Volume']),
                "Signal": signal
            })

    except Exception as e:
        st.error(f"{ticker} error: {e}")

st.markdown("## 📊 Screener Results")

if results:
    df_result = pd.DataFrame(results)
    st.dataframe(df_result)

    csv = df_result.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="screener_results.csv", mime="text/csv")
else:
    st.info("No matching stocks found with current filters.")
