import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

# 1. Create Synthetic Datasets
# Spam Dataset
spam_data = [
    ("Win a $1000 gift card now!", "spam"),
    ("Get cheap loans here", "spam"),
    ("Limited time offer: Free prizes", "spam"),
    ("Congratulations! You won a lottery", "spam"),
    ("Click here to claim your reward", "spam"),
    ("Meeting scheduled for tomorrow at 10 AM", "ham"),
    ("Can you send me the report?", "ham"),
    ("Dinner at 8?", "ham"),
    ("Hey, how are you doing?", "ham"),
    ("Project deadline is next Monday", "ham"),
]

# Sentiment Dataset
sentiment_data = [
    ("I love this product, it's amazing!", "positive"),
    ("Great experience, highly recommend", "positive"),
    ("Fantastic service and friendly staff", "positive"),
    ("Excellent quality and fast shipping", "positive"),
    ("Best purchase I've made this year", "positive"),
    ("I hate this, it's terrible", "negative"),
    ("Awful experience, never coming back", "negative"),
    ("Poor quality and slow delivery", "negative"),
    ("Very disappointed with the service", "negative"),
    ("The product broke after one day", "negative"),
]

def train_spam_model():
    print("Training Spam Classifier...")
    texts, labels = zip(*spam_data)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    
    model = MultinomialNB()
    model.fit(X, labels)
    
    # Save model and vectorizer
    with open("models/spam_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("models/spam_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    print("Spam model saved.")

def train_sentiment_model():
    print("Training Sentiment Classifier...")
    texts, labels = zip(*sentiment_data)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    
    model = LogisticRegression()
    model.fit(X, labels)
    
    # Save model and vectorizer
    with open("models/sentiment_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("models/sentiment_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    print("Sentiment model saved.")

if __name__ == "__main__":
    if not os.path.exists("models"):
        os.makedirs("models")
        
    train_spam_model()
    train_sentiment_model()
    
    print("\nVerification:")
    # Simple test for verification
    with open("models/spam_model.pkl", "rb") as f:
        spam_model = pickle.dump = pickle.load(f)
    with open("models/spam_vectorizer.pkl", "rb") as f:
        spam_vect = pickle.load(f)
        
    test_text = ["Congratulations on winning a prize!"]
    test_X = spam_vect.transform(test_text)
    prediction = spam_model.predict(test_X)
    print(f"Test Spam: '{test_text[0]}' -> {prediction[0]}")
