import streamlit as st
import pandas as pd

# === CONFIGURATION ===
st.set_page_config(page_title="BankNifty Volume Buy/Sell", layout="wide")

# === PARAMETERS ===
VOLUME_THRESHOLD = 19880

# === SAMPLE OHLCV DATA ===
# You can replace this with your own data from a CSV, API, etc.
data = {
    'open': [100, 102, 101, 105, 108, 107],
    'high': [105, 106, 103, 110, 112, 110],
    'low': [99, 100, 100, 104, 107, 106],
    'close': [104, 101, 102, 108, 111, 106],
    'volume': [20000, 15000, 22000, 25000, 23000, 12000]
}
df = pd.DataFrame(data)

# === LOGIC ===
df['is_bullish'] = df['close'] > df['open']
df['is_bearish'] = df['close'] < df['open']
df['is_high_volume'] = df['volume'] >= VOLUME_THRESHOLD

df['buy_signal'] = df['is_bullish'] & df['is_high_volume']
df['sell_signal'] = df['is_bearish'] & df['is_high_volume']

# === STREAMLIT UI ===
st.title("📈 BankNifty Volume Buy/Sell Signal (19880+)")

# Chart
st.subheader("🔹 Close Price Chart")
st.line_chart(df['close'])

# Buy Signals
buy_df = df[df['buy_signal']].copy()
st.success("✅ Buy Signals Detected:")
if not buy_df.empty:
    st.dataframe(buy_df[['open', 'close', 'volume']])
else:
    st.write("No buy signals found.")

# Sell Signals
sell_df = df[df['sell_signal']].copy()
st.error("🔻 Sell Signals Detected:")
if not sell_df.empty:
    st.dataframe(sell_df[['open', 'close', 'volume']])
else:
    st.write("No sell signals found.")

# Debug
with st.expander("🛠 Full Data (Debug Info)"):
    st.dataframe(df)
