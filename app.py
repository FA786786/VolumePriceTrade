import streamlit as st
import yfinance as yf
import pandas as pd
from strategy import analyze_stock

st.set_page_config(page_title="📈 Volume Price Strategy", layout="wide")

st.title("📊 Volume & Price Strategy — Indian Stocks")
st.markdown("Analyze NSE stocks using a volume-price based strategy.")

# Sidebar input
ticker = st.sidebar.text_input("Enter NSE Stock Symbol", value="RELIANCE.NS")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))
run_analysis = st.sidebar.button("🚀 Run Strategy")

if run_analysis:
    try:
        # Pull data
        st.write(f"Fetching data for: **{ticker}**")
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            st.error("⚠️ No data found for the selected ticker and time period.")
        else:
            # Run strategy
            df_result, signals_df = analyze_stock(df)

            st.subheader("📈 Stock Price & Indicators")
            st.line_chart(df_result[['Close']])

            st.subheader("🪙 Buy/Sell Signals")
            if signals_df.empty:
                st.info("No buy/sell signals for this period.")
            else:
                st.dataframe(signals_df)

    except Exception as e:
        st.error(f"❌ Error while analyzing stock: {e}")
