import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    """Calculate the Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(series, period=50):
    """Calculate Exponential Moving Average."""
    return series.ewm(span=period, adjust=False).mean()

def calculate_avg_volume(df, window=10):
    """Calculate average volume over a rolling window."""
    return df['Volume'].rolling(window=window).mean()

def preprocess_data(df):
    """Add required indicators to DataFrame."""
    df = df.copy()
    df['EMA50'] = calculate_ema(df['Close'], 50)
    df['RSI'] = calculate_rsi(df['Close'], 14)
    df['10_avg_vol'] = calculate_avg_volume(df, 10)
    df.dropna(inplace=True)
    return df
