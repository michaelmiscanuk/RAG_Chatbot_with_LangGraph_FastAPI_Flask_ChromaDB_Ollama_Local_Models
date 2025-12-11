# 💾 Memory Issue - Ollama Getting Killed

## The Problem
Error: `llama runner process has terminated: signal: killed`

This means Ollama ran out of memory (OOM). The OS killed the process to prevent system crash.

## Why It Happens
- **qwen2.5-coder:0.5b** needs ~2GB RAM minimum
- Railway's free tier: Limited memory
- After OS + Ollama overhead: Not enough left for the model

## ✅ Solutions

### Solution 1: Upgrade Railway Plan (Recommended)
Railway's paid plans have more memory:
- **Hobby ($5/month)**: 8GB RAM - Should work
- **Pro ($20/month)**: 32GB RAM - Plenty of room

**How to upgrade:**
1. Go to Railway Dashboard
2. Click your project
3. Go to Settings → Usage
4. Click "Upgrade Plan"

### Solution 2: Use External Ollama
Run Ollama on a service with more RAM:
- **RunPod**: GPU-enabled, ~$0.20/hour
- **Vast.ai**: GPU marketplace, ~$0.10/hour
- **Your local machine**: Free, unlimited

Then point `OLLAMA_HOST` in Railway to your external Ollama URL.

### Solution 3: Switch to API-based LLM
Instead of running Ollama, use an API service:
- **OpenAI API**: Reliable, $0.002/1K tokens
- **Anthropic Claude**: Good quality
- **Groq**: Very fast, free tier available

This requires code changes but no infrastructure worries.

## 🔍 Verify Memory Usage
After deploying, check Railway logs for:
```
time=... level=INFO msg="inference compute" ... available="XXX MiB"
```

If available memory is < 2GB, the model won't run reliably.
