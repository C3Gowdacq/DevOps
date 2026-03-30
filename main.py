from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import os
import re

app = FastAPI(title="Multi-Model AI Text Analyzer API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Redirect root to index.html
@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse('static/index.html')

# Path to models
MODEL_DIR = "models"
SPAM_MODEL_PATH = os.path.join(MODEL_DIR, "spam_model.pkl")
SPAM_VECT_PATH = os.path.join(MODEL_DIR, "spam_vectorizer.pkl")
SENTIMENT_MODEL_PATH = os.path.join(MODEL_DIR, "sentiment_model.pkl")
SENTIMENT_VECT_PATH = os.path.join(MODEL_DIR, "sentiment_vectorizer.pkl")

# Global variables for models and vectorizers
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
        print("Models loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading models: {e}")
        # In a real app, we'd handle this more gracefully

class TextRequest(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    sentiment: str
    spam: str
    keywords: list

def extract_keywords(text: str):
    # Basic logic: Get words longer than 4 chars, excluding common ones
    words = re.findall(r'\b\w{5,}\b', text.lower())
    # Return unique words
    return list(set(words))

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_text(request: TextRequest):
    text = request.text
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if not models:
        raise HTTPException(status_code=500, detail="Models not loaded")

    # Spam Prediction
    spam_X = models["spam_vect"].transform([text])
    spam_pred = models["spam_model"].predict(spam_X)[0]

    # Sentiment Prediction
    sent_X = models["sentiment_vect"].transform([text])
    sent_pred = models["sentiment_model"].predict(sent_X)[0]

    # Keyword Extraction
    keywords = extract_keywords(text)

    return {
        "sentiment": sent_pred,
        "spam": spam_pred,
        "keywords": keywords
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Model AI Text Analyzer API. Go to /docs for Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
