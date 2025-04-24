import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import datetime
from io import BytesIO

# ------------------ Streamlit Setup ------------------
st.set_page_config(page_title="Indian Stock Screener", layout="wide")
st.title("📈 Indian Futures Stock Screener")
st.caption("By FA786786 • Powered by yfinance + ta")

# ------------------ Tickers ------------------
tickers = [
    "RELIANCE.NS", "TCS.NS", "ICICIBANK.NS", "SBIN.NS",
    "HDFCBANK.NS", "LT.NS", "INFY.NS", "AXISBANK.NS"
]

# ------------------ Sidebar ------------------
selected_tickers = st.multiselect("Select Stocks", tickers, default=tickers)
timeframe = st.selectbox("Timeframe", ["5m", "15m", "1h", "1d"], index=1)
period = st.selectbox("Period", ["5d", "7d", "1mo"], index=0)
rsi_thresh = st.slider("RSI Threshold", 50, 80, 55)
volume_multiplier = st.slider("Volume Multiplier", 1.0, 3.0, 1.5)

# ------------------ Screener Logic ------------------
def fetch_data(ticker):
    df = yf.download(ticker, interval=timeframe, period=period, progress=False)
    if df.empty or len(df) < 50:
        return None
    df['EMA50'] = ta.trend.ema_indicator(df['Close'], 50)
    df['EMA200'] = ta.trend.ema_indicator(df['Close'], 200)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], 14).rsi()
    df['VolumeSMA'] = df['Volume'].rolling(20).mean()
    return df

results = []
for ticker in selected_tickers:
    try:
        df = fetch_data(ticker)
        if df is None:
            continue
        latest = df.iloc[-1]
        if (
            latest['Close'] > latest['EMA50'] > latest['EMA200'] and
            latest['RSI'] > rsi_thresh and
            latest['Volume'] > volume_multiplier * latest['VolumeSMA'] and
            latest['Close'] >= 0.98 * latest['High']
        ):
            results.append({
                "Stock": ticker.replace(".NS", ""),
                "Close": latest['Close'],
                "EMA50": latest['EMA50'],
                "EMA200": latest['EMA200'],
                "RSI": latest['RSI'],
                "Volume": latest['Volume'],
                "Time": df.index[-1]
            })
    except Exception as e:
        st.warning(f"{ticker} error: {e}")

# ------------------ Results ------------------
st.subheader("📊 Screener Results")
if results:
    df_results = pd.DataFrame(results).sort_values(by="RSI", ascending=False)
    st.dataframe(df_results, use_container_width=True)

    def convert_df(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        return output.getvalue()

    st.download_button(
        "⬇️ Download CSV",
        data=convert_df(df_results),
        file_name=f"screener_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )
else:
    st.info("No matching stocks found with current filters.")

# ------------------ Footer ------------------
st.markdown("---")
st.caption("Developed by FA786786 • Streamlit App • 2025")
