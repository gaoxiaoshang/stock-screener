#!/usr/bin/env python3
"""
Web-based Stock Screener
This script creates a simple web interface for the stock screener using Python's built-in http.server.
"""

import http.server
import socketserver
import webbrowser
import json
import random
import time
import urllib.parse
from stock_tickers import TICKERS

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票智能筛选器</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="number"], select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .checkbox-group {
            margin-top: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .stats {
            margin-top: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .stat-card {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            flex: 1;
            min-width: 200px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            margin-top: 0;
            color: #333;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>股票智能筛选器</h1>
        
        <form id="screenForm">
            <div class="form-group">
                <label for="numStocks">分析股票数量:</label>
                <input type="number" id="numStocks" name="numStocks" min="10" max="100" value="50">
            </div>
            
            <div class="form-group">
                <label for="minMarketCap">最小市值 (十亿美元):</label>
                <input type="number" id="minMarketCap" name="minMarketCap" min="0" step="0.5" value="2.0">
            </div>
            
            <div class="form-group">
                <label for="minPrice">最小股价 (美元):</label>
                <input type="number" id="minPrice" name="minPrice" min="0" step="0.5" value="10.0">
            </div>
            
            <div class="form-group checkbox-group">
                <input type="checkbox" id="positiveReturn" name="positiveReturn" checked>
                <label for="positiveReturn" style="display: inline;">只显示250天涨幅为正的股票</label>
            </div>
            
            <button type="submit">筛选股票</button>
        </form>
        
        <div id="loading" class="loading">
            <div class="spinner"></div>
            <p>正在获取股票数据，请稍候...</p>
        </div>
        
        <div id="results" style="display: none;">
            <h2>筛选结果</h2>
            <p id="resultCount"></p>
            
            <table id="stockTable">
                <thead>
                    <tr>
                        <th>股票代码</th>
                        <th>公司名称</th>
                        <th>当前价格 ($)</th>
                        <th>市值 ($B)</th>
                        <th>250天涨幅 (%)</th>
                        <th>行业</th>
                    </tr>
                </thead>
                <tbody id="stockTableBody">
                    <!-- Stock data will be inserted here -->
                </tbody>
            </table>
            
            <div class="stats" id="statsSection">
                <!-- Statistics will be inserted here -->
            </div>
        </div>
    </div>

    <script>
        document.getElementById('screenForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading indicator
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            // Get form values
            const numStocks = document.getElementById('numStocks').value;
            const minMarketCap = document.getElementById('minMarketCap').value;
            const minPrice = document.getElementById('minPrice').value;
            const positiveReturn = document.getElementById('positiveReturn').checked;
            
            // Build query string
            const queryString = `?numStocks=${numStocks}&minMarketCap=${minMarketCap}&minPrice=${minPrice}&positiveReturn=${positiveReturn}`;
            
            // Fetch data from our API endpoint
            fetch('/api/screen' + queryString)
                .then(response => response.json())
                .then(data => {
                    // Hide loading indicator
                    document.getElementById('loading').style.display = 'none';
                    
                    // Show results
                    document.getElementById('results').style.display = 'block';
                    
                    // Update result count
                    document.getElementById('resultCount').textContent = 
                        `找到 ${data.filtered_stocks.length} 支符合条件的股票`;
                    
                    // Clear previous results
                    const tableBody = document.getElementById('stockTableBody');
                    tableBody.innerHTML = '';
                    
                    // Add stock rows
                    data.filtered_stocks.forEach(stock => {
                        const row = document.createElement('tr');
                        
                        row.innerHTML = `
                            <td>${stock.Ticker}</td>
                            <td>${stock['Company Name']}</td>
                            <td>$${stock['Current Price'].toFixed(2)}</td>
                            <td>$${stock['Market Cap (B)'].toFixed(2)}B</td>
                            <td>${stock['250-Day Return'].toFixed(2)}%</td>
                            <td>${stock.Sector}</td>
                        `;
                        
                        tableBody.appendChild(row);
                    });
                    
                    // Update statistics
                    const statsSection = document.getElementById('statsSection');
                    statsSection.innerHTML = '';
                    
                    if (data.stats) {
                        const stats = [
                            { name: '平均市值', value: `$${data.stats.avg_market_cap.toFixed(2)}B` },
                            { name: '平均250天涨幅', value: `${data.stats.avg_return.toFixed(2)}%` },
                            { name: '最高市值', value: `$${data.stats.max_market_cap.toFixed(2)}B` },
                            { name: '最高250天涨幅', value: `${data.stats.max_return.toFixed(2)}%` }
                        ];
                        
                        stats.forEach(stat => {
                            const statCard = document.createElement('div');
                            statCard.className = 'stat-card';
                            statCard.innerHTML = `
                                <h3>${stat.name}</h3>
                                <div class="stat-value">${stat.value}</div>
                            `;
                            statsSection.appendChild(statCard);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('loading').style.display = 'none';
                    alert('获取数据时出错，请重试。');
                });
        });
    </script>
</body>
</html>
"""

# Generate mock stock data
def generate_mock_stock_data(tickers):
    """
    Generate mock stock data for demonstration purposes
    """
    sectors = ["Technology", "Healthcare", "Finance", "Consumer Goods", "Energy", "Utilities", "Real Estate"]
    industries = ["Software", "Hardware", "Pharmaceuticals", "Banking", "Retail", "Oil & Gas", "Electric"]
    
    data = []
    
    for ticker in tickers:
        # Generate random but realistic data
        market_cap = random.uniform(0.5, 500)  # $0.5B to $500B
        current_price = random.uniform(5, 500)  # $5 to $500
        return_250d = random.uniform(-30, 70)  # -30% to +70%
        
        # Create mock stock data
        stock_data = {
            'Ticker': ticker,
            'Company Name': f"{ticker} Inc.",
            'Current Price': current_price,
            'Market Cap (B)': market_cap,
            '250-Day Return': return_250d,
            'Sector': random.choice(sectors),
            'Industry': random.choice(industries),
        }
        
        data.append(stock_data)
    
    return data

# Filter stocks based on criteria
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

# Calculate statistics
def calculate_statistics(stocks):
    """
    Calculate statistics for the filtered stocks
    """
    if not stocks:
        return None
        
    avg_market_cap = sum(stock['Market Cap (B)'] for stock in stocks) / len(stocks)
    avg_return = sum(stock['250-Day Return'] for stock in stocks) / len(stocks)
    max_market_cap = max(stock['Market Cap (B)'] for stock in stocks)
    max_return = max(stock['250-Day Return'] for stock in stocks)
    
    return {
        'avg_market_cap': avg_market_cap,
        'avg_return': avg_return,
        'max_market_cap': max_market_cap,
        'max_return': max_return
    }

# Custom HTTP request handler
class StockScreenerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the main page
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
            return
            
        # Handle API requests
        elif self.path.startswith('/api/screen'):
            # Parse query parameters
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            # Get parameters with defaults
            num_stocks = int(params.get('numStocks', ['50'])[0])
            min_market_cap = float(params.get('minMarketCap', ['2.0'])[0])
            min_price = float(params.get('minPrice', ['10.0'])[0])
            positive_return = params.get('positiveReturn', ['true'])[0].lower() == 'true'
            
            # Limit number of stocks
            num_stocks = min(num_stocks, len(TICKERS))
            selected_tickers = TICKERS[:num_stocks]
            
            # Generate and filter stock data
            stocks = generate_mock_stock_data(selected_tickers)
            filtered_stocks = filter_stocks(stocks, min_market_cap, min_price, positive_return)
            
            # Calculate statistics
            stats = calculate_statistics(filtered_stocks)
            
            # Prepare response
            response = {
                'filtered_stocks': filtered_stocks,
                'stats': stats
            }
            
            # Add a small delay to simulate API call
            time.sleep(1)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
            
        # Serve 404 for other paths
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
            return

def main():
    # Set up the server
    port = 8000
    handler = StockScreenerHandler
    
    # Try to find an available port
    while True:
        try:
            with socketserver.TCPServer(("", port), handler) as httpd:
                print(f"Starting server at http://localhost:{port}")
                # Open browser automatically
                webbrowser.open(f"http://localhost:{port}")
                # Start the server
                httpd.serve_forever()
        except OSError:
            print(f"Port {port} is in use, trying {port+1}")
            port += 1
        except KeyboardInterrupt:
            print("Server stopped.")
            break

if __name__ == "__main__":
    main()