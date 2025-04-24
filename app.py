import pandas as pd
import streamlit as st

# === PARAMETERS ===
volume_threshold = 19880

# === SAMPLE DATA ===
df = pd.DataFrame({
    'open': [100, 102, 101, 105],
    'high': [105, 106, 103, 110],
    'low': [99, 100, 100, 104],
    'close': [104, 101, 102, 108],
    'volume': [20000, 15000, 22000, 25000]
})

# === CONDITIONS ===
df['is_bullish'] = df['close'] > df['open']
df['is_bearish'] = df['close'] < df['open']
df['is_high_volume'] = df['volume'] >= volume_threshold

df['buy_signal'] = df['is_bullish'] & df['is_high_volume']
df['sell_signal'] = df['is_bearish'] & df['is_high_volume']

# === DISPLAY ===
st.title("BankNifty Volume Buy/Sell Signals")
st.line_chart(df['close'])

# Show signals
st.write("Buy Signals:")
st.dataframe(df[df['buy_signal']][['close', 'volume']])

st.write("Sell Signals:")
st.dataframe(df[df['sell_signal']][['close', 'volume']])
