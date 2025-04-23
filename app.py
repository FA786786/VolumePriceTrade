import streamlit as st
import pandas as pd
from strategy import analyze_stock
import yfinance as yf
import plotly.graph_objs as go

st.title("📊 Price-Volume Action Strategy - Indian Markets")

ticker = st.text_input("Enter Stock Ticker (e.g. RELIANCE.NS):", "RELIANCE.NS")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if st.button("Analyze"):
    df = yf.download(ticker, start=start_date, end=end_date)
    
    if df.empty:
        st.error("Failed to fetch data. Check ticker.")
    else:
        result_df, signals = analyze_stock(df)
        st.dataframe(signals)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=result_df.index,
            open=result_df['Open'],
            high=result_df['High'],
            low=result_df['Low'],
            close=result_df['Close'],
            name='Candlestick'
        ))

        for signal in signals.itertuples():
            color = 'green' if signal.Signal == 'Buy' else 'red'
            fig.add_trace(go.Scatter(
                x=[signal.Index], y=[signal.Close],
                mode='markers',
                marker=dict(color=color, size=10),
                name=signal.Signal
            ))

        st.plotly_chart(fig)
