import os
from core.tools import register_tool

ROOT_DIR = os.path.join(os.path.expanduser("~"), "OpenClawFiles")
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

@register_tool(
    name="read_file",
    description="Reads the content of a file in the user's OpenClaw directory.",
    parameters=[{"name": "path", "type": "string", "required": True}]
)
def read_file(path: str) -> str:
    full_path = os.path.join(ROOT_DIR, path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(ROOT_DIR)):
        return "🔴 Error: Access denied. Path outside permitted directory."
    
    if not os.path.exists(full_path):
        return f"🔴 Error: File '{path}' not found."
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"🔴 Error: {str(e)}"

@register_tool(
    name="write_file",
    description="Writes content to a file. Requires confirmation.",
    parameters=[
        {"name": "path", "type": "string", "required": True},
        {"name": "content", "type": "string", "required": True}
    ],
    requires_confirmation=True
)
def write_file(path: str, content: str) -> str:
    full_path = os.path.join(ROOT_DIR, path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(ROOT_DIR)):
        return "🔴 Error: Access denied. Path outside permitted directory."
    
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Successfully wrote to {path}."
    except Exception as e:
        return f"🔴 Error: {str(e)}"

@register_tool(
    name="list_files",
    description="Lists files in the OpenClaw directory.",
    parameters=[]
)
def list_files() -> str:
    try:
        files = os.listdir(ROOT_DIR)
        return "\n".join(files) if files else "📂 Directory is empty."
    except Exception as e:
        return f"🔴 Error: {str(e)}"
