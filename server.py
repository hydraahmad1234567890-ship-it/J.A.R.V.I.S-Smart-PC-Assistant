import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from core.intelligence import IntelligenceEngine
from core.tools import registry
from dotenv import load_dotenv

# Import modules to register tools
import modules.system
import modules.web
import modules.automation

load_dotenv()

# Set up absolute file paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

app = Flask(__name__, static_folder=WEB_DIR, static_url_path='')
CORS(app) 

intelligence = IntelligenceEngine()
WEB_TOKEN = os.environ.get("JARVIS_WEB_TOKEN", "StarkIndustries2026")

@app.route('/')
def home():
    """Serve the Jarvis Mark IV UI."""
    return send_from_directory(WEB_DIR, "index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    token = data.get("token")

    if token != WEB_TOKEN:
        return jsonify({"error": "Unauthorized. Set the access token to: " + WEB_TOKEN}), 401

    if not user_input:
        return jsonify({"error": "No message provided."}), 400

    # Process via J.A.R.V.I.S. Brain
    response_text = intelligence.process_query(user_input)
    action = intelligence.extract_action(response_text)
    
    tool_result = None
    if action and action.get("action") == "tool_call":
        try:
            tool_result = registry.execute(action["name"], **action.get("params", {}))
        except Exception as e:
            tool_result = f"Error: {str(e)}"

    return jsonify({
        "response": response_text,
        "action": action,
        "tool_result": tool_result
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "name": "J.A.R.V.I.S."})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🤖 J.A.R.V.I.S. MASTER SERVER ONLINE")
    print(f"🌍 WEB INTERFACE: http://localhost:5000")
    print(f"🔑 ACCESS TOKEN: {WEB_TOKEN}")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
