import pandas as pd
from utils import calculate_ema, calculate_rsi, calculate_avg_volume

def analyze_stock(df: pd.DataFrame):
    # Calculate indicators
    df = calculate_ema(df, period=50)
    df = calculate_rsi(df, period=14)
    df = calculate_avg_volume(df, window=10)

    # Clean data
    df.dropna(subset=['EMA50', 'RSI', '10_avg_vol', 'Close', 'Volume'], inplace=True)

    signals = []

    for i in range(1, len(df)):
        price = df['Close'].iloc[i]
        ema = df['EMA50'].iloc[i]
        rsi = df['RSI'].iloc[i]
        volume = df['Volume'].iloc[i]
        avg_vol = df['10_avg_vol'].iloc[i]

        prev_price = df['Close'].iloc[i - 1]

        # Buy Signal Logic
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

        # Sell Signal Logic
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
