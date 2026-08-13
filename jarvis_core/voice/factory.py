"""Assembles the voice pipeline from config, gated by the MICROPHONE
capability.

Enforcement happens here, at the orchestration boundary -- the same
principle as .jarvis/security_policy.md "Safe plugin loading" applies to
Core's own subsystems: the low-level engines (wakeword.py, stt.py,
audio_io.py) don't check permissions themselves, the assembly point does.
"""

import sqlite3
from pathlib import Path

from jarvis_core.config.schema import JarvisConfig
from jarvis_core.permissions.capabilities import Capability
from jarvis_core.permissions.checker import require
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.voice import audio_io
from jarvis_core.voice.pipeline import EchoPipeline, ListenLoop
from jarvis_core.voice.stt import FasterWhisperEngine
from jarvis_core.voice.tts import Pyttsx3Engine
from jarvis_core.voice.wakeword import OpenWakeWordEngine


def build_listen_loop(
    config: JarvisConfig,
    permission_store: PermissionStore,
    conn: sqlite3.Connection | None = None,
) -> ListenLoop:
    require(permission_store, Capability.MICROPHONE, conn)

    capture_dir = config.resolved_voice_capture_dir()
    capture_dir.mkdir(parents=True, exist_ok=True)

    wakeword_engine = OpenWakeWordEngine(
        wakeword_models=config.voice.wakeword_models or None,
        threshold=config.voice.wakeword_threshold,
    )
    stt_engine = FasterWhisperEngine(model_size=config.voice.stt_model_size)
    tts_engine = Pyttsx3Engine(rate=config.voice.tts_rate)
    echo_pipeline = EchoPipeline(stt_engine, tts_engine)

    record_seconds = config.voice.record_seconds

    def record_fn() -> Path:
        audio = audio_io.record_seconds(record_seconds)
        return audio_io.save_wav(audio, capture_dir / "input.wav")

    return ListenLoop(
        wakeword_engine=wakeword_engine,
        echo_pipeline=echo_pipeline,
        record_fn=record_fn,
        play_fn=audio_io.play_wav,
        capture_dir=capture_dir,
    )
