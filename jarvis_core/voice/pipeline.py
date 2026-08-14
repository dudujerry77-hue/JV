"""Voice conversation pipeline -- see .jarvis/decisions.md D-0014.

No AI brain exists yet (Phase 3), so EchoPipeline's "response" is just the
transcript spoken back -- this proves the wake-word -> STT -> TTS
mechanics end-to-end. Phase 3 replaces the echo with a real answer,
without needing to change ListenLoop's control flow.
"""

from collections.abc import Callable
from pathlib import Path

import numpy as np

from jarvis_core.observability.logging import get_logger
from jarvis_core.voice.stt import FasterWhisperEngine
from jarvis_core.voice.tts import Pyttsx3Engine
from jarvis_core.voice.wakeword import OpenWakeWordEngine

logger = get_logger("voice.pipeline")


class EchoPipeline:
    def __init__(self, stt_engine: FasterWhisperEngine, tts_engine: Pyttsx3Engine):
        self._stt = stt_engine
        self._tts = tts_engine

    def respond_to_audio(self, input_audio_path: str | Path, output_audio_path: str | Path) -> str:
        transcript = self._stt.transcribe(input_audio_path)
        reply_text = f"You said: {transcript}" if transcript else "I didn't catch that."

        logger.info("echo pipeline heard %r, replying %r", transcript, reply_text)
        self._tts.synthesize_to_file(reply_text, output_audio_path)

        return reply_text


class ListenLoop:
    """Wake-word-gated state machine: listen -> (wake word detected) ->
    record -> respond -> back to listening.

    Audio I/O is injected (`record_fn`, `play_fn`) so this control flow is
    unit-testable without real microphone/speaker hardware, which does not
    exist in the agent's sandbox.

    IMPORTANT: handle_audio_chunk() runs model inference and must be
    called from a normal consumer loop, never directly from a real-time
    audio callback (e.g. sounddevice's `InputStream(callback=...)`).
    Doing so was the root cause of the first real-hardware wake-word test
    failing (see .jarvis/decisions.md D-0016) -- inference inside the
    callback can fall behind PortAudio's deadline and silently drop input.
    Use jarvis_core.voice.audio_io.MicrophoneChunkStream to decouple fast
    capture from this slower processing.
    """

    def __init__(
        self,
        wakeword_engine: OpenWakeWordEngine,
        echo_pipeline: EchoPipeline,
        record_fn: Callable[[], Path],
        play_fn: Callable[[Path], None],
        capture_dir: str | Path,
    ):
        self._wakeword = wakeword_engine
        self._echo = echo_pipeline
        self._record_fn = record_fn
        self._play_fn = play_fn
        self._capture_dir = Path(capture_dir)

    def handle_audio_chunk(self, chunk: np.ndarray) -> str | None:
        """Feed one chunk of streaming audio in. Returns the detected
        wake word's name, or None if nothing crossed the threshold."""
        scores = self._wakeword.predict(chunk)
        name = self._wakeword.detected(scores)

        if name is not None:
            logger.info("wake word detected: %s", name)
            self._wakeword.reset()
            self._on_wake_detected()

        return name

    def _on_wake_detected(self) -> None:
        input_path = self._record_fn()
        output_path = self._capture_dir / "response.wav"

        self._echo.respond_to_audio(input_path, output_path)
        self._play_fn(output_path)
