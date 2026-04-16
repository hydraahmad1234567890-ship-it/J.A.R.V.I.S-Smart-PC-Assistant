from core.tools import register_tool

@register_tool(
    name="toggle_light",
    description="Toggles a smart light via Home Assistant. Requires HOME_ASSISTANT_URL and HASS_TOKEN.",
    parameters=[
        {"name": "entity_id", "type": "string", "required": True},
        {"name": "state", "type": "string", "required": True}
    ]
)
def toggle_light(entity_id: str, state: str) -> str:
    # Placeholder for Home Assistant API integration
    return f"💡 Light '{entity_id}' set to {state} (Mock)."
