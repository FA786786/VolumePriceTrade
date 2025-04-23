import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from strategy import analyze_stock

st.set_page_config(page_title="Volume Price Action Strategy", layout="wide")

st.title("📈 Volume Price Action Strategy for Indian Markets")

# Sidebar inputs
with st.sidebar:
    st.header("Input Parameters")
    ticker = st.text_input("Enter NSE stock ticker (e.g., RELIANCE.NS)", value="RELIANCE.NS")
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("today"))

# Download data
@st.cache_data
def load_data(ticker, start, end):
    try:
        df = yf.download(ticker, start=start, end=end)
        return df
    except Exception as e:
        st.error(f"Failed to download data: {e}")
        return pd.DataFrame()

df = load_data(ticker, start_date, end_date)

# Check if data is valid
if df.empty or df.shape[0] < 30:
    st.warning("⚠️ Not enough data fetched. Please check the ticker or date range.")
else:
    try:
        result_df, signals_df = analyze_stock(df)

        st.subheader("📊 Chart with Signals")

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=result_df.index,
            open=result_df['Open'],
            high=result_df['High'],
            low=result_df['Low'],
            close=result_df['Close'],
            name='Candlestick'
        ))

        # Add signals
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

        st.subheader("📝 Signal Table")
        st.dataframe(signals_df)

    except Exception as e:
        st.error(f"🚫 Error while analyzing stock: {e}")
