# 📦 Deployment Files Summary

This directory contains all the configuration files needed to deploy your application stack:

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└───────────────┬─────────────────────────┬───────────────────┘
                │                         │
                ▼                         ▼
┌───────────────────────────┐  ┌──────────────────────────────┐
│   Vercel (Frontend)       │  │   Railway (Backend + Ollama)  │
│                           │  │                               │
│  Flask + Modern CSS       │──▶  ┌─────────────────────┐    │
│                           │  │  │  FastAPI Backend    │    │
│  URL: summarizer-agent-   │  │  │  :8000              │    │
│  langgraph-ufot.vercel.app│  │  └──────────┬──────────┘    │
└───────────────────────────┘  │             │                │
                               │             │ Private Network│
                               │             ▼                │
                               │  ┌──────────────────────┐   │
                               │  │  Ollama Service      │   │
                               │  │  :11434              │   │
                               │  │  qwen2.5-coder:0.5b  │   │
                               │  └──────────────────────┘   │
                               └──────────────────────────────┘
```

## 📄 File Overview

### Railway Configuration Files

#### `railway.json` (Single Service)
- **Purpose**: Deploys backend API only (without Ollama)
- **Use When**: You have Ollama running elsewhere or want minimal setup
- **Deploy**: `railway up` in backend directory

#### `railway-multi.yaml` (Multi-Service) ⭐ **RECOMMENDED**
- **Purpose**: Deploys both backend API + Ollama service
- **Use When**: You want complete LLM inference on Railway
- **Deploy**: Requires manual Railway dashboard setup (see OLLAMA_RAILWAY_SETUP.md)
- **Features**:
  - Private network between services
  - Volume persistence for models
  - Automatic environment variable injection

#### `nixpacks.toml`
- **Purpose**: Build configuration for Railway
- **Features**:
  - Python 3.12
  - Poetry package manager
  - Install phases configuration
  - Start command override

### Docker Files

#### `Dockerfile` (Backend)
- Standard FastAPI + LangGraph backend
- Installs dependencies from `pyproject.toml`
- Runs uvicorn server on port 8000

#### `Dockerfile.ollama` (Ollama Service)
- Based on official `ollama/ollama:latest`
- Auto-pulls `qwen2.5-coder:0.5b` on startup
- Runs Ollama server in background
- Includes health check support

### Vercel Configuration

#### `frontend/vercel.json`
- Routes configuration for Flask app
- Build settings for Vercel
- Environment variables:
  - `API_BASE_URL`: Points to Railway backend
  - `FLASK_ENV`: Production settings

## 🚀 Quick Start

### Deploy Everything (Recommended)

1. **Deploy Frontend to Vercel**
   ```bash
   cd frontend
   vercel --prod
   ```

2. **Deploy Backend + Ollama to Railway**
   - Follow the guide in `OLLAMA_RAILWAY_SETUP.md`
   - Uses `railway-multi.yaml` configuration
   - Creates 2 services: backend + ollama

3. **Connect Services**
   - Backend already configured to use `OLLAMA_HOST` from Railway
   - Frontend configured to use backend via `API_BASE_URL`

### Deploy Backend Only (Minimal)

If you already have Ollama running or want to test without it:

```bash
cd backend
railway up
```

This uses `railway.json` for a single-service deployment.

## 🔧 Environment Variables

### Backend (Railway)
```env
PORT=8000                                        # Railway assigns this
RELOAD=false                                     # Production setting
OLLAMA_HOST=http://${ollama.RAILWAY_PRIVATE_DOMAIN}:11434  # Auto-injected
```

### Ollama (Railway)
```env
OLLAMA_HOST=0.0.0.0:11434                       # Listen on all interfaces
OLLAMA_ORIGINS=*                                 # Allow all origins (private network)
```

### Frontend (Vercel)
```env
API_BASE_URL=https://summarizer-agent-langgraph-production.up.railway.app
FLASK_ENV=production
```

## 📊 Deployment Comparison

| Feature | Single Service (`railway.json`) | Multi-Service (`railway-multi.yaml`) |
|---------|--------------------------------|-------------------------------------|
| **Ollama** | ❌ External required | ✅ Included |
| **Setup Complexity** | Simple | Moderate |
| **Cost** | ~$2.50/month | ~$5/month |
| **Latency** | Higher (external Ollama) | Lower (private network) |
| **Best For** | Testing, dev | Production |

## 🎯 Recommended Setup for Production

**Use the multi-service setup** (`railway-multi.yaml`):

✅ **Pros**:
- Everything in one place (Railway)
- Private network = faster + more secure
- Model persistence with volumes
- Easy monitoring

❌ **Cons**:
- Slightly more complex setup
- CPU-only (no GPU)
- 5-15 tokens/sec inference speed

## 📚 Detailed Guides

- **Ollama Setup**: See `OLLAMA_RAILWAY_SETUP.md`
- **Service Connection**: See `DEPLOYMENT.md`
- **Architecture**: See `backend/ARCHITECTURE.md`

## 🐛 Common Issues

### Issue: Railway build fails
- Check `nixpacks.toml` for correct Python version
- Ensure `pyproject.toml` has all dependencies

### Issue: Ollama not connecting
- Verify `OLLAMA_HOST` environment variable
- Check Ollama service logs for "Model ready!" message
- Ensure volume is mounted: `/root/.ollama`

### Issue: Frontend can't reach backend
- Check CORS settings in `backend/api.py`
- Verify `API_BASE_URL` in Vercel environment variables
- Test backend health: `https://your-backend.railway.app/health`

## 💡 Tips

1. **Use Railway CLI** for faster deployments: `railway up`
2. **Check logs** regularly: `railway logs` or Railway dashboard
3. **Monitor costs**: Railway dashboard → Project → Usage
4. **Persist models**: Always use volumes for Ollama to avoid re-downloading
5. **Test locally first**: Run `docker-compose up` before deploying

## 🔗 URLs

- **Frontend**: https://summarizer-agent-langgraph-ufot.vercel.app
- **Backend**: https://summarizer-agent-langgraph-production.up.railway.app
- **Backend API Docs**: https://summarizer-agent-langgraph-production.up.railway.app/docs

## 📝 Next Steps After Deployment

1. ✅ Test health endpoint: `/health`
2. ✅ Test analyze endpoint: `/api/analyze`
3. ✅ Check Ollama logs for model pull
4. ✅ Test full flow: Frontend → Backend → Ollama
5. ✅ Set up monitoring/alerts
6. ✅ Configure custom domain (optional)

---

**Need help?** Check the detailed guides or Railway/Vercel documentation!
