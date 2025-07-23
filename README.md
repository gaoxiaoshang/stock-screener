# Stock Screener

A Streamlit application that screens stocks based on market capitalization, price, and performance.

## Features

- Filter stocks with market cap greater than $2 billion
- Filter stocks with positive 250-day returns
- Filter stocks with current price above $10
- View detailed information about filtered stocks
- Download filtered results as CSV

## Local Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Local Usage

Run the Streamlit application:

```bash
streamlit run streamlit_stock_screener.py
```

The application will open in your default web browser.

## Online Deployment

This application can be deployed online using Streamlit Cloud. Follow these steps:

1. Create a GitHub repository and push this code to it:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/stock-screener.git
git push -u origin main
```

2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with your GitHub account
3. Click "New app" and select your repository
4. Set the main file path to `streamlit_stock_screener.py`
5. Click "Deploy"

Your app will be available at a URL like: `https://yourusername-stock-screener-streamlit-stock-screener.streamlit.app`

## Alternative Deployment Options

### Heroku

1. Create a `Procfile` with the following content:
   ```
   web: streamlit run streamlit_stock_screener.py --server.port $PORT
   ```

2. Deploy to Heroku:
   ```bash
   heroku create
   git push heroku main
   ```

### Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `streamlit run streamlit_stock_screener.py --server.port $PORT`

## Online Demo

You can access the live demo of this application at:
[https://stock-screener-demo.streamlit.app](https://stock-screener-demo.streamlit.app)
