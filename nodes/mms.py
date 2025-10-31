import json
from ._base import NodeTTSBase


class TTS_MMSNode(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "language": ("STRING", {"default": "eng"}),
                "speaking_rate": ("FLOAT", {"default": 1.0, "min": 0.25, "max": 4.0, "step": 0.05}),
                "noise_scale": ("FLOAT", {"default": 0.667, "min": 0.0, "max": 2.0, "step": 0.01}),
                "noise_scale_duration": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 2.0, "step": 0.01}),
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

    def synthesize(self, text, api_base, api_key="", language="eng", speaking_rate=1.0, noise_scale=0.667, noise_scale_duration=0.8, timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "mms",
            "input": text,
            "voice": "",
            "speed": speaking_rate,
            "response_format": "wav",
            "params": {
                "language": language,
                "speaking_rate": speaking_rate,
                "noise_scale": noise_scale,
                "noise_scale_duration": noise_scale_duration,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "mms", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
