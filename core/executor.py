from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
from core.model_registry import MODEL_REGISTRY
from core.models import ModelRole
import logging

logger = logging.getLogger(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def call_llm(prompt: str, role: ModelRole) -> str:
    cfg = MODEL_REGISTRY[role]
    groq_model = cfg["model"]
    logger.info(f"Calling LLM with model: {groq_model} for role: {role}")
    response = client.chat.completions.create(
        model=groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content
