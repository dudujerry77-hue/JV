"""openWakeWord's real models require a download this sandbox's network
policy blocks (see .jarvis/decisions.md D-0015), so these tests exercise
OpenWakeWordEngine's own logic against a fake model loader. Real
detection accuracy must be verified on a machine with a real microphone
and normal internet access.
"""

from types import SimpleNamespace

import numpy as np

from jarvis_core.voice.wakeword import OpenWakeWordEngine


def _fake_model(predict_return, reset_tracker=None):
    return SimpleNamespace(
        predict=lambda x, **kwargs: predict_return,
        reset=lambda: (reset_tracker.append(1) if reset_tracker is not None else None),
    )


def test_model_not_loaded_until_predict_is_called():
    load_calls = []

    def loader(wakeword_models):
        load_calls.append(wakeword_models)
        return _fake_model({})

    OpenWakeWordEngine(model_loader=loader)

    assert load_calls == []


def test_predict_returns_underlying_model_scores():
    def loader(wakeword_models):
        return _fake_model({"hey_jarvis": 0.9})

    engine = OpenWakeWordEngine(model_loader=loader)
    scores = engine.predict(np.zeros(1280, dtype=np.int16))

    assert scores == {"hey_jarvis": 0.9}


def test_detected_returns_name_when_above_threshold():
    engine = OpenWakeWordEngine(threshold=0.5, model_loader=lambda m: _fake_model({}))

    assert engine.detected({"hey_jarvis": 0.9}) == "hey_jarvis"


def test_detected_returns_none_when_below_threshold():
    engine = OpenWakeWordEngine(threshold=0.5, model_loader=lambda m: _fake_model({}))

    assert engine.detected({"hey_jarvis": 0.1}) is None


def test_reset_is_a_noop_if_model_never_loaded():
    load_calls = []

    def loader(wakeword_models):
        load_calls.append(1)
        return _fake_model({})

    engine = OpenWakeWordEngine(model_loader=loader)
    engine.reset()  # should not trigger a load

    assert load_calls == []


def test_reset_delegates_to_underlying_model_once_loaded():
    reset_tracker = []

    def loader(wakeword_models):
        return _fake_model({}, reset_tracker=reset_tracker)

    engine = OpenWakeWordEngine(model_loader=loader)
    engine.predict(np.zeros(1280, dtype=np.int16))  # forces load
    engine.reset()

    assert reset_tracker == [1]
