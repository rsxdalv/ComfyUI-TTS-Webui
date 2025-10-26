import io
import wave
import numpy as np
import torch


def _wav_to_audio_obj(wav_bytes: bytes, channels_first=True):
    with wave.open(io.BytesIO(wav_bytes), "rb") as w:
        sr = w.getframerate()
        nframes = w.getnframes()
        nch = w.getnchannels()
        sampwidth = w.getsampwidth()
        raw = w.readframes(nframes)

    if sampwidth == 1:
        arr = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
        arr = (arr - 128.0) / 128.0
    elif sampwidth == 2:
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sampwidth == 4:
        try:
            arr = np.frombuffer(raw, dtype=np.float32)
            if np.nanmax(np.abs(arr)) > 2.0e4:
                raise ValueError("Not float32")
        except Exception:
            arr = (np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0)
    else:
        max_int = float(2 ** (8 * sampwidth - 1))
        arr = np.frombuffer(raw, dtype=np.int8).astype(np.float32) / max_int

    if nch > 1:
        arr = arr.reshape(-1, nch)
    else:
        arr = arr.reshape(-1, 1)

    arr = arr.astype(np.float32, copy=False)

    if channels_first:
        arr = arr.T

    waveform = torch.from_numpy(arr).to(torch.float32).contiguous().cpu().unsqueeze(0)
    return {"waveform": waveform, "sample_rate": sr}


def _wav_metadata(path: str) -> dict:
    meta = {"path": path, "format": "wav"}
    try:
        with wave.open(path, "rb") as w:
            fr = w.getframerate()
            nf = w.getnframes()
            ch = w.getnchannels()
            sw = w.getsampwidth()
            dur = nf / float(fr) if fr else 0.0
            meta.update(
                {
                    "sample_rate": fr,
                    "num_frames": nf,
                    "channels": ch,
                    "sample_width_bytes": sw,
                    "duration_sec": dur,
                }
            )
    except Exception as e:
        meta["probe_error"] = str(e)
    return meta
