#!/bin/bash
# Railway Multi-Service Deployment Script
# This script helps deploy both backend and Ollama services to Railway

set -e  # Exit on error

echo "🚂 Railway Multi-Service Deployment Script"
echo "==========================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo "📦 Install it with: npm i -g @railway/cli"
    echo "🔗 Or visit: https://docs.railway.app/develop/cli"
    exit 1
fi

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Not logged in to Railway"
    echo "Please run: railway login"
    exit 1
fi

echo "✅ Railway CLI is ready"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

echo "📍 Current directory: $(pwd)"
echo ""

# Deploy backend service
echo "🚀 Step 1: Deploying Backend API..."
echo "-----------------------------------"
railway up --service backend || railway up

echo ""
echo "✅ Backend deployed successfully!"
echo ""

# Deploy Ollama service
echo "🤖 Step 2: Deploying Ollama Service..."
echo "--------------------------------------"
echo ""
echo "⚠️  Note: This will use Dockerfile.ollama"
echo "⚠️  First deployment will take 2-3 minutes to pull model"
echo ""

# Check if Ollama service exists
if railway status --service ollama &> /dev/null; then
    echo "📦 Ollama service found, updating..."
    railway up --service ollama --dockerfile Dockerfile.ollama
else
    echo "📦 Creating new Ollama service..."
    echo ""
    echo "⚠️  Manual step required:"
    echo "   1. Go to Railway dashboard"
    echo "   2. Click 'New' → 'Empty Service'"
    echo "   3. Name it 'ollama'"
    echo "   4. Connect your GitHub repo"
    echo "   5. Set root directory: 'backend'"
    echo "   6. Set Dockerfile: 'Dockerfile.ollama'"
    echo "   7. Add volume: '/root/.ollama'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo ""
echo "✅ Ollama service deployed!"
echo ""

# Set environment variables
echo "🔧 Step 3: Setting Environment Variables..."
echo "-------------------------------------------"

echo "Setting OLLAMA_HOST for backend..."
railway variables --set OLLAMA_HOST='http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434' --service backend

echo "Setting Ollama configuration..."
railway variables --set OLLAMA_HOST=0.0.0.0:11434 --service ollama
railway variables --set OLLAMA_ORIGINS='*' --service ollama

echo ""
echo "✅ Environment variables configured!"
echo ""

# Show deployment status
echo "📊 Deployment Status"
echo "-------------------"
railway status

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "📝 Next Steps:"
echo "   1. Check logs: railway logs --service backend"
echo "   2. Check Ollama: railway logs --service ollama"
echo "   3. Wait for 'Model ready!' message in Ollama logs"
echo "   4. Test backend: https://your-backend.railway.app/health"
echo "   5. Update frontend API_BASE_URL in Vercel"
echo ""
echo "📚 Documentation:"
echo "   - Setup Guide: ../OLLAMA_RAILWAY_SETUP.md"
echo "   - Deployment Files: ../DEPLOYMENT_FILES_README.md"
echo ""
