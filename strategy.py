from utils import preprocess_data
import pandas as pd

def analyze_stock(df):
    # Preprocess the DataFrame to add indicators
    df = preprocess_data(df)

    # Ensure required columns are clean (no NaNs)
    df = df.dropna(subset=['EMA50', 'RSI', '10_avg_vol', 'High', 'Low', 'Close', 'Volume'])

    signals = []

    for i in range(1, len(df)):
        try:
            # Bullish breakout condition
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

            # Bearish breakdown condition
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
            # In case of any edge case errors (e.g., NaNs that sneak through)
            print(f"Skipping index {i} due to error: {e}")

    signals_df = pd.DataFrame(signals)
    return df, signals_df
