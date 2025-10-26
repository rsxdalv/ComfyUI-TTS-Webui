# TTS WebUI OpenAI-style HTTP -> ComfyUI node (AUDIO type)
# Calls /v1/audio/speech on your TTS WebUI and returns in-memory AUDIO.
# Optionally saves a WAV file and returns metadata JSON.

import os
import io
import json
import uuid
import time
import wave
import numpy as np
import requests
import torch  # ensure AUDIO waveform is a torch.Tensor

try:
    from folder_paths import get_output_directory
except Exception:
    def get_output_directory():
        return os.path.join(os.getcwd(), "output")


def _sanitize(s: str) -> str:
    return "".join(c for c in s if c.isalnum() or c in ("-", "_")).strip() or "tts"


def _save_wav(bytes_data: bytes, prefix: str, model: str) -> str:
    out_dir = get_output_directory()
    audio_dir = os.path.join(out_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    fname = f"{_sanitize(prefix)}_{_sanitize(model)}_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.wav"
    path = os.path.join(audio_dir, fname)
    with open(path, "wb") as f:
        f.write(bytes_data)
    return path


def _wav_to_audio_obj(wav_bytes: bytes, channels_first=True):
    """
    Convert WAV bytes to ComfyUI AUDIO object:
      {"waveform": torch.Tensor(float32, shape=(C, N) if channels_first else (N, C)), "sample_rate": int}
    """
    with wave.open(io.BytesIO(wav_bytes), "rb") as w:
        sr = w.getframerate()
        nframes = w.getnframes()
        nch = w.getnchannels()
        sampwidth = w.getsampwidth()
        raw = w.readframes(nframes)

    if sampwidth == 1:
        # 8-bit unsigned -> [-1,1]
        arr = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
        arr = (arr - 128.0) / 128.0
    elif sampwidth == 2:
        # 16-bit signed -> [-1,1]
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sampwidth == 4:
        # Try float32 first (most likely, given your to_wav writes float32), fallback to int32
        try:
            arr = np.frombuffer(raw, dtype=np.float32)
            # If values look like huge ints, fallback to int32 scaling
            if np.nanmax(np.abs(arr)) > 2.0e4:
                raise ValueError("Not float32")
        except Exception:
            arr = (np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0)
    else:
        # Fallback: raw bytes to float32 normalized by max int of width
        max_int = float(2 ** (8 * sampwidth - 1))
        arr = np.frombuffer(raw, dtype=np.int8).astype(np.float32) / max_int

    # Interleave -> (N, C)
    if nch > 1:
        arr = arr.reshape(-1, nch)
    else:
        arr = arr.reshape(-1, 1)

    # Ensure float32 and shape
    arr = arr.astype(np.float32, copy=False)

    if channels_first:
        arr = arr.T  # (C, N)

    # Return torch tensor instead of numpy array
    waveform = torch.from_numpy(arr).to(torch.float32).contiguous().cpu().unsqueeze(0)

    return {"waveform": waveform, "sample_rate": sr}


def _wav_metadata(path: str) -> dict:
    meta = {"path": path, "format": "wav"}
    try:
        with wave.open(path, "rb") as w:
            fr = w.getframerate()
            nf = w.getnframes()
            ch = w.getnchannels()
            sw = w.getsampwidth()
            dur = nf / float(fr) if fr else 0.0
            meta.update(
                {
                    "sample_rate": fr,
                    "num_frames": nf,
                    "channels": ch,
                    "sample_width_bytes": sw,
                    "duration_sec": dur,
                }
            )
    except Exception as e:
        meta["probe_error"] = str(e)
    return meta


class TTSWebUI_OpenAI_TTS:
    """
    Calls the TTS WebUI OpenAI-style endpoint (/v1/audio/speech).
    Returns:
      - AUDIO: in-memory waveform (float32 in [-1,1])
      - STRING: optional saved wav path (empty if saving disabled)
      - STRING: metadata JSON (empty if disabled)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "Hello from ComfyUI"}),
                "model": ("STRING", {"default": "kokoro"}),  # kokoro, chatterbox, styletts2, f5-tts, kitten-tts, global_preset
                "voice": ("STRING", {"default": "random"}),  # path/preset or "random"
                "speed": ("FLOAT", {"default": 1.0, "min": 0.25, "max": 4.0, "step": 0.05}),
                "params_json": ("STRING", {"multiline": True, "default": "{}", "placeholder": '{"temperature":0.7,"rvc_params":{...}}'}),
                "api_base": ("STRING", {"default": "http://127.0.0.1:7778"}),  # Where /v1/audio/speech lives
            },
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "timeout_sec": ("INT", {"default": 120, "min": 1, "max": 600}),
                "channels_first": ("BOOLEAN", {"default": True}),  # AUDIO shape (C,N) if True, else (N,C)
                "also_save_wav": ("BOOLEAN", {"default": False}),
                "save_prefix": ("STRING", {"default": "tts"}),
                "return_metadata": ("BOOLEAN", {"default": True}),
                # If provided (non-empty), raw JSON overrides the payload fully.
                "advanced_request_json": ("STRING", {"multiline": True, "default": "", "placeholder": '{"model":"kokoro","input":"...","voice":"random","speed":1.0,"response_format":"wav","params":{...}}'}),
            },
        }

    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "wav_path", "metadata_json")
    FUNCTION = "synthesize"
    CATEGORY = "Audio/TTS"

    def synthesize(
        self,
        text: str,
        model: str,
        voice: str,
        speed: float,
        params_json: str,
        api_base: str,
        api_key: str = "",
        timeout_sec: int = 120,
        channels_first: bool = True,
        also_save_wav: bool = False,
        save_prefix: str = "tts",
        return_metadata: bool = True,
        advanced_request_json: str = "",
    ):
        base = api_base.rstrip("/")
        url = f"{base}/v1/audio/speech"

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # Build request payload
        if advanced_request_json and advanced_request_json.strip():
            try:
                payload = json.loads(advanced_request_json)
            except Exception as e:
                raise RuntimeError(f"Invalid advanced_request_json: {e}")
        else:
            try:
                params = json.loads(params_json) if params_json.strip() else {}
                if not isinstance(params, dict):
                    raise ValueError("params_json must decode to an object")
            except Exception as e:
                raise RuntimeError(f"Invalid params_json: {e}")

            payload = {
                "model": model,
                "input": text,
                "voice": voice,
                "speed": speed,
                "response_format": "wav",
                "params": params,
            }

        # HTTP call
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout_sec)
        except Exception as e:
            raise RuntimeError(f"HTTP request failed: {e}")

        if resp.status_code != 200:
            try:
                err = resp.json()
            except Exception:
                err = resp.text
            raise RuntimeError(f"TTS API error {resp.status_code}: {err}")

        audio_bytes = resp.content
        if not audio_bytes:
            raise RuntimeError("Empty response from TTS API")

        # Build AUDIO object
        audio_obj = _wav_to_audio_obj(audio_bytes, channels_first=channels_first)

        # Optional save
        wav_path = _save_wav(audio_bytes, save_prefix, model) if also_save_wav else ""

        # Metadata
        meta_json = ""
        if return_metadata:
            meta = {"request": payload, "api_base": base, "status_code": resp.status_code, "content_type": resp.headers.get("Content-Type", "")}
            if wav_path:
                meta.update(_wav_metadata(wav_path))
            meta_json = json.dumps(meta)

        return (audio_obj, wav_path, meta_json)


NODE_CLASS_MAPPINGS = {
    "TTSWebUI_OpenAI_TTS": TTSWebUI_OpenAI_TTS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TTSWebUI_OpenAI_TTS": "TTS WebUI via API",
}