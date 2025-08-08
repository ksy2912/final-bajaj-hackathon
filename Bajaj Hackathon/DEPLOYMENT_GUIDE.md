# 🚀 Deployment Guide - LLM-Powered Intelligent Query–Retrieval System

## 📋 Overview

This guide shows you the **easiest ways** to deploy your LLM-Powered Intelligent Query–Retrieval System to production.

## 🎯 **RECOMMENDED: Railway.app (Easiest)**

### Why Railway?
- ✅ **Free tier available**
- ✅ **Automatic deployments from GitHub**
- ✅ **Easy environment variable management**
- ✅ **No configuration needed**
- ✅ **Fast deployment**

### Step-by-Step Deployment

1. **Prepare Your Code**
   ```bash
   # Ensure all files are committed to git
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Railway**
   - Go to [https://railway.app](https://railway.app)
   - Sign up with your GitHub account
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect it's a Python app

3. **Configure Environment Variables**
   - In Railway dashboard, go to "Variables" tab
   - Add: `GOOGLE_API_KEY` = `your_google_api_key_here`
   - Add: `PORT` = `8000` (optional, Railway sets this automatically)

4. **Deploy**
   - Railway will automatically build and deploy your app
   - Your API will be live at: `https://your-app-name.railway.app`

5. **Test Your Deployment**
   ```bash
   # Test the health endpoint
   curl https://your-app-name.railway.app/
   
   # Test the main endpoint
   curl -X POST "https://your-app-name.railway.app/hackrx/run" \
     -H "Authorization: Bearer 407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
       "questions": ["What is the grace period for premium payment?"]
     }'
   ```

---

## 🥈 **ALTERNATIVE: Render.com**

### Why Render?
- ✅ **Free tier available**
- ✅ **Easy GitHub integration**
- ✅ **Automatic HTTPS**
- ✅ **Good performance**

### Step-by-Step Deployment

1. **Go to Render**
   - Visit [https://render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   - **Name**: `llm-query-retrieval`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Go to "Environment" tab
   - Add: `GOOGLE_API_KEY` = `your_google_api_key_here`

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your API will be live at: `https://your-app-name.onrender.com`

---

## 🥉 **ALTERNATIVE: Heroku**

### Why Heroku?
- ✅ **Well-established platform**
- ✅ **Good documentation**
- ✅ **Free tier (limited)**

### Step-by-Step Deployment

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your_google_api_key_here
   ```

6. **Open App**
   ```bash
   heroku open
   ```

---

## 🐳 **DOCKER DEPLOYMENT**

### For Advanced Users

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and Run**
   ```bash
   # Build image
   docker build -t llm-query-retrieval .
   
   # Run container
   docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key llm-query-retrieval
   ```

3. **Deploy to Docker Hub**
   ```bash
   # Tag image
   docker tag llm-query-retrieval your-username/llm-query-retrieval
   
   # Push to Docker Hub
   docker push your-username/llm-query-retrieval
   ```

---

## 🔧 **LOCAL PRODUCTION DEPLOYMENT**

### Using Gunicorn (Recommended for Production)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn Config**
   ```python
   # gunicorn_config.py
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "uvicorn.workers.UvicornWorker"
   timeout = 120
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -c gunicorn_config.py main:app
   ```

---

## 🧪 **TESTING YOUR DEPLOYMENT**

### 1. Health Check
```bash
curl https://your-app-url/
```

### 2. API Documentation
- Visit: `https://your-app-url/docs`
- Click "Authorize" and enter: `407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9`
- Test the `/hackrx/run` endpoint

### 3. Full API Test
```bash
curl -X POST "https://your-app-url/hackrx/run" \
  -H "Authorization: Bearer 407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
      "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
      "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
  }'
```

---

## 🔐 **ENVIRONMENT VARIABLES**

### Required Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key

### Optional Variables
- `PORT`: Port number (usually set by platform)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

---

## 📊 **DEPLOYMENT COMPARISON**

| Platform | Ease | Free Tier | Performance | Setup Time |
|----------|------|-----------|-------------|------------|
| **Railway** | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ | 5 min |
| **Render** | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ | 10 min |
| **Heroku** | ⭐⭐⭐ | ⚠️ Limited | ⭐⭐⭐ | 15 min |
| **Docker** | ⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ | 30 min |

---

## 🚨 **TROUBLESHOOTING**

### Common Issues

1. **Port Issues**
   ```bash
   # Make sure your app uses $PORT environment variable
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Dependencies Issues**
   ```bash
   # Ensure all dependencies are in requirements.txt
   pip freeze > requirements.txt
   ```

3. **Environment Variables**
   - Make sure `GOOGLE_API_KEY` is set in your deployment platform
   - Check that the key is valid and has sufficient quota

4. **Memory Issues**
   - Reduce chunk count in `main.py` if needed
   - Optimize embedding generation

---

## 🎯 **RECOMMENDED WORKFLOW**

1. **Choose Railway.app** (easiest option)
2. **Push code to GitHub**
3. **Connect repository to Railway**
4. **Set environment variables**
5. **Deploy and test**
6. **Share your API URL**

---

## 📞 **SUPPORT**

If you encounter issues:
1. Check the platform's documentation
2. Verify environment variables are set correctly
3. Check the deployment logs
4. Test locally first with `uvicorn main:app --reload`

---

**Happy Deploying! 🚀**
