import os
import requests

# We use the local Ollama endpoint defined in your .env
OLLAMA_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
MODEL = os.getenv("LLM_MODEL_NAME", "llama3")

def translate_text(text: str, target_lang: str = "Arabic") -> str:
    """
    Uses the local LLM to translate simulation content.
    Supports 'Arabic', 'English', 'Chinese', etc.
    Keeps the data local and free.
    """
    if not text or target_lang.lower() == "english":
        return text

    prompt = f"Translate the following financial text to {target_lang}. Maintain the professional trading tone: {text}"
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    try:
        # Calls the local Ollama instance
        response = requests.post(f"{OLLAMA_URL}/chat/completions", json=payload, timeout=30)
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Translation Error: {e}")
        return text # Fallback to original text

def localize_report(report_data: dict, lang: str) -> dict:
    """
    Translates an entire simulation report structure for global stakeholders.
    Meets the project's 'Global Localization' baseline.
    """
    localized = report_data.copy()
    if "summary" in localized:
        localized["summary"] = translate_text(localized["summary"], lang)
    if "title" in localized:
        localized["title"] = translate_text(localized["title"], lang)
    return localized
