import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "http://127.0.0.1:8000/api/coach/chat"
headers = {"Content-Type": "application/json"}
payload = {
    "message": "Hello, is this working?",
    "context_data": "I just ate a donut."
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
