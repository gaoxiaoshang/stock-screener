#!/usr/bin/env python3
"""
Stock Screener CLI
This script screens stocks based on market cap, price, and performance.
"""

import yfinance as yf
import pandas as pd
import time
import sys
from stock_tickers import TICKERS

def get_stock_data(tickers, period="1y"):
    """
    Fetch stock data for the given tickers
    """
    data = {}
    total = len(tickers)
    
    print(f"Fetching data for {total} stocks...")
    
    for i, ticker in enumerate(tickers):
        try:
            # Show progress
            progress = (i / total) * 100
            sys.stdout.write(f"\rProgress: {progress:.1f}% - Processing {ticker} ({i+1}/{total})")
            sys.stdout.flush()
            
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
            print(f"\nError fetching data for {ticker}: {str(e)}")
            print("Skipping and continuing...")
    
    print("\nProcessing complete!")
    return pd.DataFrame(list(data.values()))

def main():
    print("===== Stock Screener =====")
    print("This tool screens stocks based on market cap, price, and performance")
    
    # Default filter values
    min_market_cap = 2.0  # $2 billion
    min_price = 10.0      # $10
    positive_return = True
    
    # Ask for number of stocks to analyze
    try:
        num_stocks = int(input(f"Number of stocks to analyze (max {len(TICKERS)}, default 50): ") or "50")
        num_stocks = min(num_stocks, len(TICKERS))
    except ValueError:
        num_stocks = 50
    
    # Use only the selected number of stocks
    selected_tickers = TICKERS[:num_stocks]
    
    print(f"\nAnalyzing {len(selected_tickers)} stocks. This may take a few minutes...")
    df = get_stock_data(selected_tickers)
    
    if df.empty:
        print("No data was retrieved. Please try again.")
        return
    
    # Apply filters
    print("\nApplying filters:")
    print(f"- Market Cap >= ${min_market_cap} billion")
    print(f"- Current Price >= ${min_price}")
    if positive_return:
        print("- 250-Day Return > 0%")
    
    filtered_df = df[
        (df['Market Cap ($B)'] >= min_market_cap) &
        (df['Current Price ($)'] >= min_price)
    ]
    
    if positive_return:
        filtered_df = filtered_df[filtered_df['250-Day Return (%)'] > 0]
    
    # Sort by market cap
    filtered_df = filtered_df.sort_values(by='Market Cap ($B)', ascending=False)
    
    # Display results
    print(f"\nFound {len(filtered_df)} stocks matching your criteria:")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.float_format', '${:.2f}'.format)
    
    # Format the 250-Day Return column separately
    filtered_df_display = filtered_df.copy()
    filtered_df_display['250-Day Return (%)'] = filtered_df_display['250-Day Return (%)'].apply(lambda x: f"{x:.2f}%")
    
    print(filtered_df_display[['Ticker', 'Company Name', 'Current Price ($)', 'Market Cap ($B)', '250-Day Return (%)', 'Sector']])
    
    # Show statistics
    print("\nStatistics:")
    print(f"Average Market Cap: ${filtered_df['Market Cap ($B)'].mean():.2f}B")
    print(f"Average 250-Day Return: {filtered_df['250-Day Return (%)'].mean():.2f}%")
    print(f"Highest Market Cap: ${filtered_df['Market Cap ($B)'].max():.2f}B")
    print(f"Highest 250-Day Return: {filtered_df['250-Day Return (%)'].max():.2f}%")
    
    # Save to CSV
    save_option = input("\nDo you want to save the results to a CSV file? (y/n): ")
    if save_option.lower() == 'y':
        filename = "stock_screener_results.csv"
        filtered_df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    main()