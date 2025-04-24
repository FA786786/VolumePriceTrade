import pandas as pd
import matplotlib.pyplot as plt

# === PARAMETERS ===
volume_threshold = 19880

# === EXAMPLE DATA ===
# Replace this with your real OHLCV data
# DataFrame `df` should contain columns: ['open', 'high', 'low', 'close', 'volume']
# Example:
# df = pd.read_csv('your_data.csv')

# Sample structure for context
df = pd.DataFrame({
    'open': [100, 102, 101, 105],
    'high': [105, 106, 103, 110],
    'low': [99, 100, 100, 104],
    'close': [104, 101, 102, 108],
    'volume': [20000, 15000, 22000, 25000]
})

# === CANDLE CONDITIONS ===
df['is_bullish'] = df['close'] > df['open']
df['is_bearish'] = df['close'] < df['open']
df['is_high_volume'] = df['volume'] >= volume_threshold

# === SIGNAL CONDITIONS ===
df['buy_signal'] = df['is_bullish'] & df['is_high_volume']
df['sell_signal'] = df['is_bearish'] & df['is_high_volume']

# === PLOTTING ===
plt.figure(figsize=(12, 6))
plt.plot(df['close'], label='Close Price', color='black')

# Buy signals
plt.scatter(df.index[df['buy_signal']], df['low'][df['buy_signal']] - 1, color='green', marker='^', label='Buy Signal')

# Sell signals
plt.scatter(df.index[df['sell_signal']], df['high'][df['sell_signal']] + 1, color='red', marker='v', label='Sell Signal')

# === OPTIONAL: Show volume for alerts/debug ===
# plt.bar(df.index, df['volume'], alpha=0.3, color='orange', label='Volume')

# === LABELS (printout for debug/alerts) ===
for idx, row in df.iterrows():
    if row['buy_signal']:
        print(f"{idx}: BUY - Volume: {row['volume']}")
    elif row['sell_signal']:
        print(f"{idx}: SELL - Volume: {row['volume']}")

plt.title('BankNifty Volume Buy/Sell Signals')
plt.legend()
plt.grid(True)
plt.show()
