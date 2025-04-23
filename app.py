import streamlit as st
import yfinance as yf
import pandas as pd
from strategy import analyze_stock

st.set_page_config(page_title="Volume Threshold Strategy", layout="wide")
st.title("BankNifty Volume Strategy (19880+)")

st.markdown("This strategy triggers **Buy** on high-volume green candles and **Sell** on high-volume red candles. Volume threshold: `19880`")

# Sidebar inputs
ticker = st.sidebar.text_input("Enter NSE Symbol", value="^NSEBANK")  # BankNifty index
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))
run_button = st.sidebar.button("Run Strategy")

if run_button:
    try:
        # Fetch data
        st.write(f"Fetching data for: {ticker}")
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if df.empty:
            st.error("No data found for the selected symbol and time range.")
        else:
            # Run strategy logic
            df_result, signal_df = analyze_stock(df)

            # Price Chart
            st.subheader("Price Chart")
            st.line_chart(df_result["Close"])

            # Show signals
            st.subheader("Signals")
            if signal_df.empty:
                st.info("No Buy/Sell signals found for this period.")
            else:
                st.dataframe(signal_df)

    except Exception as e:
        st.error(f"Error while running strategy: {e}")
