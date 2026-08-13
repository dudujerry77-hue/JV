"""Text-to-speech via the OS-native voice engine -- see .jarvis/decisions.md
D-0015.

pyttsx3 wraps SAPI5 on Windows (the owner's actual machine, D-0009),
espeak on Linux (used to develop/test this wrapper for real), and NSSpeechSynthesizer
on macOS. No model download, works offline immediately -- unlike the wake
word and STT engines in this package, this one is genuinely verified here,
not just mock-tested.
"""

from pathlib import Path

import pyttsx3

from jarvis_core.observability.logging import get_logger

logger = get_logger("voice.tts")


class Pyttsx3Engine:
    def __init__(self, rate: int | None = None, voice_id: str | None = None):
        self._engine = pyttsx3.init()
        if rate is not None:
            self._engine.setProperty("rate", rate)
        if voice_id is not None:
            self._engine.setProperty("voice", voice_id)

    def synthesize_to_file(self, text: str, output_path: str | Path) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.debug("synthesizing %d chars to %s", len(text), output_path)
        self._engine.save_to_file(text, str(output_path))
        self._engine.runAndWait()

        return output_path
