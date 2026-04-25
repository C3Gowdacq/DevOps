from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import os
import re

app = FastAPI(title="Multi-Model AI Text Analyzer API")

# Version tracker to ensure we are running the latest code
SYSTEM_VERSION = "2.0.0-Hybrid"

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Path to models
MODEL_DIR = "models"
SENTIMENT_MODEL_PATH = os.path.join(MODEL_DIR, "sentiment_model.pkl")
SENTIMENT_VECT_PATH = os.path.join(MODEL_DIR, "sentiment_vectorizer.pkl")
SPAM_MODEL_PATH = os.path.join(MODEL_DIR, "spam_model.pkl")
SPAM_VECT_PATH = os.path.join(MODEL_DIR, "spam_vectorizer.pkl")

models = {}

@app.on_event("startup")
def load_models():
    try:
        with open(SPAM_MODEL_PATH, "rb") as f:
            models["spam_model"] = pickle.load(f)
        with open(SPAM_VECT_PATH, "rb") as f:
            models["spam_vect"] = pickle.load(f)
        with open(SENTIMENT_MODEL_PATH, "rb") as f:
            models["sentiment_model"] = pickle.load(f)
        with open(SENTIMENT_VECT_PATH, "rb") as f:
            models["sentiment_vect"] = pickle.load(f)
        print(f"--- System Version {SYSTEM_VERSION} Loaded ---")
    except Exception as e:
        print(f"Error loading models: {e}")

class TextRequest(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    sentiment: str
    spam: str
    keywords: list
    version: str  # Added to track if we are on the right version

def extract_keywords(text: str):
    return list(set(re.findall(r'\b\w{4,}\b', text.lower())))

POSITIVE_SLANG_PATTERNS = ["killed the", "killing the", "nailed it", "sick", "insane", "crushed it", "savage", "killed it"]

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse('static/index.html')

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_text(request: TextRequest):
    text = request.text.lower().strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # 1. ML Prediction
    sent_X = models["sentiment_vect"].transform([text])
    sent_pred = models["sentiment_model"].predict(sent_X)[0]
    
    # 2. Slang Override
    for pattern in POSITIVE_SLANG_PATTERNS:
        if pattern in text:
            if not any(neg in text for neg in ["error", "bug", "crash", "delay", "failure"]):
                print(f"[SENTIMENT DEBUG] Slang Overide Triggered for: '{pattern}'")
                sent_pred = "positive"
                break

    # 3. Spam
    spam_X = models["spam_vect"].transform([text])
    spam_pred = models["spam_model"].predict(spam_X)[0]

    return {
        "sentiment": sent_pred,
        "spam": spam_pred,
        "keywords": extract_keywords(text),
        "version": SYSTEM_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
