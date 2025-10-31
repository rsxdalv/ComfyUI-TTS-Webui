import json
from ._base import NodeTTSBase


class TTS_FireRedTTS2Node(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 2.0, "step": 0.05}),
                "topk": ("INT", {"default": 30, "min": 1, "max": 100}),
                "prompt_wav": ("STRING", {"default": ""}),
                "prompt_text": ("STRING", {"default": ""}),
                "model_name": ("STRING", {"default": "monologue"}),
                "device": ("STRING", {"default": "cuda"}),
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

    def synthesize(self, text, api_base, api_key="", temperature=0.9, topk=30, prompt_wav="", prompt_text="", model_name="monologue", device="cuda", timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "fireredtts2",
            "input": text,
            "voice": "",
            "speed": 1.0,
            "response_format": "wav",
            "params": {
                "temperature": temperature,
                "topk": topk,
                "prompt_wav": prompt_wav if prompt_wav else None,
                "prompt_text": prompt_text if prompt_text else None,
                "model_name": model_name,
                "device": device,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "fireredtts2", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
