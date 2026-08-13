"""Wake-word detection via openWakeWord -- see .jarvis/decisions.md D-0015.

Same lazy-loading rationale as jarvis_core/voice/stt.py: openWakeWord
downloads its pretrained models on first use, which this sandbox's network
policy blocks, so loading is deferred and tests inject a fake model
loader. Real detection accuracy must be verified on a machine with normal
internet access and an actual microphone.
"""

from collections.abc import Callable
from typing import Any

import numpy as np

from jarvis_core.observability.logging import get_logger

logger = get_logger("voice.wakeword")

DEFAULT_THRESHOLD = 0.5


def _default_model_loader(wakeword_models: list[str] | None) -> Any:
    from openwakeword.model import Model

    kwargs = {"wakeword_models": wakeword_models} if wakeword_models else {}
    return Model(**kwargs)


class OpenWakeWordEngine:
    def __init__(
        self,
        wakeword_models: list[str] | None = None,
        threshold: float = DEFAULT_THRESHOLD,
        model_loader: Callable[[list[str] | None], Any] = _default_model_loader,
    ):
        self._wakeword_models = wakeword_models
        self._threshold = threshold
        self._model_loader = model_loader
        self._model: Any | None = None

    def _ensure_model(self) -> Any:
        if self._model is None:
            logger.info(
                "loading wake-word model(s) %s (downloads default models on "
                "first use if none specified)",
                self._wakeword_models or "(default)",
            )
            self._model = self._model_loader(self._wakeword_models)
        return self._model

    def predict(self, audio_chunk: np.ndarray) -> dict[str, float]:
        model = self._ensure_model()
        return dict(model.predict(audio_chunk))

    def reset(self) -> None:
        if self._model is not None:
            self._model.reset()

    def detected(self, scores: dict[str, float]) -> str | None:
        for name, score in scores.items():
            if score >= self._threshold:
                return name
        return None
