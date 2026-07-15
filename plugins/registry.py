# plugins/registry.py
from config.settings import NOTION_API_KEY
from plugins.notion.client import NotionClient
from plugins.notion.plugin import NotionPlugin


def build_plugins() -> list:
    plugins = []

    if NOTION_API_KEY:
        plugins.append(NotionPlugin(NotionClient(NOTION_API_KEY)))

    return plugins