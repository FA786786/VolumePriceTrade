import yfinance as yf
import pandas as pd
import ta

# 🔧 SETTINGS
tickers = [
    "RELIANCE.NS", "TCS.NS", "ICICIBANK.NS", "SBIN.NS", 
    "HDFCBANK.NS", "LT.NS", "INFY.NS", "AXISBANK.NS"
]

timeframe = "15m"  # Options: '1d', '1h', '15m', '5m', etc.
period = "5d"      # Options: '1mo', '5d', '7d', '60d', etc.

# 🚀 Screener logic
def fetch_and_screen(ticker):
    df = yf.download(ticker, interval=timeframe, period=period, progress=False)
    if df.empty or len(df) < 50:
        return None

    df['EMA50'] = ta.trend.ema_indicator(df['Close'], 50)
    df['EMA200'] = ta.trend.ema_indicator(df['Close'], 200)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], 14).rsi()
    df['VolumeSMA'] = df['Volume'].rolling(20).mean()
    
    latest = df.iloc[-1]

    conditions = [
        latest['Close'] > latest['EMA50'] > latest['EMA200'],
        latest['RSI'] > 55,
        latest['Volume'] > 1.5 * latest['VolumeSMA'],
        latest['Close'] >= 0.98 * latest['High']
    ]

    return ticker.replace(".NS", "") if all(conditions) else None

# 🔍 Run screener
candidates = []
for ticker in tickers:
    try:
        result = fetch_and_screen(ticker)
        if result:
            candidates.append(result)
    except Exception as e:
        print(f"Error with {ticker}: {e}")

# 📢 Result
print(f"📊 Timeframe: {timeframe}, Period: {period}")
print("🔥 Matching Stocks:")
print("\n".join(candidates) if candidates else "No matches.")
