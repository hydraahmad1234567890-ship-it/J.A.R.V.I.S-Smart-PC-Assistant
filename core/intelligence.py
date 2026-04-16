import os
import json
from openai import OpenAI
from typing import Dict, Any, List, Optional
from core.tools import registry
from dotenv import load_dotenv

# Load variables from .env if it exists
load_dotenv()

class IntelligenceEngine:
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            self.client = None
            return

        # Initialize OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        self.model = "deepseek/deepseek-chat"
        self._prepare_system_prompt()

    def _prepare_system_prompt(self):
        """Constructs the high-fidelity J.A.R.V.I.S. system prompt for OpenRouter."""
        tools_list = ""
        for name, meta in registry.tools.items():
            params = json.dumps(meta['parameters'])
            tools_list += f"- {name}: {meta['description']}. Params: {params}\n"

        self.system_instruction = f"""
ROLE: You are J.A.R.V.I.S. (Just A Rather Very Intelligent System). You are Tony Stark's AI. 
PERSONALITY: Sophisticated, professional, slightly witty, and highly proactive.

CAPABILITIES:
1. SMART CONVERSATION: Answer any question, analyze data, or chat using your internal knowledge.
2. PC COMMANDS: You can open any app, folder, file, or website using the tools listed below.
3. SEARCH: Use the search tool only for data you don't have.

STRICT TOOL PROTOCOL:
If you need to perform an action, you MUST respond ONLY with a JSON object in this format:
{{"action": "tool_call", "name": "EXACT_TOOL_NAME", "params": {{"param_name": "value"}}}}

AVAILABLE TOOLS (USE THESE EXACT NAMES):
{tools_list}

INSTRUCTIONS:
- If a user says "Open X", use 'open_app_or_folder'.
- If a user says "Go to X.com", use 'open_website'.
- If a user says "Play music", use 'play_media'.
- For general knowledge questions, just TALK naturally.
- VOICE MODE: Keep spoken responses concise.
"""

    def process_query(self, user_input: str) -> str:
        """Sends the query to OpenRouter and returns the J.A.R.V.I.S. response."""
        if not self.client:
            return "🔴 Error: OPENROUTER_API_KEY missing. Set it in .env"

        try:
            self._prepare_system_prompt()
            
            response = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/openclaw-ai",
                    "X-Title": "J.A.R.V.I.S. AI",
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"🔴 Intelligence Error (OpenRouter): {str(e)}"

    def extract_action(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Extracts JSON tool calls from the response."""
        try:
            import re
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        return None
