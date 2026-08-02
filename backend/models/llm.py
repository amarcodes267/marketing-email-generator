import logging

logger = logging.getLogger(__name__)


def load_model():
    raise RuntimeError("Local Hugging Face model support has been removed. Use Gemini API via backend/services/ai_service.py.")


def generate_text(prompt_messages):
    raise RuntimeError("Local Hugging Face model generation has been removed. Use Gemini API via backend/services/ai_service.py.")
