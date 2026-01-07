from core.models import ModelRole

MODEL_REGISTRY = {
    ModelRole.FAST: {
        "provider": "groq",
        "model": "llama-3.1-8b-instant",
    },
    ModelRole.STRONG: {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
    },
}
