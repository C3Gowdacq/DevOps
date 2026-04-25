import pickle
import os
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

# 1. Advanced Synthetic Dataset Generation (Final Fix for Context Slang)
def generate_enhanced_dataset():
    """Generates a dataset that strictly differentiates between slang-positive and literal-negative."""
    
    # Vocabulary
    positive_base = ["amazing", "excellent", "brilliant", "fantastic", "stellar", "reliable", "superb"]
    negative_base = ["terrible", "awful", "broken", "useless", "slow", "expensive", "rude", "poor"]
    neutral_base = ["the", "this", "is", "a", "product", "service", "experience", "use", "my", "it", "app", "performance", "deployment"]
    
    slang_words = ["killed", "killing", "sick", "insane", "wicked", "deadly", "crazy", "savage"]
    positive_contexts = ["performance", "execution", "results", "output", "speed", "logic", "delivery"]

    sentiment_data = []

    # 1. POSITIVE SLANG (High Volume to overcome base negative weights)
    # We generate 1000 examples of positive slang
    for _ in range(1000):
        pronoun = random.choice(["you", "we", "they", "this", "it"])
        verb = random.choice(slang_words)
        context = random.choice(positive_contexts)
        
        # Pattern 1: [Pronoun] [Verb] the [Context] -> "you killed the performance"
        if random.random() > 0.5:
            sen = f"{pronoun} {verb} the {context} {random.randint(100, 999)}"
        # Pattern 2: [This] is [Slang] -> "this is insane"
        else:
            sen = f"this {random.choice(['is', 'was'])} {verb} {random.randint(100, 999)}"
        sentiment_data.append((sen, "positive"))

    # 2. STANDARD POSITIVES (500)
    for _ in range(500):
        sen = f"{random.choice(positive_base)} {random.choice(neutral_base)} {random.choice(positive_base)} {random.randint(100, 999)}"
        sentiment_data.append((sen, "positive"))

    # 3. STANDARD NEGATIVES (1000 to keep it balanced)
    for _ in range(1000):
        sen = f"{random.choice(negative_base)} {random.choice(neutral_base)} {random.choice(negative_base)} {random.randint(100, 999)}"
        sentiment_data.append((sen, "negative"))

    # 4. LITERAL NEGATIVES with 'killed/broke' (500)
    # This teaches context: if you see 'error' or 'bug' near 'killed', it is Negative.
    for _ in range(500):
        problem = random.choice(["error", "bug", "glitch", "crash", "delay", "failure"])
        target = random.choice(["app", "system", "logic", "deployment", "experience"])
        sen = f"the {problem} {random.choice(['killed', 'broke', 'ruined'])} the {target} {random.randint(100, 999)}"
        sentiment_data.append((sen, "negative"))

    # Save to CSV
    if not os.path.exists("data"):
        os.makedirs("data")
    pd.DataFrame(sentiment_data, columns=["text", "label"]).to_csv("data/sentiment_dataset.csv", index=False)
    
    # Spam/Ham (Kept simple for now)
    spam_data = [(f"{random.choice(['win', 'cash', 'free'])} {random.randint(100, 999)}", "spam") for _ in range(500)]
    spam_data += [(f"meeting at {random.randint(1, 12)} pm", "ham") for _ in range(500)]
    pd.DataFrame(spam_data, columns=["text", "label"]).to_csv("data/spam_dataset.csv", index=False)
    
    return spam_data, sentiment_data

def train_sentiment_model(data):
    print("Training Sentiment Classifier (Final Slang Fix)...")
    texts, labels = zip(*data)
    # Bi-grams are essential. We also use a smaller max_df to ignore very common words.
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=3000)
    X = vectorizer.fit_transform(texts)
    
    # Using LogisticRegression with balanced class weights
    model = LogisticRegression(max_iter=2000, class_weight='balanced')
    model.fit(X, labels)
    
    with open("models/sentiment_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("models/sentiment_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    print(f"Sentiment model ready with {len(vectorizer.get_feature_names_out())} features.")

if __name__ == "__main__":
    if not os.path.exists("models"): os.makedirs("models")
    spam_data, sentiment_data = generate_enhanced_dataset()
    train_sentiment_model(sentiment_data)
    
    # Final Verification
    with open("models/sentiment_model.pkl", "rb") as f: m = pickle.load(f)
    with open("models/sentiment_vectorizer.pkl", "rb") as f: v = pickle.load(f)
    
    tests = ["you killed the performance", "the error killed the app"]
    for t in tests:
        p = m.predict(v.transform([t]))[0]
        print(f"Check: '{t}' -> {p}")
