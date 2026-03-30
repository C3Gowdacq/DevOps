import requests
import time
import subprocess
import os

def test_api():
    # Start the server in the background
    print("Starting server for testing...")
    # Using python -m uvicorn to ensure it's in the path
    process = subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
    time.sleep(5)  # Wait for startup

    try:
        # Test Root
        response = requests.get("http://127.0.0.1:8000/")
        assert response.status_code == 200
        
        # Test Analyze
        payload = {"text": "I love this product!"}
        response = requests.post("http://127.0.0.1:8000/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "sentiment" in data
        assert data["sentiment"] == "positive"
        print("API tests passed!")
    finally:
        print("Stopping server...")
        process.terminate()

if __name__ == "__main__":
    test_api()
