import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from main import app, load_models, TextRequest
import asyncio

# Mocking the models loading since we are running in the same env
load_models()

async def test_api():
    test_cases = [
        "you have killed the performance",
        "i killed someone",
        "this is insane",
        "the error killed the app"
    ]
    
    print(f"Testing API Logic (Version: 2.1.0)...")
    for text in test_cases:
        request = TextRequest(text=text)
        # Manually call the endpoint function
        from main import analyze_text
        result = await analyze_text(request)
        print(f"Input: '{text}' -> Sentiment: {result['sentiment']}")

if __name__ == "__main__":
    asyncio.run(test_api())
