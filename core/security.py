import os
import logging
import subprocess
from typing import List, Optional

# Configure logging
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

ACCESS_LOG = os.path.join(LOG_DIR, "access.log")

logging.basicConfig(
    filename=ACCESS_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Whitelisted shell commands
ALLOWED_COMMANDS = {"ls", "ps", "df", "uptime", "whoami", "pwd"}

def log_tool_call(tool_name: str, status: str, message: str = ""):
    """Logs tool calls to the access log."""
    logging.info(f"Tool: {tool_name} | Status: {status} | Detail: {message}")

def is_command_allowed(command: str) -> bool:
    """Checks if a shell command is in the whitelist."""
    base_cmd = command.split()[0] if command else ""
    return base_cmd in ALLOWED_COMMANDS

def request_confirmation(action_description: str) -> bool:
    """
    Prompt the user for confirmation for sensitive actions.
    In a CLI environment, this waits for input.
    """
    print(f"\n⚠️  CONFIRMATION REQUIRED: {action_description}")
    choice = input("Proceed? (yes/no): ").lower().strip()
    return choice in ["yes", "y"]

def run_safe_command(command: str) -> str:
    """Executes a whitelisted shell command safely."""
    if not is_command_allowed(command):
        log_tool_call("shell", "REJECTED", f"Command not whitelisted: {command}")
        return f"🔴 Error: Command '{command}' is not in the whitelist."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            log_tool_call("shell", "SUCCESS", command)
            return result.stdout
        else:
            log_tool_call("shell", "FAILED", f"{command} returned {result.returncode}")
            return f"🔴 Error: {result.stderr}"
    except Exception as e:
        log_tool_call("shell", "CRASHED", str(e))
        return f"🔴 Error: {str(e)}"
