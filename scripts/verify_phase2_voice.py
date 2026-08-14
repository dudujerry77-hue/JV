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

import queue
import sys
import time
from pathlib import Path

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

    # Capture and inference are decoupled on purpose (see .jarvis/decisions.md
    # D-0016): the previous version of this script ran predict() directly
    # inside sounddevice's real-time callback, which can silently drop audio
    # if inference falls behind the callback's deadline. This loop instead
    # pulls chunks off a queue that a lightweight callback fills.
    detected_name = None
    best_scores: dict[str, float] = {}
    deadline = time.time() + 15

    with audio_io.MicrophoneChunkStream(chunk_size=CHUNK_SIZE, sample_rate=SAMPLE_RATE) as mic:
        while time.time() < deadline and detected_name is None:
            try:
                chunk = mic.get_chunk(timeout=0.5)
            except queue.Empty:
                continue

            scores = engine.predict(chunk)
            for name, score in scores.items():
                if score > best_scores.get(name, 0.0):
                    best_scores[name] = score

            detected_name = engine.detected(scores)

    if detected_name:
        print(f"PASS -- detected wake word: {detected_name}")
    else:
        print("FAIL -- no wake word detected within 15 seconds")

    if best_scores:
        top = sorted(best_scores.items(), key=lambda kv: kv[1], reverse=True)[:5]
        print("Highest score seen per model (threshold is 0.5):")
        for name, score in top:
            print(f"  {name}: {score:.3f}")
    else:
        print("No scores were produced at all -- the mic may not be capturing audio "
              "on this stream (check Windows privacy settings for microphone access).")

    return detected_name is not None


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

    triggered = False
    deadline = time.time() + 20

    print("Say 'hey jarvis' then a short sentence within 20 seconds...")
    with audio_io.MicrophoneChunkStream(chunk_size=CHUNK_SIZE, sample_rate=SAMPLE_RATE) as mic:
        while time.time() < deadline and not triggered:
            try:
                chunk = mic.get_chunk(timeout=0.5)
            except queue.Empty:
                continue

            # handle_audio_chunk() itself calls record_fn()/echo.respond_to_audio()/
            # play_fn() synchronously, which briefly blocks this loop -- that's fine
            # here since it's a plain while loop, not a real-time audio callback.
            name = loop.handle_audio_chunk(chunk)
            if name:
                triggered = True

    if triggered:
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
