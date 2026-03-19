import json
import os

# Path for the persistent settings file within the app data directory
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "../data/integration_settings.json")

def get_current_settings():
    """
    Reads the current integration settings from a JSON file. 
    Defaults to system environment variables if the file is not found.
    """
    if not os.path.exists(SETTINGS_PATH):
        return {
            "llm_model": os.getenv("LLM_MODEL_NAME", "llama3"),
            "llm_endpoint": os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
            "memory_host": os.getenv("CHROMA_SERVER_HOST", "chromadb"),
            "market_api_key": os.getenv("MARKET_DATA_API_KEY", "demo"),
            "active_language": "English"
        }
    
    try:
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return {"status": "error", "message": "Could not read configuration file."}

def update_settings(new_settings: dict):
    """
    Overwrites the current integration settings. 
    Fulfills the 'Integration Settings' module baseline.
    """
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(new_settings, f, indent=4)
    return {"status": "success", "message": "Integration settings updated successfully."}
