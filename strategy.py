from utils import preprocess_data
import pandas as pd

def analyze_stock(df):
    df = preprocess_data(df)

    required_cols = ['EMA50', 'RSI', '10_avg_vol', 'High', 'Low', 'Close', 'Volume']

    # Check if all required columns are present
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns in DataFrame: {missing_cols}")

    # Drop rows with NaN in key columns
    df = df.dropna(subset=required_cols)

    signals = []

    for i in range(1, len(df)):
        try:
            # Bullish breakout
            if (
                df['Close'].iloc[i] > df['EMA50'].iloc[i]
                and df['Volume'].iloc[i] > 1.5 * df['10_avg_vol'].iloc[i]
                and df['Close'].iloc[i] > df['High'].iloc[i - 1]
                and 55 <= df['RSI'].iloc[i] <= 65
            ):
                signals.append({
                    'Index': df.index[i],
                    'Signal': 'Buy',
                    'Close': df['Close'].iloc[i]
                })

            # Bearish breakdown
            elif (
                df['Close'].iloc[i] < df['EMA50'].iloc[i]
                and df['Volume'].iloc[i] > 1.5 * df['10_avg_vol'].iloc[i]
                and df['Close'].iloc[i] < df['Low'].iloc[i - 1]
                and df['RSI'].iloc[i] < 45
            ):
                signals.append({
                    'Index': df.index[i],
                    'Signal': 'Sell',
                    'Close': df['Close'].iloc[i]
                })

        except Exception as e:
            print(f"Skipping index {i} due to error: {e}")

    signals_df = pd.DataFrame(signals)
    return df, signals_df
