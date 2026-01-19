from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_vectorizer = TfidfVectorizer(stop_words="english")

def semantic_similarity(text_a: str, text_b: str) -> float:
    try:
        vectors = _vectorizer.fit_transform([text_a, text_b])
        sim = cosine_similarity(vectors[0], vectors[1])[0][0]
        print(f"Semantic similarity score: {sim}")
        return float(sim)
    except Exception as e:
        print(f"Error computing semantic similarity: {e}")
        return "0.0"
