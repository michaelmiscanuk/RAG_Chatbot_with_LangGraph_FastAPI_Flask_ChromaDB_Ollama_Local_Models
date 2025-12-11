import requests
import time

# Wait a moment for server to be ready
time.sleep(2)

# Test the analyze endpoint
try:
    response = requests.post(
        "http://localhost:8000/api/analyze",
        json={
            "text": "This is a test text for analysis.",
            "model_name": "qwen2.5-coder:0.5b",
        },
    )
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    print("SUCCESS: Checkpointer error is fixed!")
except Exception as e:
    print("Error:", e)
