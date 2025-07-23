# Deployment Instructions for Stock Screener

Follow these steps to deploy your Stock Screener application online so others can access it.

## Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud is a free hosting service specifically designed for Streamlit applications.

1. **Create a GitHub repository**:
   - Create a new repository on GitHub
   - Push your code to the repository:
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
   - Your app will be available at a URL like: `https://yourusername-stock-screener-streamlit-stock-screener.streamlit.app`

## Option 2: Render

Render is another platform that offers free hosting for web applications.

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `streamlit run streamlit_stock_screener.py --server.port $PORT`
   - Choose a free instance type
   - Click "Create Web Service"

3. **Access your deployed application** at the URL provided by Render

## Option 3: Heroku

Heroku is another popular platform for hosting web applications.

1. **Create a Procfile** (if not already created):
   ```
   web: streamlit run streamlit_stock_screener.py --server.port $PORT
   ```

2. **Create a Heroku account** and install the Heroku CLI

3. **Deploy to Heroku**:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. **Access your deployed application** at `https://your-app-name.herokuapp.com`

## Option 4: Share via Streamlit's Built-in Sharing Feature

For temporary sharing during development:

1. **Run your Streamlit app locally**:
   ```bash
   streamlit run streamlit_stock_screener.py
   ```

2. **Click the "Share" button** in the top-right corner of your Streamlit app

3. **Get a temporary URL** that others can use to access your app while it's running on your machine

## After Deployment

Once deployed, share the URL with others so they can access your Stock Screener application online. The application will run in the cloud and be accessible to anyone with the link.

For example, if deployed on Streamlit Cloud, your link might look like:
`https://yourusername-stock-screener-streamlit-stock-screener.streamlit.app`