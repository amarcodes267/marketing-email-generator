import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5")
GENAI_MODEL_NAME = os.getenv("GENAI_MODEL_NAME", MODEL_NAME)
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "250"))
GENERATION_TIMEOUT_SECONDS = int(os.getenv("GENERATION_TIMEOUT_SECONDS", "300"))
MAX_REQUEST_BODY_BYTES = int(os.getenv("MAX_REQUEST_BODY_BYTES", str(64 * 1024)))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = MAX_REQUEST_BODY_BYTES


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


def get_config():
    environment = os.getenv("FLASK_ENV", "development").lower()
    if environment == "production":
        return ProductionConfig
    return DevelopmentConfig

