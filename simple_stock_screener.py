#!/usr/bin/env python3
"""
Simple Stock Screener
This script screens stocks based on market cap, price, and performance without using pandas.
"""

import yfinance as yf
import time
import sys
import csv
from stock_tickers import TICKERS

def get_stock_data(tickers, period="1y"):
    """
    Fetch stock data for the given tickers
    """
    data = []
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
            
            if len(hist) > 0:
                # Get basic info
                info = stock.info
                market_cap = info.get('marketCap', 0)
                current_price = hist['Close'].iloc[-1] if len(hist) > 0 else 0
                
                # Calculate 250-day return
                if len(hist) >= 250:
                    start_price = hist['Close'].iloc[-250] if len(hist) >= 250 else hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    return_250d = (end_price - start_price) / start_price * 100
                else:
                    return_250d = 0
                
                stock_data = {
                    'Ticker': ticker,
                    'Company Name': info.get('shortName', ticker),
                    'Current Price': current_price,
                    'Market Cap (B)': market_cap / 1e9 if market_cap else 0,
                    '250-Day Return': return_250d,
                    'Sector': info.get('sector', 'N/A'),
                    'Industry': info.get('industry', 'N/A'),
                }
                
                data.append(stock_data)
        except Exception as e:
            print(f"\nError fetching data for {ticker}: {str(e)}")
            print("Skipping and continuing...")
    
    print("\nProcessing complete!")
    return data

def filter_stocks(stocks, min_market_cap=2.0, min_price=10.0, positive_return=True):
    """
    Filter stocks based on criteria
    """
    filtered = []
    
    for stock in stocks:
        if (stock['Market Cap (B)'] >= min_market_cap and 
            stock['Current Price'] >= min_price and
            (not positive_return or stock['250-Day Return'] > 0)):
            filtered.append(stock)
    
    # Sort by market cap (descending)
    filtered.sort(key=lambda x: x['Market Cap (B)'], reverse=True)
    
    return filtered

def print_table(data, headers):
    """
    Print data in a formatted table
    """
    # Calculate column widths
    col_widths = {}
    for header in headers:
        col_widths[header] = len(header)
    
    for row in data:
        for header in headers:
            value = str(row[header])
            col_widths[header] = max(col_widths[header], len(value))
    
    # Print headers
    header_row = ""
    for header in headers:
        header_row += f"{header:{col_widths[header]}} | "
    print(header_row)
    
    # Print separator
    separator = ""
    for header in headers:
        separator += "-" * col_widths[header] + "-+-"
    print(separator)
    
    # Print data
    for row in data:
        data_row = ""
        for header in headers:
            value = row[header]
            
            # Format numbers
            if header == 'Current Price':
                value = f"${value:.2f}"
            elif header == 'Market Cap (B)':
                value = f"${value:.2f}B"
            elif header == '250-Day Return':
                value = f"{value:.2f}%"
            
            data_row += f"{value:{col_widths[header]}} | "
        print(data_row)

def save_to_csv(data, filename):
    """
    Save data to a CSV file
    """
    if not data:
        return
    
    headers = data[0].keys()
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

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
    stocks = get_stock_data(selected_tickers)
    
    if not stocks:
        print("No data was retrieved. Please try again.")
        return
    
    # Apply filters
    print("\nApplying filters:")
    print(f"- Market Cap >= ${min_market_cap} billion")
    print(f"- Current Price >= ${min_price}")
    if positive_return:
        print("- 250-Day Return > 0%")
    
    filtered_stocks = filter_stocks(stocks, min_market_cap, min_price, positive_return)
    
    # Display results
    print(f"\nFound {len(filtered_stocks)} stocks matching your criteria:")
    
    headers_to_display = ['Ticker', 'Company Name', 'Current Price', 'Market Cap (B)', '250-Day Return', 'Sector']
    print_table(filtered_stocks, headers_to_display)
    
    # Show statistics
    if filtered_stocks:
        print("\nStatistics:")
        avg_market_cap = sum(stock['Market Cap (B)'] for stock in filtered_stocks) / len(filtered_stocks)
        avg_return = sum(stock['250-Day Return'] for stock in filtered_stocks) / len(filtered_stocks)
        max_market_cap = max(stock['Market Cap (B)'] for stock in filtered_stocks)
        max_return = max(stock['250-Day Return'] for stock in filtered_stocks)
        
        print(f"Average Market Cap: ${avg_market_cap:.2f}B")
        print(f"Average 250-Day Return: {avg_return:.2f}%")
        print(f"Highest Market Cap: ${max_market_cap:.2f}B")
        print(f"Highest 250-Day Return: {max_return:.2f}%")
    
    # Save to CSV
    save_option = input("\nDo you want to save the results to a CSV file? (y/n): ")
    if save_option.lower() == 'y':
        filename = "stock_screener_results.csv"
        save_to_csv(filtered_stocks, filename)
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    main()