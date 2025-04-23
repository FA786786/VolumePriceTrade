import pandas as pd
import numpy as np

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def preprocess_data(df):
    df = df.copy()

    # Ensure DataFrame has the basic required columns
    required_cols = ['Close', 'Volume', 'High', 'Low']
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing column: {col}")

    # Calculate indicators
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['10_avg_vol'] = df['Volume'].rolling(window=10).mean()
    df['RSI'] = compute_rsi(df['Close'])

    # Drop rows with NaNs in newly created columns
    df.dropna(subset=['EMA50', '10_avg_vol', 'RSI'], inplace=True)

    return df
