# 🚀 Complete Setup Guide

This guide will walk you through setting up and running the full-stack Text Analysis application locally and deploying it to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Testing Locally](#testing-locally)
4. [Deployment](#deployment)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
  ```bash
  python --version  # Should show 3.11 or higher
  ```

- **Git** ([Download](https://git-scm.com/downloads))
  ```bash
  git --version
  ```

- **Ollama** ([Download](https://ollama.ai/download))
  ```bash
  ollama --version
  ```

### Optional Tools

- **Vercel CLI** (for frontend deployment)
  ```bash
  npm install -g vercel
  ```

- **Visual Studio Code** (recommended editor)

### Accounts Needed for Deployment

- [GitHub Account](https://github.com) (free)
- [Vercel Account](https://vercel.com) (free tier available)
- [Render Account](https://render.com) (free tier available)

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd langgraph_test1
```

### Step 2: Set Up Backend

#### 2.1 Navigate to Backend

```bash
cd backend
```

#### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

#### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2.4 Set Up Ollama

**In a separate terminal:**

```bash
# Start Ollama server
ollama serve
```

**Pull a model:**
```bash
ollama pull qwen2.5-coder:0.5b
```

**Verify it works:**
```bash
ollama list  # Should show qwen2.5-coder:0.5b
```

#### 2.5 Test Backend

```bash
# Start the API
python api.py
```

**In another terminal, test it:**
```bash
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

**View API documentation:**
Open browser: `http://localhost:8000/docs`

### Step 3: Set Up Frontend

#### 3.1 Navigate to Frontend (New Terminal)

```bash
cd frontend
```

#### 3.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

#### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3.4 Configure Environment

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

**Edit `.env` file:**
```env
API_BASE_URL=http://localhost:8000
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
```

#### 3.5 Start Frontend

```bash
python app.py
```

Frontend should start at: `http://localhost:5000`

### Step 4: Alternative - Use Quick Start Scripts (Windows)

We've created convenient scripts for you!

**Backend:**
```bash
cd backend
start.bat
```

**Frontend (new terminal):**
```bash
cd frontend
start.bat
```

## Testing Locally

### 1. Open the Application

Navigate to: `http://localhost:5000`

### 2. Test Basic Functionality

1. **Enter sample text** in the textarea
2. **Select a model** from the dropdown
3. **Click "Analyze Text"**
4. **View results**: Summary and sentiment

### 3. Test Sample Texts

Click one of the "Try these samples" buttons to auto-fill the textarea with example text.

### 4. Test Error Handling

- **Empty text**: Try submitting without text
- **Long text**: Enter more than 10,000 characters
- **Backend down**: Stop backend and try analyzing

### 5. Test API Directly

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Analyze Text:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is amazing! I absolutely love this product. It exceeded all my expectations.",
    "model_name": "qwen2.5-coder:0.5b"
  }'
```

**List Models:**
```bash
curl http://localhost:8000/api/models
```

### 6. Check API Documentation

Open: `http://localhost:8000/docs`

Try the interactive API documentation!

## Deployment

### Deploying Backend to Render.com

#### Step 1: Prepare Repository

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Add backend and frontend"
   git push origin main
   ```

#### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up (free)
3. Connect your GitHub account

#### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. **Select your repository**
3. **Configure:**
   - **Name**: `text-analysis-backend`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables:**
   - Add: `PYTHON_VERSION` = `3.11.0`

5. Click **"Create Web Service"**

#### Step 4: Wait for Deployment

- Initial deployment takes 5-10 minutes
- Watch the logs for any errors
- Once deployed, you'll get a URL like: `https://your-app.onrender.com`

#### Step 5: Test Backend

```bash
curl https://your-app.onrender.com/health
```

**Important Note**: The free tier spins down after 15 minutes of inactivity. First request after spin-down will take 30-60 seconds.

### Deploying Frontend to Vercel

#### Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

#### Step 2: Deploy

**Method A: Using Vercel CLI**

```bash
cd frontend
vercel login
vercel
```

Follow the prompts.

**Method B: Using Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New..."** → **"Project"**
3. **Import your GitHub repository**
4. **Configure:**
   - **Framework Preset**: `Other`
   - **Root Directory**: `frontend`
   - **Build Command**: (leave default)
   - **Output Directory**: (leave default)

5. **Environment Variables:**
   - `API_BASE_URL`: `https://your-backend.onrender.com`
   - `SECRET_KEY`: (generate random string)
   - `FLASK_ENV`: `production`

6. Click **"Deploy"**

#### Step 3: Update Backend CORS

After frontend is deployed, update `backend/api.py`:

```python
allow_origins=[
    "https://your-frontend.vercel.app",  # Your Vercel URL
    "http://localhost:5000",
]
```

Commit and push:
```bash
git add backend/api.py
git commit -m "Update CORS for production"
git push origin main
```

Render will auto-deploy the update.

#### Step 4: Test Production

Visit your Vercel URL and test the application!

## Troubleshooting

### Backend Issues

#### "Cannot connect to Ollama"

**Problem**: Backend can't reach Ollama

**Solutions**:
1. Make sure Ollama is running: `ollama serve`
2. Check Ollama is on port 11434
3. Try: `curl http://localhost:11434/api/tags`
4. Restart Ollama if needed

#### "Module not found" errors

**Problem**: Dependencies not installed

**Solutions**:
```bash
cd backend
pip install -r requirements.txt
```

#### "Port already in use"

**Problem**: Port 8000 is occupied

**Solutions**:
1. Stop other services on port 8000
2. Or modify `api.py` to use different port

### Frontend Issues

#### "Cannot connect to backend API"

**Problem**: Frontend can't reach backend

**Solutions**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify `.env` has correct `API_BASE_URL`
3. Check CORS settings in backend
4. Check firewall/antivirus

#### "Flask not found"

**Problem**: Dependencies not installed

**Solutions**:
```bash
cd frontend
pip install -r requirements.txt
```

### Deployment Issues

#### Render: Build fails

**Common causes**:
1. Wrong Python version
2. Missing dependencies
3. Wrong start command

**Solutions**:
1. Check logs in Render dashboard
2. Verify `requirements.txt` is complete
3. Ensure start command is: `uvicorn api:app --host 0.0.0.0 --port $PORT`

#### Vercel: Deployment fails

**Common causes**:
1. Wrong root directory
2. Missing environment variables
3. Python version issues

**Solutions**:
1. Verify root directory is `frontend`
2. Check all environment variables are set
3. Review build logs

#### CORS errors in production

**Problem**: Frontend can't call backend due to CORS

**Solutions**:
1. Add frontend URL to `allow_origins` in `backend/api.py`
2. Redeploy backend
3. Clear browser cache

### Performance Issues

#### "Analysis is slow"

**Solutions**:
1. Use faster model: `qwen2.5-coder:0.5b`
2. Reduce text length
3. Upgrade Render plan (free tier is slower)
4. Check Ollama performance

#### "Cold starts taking too long"

**Problem**: Render free tier spins down

**Solutions**:
1. Upgrade to Starter plan ($7/month)
2. Or accept 30-60s cold start on free tier
3. Consider using hosted LLM instead of Ollama

## Next Steps

### After Setup

1. ✅ Test everything locally
2. ✅ Deploy backend to Render
3. ✅ Deploy frontend to Vercel
4. ✅ Test production deployment
5. ✅ Share your URL!

### Customization

- **Change colors**: Edit `frontend/static/css/style.css`
- **Add models**: Edit `backend/src/config/models.py`
- **Modify workflow**: Edit `backend/src/graph/nodes.py`
- **Update UI**: Edit templates in `frontend/templates/`

### Monitoring

- **Backend logs**: Render dashboard → Logs
- **Frontend logs**: Vercel dashboard → Deployments → View Logs
- **API docs**: `https://your-backend.onrender.com/docs`

## Need Help?

1. Check the error message carefully
2. Review logs in Render/Vercel dashboards
3. Test each component separately
4. Try the troubleshooting steps above
5. Check documentation:
   - [Backend Deployment](backend/DEPLOYMENT.md)
   - [Frontend README](frontend/README.md)
   - [Main README](README_FULLSTACK.md)

## Success! 🎉

If you've made it this far and everything works, congratulations! You now have:

- ✅ A beautiful frontend deployed on Vercel
- ✅ A powerful backend deployed on Render
- ✅ AI-powered text analysis at your fingertips
- ✅ A production-ready full-stack application

**Share your creation and happy analyzing!** 🚀
