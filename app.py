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
stock_list = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "State Bank of India",
    "AXISBANK.NS": "Axis Bank"
}

results = []

for ticker, name in stock_list.items():
    try:
        df = yf.download(ticker, period="6mo", interval="1d")
        if df.empty or len(df) < 200:
            continue

        df.dropna(inplace=True)

        # Indicators
        df['EMA50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator().to_numpy().flatten()
        df['EMA200'] = ta.trend.EMAIndicator(df['Close'], window=200).ema_indicator().to_numpy().flatten()
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi().to_numpy().flatten()
        df['VolumeSMA'] = df['Volume'].rolling(window=20).mean()

        df.dropna(inplace=True)
        latest = df.iloc[-1]

        # Conditions
        price_above_ema50 = latest['Close'] > latest['EMA50']
        price_above_ema200 = latest['Close'] > latest['EMA200']
        rsi_ok = latest['RSI'] > rsi_threshold
        volume_ok = latest['Volume'] > (latest['VolumeSMA'] * volume_multiplier)

        if price_above_ema50 and price_above_ema200 and rsi_ok and volume_ok:
            signal = "📈 Buy"
        elif latest['Close'] < latest['EMA50'] and latest['Close'] < latest['EMA200'] and latest['RSI'] < 40:
            signal = "📉 Sell"
        else:
            continue

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
        st.warning(f"{ticker} error: {e}")

# Show results
st.markdown("## 📈 Screener Results")
if results:
    df_result = pd.DataFrame(results)
    st.dataframe(df_result)

    # Optional CSV download
    csv = df_result.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", data=csv, file_name="screener_results.csv", mime="text/csv")

else:
    st.info("No matching stocks found with current filters.")
