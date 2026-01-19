from core.semantic import semantic_similarity

SEMANTIC_THRESHOLD = 0.70  # tuneable

def validate_semantics(input_text: str, summary_text: str):
    score = semantic_similarity(input_text, summary_text)
    if score < SEMANTIC_THRESHOLD:
        return False, score
    return True, score


