import json
from ._base import NodeTTSBase


class TTS_MegaTTS3Node(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "reference_audio_path": ("STRING", {"default": ""}),
                "latent_npy_path": ("STRING", {"default": ""}),
                "inference_steps": ("INT", {"default": 32, "min": 1, "max": 200}),
                "intelligibility_weight": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.05}),
                "similarity_weight": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.05}),
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

    def synthesize(self, text, api_base, api_key="", reference_audio_path="", latent_npy_path="", inference_steps=32, intelligibility_weight=0.8, similarity_weight=0.8, timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "megatts3",
            "input": text,
            "voice": "",
            "speed": 1.0,
            "response_format": "wav",
            "params": {
                "reference_audio_path": reference_audio_path,
                "latent_npy_path": latent_npy_path,
                "inference_steps": inference_steps,
                "intelligibility_weight": intelligibility_weight,
                "similarity_weight": similarity_weight,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "megatts3", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
