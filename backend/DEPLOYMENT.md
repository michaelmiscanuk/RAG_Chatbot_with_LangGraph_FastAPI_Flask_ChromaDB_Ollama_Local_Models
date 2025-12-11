# Backend API Deployment Guide 🚀

Complete guide for deploying the FastAPI backend to Render.com

## Backend API Overview

The backend provides REST API endpoints for text analysis using LangGraph workflows and Ollama models.

### Key Features

- ⚡ **FastAPI**: Modern, fast API framework
- 🤖 **LangGraph**: Multi-node workflow orchestration
- 🧠 **Ollama Integration**: Local LLM inference
- 🔒 **CORS Enabled**: Secure cross-origin requests
- 📊 **Health Monitoring**: Built-in health checks
- 📝 **Auto Documentation**: Swagger UI at `/docs`

## Deployment to Render.com

### Prerequisites

- Render.com account ([sign up free](https://render.com))
- Backend code pushed to GitHub
- Understanding of Ollama deployment options

### Important Note About Ollama

⚠️ **Ollama Consideration**: The backend requires Ollama for LLM inference. On Render.com's free tier, you have two options:

1. **Use a hosted LLM service** (Recommended for production):
   - OpenAI API
   - Anthropic Claude
   - Groq
   - Together AI
   
   Update `src/config/models.py` to use these instead of Ollama.

2. **Deploy Ollama separately**:
   - Use a dedicated server for Ollama
   - Use Render's paid tier with persistent disk
   - Configure `OLLAMA_BASE_URL` environment variable

### Deployment Steps

#### Option 1: Deploy via Render Dashboard

1. **Create New Web Service**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**:
   ```
   Name: text-analysis-backend
   Region: Oregon (US West)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```

3. **Select Plan**:
   - Free tier for testing
   - Starter ($7/month) for production

4. **Set Environment Variables**:
   ```
   OLLAMA_BASE_URL=http://your-ollama-server:11434
   PYTHON_VERSION=3.11.0
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

#### Option 2: Deploy via render.yaml

1. **Use the provided render.yaml**:
   - Already configured in `backend/render.yaml`

2. **Create Blueprint**:
   - In Render Dashboard
   - Go to "Blueprints"
   - Click "New Blueprint Instance"
   - Connect repository
   - Select `backend/render.yaml`

3. **Deploy**:
   - Review configuration
   - Click "Apply"

### Post-Deployment Configuration

1. **Get Your Backend URL**:
   ```
   https://your-app-name.onrender.com
   ```

2. **Test the API**:
   ```bash
   curl https://your-app-name.onrender.com/health
   ```

3. **Check API Documentation**:
   ```
   https://your-app-name.onrender.com/docs
   ```

4. **Update Frontend**:
   - Add backend URL to frontend environment variables
   - Update CORS in `backend/api.py`:
   ```python
   allow_origins=[
       "https://your-frontend.vercel.app",
       "http://localhost:5000",
   ]
   ```

### Environment Variables

Set these in Render Dashboard under "Environment":

| Variable | Description | Example |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Ollama server URL | `http://ollama-server:11434` |
| `PYTHON_VERSION` | Python version | `3.11.0` |
| `PORT` | Server port | Auto-set by Render |

### Alternative: Use Hosted LLM Services

For easier deployment without Ollama, modify `src/config/models.py`:

```python
from langchain_openai import ChatOpenAI

def get_model(model_name="gpt-3.5-turbo", temperature=0.7):
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY")
    )
```

Then add environment variable:
```
OPENAI_API_KEY=your-api-key
```

Update `requirements.txt`:
```
langchain-openai>=0.2.0
```

## Local Testing Before Deployment

1. **Start backend locally**:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python api.py
   ```

2. **Test endpoints**:
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Test analysis
   curl -X POST http://localhost:8000/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "This is a test", "model_name": "qwen2.5-coder:0.5b"}'
   ```

3. **Check API docs**:
   ```
   http://localhost:8000/docs
   ```

## Monitoring & Logs

### View Logs in Render

1. Go to your service in Render Dashboard
2. Click "Logs" tab
3. Monitor real-time logs
4. Search for errors or specific events

### Health Checks

Render automatically monitors `/health` endpoint:
- Green: Service is healthy
- Red: Service is down or unhealthy

### Performance Monitoring

Free tier limitations:
- Service spins down after 15 minutes of inactivity
- Cold starts take 30-60 seconds
- Limited CPU and RAM

Upgrade to Starter plan for:
- Always-on service
- No cold starts
- Better performance

## Troubleshooting

### Service won't start

**Problem**: Build or start fails

**Solutions**:
1. Check logs for specific error
2. Verify `requirements.txt` is complete
3. Ensure Python version compatibility
4. Check `api.py` for syntax errors

### Ollama connection errors

**Problem**: Cannot connect to Ollama

**Solutions**:
1. Verify `OLLAMA_BASE_URL` is set correctly
2. Check if Ollama server is accessible
3. Test connection from Render (may need VPN/networking setup)
4. Consider using hosted LLM service instead

### CORS errors

**Problem**: Frontend can't connect due to CORS

**Solutions**:
1. Update `allow_origins` in `api.py`
2. Add your Vercel URL
3. Redeploy backend
4. Clear browser cache

### Timeout errors

**Problem**: Requests timeout

**Solutions**:
1. Reduce text input size
2. Use faster model
3. Increase timeout in frontend
4. Upgrade Render plan

## Cost Estimates

### Render.com Pricing

- **Free Tier**:
  - Good for testing
  - Spins down after 15 min inactivity
  - 750 hours/month
  - Limited resources

- **Starter Plan ($7/month)**:
  - Always on
  - No cold starts
  - Better performance
  - Recommended for production

- **Standard Plan ($25/month)**:
  - More resources
  - Better for high traffic
  - Advanced features

### Optimization Tips

1. **Use faster models**: Smaller models = faster responses
2. **Optimize workflows**: Reduce unnecessary processing
3. **Cache results**: Implement caching if needed
4. **Set timeouts**: Prevent long-running requests

## Security Best Practices

1. **Environment Variables**: Never commit secrets
2. **CORS**: Only allow trusted origins
3. **Rate Limiting**: Consider adding rate limits
4. **Input Validation**: Already implemented in API
5. **HTTPS**: Render provides SSL certificates

## Updating the Deployment

### Via Git Push

1. Make changes to code
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update API"
   git push origin main
   ```
3. Render auto-deploys on push

### Manual Deploy

1. Go to Render Dashboard
2. Select your service
3. Click "Manual Deploy"
4. Select branch
5. Deploy

## Testing in Production

```bash
# Test health
curl https://your-app.onrender.com/health

# Test analysis
curl -X POST https://your-app.onrender.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Amazing product! Highly recommend.",
    "model_name": "qwen2.5-coder:0.5b"
  }'

# View API docs
# Visit: https://your-app.onrender.com/docs
```

## Scaling Considerations

For high-traffic scenarios:

1. **Horizontal Scaling**: Deploy multiple instances
2. **Load Balancer**: Use Render's load balancing
3. **Caching**: Implement Redis caching
4. **Database**: Add PostgreSQL for persistence
5. **Background Jobs**: Use Celery for async processing

## Support Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama Documentation](https://ollama.ai/docs)

---

**Next Steps**:
1. Deploy backend to Render
2. Get backend URL
3. Deploy frontend to Vercel with backend URL
4. Test end-to-end functionality

Good luck with your deployment! 🚀
