import json
from ._base import NodeTTSBase


class TTS_PiperTTSNode(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "voice_name": ("STRING", {"default": ""}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.25, "max": 4.0, "step": 0.05}),
                "noise_scale": ("FLOAT", {"default": 0.667, "min": 0.0, "max": 2.0, "step": 0.01}),
                "noise_w": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 2.0, "step": 0.01}),
                "sentence_silence": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 2.0, "step": 0.01}),
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

    def synthesize(self, text, api_base, api_key="", voice_name="", speed=1.0, noise_scale=0.667, noise_w=0.8, sentence_silence=0.2, timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "piper-tts",
            "input": text,
            "voice": voice_name,
            "speed": speed,
            "response_format": "wav",
            "params": {
                "voice_name": voice_name,
                "length_scale": 1.0 / speed if speed else 1.0,
                "noise_scale": noise_scale,
                "noise_w": noise_w,
                "sentence_silence": sentence_silence,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "piper-tts", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
