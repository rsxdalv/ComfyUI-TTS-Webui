import json
from ._base import NodeTTSBase


class TTS_GlobalPresetNode(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "voice": ("STRING", {"default": "random"}),
                "preset": ("STRING", {"default": ""}),
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

    def synthesize(self, text, api_base, api_key="", voice="random", preset="", speed=1.0, timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "global_preset",
            "input": text,
            "voice": voice,
            "speed": speed,
            "response_format": "wav",
            "params": {"preset": preset, "voice": voice, "speed": speed},
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "global_preset", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
