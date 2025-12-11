# Deployment Configuration Summary

## Backend (Railway)
- **Internal URL**: `text-analysis-backend.railway.internal` (or check Service Name in Railway)
  - *Note: Only works for services running INSIDE Railway*
- **Public URL**: `https://<your-project>-production.up.railway.app` (Check Networking tab in Railway)
  - *Note: Use this for Local and Vercel connections*
- **Configuration**: `backend/railway.json`

## Frontend (Vercel)
- **URL**: `https://summarizer-agent-langgraph-ufot.vercel.app`
- **Configuration**: `frontend/vercel.json`

## Connection Setup

### 1. Backend CORS Configuration ✅
Updated `backend/api.py` to allow requests from:
- Local development: `http://localhost:5000`
- Production: `https://summarizer-agent-langgraph-ufot.vercel.app`
- Preview deployments: `https://*.vercel.app`

### 2. Frontend API Configuration ✅
Updated frontend to connect to Railway backend:
- Environment variable: `API_BASE_URL=https://summarizer-agent-langgraph-production.up.railway.app`
- Configured in: `frontend/vercel.json`, `frontend/.env`

## Environment Variables to Set

### Railway (Backend)
Set these in Railway dashboard:
```
PORT=8000 (auto-set by Railway)
OLLAMA_HOST=<your-ollama-instance-url>
RELOAD=false
```

### Vercel (Frontend)
Set these in Vercel dashboard (Project Settings → Environment Variables):
```
API_BASE_URL=https://summarizer-agent-langgraph-production.up.railway.app
SECRET_KEY=<generate-a-random-string>
FLASK_ENV=production
```

## Testing the Connection

1. **Deploy Backend to Railway**
   - Push your code to GitHub
   - Railway will auto-deploy from `backend/railway.json`

2. **Deploy Frontend to Vercel**
   - Push your code to GitHub
   - Vercel will auto-deploy using `vercel.json`

3. **Test the Connection**
   - Visit: `https://summarizer-agent-langgraph-ufot.vercel.app`
   - Try analyzing some text
   - Check Railway logs if there are issues

## Important Notes

⚠️ **Railway URL Format**: The actual Railway public URL might be different. Check your Railway dashboard for the exact URL and update:
- `backend/api.py` (CORS origins)
- `frontend/vercel.json` (API_BASE_URL)
- `frontend/.env` (API_BASE_URL)

⚠️ **Ollama Requirement**: Railway doesn't support GPU workloads. You'll need to:
- Deploy Ollama on a GPU-enabled platform (RunPod, vast.ai)
- Or use an alternative LLM API (OpenAI, Anthropic, etc.)
- Set `OLLAMA_HOST` to point to your Ollama instance

## Quick Commands

```bash
# Update Railway backend
git add backend/
git commit -m "Update backend for Railway deployment"
git push

# Update Vercel frontend  
git add frontend/
git commit -m "Update frontend for Vercel deployment"
git push

# Check Railway logs
# Go to Railway dashboard → Your project → Deployments → View Logs

# Check Vercel logs
# Go to Vercel dashboard → Your project → Deployments → View Function Logs
```
