import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from strategy import analyze_stock

st.set_page_config(page_title="📊 Volume Price Action Strategy", layout="wide")
st.title("📈 Volume Price Action Strategy for Indian Markets")

# Sidebar input
with st.sidebar:
    st.header("Stock Selection")
    ticker = st.text_input("Enter NSE stock ticker (e.g., RELIANCE.NS)", value="RELIANCE.NS")
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("today"))

# Function to load extended data for indicators
@st.cache_data
def load_data(ticker, user_start, user_end):
    # Pull at least 6 months before user start for indicators like EMA50, RSI
    buffer_days = 180
    hist_start = user_start - pd.Timedelta(days=buffer_days)
    try:
        df = yf.download(ticker, start=hist_start, end=user_end)
        if df.empty:
            raise ValueError("Downloaded data is empty.")
        return df
    except Exception as e:
        st.error(f"❌ Failed to download data: {e}")
        return pd.DataFrame()

# Load data
df = load_data(ticker, start_date, end_date)

# Ensure enough data exists
if df.empty or df.shape[0] < 60:
    st.warning("⚠️ Not enough data. Try a different ticker or wider date range.")
    st.stop()

# Try to analyze stock
try:
    result_df, signals_df = analyze_stock(df)

    # Filter signals only within user-selected date range
    signals_df = signals_df[signals_df['Index'] >= pd.to_datetime(start_date)]

    # Plot
    st.subheader("📊 Price Action with Buy/Sell Signals")

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=result_df.index,
        open=result_df['Open'],
        high=result_df['High'],
        low=result_df['Low'],
        close=result_df['Close'],
        name='Candlesticks'
    ))

    for _, row in signals_df.iterrows():
        color = 'green' if row['Signal'] == 'Buy' else 'red'
        fig.add_trace(go.Scatter(
            x=[row['Index']],
            y=[row['Close']],
            mode='markers+text',
            marker=dict(color=color, size=10),
            name=row['Signal'],
            text=row['Signal'],
            textposition="top center"
        ))

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show signal table
    st.subheader("📝 Trade Signals")
    st.dataframe(signals_df[['Index', 'Signal', 'Close', 'RSI', 'Volume']])

except Exception as e:
    st.error(f"🚫 Error while analyzing stock: {e}")
