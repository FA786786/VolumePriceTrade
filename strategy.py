import pandas as pd
from utils import calculate_ema, calculate_rsi, calculate_avg_volume

def analyze_stock(df: pd.DataFrame):
    # Calculate indicators (safe)
    try:
        df = calculate_ema(df, period=50)
    except Exception as e:
        print(f"⚠️ EMA calc failed: {e}")
    try:
        df = calculate_rsi(df, period=14)
    except Exception as e:
        print(f"⚠️ RSI calc failed: {e}")
    try:
        df = calculate_avg_volume(df, window=10)
    except Exception as e:
        print(f"⚠️ Avg Volume calc failed: {e}")

    # Drop rows with any NaNs in available columns
    valid_cols = [col for col in ['EMA50', 'RSI', '10_avg_vol', 'Close', 'Volume'] if col in df.columns]
    df = df.dropna(subset=valid_cols)

    if df.empty:
        return df, pd.DataFrame(columns=["Index", "Signal", "Close", "RSI", "Volume"])

    signals = []

    for i in range(1, len(df)):
        try:
            price = df['Close'].iloc[i]
            ema = df.get('EMA50', pd.Series([None]*len(df))).iloc[i]
            rsi = df.get('RSI', pd.Series([None]*len(df))).iloc[i]
            volume = df['Volume'].iloc[i]
            avg_vol = df.get('10_avg_vol', pd.Series([None]*len(df))).iloc[i]
            prev_price = df['Close'].iloc[i - 1]

            if (
                pd.notna(ema) and pd.notna(rsi) and pd.notna(avg_vol)
                and price > ema and rsi < 70 and volume > 1.5 * avg_vol and price > prev_price
            ):
                signals.append({
                    'Index': df.index[i],
                    'Signal': 'Buy',
                    'Close': price,
                    'RSI': rsi,
                    'Volume': volume
                })

            elif (
                pd.notna(ema) and pd.notna(rsi) and pd.notna(avg_vol)
                and price < ema and rsi > 30 and volume > 1.5 * avg_vol and price < prev_price
            ):
                signals.append({
                    'Index': df.index[i],
                    'Signal': 'Sell',
                    'Close': price,
                    'RSI': rsi,
                    'Volume': volume
                })
        except Exception as e:
            print(f"⚠️ Error processing row {i}: {e}")

    signals_df = pd.DataFrame(signals)
    return df, signals_df
