import json
from ._base import NodeTTSBase


class TTS_KittenTTSNode(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        req = dict(cls.required_inputs())
        req.update({"voice": ("STRING", {"default": "random"})})
        return {
            "required": req,
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "model_name": ("STRING", {"default": "KittenML/kitten-tts-mini-0.1"}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.25, "max": 4.0, "step": 0.05}),
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

    def synthesize(self, text, voice, api_base, api_key="", model_name="KittenML/kitten-tts-mini-0.1", speed=1.0, timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "kitten-tts",
            "input": text,
            "voice": voice,
            "speed": speed,
            "response_format": "wav",
            "params": {"model_name": model_name},
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "kitten-tts", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
