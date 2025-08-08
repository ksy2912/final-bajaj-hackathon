# 🚀 Quick Deployment Guide

## 🎯 **EASIEST WAY: Railway.app (5 minutes)**

### Step 1: Prepare Your Code
```bash
# Make sure all files are in your project folder
ls
# Should show: main.py, requirements.txt, README.md, etc.
```

### Step 2: Push to GitHub
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for deployment"

# Push to GitHub (replace with your repo URL)
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### Step 3: Deploy to Railway
1. **Go to [Railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway will automatically detect it's a Python app**

### Step 4: Set Environment Variables
1. **In Railway dashboard, go to "Variables" tab**
2. **Add new variable:**
   - **Name**: `GOOGLE_API_KEY`
   - **Value**: `your_google_api_key_here`

### Step 5: Deploy
- **Railway will automatically build and deploy**
- **Your API will be live in 2-3 minutes**
- **URL will be: `https://your-app-name.railway.app`**

### Step 6: Test Your Deployment
```bash
# Test health endpoint
curl https://your-app-name.railway.app/

# Test main endpoint
curl -X POST "https://your-app-name.railway.app/hackrx/run" \
  -H "Authorization: Bearer 407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": ["What is the grace period for premium payment?"]
  }'
```

## 🎉 **That's it! Your API is live!**

### 📊 **What You Get**
- ✅ **Production-ready API**
- ✅ **Automatic HTTPS**
- ✅ **Free hosting**
- ✅ **Automatic deployments**
- ✅ **Easy scaling**

### 🔗 **Your API Endpoints**
- **Health Check**: `https://your-app-name.railway.app/`
- **API Docs**: `https://your-app-name.railway.app/docs`
- **Main Endpoint**: `https://your-app-name.railway.app/hackrx/run`

### 🧪 **Testing in Browser**
1. **Open**: `https://your-app-name.railway.app/docs`
2. **Click "Authorize"**
3. **Enter token**: `407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9`
4. **Test the `/hackrx/run` endpoint**

---

## 🆘 **Need Help?**

### Common Issues:
1. **"Git not found"** → Install Git from [git-scm.com](https://git-scm.com)
2. **"Repository not found"** → Make sure you pushed to GitHub first
3. **"Build failed"** → Check that `requirements.txt` exists and is correct
4. **"API key error"** → Make sure `GOOGLE_API_KEY` is set in Railway variables

### Support:
- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **GitHub Issues**: Create an issue in your repository
- **Stack Overflow**: Search for "Railway deployment issues"

---

## 🎯 **Alternative: Render.com**

If Railway doesn't work, try Render:

1. **Go to [Render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect your GitHub repo**
5. **Set build command**: `pip install -r requirements.txt`
6. **Set start command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. **Add environment variable**: `GOOGLE_API_KEY`
8. **Deploy!**

---

**Happy Deploying! 🚀**
