import pandas as pd

def calculate_ema(df: pd.DataFrame, period: int = 50) -> pd.DataFrame:
    if 'Close' not in df:
        raise ValueError("Missing 'Close' column for EMA calculation.")
    df[f'EMA{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
    return df

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    if 'Close' not in df:
        raise ValueError("Missing 'Close' column for RSI calculation.")
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_avg_volume(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    if 'Volume' not in df:
        raise ValueError("Missing 'Volume' column for avg volume calculation.")
    df[f'{window}_avg_vol'] = df['Volume'].rolling(window=window).mean()
    return df
