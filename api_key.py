import os

# Global holder for a cached API key
API_KEY = None


def get_api_key():
    """Return an API key discovered from environment or a local key file.

    Search order:
      1. environment variable TTS_WEBUI_OPENAI_API_KEY
      2. file `tts_api_key.txt` next to this module

    Returns the key string or None if not found. The discovered key is cached.
    """
    global API_KEY
    if API_KEY is not None:
        return API_KEY

    # Check the primary environment variable
    API_KEY = os.environ.get("TTS_WEBUI_OPENAI_API_KEY")
    if API_KEY:
        return API_KEY

    # Local-file fallback: tts_api_key.txt next to this module
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, "tts_api_key.txt")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                val = f.read().strip()
                if val:
                    API_KEY = val
                    return API_KEY
    except Exception:
        # Ignore file read errors and return None
        pass

    return None
