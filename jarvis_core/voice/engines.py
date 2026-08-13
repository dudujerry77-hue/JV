"""Voice engine interfaces -- see .jarvis/decisions.md D-0015.

Structural (Protocol) interfaces, not base classes: swapping the wake-word,
STT, or TTS backend later (.jarvis/architecture.md "configurable before
hard-coded") only requires satisfying these shapes, not inheriting from
anything Jarvis Core defines.
"""

from pathlib import Path
from typing import Protocol

import numpy as np


class WakeWordEngine(Protocol):
    """Scores a chunk of audio against one or more wake-word models."""

    def predict(self, audio_chunk: np.ndarray) -> dict[str, float]: ...

    def reset(self) -> None: ...


class SpeechToTextEngine(Protocol):
    """Transcribes a recorded audio file to text."""

    def transcribe(self, audio_path: str | Path) -> str: ...


class TextToSpeechEngine(Protocol):
    """Synthesizes text to speech."""

    def synthesize_to_file(self, text: str, output_path: str | Path) -> Path: ...
