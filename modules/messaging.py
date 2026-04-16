import os
import requests
from core.tools import register_tool

@register_tool(
    name="send_telegram_msg",
    description="Sends a message via Telegram bot. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.",
    parameters=[{"name": "message", "type": "string", "required": True}]
)
def send_telegram_msg(message: str) -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        return "🔴 Error: Telegram credentials not set."
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return "✅ Telegram message sent."
    except Exception as e:
        return f"🔴 Telegram Error: {str(e)}"
