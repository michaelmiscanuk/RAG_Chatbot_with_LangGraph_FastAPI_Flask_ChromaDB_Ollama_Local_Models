# � CRITICAL: You are missing the Ollama Service!

## The Problem
You said: *"I dont know ehere is OLLAMA service. I have this one service in railway now callled summarizer_agent_langgraph"*

**This is the root cause.**
You only have **ONE** service (the backend). You need **TWO** services.
1.  `backend` (Your Python API)
2.  `ollama` (The AI Model Server)

Your backend is trying to connect to `ollama`, but `ollama` **does not exist**. That is why you get `Connection refused`.

## 🛠️ The Fix: Create the Ollama Service

You need to manually create the second service in Railway.

### Step 1: Add a New Service
1.  Go to your Railway Project Dashboard.
2.  Click the **+ New** button (top right or big card).
3.  Select **Empty Service**.
4.  Click on the new service (it might be named randomly).
5.  Go to **Settings** -> **General** -> **Service Name**.
6.  Rename it to `ollama`.

### Step 2: Configure the Ollama Service
1.  **Source Code**:
    *   Go to **Settings** -> **Source**.
    *   Click **Connect Repo**.
    *   Select your `summarizer_agent_langgraph` repo.
2.  **Root Directory**:
    *   Set **Root Directory** to `backend`.
3.  **Dockerfile**:
    *   Set **Custom Dockerfile** to `Dockerfile.ollama`.
    *   *(This is CRITICAL. It tells Railway to use the Ollama setup, not Python)*.

### Step 3: Add Variables to Ollama Service
Go to the **Variables** tab in your new `ollama` service and add:
*   `OLLAMA_HOST` = `0.0.0.0:11434`
*   `OLLAMA_ORIGINS` = `*`
*   `PORT` = `11434`

### Step 4: Connect Backend to Ollama
1.  Go back to your **Backend** service (the Python one).
2.  Go to **Variables**.
3.  Update `OLLAMA_HOST` to:
    `http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434`
    *(Copy this exactly. Railway will replace the `${{...}}` part with the real internal address)*.

### Step 5: Redeploy
1.  Redeploy **Ollama** first. Wait for it to say "Model ready" in the logs (might take 2-3 mins).
2.  Redeploy **Backend**.

## ❓ Why didn't `railway.yaml` work?
Railway sometimes ignores the multi-service YAML if you already created a single-service project. The manual steps above are the most reliable way to fix it now.

---
# �🚀 Ollama on Railway - Complete Setup Guide

This guide explains how to deploy Ollama with the qwen2.5-coder:0.5b model on Railway alongside your backend API.

## 🎯 Overview

We're deploying **two separate Railway services**:
1. **Backend API** - Your FastAPI application
2. **Ollama Service** - Ollama LLM inference server with qwen2.5-coder:0.5b model

These services communicate over Railway's private network for security and performance.

## ⚠️ Important Limitations

**Railway runs on CPU only** - No GPU support is available.
- The qwen2.5-coder:0.5b model (0.5B parameters, ~494MB) is specifically chosen because it runs acceptably on CPU
- Expected inference speed: **5-15 tokens/second** on Railway's CPU
- Larger models will be too slow for production use

## 📁 Files Created

### 1. `Dockerfile.ollama`
Docker container that:
- Installs Ollama
- Automatically pulls the qwen2.5-coder:0.5b model on startup
- Runs Ollama server in the background

```dockerfile
FROM ollama/ollama:latest

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create startup script that pulls the model and starts Ollama
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama server in background..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
sleep 5\n\
echo "Pulling qwen2.5-coder:0.5b model..."\n\
ollama pull qwen2.5-coder:0.5b\n\
echo "Model ready! Ollama is running on port 11434"\n\
wait $OLLAMA_PID\n\
' > /usr/local/bin/start-ollama.sh && chmod +x /usr/local/bin/start-ollama.sh

EXPOSE 11434

CMD ["/usr/local/bin/start-ollama.sh"]
```

### 2. `railway-multi.yaml`
Multi-service Railway configuration:

```yaml
services:
  backend:
    source: backend
    build:
      dockerfile: Dockerfile
    env:
      PORT: 8000
      OLLAMA_HOST: http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434
      RELOAD: false
    healthcheckPath: /health
    
  ollama:
    source: backend
    build:
      dockerfile: Dockerfile.ollama
    env:
      OLLAMA_HOST: 0.0.0.0:11434
      OLLAMA_ORIGINS: "*"
    volumes:
      - /root/.ollama
    healthcheckPath: /
```

### 3. Updated `src/config/models.py`
Now reads `OLLAMA_HOST` environment variable from Railway:

```python
self.base_url = base_url or os.getenv(
    "OLLAMA_HOST", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)
```

## 🛠️ Deployment Steps

### Option A: Railway CLI (Recommended)

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Deploy Both Services**
   ```bash
   cd backend
   
   # Deploy the main backend
   railway up
   
   # Deploy Ollama service
   railway up --service ollama
   ```

3. **Set Environment Variables**
   Railway will automatically set `OLLAMA_HOST` using service references.
   Verify in Railway dashboard: `Settings > Variables`

