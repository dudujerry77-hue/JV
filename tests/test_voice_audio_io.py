"""record_seconds() and play_wav() need real audio hardware, which does not
exist in this sandbox -- they are intentionally not tested here and must
be verified on the owner's actual machine. save_wav() is pure file I/O and
is tested for real below. MicrophoneChunkStream's capture callback is unit-
tested directly (see .jarvis/decisions.md D-0016) without needing a real
sd.InputStream, since the bug it fixes was about *how* it's driven, not
about needing real hardware to test the queue-decoupling contract itself.
"""

import queue
import wave

import numpy as np

from jarvis_core.voice.audio_io import (
    CHANNELS,
    SAMPLE_RATE,
    _build_capture_callback,
    save_wav,
)


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


def test_capture_callback_enqueues_chunk_without_doing_any_inference():
    """This is the contract that matters: the callback must do nothing but
    enqueue, so it can never fall behind PortAudio's real-time deadline."""
    q: queue.Queue = queue.Queue()
    callback = _build_capture_callback(q)
    indata = np.array([[1], [2], [3]], dtype=np.int16)  # (frames, channels)

    callback(indata, frames=3, time_info=None, status=None)

    chunk = q.get_nowait()
    np.testing.assert_array_equal(chunk, np.array([1, 2, 3], dtype=np.int16))


def test_capture_callback_copies_data_not_a_view():
    """sounddevice reuses its internal buffer across calls -- if we queued
    a view instead of a copy, later callbacks would silently corrupt
    chunks already sitting in the queue."""
    q: queue.Queue = queue.Queue()
    callback = _build_capture_callback(q)
    indata = np.array([[10], [20]], dtype=np.int16)

    callback(indata, frames=2, time_info=None, status=None)
    indata[:, 0] = 0  # mutate after the fact, as sounddevice would reuse the buffer

    chunk = q.get_nowait()
    np.testing.assert_array_equal(chunk, np.array([10, 20], dtype=np.int16))


def test_capture_callback_does_not_raise_on_status_flags(caplog):
    """A non-empty `status` (e.g. input overflow) must be logged, not
    silently ignored and not raised -- raising inside the real callback
    would abort the stream."""
    q: queue.Queue = queue.Queue()
    callback = _build_capture_callback(q)
    indata = np.zeros((2, 1), dtype=np.int16)

    callback(indata, frames=2, time_info=None, status="input overflow")  # should not raise

    assert q.qsize() == 1
