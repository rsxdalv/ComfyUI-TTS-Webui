import json
from ._base import NodeTTSBase


class TTS_StyleTTS2Node(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "alpha": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01}),
                "beta": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "diffusion_steps": ("INT", {"default": 5, "min": 1, "max": 200}),
                "embedding_scale": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01}),
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

    def synthesize(self, text, api_base, api_key="", alpha=0.3, beta=0.7, diffusion_steps=5, embedding_scale=1.0, timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "styletts2",
            "input": text,
            "voice": "",
            "speed": 1.0,
            "response_format": "wav",
            "params": {"alpha": alpha, "beta": beta, "diffusion_steps": diffusion_steps, "embedding_scale": embedding_scale},
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "styletts2", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
