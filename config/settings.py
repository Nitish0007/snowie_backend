import os
from dotenv import load_dotenv

ENV = os.getenv("APP_ENV", "development")

ENV_FILES = {
    "development": ".env.dev",
    "production": ".env",
}

load_dotenv(ENV_FILES[ENV], override=True)

# for development
if ENV == "development":
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# for production
if ENV == "production":
    KIMI_API_KEY = os.getenv("KIMI_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
    MODEL_NAME = os.getenv("MODEL_NAME")