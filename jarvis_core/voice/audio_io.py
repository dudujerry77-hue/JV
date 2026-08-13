"""Real microphone/speaker I/O via sounddevice.

Cannot be exercised for real in the agent's sandbox -- it has zero audio
devices (confirmed: sounddevice.query_devices() returns an empty list
there). record_seconds() and play_wav() must be verified on the owner's
actual machine, which has real audio hardware. save_wav()'s file-format
correctness, by contrast, needs no hardware and is tested for real.
"""

import wave
from pathlib import Path

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000  # Hz -- matches what openWakeWord/whisper expect
CHANNELS = 1
SAMPLE_WIDTH_BYTES = 2  # int16


def record_seconds(duration_seconds: float, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Blocks for `duration_seconds`, recording from the default input device."""
    frames = sd.rec(
        int(duration_seconds * sample_rate),
        samplerate=sample_rate,
        channels=CHANNELS,
        dtype="int16",
    )
    sd.wait()
    return frames.flatten()


def save_wav(audio: np.ndarray, path: str | Path, sample_rate: int = SAMPLE_RATE) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH_BYTES)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.astype(np.int16).tobytes())
    return path


def play_wav(path: str | Path) -> None:
    """Blocks until playback finishes."""
    with wave.open(str(path), "rb") as wf:
        sample_rate = wf.getframerate()
        n_channels = wf.getnchannels()
        raw = wf.readframes(wf.getnframes())

    audio = np.frombuffer(raw, dtype=np.int16)
    if n_channels > 1:
        audio = audio.reshape(-1, n_channels)

    sd.play(audio, samplerate=sample_rate)
    sd.wait()
