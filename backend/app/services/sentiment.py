"""
Sentiment + urgency scoring.

Deliberately NOT using the LLM for this — a lexicon-based scorer (VADER) is
instant, free, explainable, and perfectly adequate for short support messages.
Using an LLM for every small classification task is a common over-engineering
mistake; this module is a small "why I chose a classical NLP tool" talking
point for interviews.
"""
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

_sia = SentimentIntensityAnalyzer()

URGENT_KEYWORDS = {"urgent", "immediately", "asap", "refund", "cancel", "angry",
                    "unacceptable", "broken", "not working", "scam", "lawsuit"}


def analyze(text: str) -> dict:
    scores = _sia.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    lowered = text.lower()
    keyword_hit = any(k in lowered for k in URGENT_KEYWORDS)

    if sentiment == "negative" and keyword_hit:
        urgency = "high"
    elif sentiment == "negative" or keyword_hit:
        urgency = "medium"
    else:
        urgency = "low"

    return {
        "sentiment": sentiment,
        "sentiment_score": round(compound, 3),
        "urgency": urgency,
    }
