from pathlib import Path
from types import SimpleNamespace

import numpy as np

from jarvis_core.voice.pipeline import EchoPipeline, ListenLoop
from jarvis_core.voice.stt import FasterWhisperEngine
from jarvis_core.voice.tts import Pyttsx3Engine
from jarvis_core.voice.wakeword import OpenWakeWordEngine


def _stt_with_canned_transcript(transcript: str) -> FasterWhisperEngine:
    def loader(model_size, device, compute_type):
        segments = [SimpleNamespace(text=transcript)]
        return SimpleNamespace(transcribe=lambda path: (segments, None))

    return FasterWhisperEngine(model_loader=loader)


def test_echo_pipeline_speaks_back_what_it_heard(tmp_path):
    stt = _stt_with_canned_transcript("hello jarvis")
    tts = Pyttsx3Engine()  # real -- no model download needed
    pipeline = EchoPipeline(stt, tts)

    output_path = tmp_path / "response.wav"
    reply = pipeline.respond_to_audio(tmp_path / "input.wav", output_path)

    assert reply == "You said: hello jarvis"
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_echo_pipeline_handles_empty_transcript(tmp_path):
    stt = _stt_with_canned_transcript("")
    tts = Pyttsx3Engine()
    pipeline = EchoPipeline(stt, tts)

    reply = pipeline.respond_to_audio(tmp_path / "input.wav", tmp_path / "out.wav")

    assert reply == "I didn't catch that."


def _fake_wakeword(score: float, threshold: float = 0.5) -> OpenWakeWordEngine:
    def loader(wakeword_models):
        return SimpleNamespace(
            predict=lambda x, **kwargs: {"hey_jarvis": score},
            reset=lambda: None,
        )

    return OpenWakeWordEngine(threshold=threshold, model_loader=loader)


def test_listen_loop_ignores_chunks_below_threshold(tmp_path):
    record_calls = []
    play_calls = []

    loop = ListenLoop(
        wakeword_engine=_fake_wakeword(score=0.1),
        echo_pipeline=EchoPipeline(_stt_with_canned_transcript("hi"), Pyttsx3Engine()),
        record_fn=lambda: record_calls.append(1) or tmp_path / "input.wav",
        play_fn=lambda path: play_calls.append(path),
        capture_dir=tmp_path,
    )

    result = loop.handle_audio_chunk(np.zeros(1280, dtype=np.int16))

    assert result is None
    assert record_calls == []
    assert play_calls == []


def test_listen_loop_triggers_full_round_trip_on_wake_word(tmp_path):
    (tmp_path / "input.wav").touch()  # respond_to_audio just needs a path to pass through
    record_calls = []
    play_calls = []

    loop = ListenLoop(
        wakeword_engine=_fake_wakeword(score=0.9),
        echo_pipeline=EchoPipeline(_stt_with_canned_transcript("turn on the lights"), Pyttsx3Engine()),
        record_fn=lambda: record_calls.append(1) or (tmp_path / "input.wav"),
        play_fn=lambda path: play_calls.append(path),
        capture_dir=tmp_path,
    )

    result = loop.handle_audio_chunk(np.zeros(1280, dtype=np.int16))

    assert result == "hey_jarvis"
    assert len(record_calls) == 1
    assert len(play_calls) == 1
    assert play_calls[0] == tmp_path / "response.wav"
    assert (tmp_path / "response.wav").exists()
