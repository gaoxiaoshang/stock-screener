# Online Deployment Guide for Stock Screener

This guide will help you deploy your Stock Screener application online so you can share it with others via a public URL.

## Files Ready for Deployment

You now have all the necessary files for deployment:

- `streamlit_stock_screener.py`: The main application file
- `stock_tickers.py`: Contains the list of stock tickers
- `requirements.txt`: Lists the required Python packages
- `.streamlit/config.toml`: Streamlit configuration
- `setup.sh`: Setup script for deployment
- `Procfile`: Used by platforms like Heroku
- `.gitignore`: Specifies files to exclude from version control

## Step-by-Step Deployment Guide

### Option 1: Deploy to Streamlit Cloud (Recommended)

1. **Create a GitHub repository**:
   - Go to [GitHub](https://github.com) and create a new repository
   - Initialize the repository locally and push your code:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/stock-screener.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch (main), and set the main file path to `streamlit_stock_screener.py`
   - Click "Deploy"
   - After a few minutes, your app will be available at a URL like: 
     `https://yourusername-stock-screener-streamlit-stock-screener.streamlit.app`

### Option 2: Deploy to Render

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `streamlit run streamlit_stock_screener.py --server.port $PORT`
   - Choose a free instance type
   - Click "Create Web Service"

3. **Access your deployed application** at the URL provided by Render

### Option 3: Deploy to Heroku

1. **Create a Heroku account** at [heroku.com](https://heroku.com) and install the Heroku CLI

2. **Deploy to Heroku**:
   ```bash
   heroku login
   heroku create your-stock-screener
   git push heroku main
   ```

3. **Access your deployed application** at `https://your-stock-screener.herokuapp.com`

## Sharing Your Application

Once deployed, you'll get a public URL that you can share with anyone. They can access your Stock Screener application from any device with an internet connection.

## Example Deployment

Here's what your deployed application will look like:

1. Users visit your application URL
2. They see the Stock Screener interface with filter options
3. They can adjust filters for market cap, price, and 250-day returns
4. After clicking "筛选股票", they see a table of filtered stocks
5. Statistics are displayed below the table
6. They can download the results as a CSV file

## Maintenance

Your application will remain online as long as the hosting service is active. If you make changes to your code, you'll need to push the changes to GitHub and redeploy (or set up automatic deployments).

## Getting Help

If you encounter any issues during deployment:
- Check the deployment logs on your chosen platform
- Ensure all required files are included in your repository
- Verify that your `requirements.txt` file includes all necessary dependencies
- Make sure your application runs correctly locally before deploying