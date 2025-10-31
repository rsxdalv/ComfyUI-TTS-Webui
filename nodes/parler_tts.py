import json
from ._base import NodeTTSBase


class TTS_ParlerTTSNode(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "description": ("STRING", {"default": "A neutral voice.", "multiline": True}),
                "model_name": ("STRING", {"default": "parler-tts/parler-tts-mini-v1"}),
                "attn_implementation": ("STRING", {"default": "eager"}),
                "compile_mode": ("STRING", {"default": ""}),
                "timeout_sec": ("INT", {"default": 120, "min": 1, "max": 600}),
                "channels_first": ("BOOLEAN", {"default": True}),
                "also_save_wav": ("BOOLEAN", {"default": False}),
                "save_prefix": ("STRING", {"default": "tts"}),
                "return_metadata": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "wav_path", "metadata_json")
    FUNCTION = "synthesize"
    CATEGORY = "Audio/TTS"

    def synthesize(self, text, api_base, api_key="", description="A neutral voice.", model_name="parler-tts/parler-tts-mini-v1", attn_implementation="eager", compile_mode="", timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "parler-tts",
            "input": text,
            "voice": "",
            "speed": 1.0,
            "response_format": "wav",
            "params": {
                "description": description,
                "model_name": model_name,
                "attn_implementation": attn_implementation,
                "compile_mode": compile_mode if compile_mode else None,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "parler-tts", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
