"""record_seconds() and play_wav() need real audio hardware, which does not
exist in this sandbox -- they are intentionally not tested here and must
be verified on the owner's actual machine. save_wav() is pure file I/O and
is tested for real below.
"""

import wave

import numpy as np

from jarvis_core.voice.audio_io import CHANNELS, SAMPLE_RATE, save_wav


def test_save_wav_writes_a_valid_wav_file(tmp_path):
    audio = np.array([0, 100, -100, 32000], dtype=np.int16)
    output_path = tmp_path / "out.wav"

    result_path = save_wav(audio, output_path)

    assert result_path == output_path
    assert output_path.exists()

    with wave.open(str(output_path), "rb") as wf:
        assert wf.getnchannels() == CHANNELS
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == SAMPLE_RATE
        assert wf.getnframes() == len(audio)


def test_save_wav_creates_parent_directories(tmp_path):
    audio = np.zeros(10, dtype=np.int16)
    output_path = tmp_path / "nested" / "dir" / "out.wav"

    save_wav(audio, output_path)

    assert output_path.exists()
