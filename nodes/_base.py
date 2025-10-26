import json
import requests
from ..api_key import get_api_key
from ..utils import _wav_to_audio_obj, _save_wav, _wav_metadata


class NodeTTSBase:
    @classmethod
    def required_inputs(
        cls,
        text_default: str = "Hello",
        api_base_default: str = "http://127.0.0.1:7778",
        text_multiline: bool = True,
    ) -> dict:
        return {
            "text": ("STRING", {"multiline": text_multiline, "default": text_default}),
            "api_base": ("STRING", {"default": api_base_default}),
        }

    def _post_json(self, api_base: str, payload: dict, api_key: str = "", timeout: int = 120):
        base = api_base.rstrip("/")
        url = f"{base}/v1/audio/speech"
        headers = {"Content-Type": "application/json"}
        key = api_key or get_api_key()
        if key:
            headers["Authorization"] = f"Bearer {key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"HTTP request failed: {e}")
        if resp.status_code != 200:
            try:
                err = resp.json()
            except Exception:
                err = resp.text
            raise RuntimeError(f"TTS API error {resp.status_code}: {err}")
        return resp

    def _finalize(self, resp, model: str, api_base: str, channels_first: bool, also_save_wav: bool, save_prefix: str, return_metadata: bool):
        audio_bytes = resp.content
        if not audio_bytes:
            raise RuntimeError("Empty response from TTS API")
        audio_obj = _wav_to_audio_obj(audio_bytes, channels_first=channels_first)
        wav_path = _save_wav(audio_bytes, save_prefix, model) if also_save_wav else ""
        meta_json = ""
        if return_metadata:
            meta = {
                "request_model": model,
                "api_base": api_base.rstrip("/"),
                "status_code": resp.status_code,
                "content_type": resp.headers.get("Content-Type", ""),
            }
            if wav_path:
                meta.update(_wav_metadata(wav_path))
            meta_json = json.dumps(meta)
        return audio_obj, wav_path, meta_json
