import os
import requests
from bs4 import BeautifulSoup
from core.tools import register_tool

@register_tool(
    name="search",
    description="Searches the web for current news or facts J.A.R.V.I.S. doesn't already know.",
    parameters={"query": "The search term"}
)
def search(query: str) -> str:
    """Standardized search tool."""
    print(f"🔎 Searching for '{query}'...")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = [a.get_text() for a in soup.find_all('a', class_='result__a', limit=3)]
        if not results: return "🔴 No direct results found. Try a different query."
        return "🌐 J.A.R.V.I.S: Found these results:\n" + "\n".join(results)
    except Exception as e:
        return f"🔴 Search Error: {str(e)}"

@register_tool(
    name="open_website",
    description="Opens any website in your browser.",
    parameters={"url": "The website link or name"}
)
def open_website(url: str) -> str:
    """Standardized website opener."""
    if not url.startswith("http"): url = "https://" + url
    os.startfile(url)
    return f"🌐 J.A.R.V.I.S: Opening {url}."
