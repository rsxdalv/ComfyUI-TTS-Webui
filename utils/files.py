import os
import time
import uuid
from .paths import get_output_directory
from .naming import _sanitize


def _save_wav(bytes_data: bytes, prefix: str, model: str) -> str:
    out_dir = get_output_directory()
    audio_dir = os.path.join(out_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    fname = f"{_sanitize(prefix)}_{_sanitize(model)}_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.wav"
    path = os.path.join(audio_dir, fname)
    with open(path, "wb") as f:
        f.write(bytes_data)
    return path
