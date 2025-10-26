import json
from ._base import NodeTTSBase


class TTSWebUI_OpenAI_TTS(NodeTTSBase):
    @classmethod
    def INPUT_TYPES(cls):
        req = dict(cls.required_inputs(text_default="Hello from ComfyUI"))
        req.update({
            "model": ("STRING", {"default": "kokoro"}),
            "voice": ("STRING", {"default": "random"}),
            "speed": ("FLOAT", {"default": 1.0, "min": 0.25, "max": 4.0, "step": 0.05}),
            "params_json": ("STRING", {"multiline": True, "default": "{}", "placeholder": '{"temperature":0.7,"rvc_params":{...}}'}),
        })
        return {
            "required": req,
            "optional": {
                "api_key": ("STRING", {"default": "", "password": True}),
                "timeout_sec": ("INT", {"default": 120, "min": 1, "max": 600}),
                "channels_first": ("BOOLEAN", {"default": True}),
                "also_save_wav": ("BOOLEAN", {"default": False}),
                "save_prefix": ("STRING", {"default": "tts"}),
                "return_metadata": ("BOOLEAN", {"default": True}),
                "advanced_request_json": ("STRING", {"multiline": True, "default": "", "placeholder": '{"model":"kokoro","input":"...","voice":"random","speed":1.0,"response_format":"wav","params":{...}}'}),
            },
        }

    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "wav_path", "metadata_json")
    FUNCTION = "synthesize"
    CATEGORY = "Audio/TTS"

    def synthesize(self, text, model, voice, speed, params_json, api_base, api_key="", timeout_sec=120, channels_first=True, also_save_wav=False, save_prefix="tts", return_metadata=True, advanced_request_json=""):
        base = api_base.rstrip("/")
        model_key = model.lower() if isinstance(model, str) else str(model)

        if advanced_request_json and advanced_request_json.strip():
            try:
                payload = json.loads(advanced_request_json)
            except Exception as e:
                raise RuntimeError(f"Invalid advanced_request_json: {e}")
            resp = self._post_json(base, payload, api_key, timeout=timeout_sec)
        else:
            try:
                params = json.loads(params_json) if params_json.strip() else {}
                if not isinstance(params, dict):
                    raise ValueError("params_json must decode to an object")
            except Exception as e:
                raise RuntimeError(f"Invalid params_json: {e}")
            payload = {"model": model, "input": text, "voice": voice, "speed": speed, "response_format": "wav", "params": params}
            resp = self._post_json(base, payload, api_key, timeout=timeout_sec)

        return self._finalize(resp, model, base, channels_first, also_save_wav, save_prefix, return_metadata)
