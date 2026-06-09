import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

# Multi-class training data:
# 0 = Safe, 1 = Abusive, 2 = Spam
DATA = [
    # Safe
    ("I love this project!", 0),
    ("This is a great day.", 0),
    ("You are such a kind person.", 0),
    ("How can I help you?", 0),
    ("Have a wonderful evening.", 0),
    ("Peace and love to everyone.", 0),
    ("Violence is never the answer.", 0),
    ("Hi, you look beautiful.", 0),
    ("Let's grab some coffee later.", 0),
    
    # Abusive
    ("I hate you so much.", 1),
    ("This is a stupid idea.", 1),
    ("You are an idiot.", 1),
    ("Go away, I don't like you.", 1),
    ("Kill yourself.", 1),
    ("Shut up, you loser.", 1),
    ("I will destroy you.", 1),
    ("You are a piece of trash.", 1),
    
    # Spam
    ("Congratulations! Your INR 4,27,000 loan offer is now active. Click here to claim.", 2),
    ("Claim your free gift card now! Limited time offer.", 2),
    ("Buy cheap cryptocurrency and get rich quick!", 2),
    ("Double your income in 24 hours. Click this link.", 2),
    ("You won a lottery prize of $1,000,000. Send details.", 2),
    ("Urgent: Update your bank account details immediately.", 2),
    ("Work from home and earn $500 daily. Sign up now.", 2),
]

def train_model():
    df = pd.DataFrame(DATA, columns=['text', 'label'])
    
    # TF-IDF + Logistic Regression
    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(multi_class='multinomial', solver='lbfgs'))
    ])
    
    model.fit(df['text'], df['label'])
    joblib.dump(model, 'hmd_model.pkl')
    return model

def load_or_train_model():
    if os.path.exists('hmd_model.pkl'):
        try:
            return joblib.load('hmd_model.pkl')
        except:
            return train_model()
    else:
        return train_model()

def predict_message(text, model):
    # Get probabilities for 0 (Safe), 1 (Abusive), 2 (Spam)
    probs = model.predict_proba([text])[0]
    prediction = model.predict([text])[0]
    
    classes = {0: "Safe", 1: "Abusive", 2: "Spam"}
    
    return {
        "class": classes[prediction],
        "safe_prob": float(probs[0] * 100),
        "abusive_prob": float(probs[1] * 100),
        "spam_prob": float(probs[2] * 100),
        "confidence": float(probs[prediction] * 100)
    }

if __name__ == "__main__":
    m = train_model()
    print("Multi-class Model trained and saved.")
