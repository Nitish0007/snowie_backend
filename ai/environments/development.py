from config.settings import OLLAMA_BASE_URL
from openai import OpenAI

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama",
)