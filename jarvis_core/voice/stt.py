"""Speech-to-text via faster-whisper -- see .jarvis/decisions.md D-0015.

Model loading is deferred to first use (not constructor time). faster-
whisper downloads pretrained weights from Hugging Face on first use, which
this sandbox's network policy blocks -- lazy loading means importing and
wiring this engine up doesn't require that network access, and tests can
inject a fake loader instead of hitting the real model. Real transcription
accuracy must be verified on a machine with normal internet access.
"""

from collections.abc import Callable
from pathlib import Path
from typing import Any

from jarvis_core.observability.logging import get_logger

logger = get_logger("voice.stt")


def _default_model_loader(model_size: str, device: str, compute_type: str) -> Any:
    from faster_whisper import WhisperModel

    return WhisperModel(model_size, device=device, compute_type=compute_type)


class FasterWhisperEngine:
    def __init__(
        self,
        model_size: str = "tiny",
        device: str = "cpu",
        compute_type: str = "int8",
        model_loader: Callable[[str, str, str], Any] = _default_model_loader,
    ):
        self._model_size = model_size
        self._device = device
        self._compute_type = compute_type
        self._model_loader = model_loader
        self._model: Any | None = None

    def _ensure_model(self) -> Any:
        if self._model is None:
            logger.info(
                "loading speech-to-text model '%s' (downloads on first use)",
                self._model_size,
            )
            self._model = self._model_loader(
                self._model_size, self._device, self._compute_type
            )
        return self._model

    def transcribe(self, audio_path: str | Path) -> str:
        model = self._ensure_model()
        segments, _info = model.transcribe(str(audio_path))
        text = " ".join(segment.text.strip() for segment in segments)
        logger.debug("transcribed %s -> %d chars", audio_path, len(text))
        return text.strip()
