import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(layout="wide")
st.title("📊 Volume, Price, Trade Screener")

# --- Screener Settings ---
rsi_threshold = st.slider("RSI Threshold", 50, 80, 55)
volume_multiplier = st.slider("Volume Multiplier", 1.0, 3.0, 1.5)

# --- Stock List ---
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

# --- Screener Logic ---
for ticker, name in stock_list.items():
    try:
        df = yf.download(ticker, period="6mo", interval="1d")
        
        if df.empty or len(df) < 100:
            st.warning(f"{ticker} skipped: Not enough data.")
            continue

        df.dropna(inplace=True)

        # ✅ Use Series (1D), NOT DataFrame (2D)
        df['EMA50'] = ta.trend.ema_indicator(close=df['Close'], window=50)
        df['EMA200'] = ta.trend.ema_indicator(close=df['Close'], window=200)
        df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
        df['VolumeSMA'] = df['Volume'].rolling(window=20).mean()

        df.dropna(inplace=True)

        latest = df.iloc[-1]

        # Signal Conditions
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
                "Stock Name": name,
                "Ticker": ticker,
                "Close": round(latest['Close'], 2),
                "RSI": round(latest['RSI'], 2),
                "Volume": int(latest['Volume']),
                "Avg Volume": int(latest['VolumeSMA']),
                "Signal": signal
            })

    except Exception as e:
        st.error(f"{ticker} error: {e}")

# --- Display Results ---
st.markdown("## 📈 Screener Results")
if results:
    df_result = pd.DataFrame(results)
    st.dataframe(df_result)

    csv = df_result.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", data=csv, file_name="screener_results.csv", mime="text/csv")
else:
    st.info("No matching stocks found with current filters.")
