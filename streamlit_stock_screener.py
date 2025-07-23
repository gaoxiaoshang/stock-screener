import streamlit as st
import pandas as pd
import random
import time
from stock_tickers import TICKERS

# Page configuration
st.set_page_config(
    page_title="股票智能筛选器",
    page_icon="📈",
    layout="wide"
)

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
    
    return pd.DataFrame(data)

# Filter stocks based on criteria
def filter_stocks(df, min_market_cap=2.0, min_price=10.0, positive_return=True):
    """
    Filter stocks based on criteria
    """
    # Apply filters
    filtered_df = df[
        (df['Market Cap (B)'] >= min_market_cap) &
        (df['Current Price'] >= min_price)
    ]
    
    if positive_return:
        filtered_df = filtered_df[filtered_df['250-Day Return'] > 0]
    
    # Sort by market cap (descending)
    filtered_df = filtered_df.sort_values(by='Market Cap (B)', ascending=False)
    
    return filtered_df

# Main function
def main():
    # Title and description
    st.title("股票智能筛选器")
    st.markdown("""
    这个应用程序可以帮助您根据市值、价格和表现筛选股票。
    """)
    
    # Sidebar filters
    st.sidebar.header("筛选条件")
    
    # Number of stocks to analyze
    num_stocks = st.sidebar.slider(
        "分析股票数量",
        min_value=10,
        max_value=len(TICKERS),
        value=50,
        step=10
    )
    
    # Market Cap filter
    min_market_cap = st.sidebar.slider(
        "最小市值 (十亿美元)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.5
    )
    
    # Price filter
    min_price = st.sidebar.slider(
        "最小股价 (美元)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=1.0
    )
    
    # 250-day return filter
    positive_return = st.sidebar.checkbox("只显示250天涨幅为正的股票", value=True)
    
    # Fetch data button
    if st.sidebar.button("筛选股票"):
        with st.spinner("正在获取股票数据，请稍候..."):
            # Use only the selected number of stocks
            selected_tickers = TICKERS[:num_stocks]
            
            # Generate and filter stock data
            progress_bar = st.progress(0)
            for i in range(101):
                # Update progress bar
                progress_bar.progress(i)
                time.sleep(0.01)
            
            df = generate_mock_stock_data(selected_tickers)
            filtered_df = filter_stocks(df, min_market_cap, min_price, positive_return)
            
            # Store in session state
            st.session_state.filtered_df = filtered_df
            st.session_state.all_df = df
            
            # Clear progress bar
            progress_bar.empty()
    
    # Display results
    if 'filtered_df' in st.session_state:
        st.header("筛选结果")
        st.write(f"找到 {len(st.session_state.filtered_df)} 支符合条件的股票")
        
        # Display the filtered stocks
        st.dataframe(
            st.session_state.filtered_df,
            column_config={
                "Ticker": st.column_config.TextColumn("股票代码"),
                "Company Name": st.column_config.TextColumn("公司名称"),
                "Current Price": st.column_config.NumberColumn("当前价格 ($)", format="$%.2f"),
                "Market Cap (B)": st.column_config.NumberColumn("市值 ($B)", format="$%.2f"),
                "250-Day Return": st.column_config.NumberColumn("250天涨幅 (%)", format="%.2f%%"),
                "Sector": st.column_config.TextColumn("行业"),
                "Industry": st.column_config.TextColumn("子行业"),
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Show statistics
        st.header("统计数据")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "平均市值", 
                f"${st.session_state.filtered_df['Market Cap (B)'].mean():.2f}B"
            )
        
        with col2:
            st.metric(
                "平均250天涨幅", 
                f"{st.session_state.filtered_df['250-Day Return'].mean():.2f}%"
            )
        
        with col3:
            st.metric(
                "最高市值", 
                f"${st.session_state.filtered_df['Market Cap (B)'].max():.2f}B"
            )
        
        with col4:
            st.metric(
                "最高250天涨幅", 
                f"{st.session_state.filtered_df['250-Day Return'].max():.2f}%"
            )
        
        # Download button
        csv = st.session_state.filtered_df.to_csv(index=False)
        st.download_button(
            label="下载CSV文件",
            data=csv,
            file_name="stock_screener_results.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()