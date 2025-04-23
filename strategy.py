
import pandas as pd

def analyze_stock(df: pd.DataFrame, volume_threshold=19880):
    signals = []

    # Ensure basic columns exist
    required_cols = ['Open', 'Close', 'Volume', 'High']
    if not all(col in df.columns for col in required_cols):
        return df, pd.DataFrame(columns=["Index", "Signal", "Close", "Volume"])

    df = df.dropna(subset=required_cols)

    for i in range(1, len(df)):
        open_price = df['Open'].iloc[i]
        close_price = df['Close'].iloc[i]
        volume = df['Volume'].iloc[i]

        is_bullish = close_price > open_price
        is_bearish = close_price < open_price
        is_high_volume = volume >= volume_threshold

        if is_bullish and is_high_volume:
            signals.append({
                'Index': df.index[i],
                'Signal': 'Buy',
                'Close': close_price,
                'Volume': volume
            })
        elif is_bearish and is_high_volume:
            signals.append({
                'Index': df.index[i],
                'Signal': 'Sell',
                'Close': close_price,
                'Volume': volume
            })

    signals_df = pd.DataFrame(signals)
    return df, signals_df
