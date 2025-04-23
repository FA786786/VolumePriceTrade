import pandas as pd
from utils import calculate_ema, calculate_rsi, calculate_avg_volume

def analyze_stock(df: pd.DataFrame):
    try:
        df = calculate_ema(df, period=50)
        df = calculate_rsi(df, period=14)
        df = calculate_avg_volume(df, window=10)
    except Exception as e:
        raise ValueError(f"Error during indicator calculation: {e}")

    # Check if all required columns exist
    required_cols = ['EMA50', 'RSI', '10_avg_vol', 'Close', 'Volume']
    missing = [col for col in required_cols if col not in df.columns or df[col].isna().all()]
    if missing:
        raise ValueError(f"Missing or invalid data in columns: {missing}")

    df = df.dropna(subset=required_cols)

    signals = []
    for i in range(1, len(df)):
        price = df['Close'].iloc[i]
        ema = df['EMA50'].iloc[i]
        rsi = df['RSI'].iloc[i]
        volume = df['Volume'].iloc[i]
        avg_vol = df['10_avg_vol'].iloc[i]
        prev_price = df['Close'].iloc[i - 1]

        if (
            price > ema and rsi < 70 and
            volume > 1.5 * avg_vol and price > prev_price
        ):
            signals.append({
                'Index': df.index[i],
                'Signal': 'Buy',
                'Close': price,
                'RSI': rsi,
                'Volume': volume
            })
        elif (
            price < ema and rsi > 30 and
            volume > 1.5 * avg_vol and price < prev_price
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
