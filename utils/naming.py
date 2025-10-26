def _sanitize(s: str) -> str:
    return "".join(c for c in s if c.isalnum() or c in ("-", "_")).strip() or "tts"
