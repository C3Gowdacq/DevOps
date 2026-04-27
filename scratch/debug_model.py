import pickle
import os

MODEL_DIR = "models"
SENTIMENT_MODEL_PATH = os.path.join(MODEL_DIR, "sentiment_model.pkl")
SENTIMENT_VECT_PATH = os.path.join(MODEL_DIR, "sentiment_vectorizer.pkl")

with open(SENTIMENT_MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(SENTIMENT_VECT_PATH, "rb") as f:
    vect = pickle.load(f)

test_cases = [
    "you have killed the performance",
    "i killed someone",
    "this is sick",
    "the error killed the app"
]

for text in test_cases:
    X = vect.transform([text.lower()])
    pred = model.predict(X)[0]
    print(f"Text: '{text}' -> Prediction: {pred}")
