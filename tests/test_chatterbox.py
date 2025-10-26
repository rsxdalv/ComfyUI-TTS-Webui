import io
import wave
import json
import importlib
import types
from unittest.mock import patch, Mock


def _make_sine_wav_bytes(duration_sec=0.05, sr=16000, freq=440.0, nch=1, sampwidth=2):
    """Create a tiny valid WAV file in-memory and return raw bytes.

    - sampwidth=2 -> 16-bit PCM
    - nch=1 mono keeps parsing simple for the test
    """
    # Generate a tiny 16-bit PCM sine tone without numpy to avoid heavy deps
    n_samples = int(duration_sec * sr)
    import math

    frames = bytearray()
    for n in range(n_samples):
        s = 0.1 * math.sin(2 * math.pi * freq * (n / sr))
        intval = max(-32768, min(32767, int(s * 32767.0)))
        frames += int(intval).to_bytes(2, byteorder="little", signed=True)

    with io.BytesIO() as buf:
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(nch)
            wf.setsampwidth(sampwidth)
            wf.setframerate(sr)
            wf.writeframes(bytes(frames))
        return buf.getvalue()


def test_chatterbox_synthesize_basic():
    # Provide lightweight stubs for numpy and torch so module imports don't fail
    np_stub = types.ModuleType("numpy")
    torch_stub = types.ModuleType("torch")
    requests_stub = types.ModuleType("requests")
    def _dummy_post(*args, **kwargs):  # will be patched later
        raise RuntimeError("requests.post should be patched in the test")
    requests_stub.post = _dummy_post

    with patch.dict("sys.modules", {"numpy": np_stub, "torch": torch_stub, "requests": requests_stub}):
        # Create a synthetic top-level package so relative imports (..api_key) resolve
        import os, sys
        repo_root = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(repo_root)  # .../ComfyUI-TTS-Webui
        pkg_name = "comfy_tts_webui"
        pkg = types.ModuleType(pkg_name)
        pkg.__path__ = [repo_root]
        sys.modules[pkg_name] = pkg

        # Import the node under test only after stubbing heavy deps and creating the package
        cb_mod = importlib.import_module(f"{pkg_name}.nodes.chatterbox")
        base_mod = importlib.import_module(f"{pkg_name}.nodes._base")
        node = cb_mod.TTS_ChatterboxNode()

    # Prepare a fake HTTP response object
    wav_bytes = _make_sine_wav_bytes()
    fake_resp = Mock()
    fake_resp.status_code = 200
    fake_resp.content = wav_bytes
    fake_resp.headers = {"Content-Type": "audio/wav"}

    # Patch requests.post and the audio conversion to avoid heavy deps in this unit test
    with patch(f"{pkg_name}.nodes._base.requests.post", return_value=fake_resp) as post_mock, \
        patch.object(base_mod, "_wav_to_audio_obj", return_value={"waveform": object(), "sample_rate": 16000}):
        audio, wav_path, meta_json = node.synthesize(
            text="hello",
            api_base="http://127.0.0.1:7778",
            api_key="",  # empty is fine for unit test
            also_save_wav=False,  # don't write files in this unit test
            return_metadata=True,
        )

    # requests.post must have been called once with expected URL and JSON payload containing model chatterbox
    assert post_mock.called, "Expected HTTP post to be invoked"
    args, kwargs = post_mock.call_args
    assert args[0].endswith("/v1/audio/speech"), "Unexpected URL used"
    assert kwargs.get("json", {}).get("model") == "chatterbox"

    # Validate audio object and sample rate (waveform specifics depend on backend)
    assert isinstance(audio, dict)
    assert "waveform" in audio and "sample_rate" in audio
    sr = audio["sample_rate"]
    assert sr == 16000

    # No file was saved
    assert wav_path == ""

    # Metadata JSON should be valid and contain basic fields
    meta = json.loads(meta_json)
    assert meta["request_model"] == "chatterbox"
    assert meta["status_code"] == 200
    assert meta["content_type"] == "audio/wav"
