"""Real (not mocked) tests -- pyttsx3 needs no model download, so unlike
the wake-word/STT tests, this one genuinely exercises synthesis.
"""

from jarvis_core.voice.tts import Pyttsx3Engine


def test_synthesize_to_file_produces_a_real_wav(tmp_path):
    engine = Pyttsx3Engine()
    output_path = tmp_path / "speech.wav"

    result_path = engine.synthesize_to_file("hello jarvis", output_path)

    assert result_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0

    header = output_path.read_bytes()[:4]
    assert header == b"RIFF"  # valid WAV container


def test_synthesize_creates_parent_directories(tmp_path):
    engine = Pyttsx3Engine()
    output_path = tmp_path / "nested" / "dir" / "speech.wav"

    engine.synthesize_to_file("test", output_path)

    assert output_path.exists()
