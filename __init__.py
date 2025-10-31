from .nodes.tts_webui_openai_tts import TTSWebUI_OpenAI_TTS
from .nodes.kokoro import TTS_KokoroNode
from .nodes.chatterbox import TTS_ChatterboxNode
from .nodes.styletts2 import TTS_StyleTTS2Node
from .nodes.kitten_tts import TTS_KittenTTSNode
from .nodes.f5_tts import TTS_F5TTSNode
from .nodes.global_preset import TTS_GlobalPresetNode
from .nodes.megatts3 import TTS_MegaTTS3Node
from .nodes.fireredtts2 import TTS_FireRedTTS2Node
from .nodes.higgs_v2 import TTS_HiggsV2Node
from .nodes.mms import TTS_MMSNode
from .nodes.parler_tts import TTS_ParlerTTSNode
from .nodes.piper_tts import TTS_PiperTTSNode
from .nodes.vall_e_x import TTS_VallEXNode

NODE_CLASS_MAPPINGS = {
    "TTSWebUI_OpenAI_TTS": TTSWebUI_OpenAI_TTS,
    "TTS_KokoroNode": TTS_KokoroNode,
    "TTS_ChatterboxNode": TTS_ChatterboxNode,
    "TTS_StyleTTS2Node": TTS_StyleTTS2Node,
    "TTS_KittenTTSNode": TTS_KittenTTSNode,
    "TTS_F5TTSNode": TTS_F5TTSNode,
    "TTS_GlobalPresetNode": TTS_GlobalPresetNode,
    "TTS_MegaTTS3Node": TTS_MegaTTS3Node,
    "TTS_FireRedTTS2Node": TTS_FireRedTTS2Node,
    "TTS_HiggsV2Node": TTS_HiggsV2Node,
    "TTS_MMSNode": TTS_MMSNode,
    "TTS_ParlerTTSNode": TTS_ParlerTTSNode,
    "TTS_PiperTTSNode": TTS_PiperTTSNode,
    "TTS_VallEXNode": TTS_VallEXNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TTSWebUI_OpenAI_TTS": "TTS WebUI via API",
    "TTS_KokoroNode": "TTS WebUI Kokoro",
    "TTS_ChatterboxNode": "TTS WebUI Chatterbox",
    "TTS_StyleTTS2Node": "TTS WebUI StyleTTS2",
    "TTS_KittenTTSNode": "TTS WebUI Kitten TTS",
    "TTS_F5TTSNode": "TTS WebUI F5-TTS",
    "TTS_GlobalPresetNode": "TTS WebUI Preset",
    "TTS_MegaTTS3Node": "TTS WebUI MegaTTS3",
    "TTS_FireRedTTS2Node": "TTS WebUI FireRedTTS2",
    "TTS_HiggsV2Node": "TTS WebUI Higgs V2",
    "TTS_MMSNode": "TTS WebUI MMS",
    "TTS_ParlerTTSNode": "TTS WebUI Parler TTS",
    "TTS_PiperTTSNode": "TTS WebUI Piper TTS",
    "TTS_VallEXNode": "TTS WebUI Vall-E-X",
}
