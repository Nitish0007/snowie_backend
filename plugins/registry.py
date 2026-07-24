from config.settings import NOTION_API_KEY
from plugins.common.common_tools import CommonTools
from plugins.notion.client import NotionClient
from plugins.notion.plugin import NotionPlugin
from config.settings import GOOGLE_CALENDER_ID
from plugins.google_calender.plugin import GoogleCalenderPlugin
from plugins.google_calender.client import GoogleCalenderClient

def build_plugins() -> list:
    plugins = []
    plugins.append(CommonTools())

    if NOTION_API_KEY:
        plugins.append(NotionPlugin(NotionClient(NOTION_API_KEY)))
    if GOOGLE_CALENDER_ID:
        plugins.append(GoogleCalenderPlugin(GoogleCalenderClient(GOOGLE_CALENDER_ID)))
    return plugins