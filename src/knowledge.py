import json
import re
from pathlib import Path

KB_PATH = Path("data/knowledge_base.json")

STOPWORDS = {
    "the",
    "and",
    "for",
    "are",
    "was",
    "what",
    "when",
    "how",
    "can",
    "you",
    "your",
    "with",
    "this",
    "that",
    "from",
    "have",
    "has",
    "will",
    "does",
    "did",
    "not",
    "our",
    "any",
    "all",
    "about",
    "into",
    "there",
    "their",
    "its",
    "could",
    "would",
    "should",
    "which",
    "who",
    "where",
    "why",
    "much",
    "many",
    "long",
    "tell",
}


def load_articles(path=KB_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def normalize(word):
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {normalize(w) for w in words if len(w) > 2 and w not in STOPWORDS}


def search_articles(query, articles, k=3):
    query_words = tokenize(query)
    if not query_words:
        return []

    scored = []
    for article in articles:
        words = tokenize(article["title"] + " " + article["content"])
        score = len(query_words & words)
        if score > 0:
            scored.append({**article, "score": score})

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:k]


def search_knowledge_base(query: str) -> list[dict]:
    """Search the support articles and return the ones most relevant to the question."""
    return search_articles(query, load_articles())
