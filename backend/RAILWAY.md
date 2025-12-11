# Railway Configuration for Backend (Simplified)
# Place this file in the root of your backend directory

# If the above railway.yaml doesn't work, Railway also supports simpler configurations
# You can also configure everything via the Railway dashboard instead

# Required Environment Variables to set in Railway Dashboard:
# - PORT: Set automatically by Railway
# - OLLAMA_HOST: URL to your Ollama instance (see note below)
# - RELOAD: false (for production)

# IMPORTANT NOTE ABOUT OLLAMA:
# Railway doesn't natively support Ollama since it requires GPU resources.
# You have several options:
#
# 1. Use Ollama Cloud API (if available)
# 2. Deploy Ollama on a different platform that supports GPUs (e.g., RunPod, vast.ai)
# 3. Use alternative LLM providers with HTTP APIs:
#    - OpenAI API
#    - Anthropic Claude API
#    - Hugging Face Inference API
#    - Together AI
#    - Replicate
#
# You'll need to modify the code to use one of these alternatives or
# point OLLAMA_HOST to an external Ollama instance.

# Deployment Steps:
# 1. Create a new project in Railway (https://railway.app)
# 2. Connect your GitHub repository
# 3. Select the backend directory as the root
# 4. Railway will auto-detect Python and install dependencies
# 5. Set environment variables in the Railway dashboard
# 6. Deploy!

# The start command will be:
# uvicorn api:app --host 0.0.0.0 --port $PORT --log-level info
