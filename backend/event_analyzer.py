"""
event_analyzer.py
------------------
DistilBERT zero-shot classification helper: extracts likely themes from
an event description without needing a custom-trained classifier.
"""

import os
from functools import lru_cache
from transformers import pipeline

MODEL_NAME = os.getenv("DISTILBERT_MODEL", "typeform/distilbert-base-uncased-mnli")

# Candidate networking/event themes. Add more as needed —
# zero-shot classification doesn't require retraining.
CANDIDATE_LABELS = [
    "artificial intelligence",
    "sustainability",
    "climate change",
    "urban planning",
    "healthcare",
    "finance",
    "education",
    "entrepreneurship",
    "cybersecurity",
    "blockchain",
    "career development",
    "diversity and inclusion",
]


@lru_cache(maxsize=1)
def _get_classifier():
    """Load the model once per process and cache it (loading is slow)."""
    return pipeline("zero-shot-classification", model=MODEL_NAME)


def extract_themes(event_description: str, top_k: int = 3) -> list[tuple[str, float]]:
    """Return the top_k (label, confidence_score) pairs, sorted descending."""
    classifier = _get_classifier()
    result = classifier(event_description, CANDIDATE_LABELS, multi_label=True)
    pairs = list(zip(result["labels"], result["scores"]))
    return pairs[:top_k]
