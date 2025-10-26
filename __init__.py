from .nodes.tts_webui_openai_tts import TTSWebUI_OpenAI_TTS
from .nodes.kokoro import TTS_KokoroNode
from .nodes.chatterbox import TTS_ChatterboxNode
from .nodes.styletts2 import TTS_StyleTTS2Node
from .nodes.kitten_tts import TTS_KittenTTSNode
from .nodes.f5_tts import TTS_F5TTSNode
from .nodes.global_preset import TTS_GlobalPresetNode

NODE_CLASS_MAPPINGS = {
    "TTSWebUI_OpenAI_TTS": TTSWebUI_OpenAI_TTS,
    "TTS_KokoroNode": TTS_KokoroNode,
    "TTS_ChatterboxNode": TTS_ChatterboxNode,
    "TTS_StyleTTS2Node": TTS_StyleTTS2Node,
    "TTS_KittenTTSNode": TTS_KittenTTSNode,
    "TTS_F5TTSNode": TTS_F5TTSNode,
    "TTS_GlobalPresetNode": TTS_GlobalPresetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TTSWebUI_OpenAI_TTS": "TTS WebUI via API",
    "TTS_KokoroNode": "TTS WebUI Kokoro",
    "TTS_ChatterboxNode": "TTS WebUI Chatterbox",
    "TTS_StyleTTS2Node": "TTS WebUI StyleTTS2",
    "TTS_KittenTTSNode": "TTS WebUI Kitten TTS",
    "TTS_F5TTSNode": "TTS WebUI F5-TTS",
    "TTS_GlobalPresetNode": "TTS WebUI Preset",
}
