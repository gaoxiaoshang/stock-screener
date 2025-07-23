# Deploying Your Stock Screener to GitHub Pages

Follow these steps to deploy your stock screener to GitHub Pages and get a shareable link:

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in to your account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Name your repository (e.g., "stock-screener")
4. Make sure the repository is set to "Public"
5. Click "Create repository"

## Step 2: Push Your Code to GitHub

Open a terminal and run the following commands:

```bash
# Initialize a Git repository
git init

# Add all files to the repository
git add .

# Commit the changes
git commit -m "Initial commit"

# Set the remote repository URL
git branch -M main
git remote add origin https://github.com/yourusername/stock-screener.git

# Push the code to GitHub
git push -u origin main
```

Replace `yourusername` with your actual GitHub username.

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to the "GitHub Pages" section
4. Under "Source", select "main" branch
5. Click "Save"

## Step 4: Access Your Deployed Application

After a few minutes, your stock screener will be available at:

```
https://yourusername.github.io/stock-screener/
```

Replace `yourusername` with your GitHub username.

## Step 5: Share Your Link

You can now share this link with anyone, and they'll be able to access your stock screener application online.

## Alternative: Use a Free Hosting Service

If you prefer not to use GitHub Pages, you can use one of these free hosting services:

1. **Netlify**:
   - Sign up at [netlify.com](https://www.netlify.com/)
   - Drag and drop your project folder to deploy
   - Get a shareable link like `https://your-site-name.netlify.app`

2. **Vercel**:
   - Sign up at [vercel.com](https://vercel.com/)
   - Connect your GitHub repository
   - Get a shareable link like `https://your-site-name.vercel.app`

3. **Surge**:
   - Install Surge: `npm install -g surge`
   - Run `surge` from your project directory
   - Get a shareable link like `https://your-site-name.surge.sh`

## Note About the HTML Version

The HTML version (`index.html`) uses client-side JavaScript to generate mock stock data. This means:

1. All processing happens in the user's browser
2. No server is required
3. The data is randomly generated each time
4. It's perfect for demonstration purposes

For a production application with real stock data, you would need to use the Streamlit version and deploy it to a platform that supports Python applications.