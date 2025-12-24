import requests
import json

def test_title_generation():
    url = "http://127.0.0.1:8000/api/coach/title"
    
    # Simulate a conversation
    history = [
        {"role": "user", "content": "I want to lose weight and I love pizza."},
        {"role": "assistant", "content": "That's a common challenge! We can modify your pizza toppings to be healthier."},
        {"role": "user", "content": "What about increasing protein?"}
    ]
    
    payload = {"history": history}
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        if response.ok:
            print("Response JSON:", response.json())
        else:
            print("Error Response:", response.text)
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_title_generation()
