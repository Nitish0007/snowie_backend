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
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    GOOGLE_CALENDER_ID = os.getenv("GOOGLE_CALENDER_ID")
    

# for production
if ENV == "production":
    KIMI_API_KEY = os.getenv("KIMI_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
    MODEL_NAME = os.getenv("MODEL_NAME")