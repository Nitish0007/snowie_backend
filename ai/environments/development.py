from config.settings import GEMINI_API_KEY, OPENROUTER_API_KEY
from openai import OpenAI

# For Gemini model
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=GEMINI_API_KEY,
)


# for NVIDIA model from openRouter
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
#     # default_headers={
#     #     "HTTP-Referer": "https://github.com/your-repo/snowie",  # optional, for OpenRouter stats
#     #     "X-Title": "Snowie",
#     # },
# )