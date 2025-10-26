import json
from ._base import NodeTTSBase


class TTS_F5TTSNode(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "ref_audio_orig": ("STRING", {"default": ""}),
                "ref_text": ("STRING", {"default": ""}),
                "model": ("STRING", {"default": "default"}),
                "remove_silence": ("BOOLEAN", {"default": False}),
                "cross_fade_duration": ("FLOAT", {"default": 0.15, "min": 0.0, "max": 5.0, "step": 0.01}),
                "nfe_step": ("INT", {"default": 32, "min": 1, "max": 256}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.25, "max": 4.0, "step": 0.05}),
                "show_info": ("BOOLEAN", {"default": False}),
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

    def synthesize(self, text, api_base, api_key="", ref_audio_orig="", ref_text="", model="default", remove_silence=False, cross_fade_duration=0.15, nfe_step=32, speed=1.0, show_info=False, timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "f5-tts",
            "input": text,
            "voice": "",
            "speed": speed,
            "response_format": "wav",
            "params": {
                "ref_audio_orig": ref_audio_orig,
                "ref_text": ref_text,
                "model": model,
                "remove_silence": remove_silence,
                "cross_fade_duration": cross_fade_duration,
                "nfe_step": nfe_step,
                "show_info": show_info,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "f5-tts", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
