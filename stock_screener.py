import streamlit as st
st.set_page_config(page_title="Stock Screener", layout="wide")

import yfinance as yf
import pandas as pd
import datetime
import traceback
from stock_tickers import TICKERS

st.set_page_config(page_title="Stock Screener", layout="wide")

def get_stock_data(tickers, period="1y"):
    """
    Fetch stock data for the given tickers
    """
    data = {}
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(tickers):
        try:
            # Update progress
            progress = int((i / len(tickers)) * 100)
            progress_bar.progress(progress)
            status_text.text(f"Processing {ticker}... ({i+1}/{len(tickers)})")
            
            # Get stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if not hist.empty:
                # Get basic info
                info = stock.info
                market_cap = info.get('marketCap', 0)
                current_price = hist['Close'].iloc[-1] if not hist.empty else 0
                
                # Calculate 250-day return
                if len(hist) >= 250:
                    start_price = hist['Close'].iloc[-250] if len(hist) >= 250 else hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    return_250d = (end_price - start_price) / start_price * 100
                else:
                    return_250d = 0
                
                data[ticker] = {
                    'Ticker': ticker,
                    'Company Name': info.get('shortName', ticker),
                    'Current Price ($)': current_price,
                    'Market Cap ($B)': market_cap / 1e9 if market_cap else 0,
                    '250-Day Return (%)': return_250d,
                    'Sector': info.get('sector', 'N/A'),
                    'Industry': info.get('industry', 'N/A'),
                }
        except Exception as e:
            st.sidebar.warning(f"Error fetching data for {ticker}: {str(e)}")
            st.sidebar.info(f"Skipping {ticker} and continuing...")
    
    # Complete the progress bar
    progress_bar.progress(100)
    status_text.text("Processing complete!")
    
    return pd.DataFrame(list(data.values()))

def main():
    st.title("Stock Screener")
    st.write("Filter stocks based on market cap, price, and performance")
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Market Cap filter
    min_market_cap = st.sidebar.slider(
        "Minimum Market Cap ($B)",
        min_value=0.0,
        max_value=500.0,
        value=2.0,
        step=0.5
    )
    
    # Price filter
    min_price = st.sidebar.slider(
        "Minimum Stock Price ($)",
        min_value=0.0,
        max_value=1000.0,
        value=10.0,
        step=1.0
    )
    
    # 250-day return filter
    positive_return = st.sidebar.checkbox("Only show stocks with positive 250-day return", value=True)
    
    # Number of stocks to analyze
    num_stocks = st.sidebar.slider(
        "Number of stocks to analyze",
        min_value=10,
        max_value=len(TICKERS),
        value=min(50, len(TICKERS)),
        step=10
    )
    
    # Fetch data button
    if st.sidebar.button("Fetch Stock Data"):
        try:
            with st.spinner("Fetching stock data..."):
                # Use only the selected number of stocks
                selected_tickers = TICKERS[:num_stocks]
                st.info(f"Analyzing {len(selected_tickers)} stocks. This may take a few minutes...")
                
                df = get_stock_data(selected_tickers)
                
                if df.empty:
                    st.error("No data was retrieved. Please try again.")
                    return
                
                # Apply filters
                filtered_df = df[
                    (df['Market Cap ($B)'] >= min_market_cap) &
                    (df['Current Price ($)'] >= min_price)
                ]
                
                if positive_return:
                    filtered_df = filtered_df[filtered_df['250-Day Return (%)'] > 0]
                
                # Sort by market cap
                filtered_df = filtered_df.sort_values(by='Market Cap ($B)', ascending=False)
                
                # Store in session state
                st.session_state.filtered_df = filtered_df
                st.session_state.all_df = df
                
                st.success(f"Data fetched successfully for {len(df)} stocks!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Stack trace:")
            st.code(traceback.format_exc())
    
    # Display results
    if 'filtered_df' in st.session_state:
        st.header("Filtered Stocks")
        st.write(f"Found {len(st.session_state.filtered_df)} stocks matching your criteria")
        
        st.dataframe(
            st.session_state.filtered_df,
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker"),
                "Company Name": st.column_config.TextColumn("Company Name"),
                "Current Price ($)": st.column_config.NumberColumn("Price ($)", format="$.2f"),
                "Market Cap ($B)": st.column_config.NumberColumn("Market Cap ($B)", format="$.2f"),
                "250-Day Return (%)": st.column_config.NumberColumn("250-Day Return (%)", format="%.2f%%"),
                "Sector": st.column_config.TextColumn("Sector"),
                "Industry": st.column_config.TextColumn("Industry"),
            },
            hide_index=True,
        )
        
        # Show statistics
        st.header("Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Average Market Cap ($B)", 
                     f"${st.session_state.filtered_df['Market Cap ($B)'].mean():.2f}B")
            st.metric("Average 250-Day Return", 
                     f"{st.session_state.filtered_df['250-Day Return (%)'].mean():.2f}%")
        
        with col2:
            st.metric("Highest Market Cap", 
                     f"${st.session_state.filtered_df['Market Cap ($B)'].max():.2f}B")
            st.metric("Highest 250-Day Return", 
                     f"{st.session_state.filtered_df['250-Day Return (%)'].max():.2f}%")

if __name__ == "__main__":
    main()