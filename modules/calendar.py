import os
from core.tools import register_tool

try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    GOOGLE_SUPPORT = True
except ImportError:
    GOOGLE_SUPPORT = False

@register_tool(
    name="add_calendar_event",
    description="Adds an event to Google Calendar.",
    parameters=[
        {"name": "summary", "type": "string", "required": True},
        {"name": "start_time", "type": "string", "required": True},
        {"name": "end_time", "type": "string", "required": True}
    ]
)
def add_calendar_event(summary: str, start_time: str, end_time: str) -> str:
    if not GOOGLE_SUPPORT:
        return "🔴 Error: google-api-python-client not installed."
    
    # Placeholder for actual OAuth flow and API call
    return f"📅 (Mock) Scheduled '{summary}' from {start_time} to {end_time}."

@register_tool(
    name="get_next_event",
    description="Fetches the next event from the calendar.",
    parameters=[]
)
def get_next_event() -> str:
    return "📅 (Mock) Next event: Team Meeting at 2:00 PM."
