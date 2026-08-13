"""Phase 2 manual hardware verification.

Run this on the OWNER'S ACTUAL MACHINE -- it needs a real microphone, real
speakers, and real internet access (to download the openWakeWord and
faster-whisper models on first use). It cannot run in the agent's
development sandbox, which has neither audio hardware nor access to the
model-download host (see .jarvis/decisions.md D-0015).

Usage (Windows PowerShell, after activating the project's venv):
    python scripts\\verify_phase2_voice.py

Walks through each check in .jarvis/current_phase.md's verification list
in order, asking you to confirm what you heard/said. Copy the FULL console
output and report it back -- it gets recorded in
.jarvis/phase_completion_records/P002-completion.md, and Phase 2 is only
marked `verified` in roadmap.md once these checks genuinely pass.
"""

import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd

from jarvis_core.voice import audio_io
from jarvis_core.voice.pipeline import EchoPipeline, ListenLoop
from jarvis_core.voice.stt import FasterWhisperEngine
from jarvis_core.voice.tts import Pyttsx3Engine
from jarvis_core.voice.wakeword import OpenWakeWordEngine

CAPTURE_DIR = Path("./voice_verification_output")
CAPTURE_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80ms at 16kHz -- what openWakeWord expects


def _section(name: str) -> None:
    print(f"\n=== {name} ===")


def step_0_list_devices() -> None:
    _section("0. Audio devices available")
    print(sd.query_devices())
    default_in, default_out = sd.default.device
    print(f"Default input device index: {default_in}")
    print(f"Default output device index: {default_out}")
    # PortAudio reports "no device" as -1 on some platforms, None on others.
    if default_in in (None, -1) or default_out in (None, -1):
        print("FAIL: no default input/output device found. Fix Windows audio settings first.")
        sys.exit(1)
    print("PASS: default input/output devices found.")


def step_1_tts() -> None:
    _section("1. Text-to-speech through your speakers")
    engine = Pyttsx3Engine()
    out_path = CAPTURE_DIR / "tts_check.wav"
    engine.synthesize_to_file("Hello, this is Jarvis. Can you hear me?", out_path)
    print(f"Wrote {out_path} -- playing it now, listen for the voice.")
    audio_io.play_wav(out_path)
    result = input("Did you hear it clearly? (y/n): ").strip().lower()
    print("PASS -- TTS playback" if result == "y" else "FAIL -- TTS playback")


def step_2_stt() -> str:
    _section("2. Speech-to-text from your microphone")
    input("Press Enter, then say a short sentence clearly (recording starts immediately, 4 seconds)...")
    audio = audio_io.record_seconds(4.0)
    input_path = audio_io.save_wav(audio, CAPTURE_DIR / "stt_check.wav")
    print("Loading faster-whisper model (downloads on first use -- needs real internet)...")
    stt = FasterWhisperEngine(model_size="tiny")
    transcript = stt.transcribe(input_path)
    print(f"Transcribed: {transcript!r}")
    result = input("Was that roughly correct? (y/n): ").strip().lower()
    print("PASS -- STT accuracy" if result == "y" else "FAIL -- STT accuracy")
    return transcript


def step_3_wakeword() -> bool:
    _section("3. Wake-word detection (say 'hey jarvis' within 15 seconds)")
    print("Loading openWakeWord model (downloads on first use -- needs real internet)...")
    engine = OpenWakeWordEngine(threshold=0.5)

    detected = {"name": None}

    def callback(indata, frames, time_info, status):
        if detected["name"] is not None:
            return
        chunk = indata[:, 0].astype(np.int16)
        scores = engine.predict(chunk)
        name = engine.detected(scores)
        if name:
            detected["name"] = name

    with sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=CHUNK_SIZE, callback=callback
    ):
        for _ in range(15):
            if detected["name"]:
                break
            time.sleep(1)

    if detected["name"]:
        print(f"PASS -- detected wake word: {detected['name']}")
    else:
        print("FAIL -- no wake word detected within 15 seconds")
    return detected["name"] is not None


def step_4_full_pipeline() -> None:
    _section("4. Full pipeline: wake word -> record -> transcribe -> speak back")
    print("Loading models (should already be cached from steps 2-3)...")
    stt = FasterWhisperEngine(model_size="tiny")
    tts = Pyttsx3Engine()
    wakeword = OpenWakeWordEngine(threshold=0.5)
    echo = EchoPipeline(stt, tts)

    def record_fn() -> Path:
        audio = audio_io.record_seconds(4.0)
        return audio_io.save_wav(audio, CAPTURE_DIR / "pipeline_input.wav")

    loop = ListenLoop(
        wakeword_engine=wakeword,
        echo_pipeline=echo,
        record_fn=record_fn,
        play_fn=audio_io.play_wav,
        capture_dir=CAPTURE_DIR,
    )

    triggered = {"value": False}

    def callback(indata, frames, time_info, status):
        if triggered["value"]:
            return
        chunk = indata[:, 0].astype(np.int16)
        name = loop.handle_audio_chunk(chunk)
        if name:
            triggered["value"] = True

    print("Say 'hey jarvis' then a short sentence within 20 seconds...")
    with sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=CHUNK_SIZE, callback=callback
    ):
        for _ in range(20):
            if triggered["value"]:
                time.sleep(6)  # let record -> transcribe -> synthesize -> playback finish
                break
            time.sleep(1)

    if triggered["value"]:
        print("PASS -- pipeline triggered end-to-end. Did you hear Jarvis echo your sentence back?")
    else:
        print("FAIL -- pipeline never triggered (wake word not detected within 20 seconds)")


if __name__ == "__main__":
    step_0_list_devices()
    step_1_tts()
    step_2_stt()
    wake_ok = step_3_wakeword()
    if wake_ok:
        step_4_full_pipeline()
    else:
        print("\nSkipping step 4 (full pipeline) since wake word wasn't detected in step 3.")

    print("\nDone. Copy this ENTIRE console output and report it back.")
