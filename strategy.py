from utils import preprocess_data

def analyze_stock(df):
    df = preprocess_data(df)

    signals = []
    for i in range(1, len(df)):
        if (
            df['Close'].iloc[i] > df['EMA50'].iloc[i]
            and df['Volume'].iloc[i] > 1.5 * df['10_avg_vol'].iloc[i]
            and df['Close'].iloc[i] > df['High'].iloc[i - 1]
            and 55 <= df['RSI'].iloc[i] <= 65
        ):
            signals.append({'Index': df.index[i], 'Signal': 'Buy', 'Close': df['Close'].iloc[i]})
        elif (
            df['Close'].iloc[i] < df['EMA50'].iloc[i]
            and df['Volume'].iloc[i] > 1.5 * df['10_avg_vol'].iloc[i]
            and df['Close'].iloc[i] < df['Low'].iloc[i - 1]
            and df['RSI'].iloc[i] < 45
        ):
            signals.append({'Index': df.index[i], 'Signal': 'Sell', 'Close': df['Close'].iloc[i]})

    signals_df = pd.DataFrame(signals)
    return df, signals_df
