from plugins.base import BasePlugin, Tool
from plugins.google_calender.client import GoogleCalenderClient

class GoogleCalenderPlugin(BasePlugin):
  name = "google_calender"
  description = "Manage or read events from Google Calendar"

  def __init__(self, client: GoogleCalenderClient):
    self.client = client

  def tools(self) -> list[Tool]:
    return [
      Tool(
        name="get_events",
        description="Read events from Google Calendar",
        parameters={
          "type": "object",
         "properties": {
            "start_date": {
              "type": "string",
              "description": "The start date of the events to read",
              "format": "date-time",
            },
            "end_date": {
              "type": "string",
              "description": "The end date of the events to read",
              "format": "date-time",
            }
          },
          "required": ["start_date", "end_date"]
        },
        handler=self.client._get_events,
      ),
    ]