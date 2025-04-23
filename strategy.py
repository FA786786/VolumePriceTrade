import pandas as pd

def analyze_stock(df):
    df['10_avg_vol'] = df['Volume'].rolling(window=10).mean()
    df['RSI'] = df['Close'].rolling(window=14).mean()  # Replace with actual RSI logic
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    signals = []
    for i in range(1, len(df)):
        if (
            df['Close'][i] > df['EMA50'][i]
            and df['Volume'][i] > 1.5 * df['10_avg_vol'][i]
            and df['Close'][i] > df['High'][i-1]
        ):
            signals.append({'Index': df.index[i], 'Signal': 'Buy', 'Close': df['Close'][i]})
        elif (
            df['Close'][i] < df['EMA50'][i]
            and df['Volume'][i] > 1.5 * df['10_avg_vol'][i]
            and df['Close'][i] < df['Low'][i-1]
        ):
            signals.append({'Index': df.index[i], 'Signal': 'Sell', 'Close': df['Close'][i]})

    signals_df = pd.DataFrame(signals)
    return df, signals_df
