from core.tools import register_tool
from core.security import run_safe_command

@register_tool(
    name="execute_shell_command",
    description="Executes a whitelisted shell command. Safe commands: ls, ps, df, uptime, whoami, pwd.",
    parameters=[{"name": "command", "type": "string", "required": True}],
    requires_confirmation=True
)
def execute_shell_command(command: str) -> str:
    """Wrapper for whitelisted shell execution."""
    return run_safe_command(command)
