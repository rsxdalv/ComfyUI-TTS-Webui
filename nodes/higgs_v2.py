import json
from ._base import NodeTTSBase


class TTS_HiggsV2Node(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "temperature": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 2.0, "step": 0.05}),
                "audio_prompt_path": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
                "scene_description": ("STRING", {"default": "", "multiline": True}),
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

    def synthesize(self, text, api_base, api_key="", temperature=0.8, audio_prompt_path="", seed=-1, scene_description="", timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "higgs_v2",
            "input": text,
            "voice": "",
            "speed": 1.0,
            "response_format": "wav",
            "params": {
                "temperature": temperature,
                "audio_prompt_path": audio_prompt_path if audio_prompt_path else None,
                "seed": seed,
                "scene_description": scene_description if scene_description else None,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "higgs_v2", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