### Option B: Railway Dashboard (Manual)

1. **Create Project**
   - Go to https://railway.app/new
   - Click "Empty Project"
   - Name it "summarizer-agent-langgraph"

2. **Deploy Backend Service**
   - Click "New" → "GitHub Repo"
   - Select your repository
   - Set root directory: `backend`
   - Railway will detect Dockerfile automatically
   - Add environment variables:
     ```
     PORT=8000
     RELOAD=false
     ```

3. **Deploy Ollama Service**
   - Click "New" → "Empty Service"
   - Name it "ollama"
   - Settings → Connect your GitHub repo
   - Set root directory: `backend`
   - Set custom Dockerfile: `Dockerfile.ollama`
   - Add environment variables:
     ```
     OLLAMA_HOST=0.0.0.0:11434
     OLLAMA_ORIGINS=*
     ```
   - Add volume: `/root/.ollama` (to persist models)

4. **Connect Services**
   - Go to backend service settings
   - Add variable: `OLLAMA_HOST` = `http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434`
   - This creates private network connection between services

## 🔍 Verification

### 1. Check Ollama Service Logs
```
Starting Ollama server in background...
Pulling qwen2.5-coder:0.5b model...
pulling manifest
pulling 3f8eb4da87fa... 100% ▕████████████████▏ 394 MB
Model ready! Ollama is running on port 11434
```

### 2. Test Ollama Endpoint
```bash
# From Railway shell (backend service):
curl http://ollama.railway.internal:11434/api/tags

# Should return:
{"models":[{"name":"qwen2.5-coder:0.5b",...}]}
```

### 3. Test Backend API
```bash
curl https://your-backend.railway.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Test message", "model_name": "qwen2.5-coder:0.5b"}'
```

## 📊 Expected Performance

### CPU Inference Metrics
- **Model Size**: 494 MB (0.5B parameters)
- **Inference Speed**: 5-15 tokens/second on Railway CPU
- **Cold Start**: ~10-20 seconds (model loads on first request)
- **Memory Usage**: ~1-2 GB RAM

### Compared to GPU
| Metric | CPU (Railway) | GPU (T4) |
|--------|---------------|----------|
| Tokens/sec | 5-15 | 80-120 |
| Cold Start | 10-20s | 3-5s |
| Cost/month | ~$5 | ~$100 |

## 🐛 Troubleshooting

### Issue: "Connection refused" to Ollama
**Cause**: Backend trying to connect before Ollama is ready
**Solution**: 
- Check Ollama logs for "Model ready!" message
- Increase startup delay in Dockerfile.ollama (change `sleep 5` to `sleep 10`)
- Verify `OLLAMA_HOST` environment variable is set correctly

### Issue: Model pulls slowly
**Cause**: Railway's network bandwidth
**Solution**: 
- First deployment will be slow (~2-3 minutes to pull 394MB)
- Use volumes to persist models between deploys
- Model only needs to be pulled once

### Issue: Inference is too slow
**Cause**: CPU-only inference
**Solutions**:
- ✅ Use smaller models (0.5B is already the smallest)
- ✅ Increase Railway plan for more CPU power
- ✅ Consider streaming responses for better UX
- ❌ Don't use larger models (1B+) on CPU

### Issue: Container crashes with OOM
**Cause**: Not enough memory for model
**Solution**: 
- Upgrade Railway plan (Hobby: 8GB RAM, Pro: 32GB RAM)
- qwen2.5-coder:0.5b needs ~2GB RAM minimum

## 🔒 Security Notes

1. **Private Network**: Services communicate over Railway's private network
2. **No Public Ollama**: Ollama service is not exposed to the internet
3. **CORS Protected**: Backend API only accepts requests from your Vercel frontend
4. **Environment Variables**: Sensitive configs stored securely in Railway

## 💰 Cost Estimation

### Railway Hobby Plan ($5/month)
- Backend API: ~$2.50/month
- Ollama Service: ~$2.50/month
- **Total: $5/month** (includes 500 hours of compute)

### Railway Pro Plan ($20/month)
- Unlimited compute hours
- More CPU/RAM for faster inference
- Better for production workloads

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app/)
- [Ollama Docker Hub](https://hub.docker.com/r/ollama/ollama)
- [qwen2.5-coder Model Card](https://ollama.com/library/qwen2.5-coder)
- [LangChain Ollama Integration](https://python.langchain.com/docs/integrations/llms/ollama)

## 🎉 Next Steps

After deployment:
1. Update frontend to use new backend URL
2. Test full flow: Frontend → Backend → Ollama
3. Monitor performance in Railway dashboard
4. Consider implementing response streaming for better UX
5. Set up alerts for service health

## ⚡ Alternative: Railway Ollama Template

Railway offers a **one-click Ollama template**:
1. Go to https://railway.app/template/ollama
2. Click "Deploy Now"
3. Configure model to pull: `qwen2.5-coder:0.5b`
4. Connect to your backend via private network

**Note**: This template is simpler but less customizable than our Docker setup.

---

**Questions?** Check Railway logs, Ollama documentation, or create an issue in the repo!
