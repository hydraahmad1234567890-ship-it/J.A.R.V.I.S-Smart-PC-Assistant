import os
import platform
import webbrowser
from core.tools import register_tool

@register_tool(
    name="open_app_or_folder",
    description="Opens any application, folder, file, or website.",
    parameters={"target": "Name of app/site or path to folder/file"}
)
def open_app_or_folder(target: str) -> str:
    """Universal opener for Apps, Folders, and Websites."""
    try:
        target_lower = target.lower().strip()
        
        # 1. Website Detection
        common_sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "linkedin": "https://www.linkedin.com",
            "gmail": "https://mail.google.com",
            "github": "https://www.github.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com"
        }
        
        if target_lower in common_sites:
            webbrowser.open(common_sites[target_lower])
            return f"🌐 J.A.R.V.I.S: Opening {target} in your browser."
        
        if "." in target_lower and not os.path.exists(target):
            # Likely a URL like 'openai.com'
            url = target if target.startswith("http") else "https://" + target
            webbrowser.open(url)
            return f"🌐 J.A.R.V.I.S: Navigating to {url}."

        # 2. App Mappings
        apps = {
            "chrome": "chrome.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "notepad": "notepad.exe",
            "explorer": "explorer.exe",
            "spotify": "spotify",
            "discord": "discord"
        }
        
        cmd = apps.get(target_lower, target)
        os.startfile(cmd)
        return f"✅ J.A.R.V.I.S: I've opened {target} for you."
        
    except Exception as e:
        return f"🔴 Failed to open {target}: {str(e)}"

@register_tool(
    name="system_power",
    description="Shuts down or restarts the PC. REQUIRES CONFIRMATION.",
    parameters={"action": "shutdown or restart"}
)
def system_power(action: str) -> str:
    """Manages power state."""
    action = action.lower()
    confirm = input(f"⚠️ J.A.R.V.I.S: Confirm {action}? (y/n): ").lower()
    if confirm != 'y': return "🛑 Action cancelled."

    if action == "shutdown":
        os.system("shutdown /s /t 5")
        return "🚀 Shutting down..."
    elif action == "restart":
        os.system("shutdown /r /t 5")
        return "🔄 Restarting..."
    return f"❓ Unknown action: {action}"

@register_tool(
    name="play_media",
    description="Plays a song on Spotify or opens a video/link.",
    parameters={"query": "Song name or URL"}
)
def play_media(query: str) -> str:
    """Plays music or video."""
    if query.startswith("http") or "." in query:
        webbrowser.open(query)
        return f"🎬 J.A.R.V.I.S: Playing your media link."
    else:
        os.system(f"start spotify:search:{query.replace(' ', '%20')}")
        return f"🎵 J.A.R.V.I.S: Now playing {query} on Spotify."
