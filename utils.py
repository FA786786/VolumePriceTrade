import pandas as pd
import numpy as np

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def preprocess_data(df):
    df = df.copy()

    # Ensure necessary columns exist
    if 'Close' not in df or 'Volume' not in df or 'High' not in df or 'Low' not in df:
        raise ValueError("Missing required OHLCV columns in the input DataFrame.")

    # EMA50
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    # 10-day average volume
    df['10_avg_vol'] = df['Volume'].rolling(window=10).mean()

    # RSI
    df['RSI'] = compute_rsi(df['Close'])

    # Drop rows with NaNs in the calculated columns
    df.dropna(subset=['EMA50', '10_avg_vol', 'RSI'], inplace=True)

    return df
