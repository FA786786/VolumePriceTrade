        if df.empty:
            st.error("No data found for the selected symbol and time range.")
        elif not all(col in df.columns for col in ['Open', 'Close', 'Volume', 'High']):
            st.error("Downloaded data is missing required columns: Open, Close, Volume, High.")
            st.dataframe(df.head())  # Optional: show partial data for debugging
        else:
            # Run strategy logic
            df_result, signal_df = analyze_stock(df)

            st.subheader("Price Chart")
            st.line_chart(df_result["Close"])

            st.subheader("Signals")
            if signal_df.empty:
                st.info("No Buy/Sell signals found for this period.")
            else:
                st.dataframe(signal_df)
