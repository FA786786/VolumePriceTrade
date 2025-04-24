import yfinance as yf
import pandas as pd
import ta

# List of Indian tickers on Yahoo Finance (add more as needed)
tickers = [
    "RELIANCE.NS", "ICICIBANK.NS", "HDFCBANK.NS", "TCS.NS", "SBIN.NS",
    "INFY.NS", "AXISBANK.NS", "LT.NS", "KOTAKBANK.NS", "WIPRO.NS"
]

def fetch_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    df.dropna(inplace=True)
    df['EMA50'] = ta.trend.ema_indicator(df['Close'], window=50)
    df['EMA200'] = ta.trend.ema_indicator(df['Close'], window=200)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
    return df

results = []

for ticker in tickers:
    try:
        df = fetch_data(ticker)
        latest = df.iloc[-1]

        # Define your "future stock" criteria
        if (
            latest['Close'] > latest['EMA50'] > latest['EMA200'] and
            latest['RSI'] > 55 and
            latest['Volume'] > 1.5 * latest['Volume_SMA'] and
            latest['Close'] > 0.98 * latest['High']  # close near high
        ):
            results.append(ticker)
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

print("🔥 Potential Future Stocks:")
print("\n".join(results))
