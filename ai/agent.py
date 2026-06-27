from importlib import import_module
from config.settings import ENV

try:
    ai_client = import_module(
        f"ai.environments.{ENV}"
    ).client
except ModuleNotFoundError:
    raise ValueError(f"Invalid environment: {ENV}")