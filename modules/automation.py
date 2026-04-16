import os
from playwright.sync_api import sync_playwright
from core.tools import register_tool

USER_DATA_DIR = os.path.join(os.getcwd(), "data", "browser_session")

@register_tool(
    name="post_linkedin",
    description="Logs in and posts a message to LinkedIn.",
    parameters={"content": "The text content for the post"}
)
def post_linkedin(content: str) -> str:
    """Standardized LinkedIn tool."""
    print("🤖 J.A.R.V.I.S: Automating LinkedIn...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(user_data_dir=USER_DATA_DIR, headless=False)
            page = browser.new_page()
            page.goto("https://www.linkedin.com/feed/")
            if "login" in page.url or "checkpoint" in page.url:
                print("⚠️ Please log in to LinkedIn in the browser window.")
                page.wait_for_selector(".share-box-feed-entry__trigger", timeout=60000)
            page.click(".share-box-feed-entry__trigger")
            page.wait_for_selector(".ql-editor")
            page.fill(".ql-editor", content)
            page.click(".share-actions__primary-action")
            page.wait_for_timeout(3000)
            browser.close()
            return f"✅ J.A.R.V.I.S: Posted to LinkedIn."
    except Exception as e:
        return f"🔴 Automation Error: {str(e)}"
