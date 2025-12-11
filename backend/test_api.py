import requests
import time
import uuid

# Wait a moment for server to be ready
time.sleep(2)

# Test the chat endpoint
try:
    thread_id = str(uuid.uuid4())
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={
            "message": "Hello, what services do you offer?",
            "thread_id": thread_id,
        },
    )
    print("Status Code:", response.status_code)
    print("Response:", response.json())

    if response.status_code == 200:
        print("SUCCESS: Chat endpoint is working!")
    else:
        print("FAILURE: Chat endpoint returned error.")

except Exception as e:
    print("Error:", e)
