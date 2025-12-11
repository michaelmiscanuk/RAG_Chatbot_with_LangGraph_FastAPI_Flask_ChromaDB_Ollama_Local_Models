# 🔍 Troubleshooting Ollama Connection

## 1. Check the Error Log
I have updated the code to print the **exact error** instead of just "Ollama not available".
Please **redeploy** your backend and check the logs again. You should see something like:
`Ollama not available, using mock model. Error: ...`

## 2. Common Reasons for Failure

### A. Model Still Pulling
The Ollama service takes **2-3 minutes** to start the first time because it downloads the model (500MB).
*   **Check Ollama Logs**: Go to Railway -> Ollama Service -> Logs.
*   Wait until you see: `success` or `pulling ... 100%`.

### B. Connection Refused
If the error is `Connection refused`, it means the backend tried to connect before Ollama was ready.
*   **Solution**: Just wait a minute and try clicking "Analyze" again. The backend will retry on the next request.

### C. Wrong Hostname
If the error is `Name or service not known`, the `OLLAMA_HOST` variable might be wrong.
*   In `railway.yaml`, it is set to: `http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434`
*   Verify in Railway Dashboard -> Backend -> Variables that `OLLAMA_HOST` has a value like `http://ollama.railway.internal:11434`.

## 3. How to Fix "Model Still Pulling"
If the model takes too long to pull every time you deploy, we can improve the `Dockerfile.ollama` to be more robust.

**Current behavior**: It pulls every time the container starts.
**Better behavior**: Check if model exists, only pull if missing.

But first, let's see the error message from the logs!
