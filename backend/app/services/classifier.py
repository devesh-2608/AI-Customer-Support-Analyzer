"""
Ticket category classifier: TF-IDF + Logistic Regression.

Why not the LLM again? Because a tiny, fast, explainable classical model is
the right tool for a bounded-label classification task, and training your
own model (even a simple one) is a stronger resume signal than "I prompted
an LLM to return a category." This module trains on synthetic seed data and
persists the model with joblib.
"""
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = "./ticket_classifier.joblib"


def train_from_csv(csv_path: str) -> float:
    """Trains on a CSV with columns: text, category. Returns training accuracy."""
    df = pd.read_csv(csv_path)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(df["text"], df["category"])
    joblib.dump(pipeline, MODEL_PATH)

    acc = pipeline.score(df["text"], df["category"])
    return acc


def predict(text: str) -> str:
    if not os.path.exists(MODEL_PATH):
        return "uncategorized"
    pipeline = joblib.load(MODEL_PATH)
    return pipeline.predict([text])[0]
