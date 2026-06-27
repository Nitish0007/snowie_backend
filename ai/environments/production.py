from config.settings import KIMI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=KIMI_API_KEY)