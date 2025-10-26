import json
from ._base import NodeTTSBase


class TTS_ChatterboxNode(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": cls.required_inputs(),
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "exaggeration": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0, "step": 0.01}),
                "cfg_weight": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0, "step": 0.01}),
                "temperature": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 2.0, "step": 0.01}),
                "audio_prompt_path": ("STRING", {"default": ""}),
                "model_name": ("STRING", {"default": "just_a_placeholder"}),
                "language_id": ("STRING", {"default": "en"}),
                "device": ("STRING", {"default": "cuda"}),
                "dtype": ("STRING", {"default": "float32"}),
                "cpu_offload": ("BOOLEAN", {"default": False}),
                "chunked": ("BOOLEAN", {"default": False}),
                "cache_voice": ("BOOLEAN", {"default": False}),
                "desired_length": ("INT", {"default": 200, "min": 1, "max": 4000}),
                "max_length": ("INT", {"default": 300, "min": 1, "max": 4000}),
                "halve_first_chunk": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
                "streaming": ("BOOLEAN", {"default": False}),
                "max_new_tokens": ("INT", {"default": 1000, "min": 1, "max": 4096}),
                "max_cache_len": ("INT", {"default": 1500, "min": 1, "max": 8192}),
                "initial_forward_pass_backend": ("STRING", {"default": "eager"}),
                "generate_token_backend": ("STRING", {"default": "cudagraphs-manual"}),
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

    def synthesize(self, text, api_base, api_key="", exaggeration=0.5, cfg_weight=0.5, temperature=0.8, audio_prompt_path=None, model_name="just_a_placeholder", language_id="en", device="cuda", dtype="float32", cpu_offload=False, chunked=False, cache_voice=False, desired_length=200, max_length=300, halve_first_chunk=False, seed=-1, streaming=False, max_new_tokens=1000, max_cache_len=1500, initial_forward_pass_backend="eager", generate_token_backend="cudagraphs-manual", timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True):
        payload = {
            "model": "chatterbox",
            "input": text,
            "voice": "",
            "speed": 1.0,
            "response_format": "wav",
            "params": {
                "exaggeration": exaggeration,
                "cfg_weight": cfg_weight,
                "temperature": temperature,
                "audio_prompt_path": audio_prompt_path,
                "model_name": model_name,
                "language_id": language_id,
                "device": device,
                "dtype": dtype,
                "cpu_offload": cpu_offload,
                "chunked": chunked,
                "cache_voice": cache_voice,
                "desired_length": desired_length,
                "max_length": max_length,
                "halve_first_chunk": halve_first_chunk,
                "seed": seed,
                "streaming": streaming,
                "max_new_tokens": max_new_tokens,
                "max_cache_len": max_cache_len,
                "initial_forward_pass_backend": initial_forward_pass_backend,
                "generate_token_backend": generate_token_backend,
            },
        }
        resp = self._post_json(api_base, payload, api_key, timeout=timeout_sec)
        return self._finalize(resp, "chatterbox", api_base, channels_first, also_save_wav, save_prefix, return_metadata)
