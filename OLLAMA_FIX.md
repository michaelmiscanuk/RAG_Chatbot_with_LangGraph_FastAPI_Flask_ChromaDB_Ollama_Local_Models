# ⚠️ Ollama Connection Issue

## The Problem
Your backend is running, but it says:
`Ollama not available, using mock model`

This means your backend cannot talk to the Ollama service.

## 🔍 Diagnosis
You likely deployed **only the backend** using the default `railway.yaml` or the "Deploy" button, which does NOT include Ollama.

Railway does not provide Ollama by default. You must deploy it as a **separate service**.

## 🛠️ The Fix (Deploy Ollama)

### Option 1: Use the Multi-Service Config (Recommended)
I have created a `railway-multi.yaml` file that defines BOTH services.

1.  **Rename the file**:
    ```cmd
    ren railway.yaml railway-single.yaml
    ren railway-multi.yaml railway.yaml
    ```
2.  **Push to GitHub**:
    ```cmd
    git add .
    git commit -m "Switch to multi-service deployment"
    git push
    ```
3.  **Deploy in Railway**:
    *   Railway should detect the new config and deploy both services.
    *   If not, run: `railway up`

### Option 2: Manual Setup (If you prefer the Dashboard)

1.  **Create New Service**:
    *   In your Railway project, click **New** -> **Empty Service**.
    *   Name it `ollama`.
2.  **Configure Service**:
    *   **Source**: Connect to your GitHub repo.
    *   **Root Directory**: `backend`
    *   **Dockerfile**: `Dockerfile.ollama` (Important!)
3.  **Add Variables**:
    *   `OLLAMA_HOST`: `0.0.0.0:11434`
    *   `OLLAMA_ORIGINS`: `*`
4.  **Connect Backend**:
    *   Go to your **Backend Service** -> **Variables**.
    *   Add/Update `OLLAMA_HOST`: `http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434`
    *   *Note: This uses Railway's variable reference feature.*

## ⏳ Wait for Model
When Ollama starts for the first time, it needs to download the model (approx 500MB).
*   Check the **Ollama Service Logs**.
*   Wait until you see: `Model ready! Ollama is running on port 11434`.

## 🧪 Verify
Once deployed, your backend logs should show:
`Using model: qwen2.5-coder:0.5b`
(Instead of "mock model")
