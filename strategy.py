import pandas as pd
from utils import calculate_ema, calculate_rsi, calculate_avg_volume

def analyze_stock(df: pd.DataFrame):
    # Calculate indicators
    try:
        df = calculate_ema(df, period=50)
    except Exception as e:
        print(f"⚠️ EMA50 calculation failed: {e}")

    try:
        df = calculate_rsi(df, period=14)
    except Exception as e:
        print(f"⚠️ RSI calculation failed: {e}")

    try:
        df = calculate_avg_volume(df, window=10)
    except Exception as e:
        print(f"⚠️ Avg Volume calculation failed: {e}")

    # Optional check to ensure required columns are present
    # But no error is raised — just silently skips missing ones
    required_cols = ['Close', 'Volume', 'EMA50', 'RSI', '10_avg_vol']
    available_cols = [col for col in required_cols if col in df.columns]

    # Drop rows with missing values only in columns that exist
    df = df.dropna(subset=available_cols)

    if df.empty or 'Close' not in df.columns or 'Volume' not in df.columns:
        return df, pd.DataFrame(columns=["Index", "Signal", "Close", "RSI", "Volume"])

    signals = []

    for i in range(1, len(df)):
        try:
            price = df['Close'].iloc[i]
            prev_price = df['Close'].iloc[i - 1_
