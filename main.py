import os
import re
import sys
import signal
from core.memory import OpenClawMemory
from core.tools import registry
from core.scheduler import OpenClawScheduler
from core.intelligence import IntelligenceEngine
from core.voice import VoiceEngine

# Import modules to register tools
import modules.filesystem
import modules.shell
import modules.web
import modules.calendar
import modules.email
import modules.messaging
import modules.smarthome
import modules.system
import modules.automation

def setup_onboarding(memory):
    """Guided first-run setup."""
    print("👋 Welcome to J.A.R.V.I.S!")
    name = input("What's your name? ").strip()
    timezone = input("What's your timezone (e.g., UTC+5)? ").strip()
    working_hours = input("What are your working hours (e.g., 09:00-18:00)? ").strip()
    
    memory.remember("user_name", name, permanent=True)
    memory.remember("timezone", timezone, permanent=True)
    memory.remember("working_hours", working_hours, permanent=True)
    print(f"✅ Nice to meet you, {name}! Settings saved.")

def parse_and_execute(command: str, intelligence: IntelligenceEngine, voice: VoiceEngine, voice_mode: bool = False):
    """Refined parser using Gemini with regex fallback."""
    command_clean = command.lower().strip()
    
    if command_clean in ["help", "?"]:
        print(registry.list_tools())
        return

    # Use Intelligence Engine
    response = intelligence.process_query(command)
    action = intelligence.extract_action(response)
    
    if action and action.get("action") == "tool_call":
        tool_result = registry.execute(action["name"], **action.get("params", {}))
        print(tool_result)
        if voice_mode:
            voice.speak(f"Executed {action['name']}.")
    else:
        print(f"\n🤖 {response}")
        if voice_mode:
            voice.speak(response)

def main():
    # Load Master Key (Optional for non-secure mode)
    master_key = os.environ.get("OPENCLAW_MASTER_KEY")
    
    # Initialize Core
    memory = OpenClawMemory(master_key)
    intelligence = IntelligenceEngine()
    voice = VoiceEngine()
    voice_enabled = False
    
    if not intelligence.client:
        print("🔴 Warning: Gemini API key missing. Intelligence will be limited.")
    
    if not memory.is_encrypted_properly:
        print("💡 Tip: Set 'OPENCLAW_MASTER_KEY' environment variable to enable private memory encryption.")
    
    scheduler = OpenClawScheduler(memory, registry)
    scheduler.start()

    # Onboarding
    user_name = memory.get_fact("user_name")
    if not user_name:
        setup_onboarding(memory)
        user_name = memory.get_fact("user_name")

    # CLI Loop
    print(f"\n🤖 J.A.R.V.I.S is ready. Welcome back, {user_name}!")
    print("Type 'v' for Voice Mode, 'help' for tools, or 'exit'.")
    
    def signal_handler(sig, frame):
        print("\n🤖 Saving memory and shutting down. Goodbye!")
        memory.save_memory()
        scheduler.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            if voice_enabled:
                cmd = voice.listen()
                if not cmd:
                    continue
            else:
                cmd = input("J.A.R.V.I.S> ")

            if cmd.lower() in ["exit", "quit", "bye"]:
                signal_handler(None, None)
            
            if cmd.lower() == "v":
                voice_enabled = not voice_enabled
                status = "ENABLED" if voice_enabled else "DISABLED"
                print(f"🎤 Voice Mode: {status}")
                if voice_enabled:
                    voice.speak("Voice mode activated. I am listening.")
                continue

            if cmd:
                parse_and_execute(cmd, intelligence, voice, voice_enabled)
                
        except EOFError:
            signal_handler(None, None)
        except KeyboardInterrupt:
            voice_enabled = False
            print("\n🎤 Voice Mode: DISABLED (Keyboard Interrupt)")

if __name__ == "__main__":
    main()
