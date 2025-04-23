# Sidebar run button
run_analysis = st.sidebar.button("🚀 Run Strategy")

# Load data
df = load_data(ticker, start_date, end_date)

# Ensure enough data exists
if df.empty or df.shape[0] < 60:
    st.warning("⚠️ Not enough data. Try a different ticker or wider date range.")
    st.stop()

# Only run analysis if button clicked
if run_analysis:
    try:
        result_df, signals_df = analyze_stock(df)

        # Filter signals within user-selected date range
        signals_df = signals_df[signals_df['Index'] >= pd.to_datetime(start_date)]

        # Chart
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

        # Signal table
        st.subheader("📝 Trade Signals")
        st.dataframe(signals_df[['Index', 'Signal', 'Close', 'RSI', 'Volume']])

    except Exception as e:
        st.error(f"🚫 Error while analyzing stock: {e}")
