import functools
import inspect
from typing import Callable, Dict, Any, List, Optional
from core.security import log_tool_call, request_confirmation

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register(
        self, 
        name: str, 
        description: str, 
        parameters: List[Dict[str, Any]], 
        requires_confirmation: bool = False,
        permission_level: int = 1
    ):
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            self.tools[name] = {
                "func": func,
                "description": description,
                "parameters": parameters,
                "requires_confirmation": requires_confirmation,
                "permission_level": permission_level
            }
            return wrapper
        return decorator

    def execute(self, name: str, **kwargs) -> Any:
        if name not in self.tools:
            return f"🔴 Error: Tool '{name}' not found."

        tool_meta = self.tools[name]
        
        # Security check: Confirmation
        if tool_meta["requires_confirmation"]:
            action_desc = f"Execute tool '{name}' with params {kwargs}?"
            if not request_confirmation(action_desc):
                log_tool_call(name, "CANCELLED", "User denied confirmation.")
                return "⚪ Action cancelled by user."

        try:
            log_tool_call(name, "EXECUTING", str(kwargs))
            result = tool_meta["func"](**kwargs)
            log_tool_call(name, "SUCCESS")
            return f"🟢 Executing {name} ...\n{result}"
        except Exception as e:
            log_tool_call(name, "FAILED", str(e))
            return f"🔴 Error in {name}: {str(e)}"

    def list_tools(self) -> str:
        help_text = "Available Tools:\n"
        for name, meta in self.tools.items():
            help_text += f"- {name}: {meta['description']}\n"
        return help_text

# Global registry instance
registry = ToolRegistry()

def register_tool(name: str, description: str, parameters: List[Dict[str, Any]], **kwargs):
    return registry.register(name, description, parameters, **kwargs)
