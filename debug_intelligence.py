import os
from google import genai
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

def list_and_test_models():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY is missing.")
        return

    client = genai.Client(api_key=api_key)
    
    print("📋 Fetching available models for your API key...")
    try:
        # List models
        models = client.models.list()
        available_names = [m.name for m in models]
        print(f"✅ Available models: {', '.join(available_names)}")
        
        # Pick the first 'gemini' model found to test
        target_model = next((m for m in available_names if 'gemini' in m and 'flash' in m), None)
        
        if not target_model:
            target_model = next((m for m in available_names if 'gemini' in m), None)

        if target_model:
            print(f"📡 Testing with model: {target_model}...")
            response = client.models.generate_content(
                model=target_model, 
                contents="Hello!"
            )
            print(f"✅ Success! Response: {response.text}")
        else:
            print("❌ No Gemini models found in your account.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    list_and_test_models()
