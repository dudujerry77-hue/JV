"""faster-whisper's real model requires a Hugging Face download this
sandbox's network policy blocks (see .jarvis/decisions.md D-0015), so
these tests exercise FasterWhisperEngine's own logic against a fake
model loader rather than the real model. Real transcription accuracy
must be verified on a machine with normal internet access.
"""

from types import SimpleNamespace

from jarvis_core.voice.stt import FasterWhisperEngine


def _fake_segment(text: str):
    return SimpleNamespace(text=text)


def test_model_not_loaded_until_transcribe_is_called():
    load_calls = []

    def loader(model_size, device, compute_type):
        load_calls.append((model_size, device, compute_type))
        return SimpleNamespace(transcribe=lambda path: ([], None))

    FasterWhisperEngine(model_loader=loader)

    assert load_calls == []  # constructor must not trigger a load


def test_transcribe_loads_model_lazily_and_joins_segments():
    load_calls = []

    def loader(model_size, device, compute_type):
        load_calls.append((model_size, device, compute_type))
        segments = [_fake_segment("hello "), _fake_segment("jarvis")]
        return SimpleNamespace(transcribe=lambda path: (segments, {"language": "en"}))

    engine = FasterWhisperEngine(model_size="tiny", model_loader=loader)
    result = engine.transcribe("some/audio.wav")

    assert result == "hello jarvis"
    assert load_calls == [("tiny", "cpu", "int8")]


def test_model_is_loaded_only_once_across_multiple_transcribe_calls():
    load_calls = []

    def loader(model_size, device, compute_type):
        load_calls.append(1)
        return SimpleNamespace(transcribe=lambda path: ([_fake_segment("hi")], None))

    engine = FasterWhisperEngine(model_loader=loader)
    engine.transcribe("a.wav")
    engine.transcribe("b.wav")

    assert len(load_calls) == 1


def test_transcribe_passes_audio_path_as_string():
    received_paths = []

    def loader(model_size, device, compute_type):
        def transcribe(path):
            received_paths.append(path)
            return ([_fake_segment("ok")], None)

        return SimpleNamespace(transcribe=transcribe)

    engine = FasterWhisperEngine(model_loader=loader)
    engine.transcribe("/some/path.wav")

    assert received_paths == ["/some/path.wav"]
