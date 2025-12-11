# 🔧 Railway Configuration Fix - Root Directory Issue

## ❌ The Problem

Railway's Railpack is trying to build from the **root directory** but your Python app is in the **backend folder**. This causes the error:

```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

## ✅ Solution: Configure Root Directory in Railway Dashboard

### **Option 1: Railway Dashboard (Recommended)**

1. **Go to Railway Dashboard**
   - Open https://railway.app/dashboard
   - Select your project: `summarizer-agent-langgraph`
   - Click on your service (backend or the service that's failing)

2. **Set Root Directory**
   - Click **Settings** (left sidebar)
   - Scroll to **Build & Deploy** section
   - Find **Root Directory** field
   - Set it to: `backend`
   - Click **Save**

3. **Set Watch Paths (Optional but Recommended)**
   - Still in Settings → Build & Deploy
   - Find **Watch Paths** field
   - Set it to: `backend/**`
   - This ensures Railway only rebuilds when backend files change
   - Click **Save**

4. **Trigger Redeploy**
   - Click **Deployments** (left sidebar)
   - Click the **⋯** menu on the latest deployment
   - Click **Redeploy**

### **Option 2: Railway CLI with Service Configuration**

If you're deploying via CLI, you need to specify the service configuration:

```cmd
# Navigate to your project root
cd e:\OneDrive\Knowledge Base\0207_GenAI\Code\langgraph_test1

# Link to your Railway project
railway link

# Set the root directory for your service
railway service root backend

# Deploy
railway up
```

### **Option 3: Use Railway's Multi-Service YAML**

Create a `railway.yaml` file in the **root directory**:

```yaml
# railway.yaml
services:
  backend:
    # Set the source to backend folder
    source: backend
    
    build:
      # Nixpacks will auto-detect Python
      builder: NIXPACKS
    
    deploy:
      startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT --log-level info
      healthcheckPath: /health
      healthcheckTimeout: 100
      restartPolicyType: ON_FAILURE
      restartPolicyMaxRetries: 10
    
    env:
      PORT: 8000
      RELOAD: false
      PYTHON_VERSION: 3.12
```

Then deploy:
```cmd
railway up --service backend
```

## 🎯 **Quick Fix (Right Now)**

**Follow these exact steps:**

1. Open Railway Dashboard: https://railway.app/dashboard
2. Click your project
3. Click your backend service
4. Click **Settings** (left sidebar)
5. Scroll to **Root Directory**
6. Type: `backend`
7. Click **Save Changes**
8. Go to **Deployments** → Click ⋯ → **Redeploy**

**That's it!** Railway will now build from the `backend` folder and detect your Python app correctly.

## 📊 What Railway Should Detect

After setting the root directory correctly, Railway should show:

```
✓ Detected Python app
✓ Found pyproject.toml
✓ Installing dependencies with Poetry
✓ Building...
✓ Starting uvicorn server
```

## 🔍 Verify Configuration

After deployment, check the build logs. You should see:

```
╭─────────────────╮
│ Nixpacks 1.x.x  │
╰─────────────────╯

✓ Detected Python 3.12
✓ Found pyproject.toml
✓ Installing Poetry
✓ Installing dependencies
✓ Build complete
```

## 🐛 If It Still Fails

### Check 1: Verify Root Directory
```cmd
railway service
```
Should show: `Root directory: backend`

### Check 2: Check for Dockerfile
If Railway finds a `Dockerfile` in the backend folder, it will use that instead of Nixpacks. That's fine! Make sure you have:

```dockerfile
# backend/Dockerfile should exist
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Check 3: Verify pyproject.toml exists
```cmd
dir backend\pyproject.toml
```
Should exist and contain your dependencies.

### Check 4: Force Nixpacks
If you want to force Nixpacks instead of Docker:
1. Railway Dashboard → Settings → Build & Deploy
2. Set **Builder**: `NIXPACKS`
3. Remove or rename `backend/Dockerfile` temporarily

## 📚 Railway Documentation

- [Root Directory Configuration](https://docs.railway.app/deploy/deployments#root-directory)
- [Python Deployment Guide](https://docs.railway.app/languages/python)
- [Nixpacks Documentation](https://nixpacks.com/docs)

---

## ✅ Summary

**The Fix:**
- Set **Root Directory** to `backend` in Railway Dashboard → Settings
- Redeploy

**Why This Works:**
- Railway will now look for your Python app in `backend/` folder
- It will find `pyproject.toml` and know it's a Python app
- Nixpacks will auto-configure everything

**Time to Fix:** 30 seconds ⚡
