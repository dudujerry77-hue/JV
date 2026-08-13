# Current Phase

Phase: **Phase 2 — Voice**
Status: `in_progress`
Last updated: 2026-08-13

Phase 1 is closed out and `verified` — see
`phase_completion_records/P001-completion.md`. Owner confirmed (D-0014)
the documented roadmap order: Voice next, before the AI Brain (Phase 3).

## Phase 2 Scope (this pass)

Per `roadmap.md`: wake word, speech recognition, text-to-speech,
conversation. Since there is no AI brain yet, "conversation" here means an
**echo pipeline**: wake word detected -> record -> transcribe -> speak the
transcript back. This proves the mechanics; Phase 3 replaces the echo with
a real response.

Stack (D-0015): `openWakeWord` (wake word), `faster-whisper` (speech-to-
text), `pyttsx3` over the OS voice engine (text-to-speech). All local-tier
per D-0006 — no cloud dependency, matches the owner's GPU-less hardware.

## Important: What Can and Cannot Be Verified From This Sandbox

This governance/implementation work is happening in a remote sandbox, not
on the owner's actual EliteBook. Two real constraints affect what "Phase 2
verified" can honestly mean:

- **No microphone or speaker hardware exists in this sandbox** — audio
  capture from a real mic cannot be tested here.
- **This sandbox's network policy blocks `huggingface.co`** (confirmed via
  a 403 from the outbound proxy), so the pretrained model weights
  `openWakeWord` and `faster-whisper` need on first use cannot be
  downloaded here.

What **was** verified for real in this sandbox: `pyttsx3` text-to-speech
actually works end-to-end (produces a real audio file via the OS voice
engine — `espeak-ng` here, will be SAPI5 on the owner's Windows machine).

What is built but **only mock-tested** here, pending the owner running it
on real hardware with real internet: wake-word detection accuracy,
speech-to-text transcription accuracy, and real microphone capture. The
code is written with lazy model loading and a swappable-engine design
specifically so it's ready to exercise for real the moment it runs
somewhere with a mic and normal internet access.

Phase 2 will **not** be marked `verified` in `roadmap.md` the way Phase 1
was, until the owner confirms the mic/model pieces work for real on their
machine.

## What's Been Built This Pass

`jarvis_core/voice/`:
- `engines.py` — Protocol interfaces for wake word / STT / TTS.
- `tts.py` — `Pyttsx3Engine`. **Genuinely verified**: produces real audio
  files via the OS voice engine in this sandbox (espeak-ng here, SAPI5 on
  the owner's Windows machine).
- `stt.py` — `FasterWhisperEngine`, lazy model loading. Wrapper logic
  (joining segments, load-once behavior) verified via mocked tests; real
  transcription accuracy **not** verified here.
- `wakeword.py` — `OpenWakeWordEngine`, lazy model loading. Wrapper logic
  (threshold detection, reset behavior) verified via mocked tests; real
  detection accuracy **not** verified here.
- `audio_io.py` — real mic/speaker adapter via `sounddevice`.
  `save_wav()`'s file format is verified for real; `record_seconds()` and
  `play_wav()` need real hardware, untested here.
- `pipeline.py` — `EchoPipeline` (hears -> transcribes -> speaks back) and
  `ListenLoop` (wake-word-gated state machine). Control flow verified via
  fakes/mocks + real TTS.
- `factory.py` — assembles the pipeline, gated by the `MICROPHONE`
  permission (deny-by-default, as required by `permissions_model.md`).

49 automated tests total, all passing. CI runs them on every push
(`.github/workflows/tests.yml`, now also installs `espeak`/`espeak-ng`/
`libportaudio2` so CI can genuinely exercise the TTS/audio-file tests, not
just skip them).

## Next Action

**This phase cannot be marked `verified` from here.** The owner needs to
run it on the actual EliteBook 645 G9 — real internet lets openWakeWord
and faster-whisper download their models, and a real microphone/speakers
let the full wake-word -> listen -> echo loop be tested end-to-end. Once
confirmed working, write `phase_completion_records/P002-completion.md`
and update `roadmap.md`'s Phase 2 status to `verified`. Only after that
should Phase 3 (Multi-AI Brain) begin.
