import pandas as pd
from utils import calculate_ema, calculate_rsi, calculate_avg_volume

def analyze_stock(df: pd.DataFrame):
    try:
        # Compute indicators
        df = calculate_ema(df, period=50)
        df = calculate_rsi(df, period=14)
        df = calculate_avg_volume(df, window=10)
    except Exception as e:
        raise ValueError(f"Error during indicator calculation: {e}")

    # Ensure all required columns exist
    required_cols = ['EMA50', 'RSI', '10_avg_vol', 'Close', 'Volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    
    # Drop rows with any NaNs in key columns
    df = df.dropna(subset=required_cols)

    # Re-check for emptiness after cleaning
    if df.empty:
        raise ValueError("Insufficient data after removing NaN rows.")

    signals = []

    for i in range(1, len(df)):
        price = df['Close'].iloc[i]
        ema = df['EMA50'].iloc[i]
        rsi = df['RSI'].iloc[i]
        volume = df['Volume'].iloc[i]
        avg_vol = df['10_avg_vol'].iloc[i]
        prev_price = df['Close'].iloc[i - 1]

        # Buy signal condition
        if (
            price > ema and
            rsi < 70 and
            volume > 1.5 * avg_vol and
            price > prev_price
        ):
            signals.append({
                'Index': df.index[i],
                'Signal': 'Buy',
                'Close': price,
                'RSI': rsi,
                'Volume': volume
            })

        # Sell signal condition
        elif (
            price < ema and
            rsi > 30 and
            volume > 1.5 * avg_vol and
            price < prev_price
        ):
            signals.append({
                'Index': df.index[i],
                'Signal': 'Sell',
                'Close': price,
                'RSI': rsi,
                'Volume': volume
            })

    signals_df = pd.DataFrame(signals)
    return df, signals_df
