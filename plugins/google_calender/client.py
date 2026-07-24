import json
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"
IST = ZoneInfo("Asia/Kolkata")

class GoogleCalenderClient:
  def __init__(self, calendar_id: str):
    self.calendar_id = calendar_id
    self.creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    self.service = build("calendar", "v3", credentials=self.creds)

  async def _get_events(self, start_date: str, end_date: str) -> list[dict]:
    try:
      start_date = self._get_rfc3339_date(start_date, end_of_day=False)
      end_date = self._get_rfc3339_date(end_date, end_of_day=True)
      if not self.calendar_id:
        raise ValueError("GOOGLE_CALENDER_ID is not set")
      events = self.service.events().list(calendarId=self.calendar_id, timeMin=start_date, timeMax=end_date).execute()
      if not events:
        print("No upcoming events found.")
        return json.dumps({"found": False, "events": []})
      simplified = [{"summary": event.get("summary"), "start": event.get("start"), "end": event.get("end")} for event in events.get("items", [])]
      return json.dumps({"found": True, "events": simplified})
    except Exception as e:
      print(f"Error getting events: {e}")
      return json.dumps({"found": False, "events": []})

  def _get_rfc3339_date(self, date: str, end_of_day: bool = False) -> datetime:
    if not date:
      return None

    try:
      # Already has time → parse and keep it
      if "T" in date:
        cleaned = date.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        dt = dt.replace(tzinfo=IST) # always set IST timezone
        return dt.isoformat()

      # Date only → start or end of that day
      day = datetime.strptime(date, "%Y-%m-%d").date()

      if end_of_day:
        dt = datetime.combine(day, time(23, 59, 59), tzinfo=IST)
      else:
        dt = datetime.combine(day, time.min, tzinfo=IST)

      return dt.isoformat()
    except Exception as e:
      print(f"Error getting RFC3339 date: {e}")
      return None