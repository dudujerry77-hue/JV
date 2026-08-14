"""Real microphone/speaker I/O via sounddevice.

Cannot be exercised for real in the agent's sandbox -- it has zero audio
devices (confirmed: sounddevice.query_devices() returns an empty list
there). record_seconds() and play_wav() must be verified on the owner's
actual machine, which has real audio hardware. save_wav()'s file-format
correctness, by contrast, needs no hardware and is tested for real.
"""

import queue
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd

from jarvis_core.observability.logging import get_logger

logger = get_logger("voice.audio_io")

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


def _build_capture_callback(chunk_queue: "queue.Queue[np.ndarray]"):
    """The audio callback itself: must return almost instantly.

    Root cause of the first real-hardware wake-word test failing (see
    .jarvis/decisions.md D-0016): running model inference directly inside
    a sounddevice callback risks it falling behind PortAudio's real-time
    deadline, causing silently dropped/overrun input. This callback does
    nothing but copy the chunk into a queue; a consumer loop running in a
    normal thread (not the audio callback) does the actual inference.
    """

    def callback(indata, frames, time_info, status) -> None:
        if status:
            logger.warning("audio input status flags: %s", status)
        chunk_queue.put(indata[:, 0].copy())

    return callback


class MicrophoneChunkStream:
    """Streams fixed-size int16 mono chunks from the default input device
    via a queue, decoupling capture (real-time, must not block) from
    whatever slower processing (e.g. wake-word inference) a consumer does
    with each chunk. See _build_capture_callback for why this exists.
    """

    def __init__(
        self,
        chunk_size: int = 1280,
        sample_rate: int = SAMPLE_RATE,
        channels: int = CHANNELS,
    ):
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.channels = channels
        self._queue: "queue.Queue[np.ndarray]" = queue.Queue()
        self._stream: sd.InputStream | None = None

    def __enter__(self) -> "MicrophoneChunkStream":
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.chunk_size,
            callback=_build_capture_callback(self._queue),
        )
        self._stream.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()

    def get_chunk(self, timeout: float | None = None) -> np.ndarray:
        return self._queue.get(timeout=timeout)
