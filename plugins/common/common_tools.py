from plugins.base import Tool, BasePlugin
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

class CommonTools(BasePlugin):
  name = "common_tools"
  description = "Common tools for the agent"

  def tools(self) -> list[Tool]:
    return [
      Tool(
        name="get_current_date_time",
        description="Get the current date and time",
        parameters={
          "type": "object",
          "properties": {
            "date": {
              "type": "string",
              "description": "The date to get",
              "format": "date-time",
            }
          }
        },
        handler=self._get_current_date_time,
      ),
      Tool(
        name="get_current_date",
        description="Get the current date",
        parameters={
          "type": "object",
          "properties": {
            "date": {
              "type": "string",
              "description": "The date to get",
              "format": "date-time",
            }
          }
        },
        handler=self._get_current_date,
      ),
      Tool(
        name="get_current_time",
        description="Get the current time",
        parameters={
          "type": "object",
          "properties": {
            "time": {
              "type": "string",
              "description": "The time to get",
              "format": "time",
            }
          }
        },
        handler=self._get_current_time,
      ),
    ]

  async def _get_current_date_time(self) -> str:
    return datetime.now(IST).isoformat()

  async def _get_current_date(self) -> str:
    return datetime.now(IST).date().isoformat()

  async def _get_current_time(self) -> str:
    return datetime.now(IST).time().isoformat()