# 🎯 Complete Deployment Guide - Backend + Ollama on Railway

This is your **step-by-step guide** to deploy the entire summarizer app with Ollama LLM on Railway.

## 📋 What You'll Deploy

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application Stack                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (Vercel)          Backend (Railway)                │
│  ┌─────────────────┐       ┌─────────────────────────┐     │
│  │  Flask App      │──────▶│  FastAPI + LangGraph    │     │
│  │  Port: 5000     │       │  Port: 8000             │     │
│  └─────────────────┘       └──────────┬──────────────┘     │
│                                        │                      │
│                                        │ Private Network      │
│                                        ▼                      │
│                            ┌─────────────────────────┐      │
│                            │  Ollama Service         │      │
│                            │  Port: 11434            │      │
│                            │  Model: qwen2.5-coder   │      │
│                            │  Size: 494MB (0.5B)     │      │
│                            └─────────────────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Total Cost**: ~$5/month on Railway Hobby plan

## ✅ Prerequisites

Before starting, make sure you have:

- [ ] GitHub account with your code pushed
- [ ] Railway account (sign up at https://railway.app)
- [ ] Vercel account (sign up at https://vercel.com)
- [ ] Railway CLI installed: `npm i -g @railway/cli`
- [ ] Git configured and code committed

## 🚀 Deployment Steps

### Part 1: Deploy to Railway (Backend + Ollama)

#### Option A: Automated Script (Windows) 🎯 **RECOMMENDED**

```cmd
# Navigate to project root
cd e:\OneDrive\Knowledge Base\0207_GenAI\Code\langgraph_test1

# Make sure you're logged in
railway login

# Run deployment script
deploy-railway.bat
```

The script will:
1. ✅ Deploy your backend API
2. ✅ Deploy Ollama service with qwen2.5-coder:0.5b
3. ✅ Configure environment variables
4. ✅ Connect services via private network

**Expected Output:**
```
========================================
   Railway Multi-Service Deployment
========================================

[OK] Railway CLI is ready

========================================
Step 1: Deploying Backend API...
========================================

✓ Building... (30s)
✓ Deploying... (10s)
✓ Backend available at: https://summarizer-agent-langgraph-production.up.railway.app

[OK] Backend deployed successfully!

========================================
Step 2: Deploying Ollama Service...
========================================

✓ Building Ollama container... (45s)
✓ Pulling qwen2.5-coder:0.5b model... (120s)
✓ Model ready! Ollama running on :11434

[OK] Ollama service deployed!

========================================
   DEPLOYMENT COMPLETE!
========================================
```

#### Option B: Manual Railway Dashboard

<details>
<summary>Click to expand manual steps</summary>

**Step 1: Create Railway Project**
1. Go to https://railway.app/new
2. Click "Empty Project"
3. Name: "summarizer-agent-langgraph"

**Step 2: Deploy Backend Service**
1. Click "New" → "GitHub Repo"
2. Select your repository
3. Configure:
   - **Root Directory**: `backend`
   - **Dockerfile**: Will auto-detect `Dockerfile`
   - **Name**: `backend`
4. Add environment variables:
   ```
   PORT=8000
   RELOAD=false
   ```
5. Click "Deploy"

**Step 3: Deploy Ollama Service**
1. Click "New" → "Empty Service"
2. Name: `ollama`
3. Settings → "Connect Repo"
4. Select your repository
5. Configure:
   - **Root Directory**: `backend`
   - **Dockerfile**: `Dockerfile.ollama`
6. Add **Volume**:
   - Mount Path: `/root/.ollama`
   - (This persists models across deploys)
7. Add environment variables:
   ```
   OLLAMA_HOST=0.0.0.0:11434
   OLLAMA_ORIGINS=*
   ```
8. Click "Deploy"

**Step 4: Connect Services**
1. Go to `backend` service
2. Variables → Add Variable
3. Name: `OLLAMA_HOST`
4. Value: `http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434`
5. Save

</details>

#### ⏱️ Wait for Deployment

**Monitor progress:**
```cmd
# Watch backend logs
railway logs --service backend

# Watch Ollama logs (in separate terminal)
railway logs --service ollama
```

**Look for these messages:**

**Backend logs:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Ollama logs:**
```
Starting Ollama server in background...
Pulling qwen2.5-coder:0.5b model...
pulling manifest
pulling 3f8eb4da87fa... 100% ▕████████████████▏ 394 MB
pulling c38d945febe2... 100% ▕████████████████▏  29 MB
Model ready! Ollama is running on port 11434
```

⚠️ **First deployment takes 2-3 minutes** to download the model. Subsequent deploys are instant (model is cached).

### Part 2: Deploy Frontend to Vercel

```cmd
# Navigate to frontend
cd frontend

# Deploy to Vercel
vercel --prod
```

**Follow prompts:**
1. Set up and deploy? **Y**
2. Scope: Select your account
3. Link to existing project? **N**
4. Project name: `summarizer-agent-langgraph`
5. Directory: `./` (current)
6. Override settings? **N**

**Configure Environment Variables:**

After deployment, add variables in Vercel dashboard:
1. Go to https://vercel.com/dashboard
2. Select your project
3. Settings → Environment Variables
4. Add:
   ```
   API_BASE_URL=https://summarizer-agent-langgraph-production.up.railway.app
   FLASK_ENV=production
   ```
5. Redeploy: Deployments → ⋯ → Redeploy

### Part 3: Verify Deployment

#### 1. Test Backend Health
```cmd
curl https://summarizer-agent-langgraph-production.up.railway.app/health
```

**Expected:**
```json
{"status":"healthy","message":"API is operational"}
```

#### 2. Test Ollama Connection
```cmd
curl https://summarizer-agent-langgraph-production.up.railway.app/api/models
```

**Expected:**
```json
{
  "models": ["qwen2.5-coder:0.5b", ...],
  "default": "qwen2.5-coder:0.5b"
}
```

#### 3. Test Full Analysis
```cmd
curl -X POST https://summarizer-agent-langgraph-production.up.railway.app/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"This is a test message for summarization\", \"model_name\": \"qwen2.5-coder:0.5b\"}"
```

**Expected:**
```json
{
  "input_text": "This is a test message...",
  "word_count": 7,
  "character_count": 42,
  "summary": "The text is a simple test message...",
  "sentiment": "neutral",
  "model_used": "qwen2.5-coder:0.5b",
  "success": true
}
```

#### 4. Test Frontend
Visit: https://summarizer-agent-langgraph-ufot.vercel.app

1. Enter some text
2. Click "Analyze"
3. Wait 2-5 seconds
4. See summary and sentiment

## 🐛 Troubleshooting

### Issue: Backend "Connection refused" to Ollama

**Symptoms:**
```
ERROR: Connection refused to http://ollama.railway.internal:11434
```

**Solutions:**
1. Check Ollama logs: `railway logs --service ollama`
2. Verify "Model ready!" message appears
3. Check environment variable:
   ```cmd
   railway variables --service backend
   # Should show: OLLAMA_HOST=http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434
   ```
4. Restart backend: Railway Dashboard → backend → Settings → Restart

### Issue: Ollama takes too long

**Symptoms:**
- Model pull stuck at 50%
- Timeout after 2 minutes

**Solutions:**
1. **First deployment is slow** - Model is 394MB, takes 2-3 minutes
2. Check Railway network status: https://railway.app/status
3. Volume not mounted? Go to Ollama service → Settings → Volumes
4. Try redeploying: `railway up --service ollama`

### Issue: "Model not found"

**Symptoms:**
```
Error: model 'qwen2.5-coder:0.5b' not found
```

**Solutions:**
1. Check Ollama logs for pull success
2. Model might be named differently:
   ```cmd
   railway run --service ollama -- ollama list
   ```
3. Manually pull in Ollama container:
   ```cmd
   railway run --service ollama -- ollama pull qwen2.5-coder:0.5b
   ```

### Issue: Frontend can't reach backend

**Symptoms:**
- "Network Error" in frontend
- CORS errors in browser console

**Solutions:**
1. Check backend URL in Vercel:
   ```
   Settings → Environment Variables → API_BASE_URL
   ```
2. Verify CORS in `backend/api.py`:
   ```python
   allow_origins=[
       "https://summarizer-agent-langgraph-ufot.vercel.app",
       "https://*.vercel.app",
   ]
   ```
3. Test backend directly: `curl <backend-url>/health`
4. Check browser console for specific CORS error

### Issue: Slow inference (>30 seconds)

**Symptoms:**
- API times out
- Very slow responses

**Explanation:**
- Railway uses **CPU only** (no GPU)
- qwen2.5-coder:0.5b should give **5-15 tokens/sec**
- Larger models will be much slower

**Solutions:**
1. ✅ Already using smallest model (0.5B)
2. ✅ Upgrade Railway plan for more CPU
3. ✅ Implement streaming for better UX
4. ❌ Don't use larger models on CPU

## 📊 Performance Expectations

### qwen2.5-coder:0.5b on Railway CPU

| Metric | Value | Notes |
|--------|-------|-------|
| **Model Size** | 494 MB | Quick to download |
| **Tokens/Second** | 5-15 | Acceptable for production |
| **Cold Start** | 10-20s | First request after idle |
| **Warm Inference** | 2-5s | Subsequent requests |
| **Memory Usage** | ~1.5 GB | Fits in Hobby plan |
| **Cost** | $5/month | Both services combined |

### Comparison with Larger Models

| Model | Size | CPU Speed | GPU Speed | Railway Viable? |
|-------|------|-----------|-----------|-----------------|
| qwen2.5-coder:0.5b | 494 MB | 5-15 tok/s | 60-80 tok/s | ✅ Yes |
| llama3.2:1b | 1.3 GB | 2-5 tok/s | 40-60 tok/s | ⚠️ Slow |
| llama3.2:3b | 2.0 GB | 1-2 tok/s | 20-30 tok/s | ❌ Too slow |
| mistral:7b | 4.1 GB | <1 tok/s | 15-20 tok/s | ❌ Too slow |

## 💰 Cost Breakdown

### Railway Hobby Plan: $5/month
- **Backend API**: ~40% ($2.00)
- **Ollama Service**: ~60% ($3.00)
- **Total Compute**: 500 hours included
- **Extra**: $0.01/hour beyond 500

### Vercel Hobby Plan: FREE
- **Bandwidth**: 100 GB/month
- **Builds**: Unlimited
- **Deployments**: Unlimited

**Total Monthly Cost: $5** 💵

## 🎉 Success Checklist

After completing all steps, verify:

- [ ] Backend health check returns 200 OK
- [ ] Ollama logs show "Model ready!"
- [ ] Frontend loads without errors
- [ ] Can submit text and get summary
- [ ] Response time < 10 seconds
- [ ] Sentiment analysis works
- [ ] CORS allows frontend requests
- [ ] Railway shows "Active" status for both services
- [ ] No errors in browser console
- [ ] Mobile responsive frontend works

## 📚 Additional Resources

### Documentation
- **Railway Docs**: https://docs.railway.app/
- **Ollama Docs**: https://github.com/ollama/ollama/blob/main/docs/README.md
- **Vercel Docs**: https://vercel.com/docs
- **LangGraph Docs**: https://python.langchain.com/docs/langgraph

### Project Documentation
- **Architecture**: `backend/ARCHITECTURE.md`
- **Ollama Setup**: `OLLAMA_RAILWAY_SETUP.md`
- **Deployment Files**: `DEPLOYMENT_FILES_README.md`
- **API Documentation**: https://your-backend.railway.app/docs

### Support
- Railway Discord: https://discord.gg/railway
- Railway Status: https://railway.app/status
- Vercel Support: https://vercel.com/support

## 🔄 Updating Your Deployment

### Update Backend Code
```cmd
# Commit changes
git add .
git commit -m "Update backend code"
git push

# Railway auto-deploys on push
# Or manually: railway up --service backend
```

### Update Ollama Model
```cmd
# SSH into Ollama container
railway run --service ollama bash

# Pull new model
ollama pull qwen2.5-coder:1b

# Exit
exit
```

### Update Frontend
```cmd
cd frontend
vercel --prod
```

## 🎯 Next Steps

Now that your app is deployed:

1. **Monitor Performance**
   - Railway Dashboard → Metrics
   - Check CPU/RAM usage
   - Monitor response times

2. **Set Up Alerts**
   - Railway → Settings → Notifications
   - Enable deployment notifications
   - Enable error notifications

3. **Custom Domain** (Optional)
   - Railway: Settings → Networking → Custom Domain
   - Vercel: Settings → Domains → Add Domain

4. **Implement Improvements**
   - Add response streaming for better UX
   - Implement caching for common queries
   - Add rate limiting to prevent abuse
   - Set up analytics

5. **Scale if Needed**
   - Upgrade to Railway Pro ($20/month)
   - More CPU for faster inference
   - Unlimited compute hours
   - Priority support

---

## 🆘 Still Having Issues?

If something doesn't work:

1. **Check logs first**: `railway logs --service <backend|ollama>`
2. **Review this guide** from the beginning
3. **Check Railway status**: https://railway.app/status
4. **Review troubleshooting section** above
5. **Check GitHub issues** for similar problems

**Good luck! 🚀**
