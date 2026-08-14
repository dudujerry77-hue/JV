# Changelog

Human-readable, chronological record of what happened, for humans skimming
project history. For *why* architectural choices were made, see
`decisions.md`. For phase-level outcomes, see `phase_completion_records/`.

## 2026-08-13

- Repository's only file (`README.md`) removed at explicit owner request.
- Governance system initialized under `.jarvis/`: constitution, vision,
  scope, architecture, roadmap, current phase, project state, decision
  log, agent rules, coding standards, testing strategy, security policy,
  permissions model, privacy policy, autonomy policy, feature spec, plugin
  spec, AI provider spec, memory spec, device integration spec, research
  engine spec, agent system spec, task system spec, observability spec,
  data retention policy, failure recovery, release strategy, and this
  changelog.
- Repository inspected: no application code exists; no technology stack
  chosen. Recorded as D-0004.
- Phase set to "Phase 0 — Governance & Architecture Initialization",
  status `in_progress`. Phase 1 implementation explicitly not started,
  pending owner review and the open questions in `current_phase.md`.
- Owner confirmed primary device is an HP EliteBook 645 G9 (integrated AMD
  Radeon graphics, no dedicated GPU, 16GB RAM). Recorded as D-0005.
- Decided a hybrid local/cloud AI execution split driven by that hardware
  constraint: lightweight always-on functions run locally for free; the
  main brain model and computer-use automation run via paid cloud API.
  Recorded as D-0006 and reflected in `ai_provider_spec.md`.
- Confirmed, per owner request, that provider consolidation (one API key
  covering multiple capabilities) is optional convenience, never a
  requirement — reaffirms the existing no-single-vendor-lock-in boundary.
  Recorded as D-0007.
- Decided Jarvis must never require payment just to run/idle; cost is
  incurred only on actual paid-provider use, and background/unattended
  tasks must keep cost exposure visible and bounded. Recorded as D-0008.
- `current_phase.md` updated to separate resolved vs. still-open
  technology-stack questions; `project_state.json` updated accordingly.
- Owner answered the remaining Phase 1-blocking questions: Windows,
  headless service + separate UI, Python, cloud-first/offline not
  required. Recorded as D-0009. Added agent-proposed, documented defaults
  for local database (SQLite, D-0010), Core-to-UI IPC (local HTTP API,
  D-0011), and credential storage (OS keyring, D-0012).
- Phase advanced to "Phase 1 — Foundation", status `in_progress`.
  `roadmap.md` and `project_state.json` updated accordingly. Beginning
  Foundation implementation: package skeleton, config, observability,
  permissions, plugin loader, core service, tests.
- Implemented the Phase 1 Foundation skeleton under `jarvis_core/`: config
  system, structured logging, SQLite storage layer, capability-based
  permission system (deny-by-default, audited), plugin manifest/discovery
  with per-plugin failure isolation, and a loopback-only FastAPI core
  service with `/health` and `/status`.
- Wrote 20 automated tests (`pytest`) covering config loading, permission
  grant/revoke/require/audit behavior, plugin discovery (valid/invalid/
  missing manifests), and the core service's endpoints. All 20 pass.
- Found and fixed a real bug during testing: `load_config()` treated an
  unset config path as `Path(".")` (always truthy), so it tried to open
  the current directory as a YAML file. Fixed by only constructing a
  `Path` when a path string is actually present.
- Ran a real end-to-end smoke test: booted the service on a real socket,
  hit `/health` and `/status` over real HTTP, confirmed a real SQLite
  database file was created and seeded correctly.
- Filled in `coding_standards.md` and `testing_strategy.md`'s previously-
  pending sections now that the stack is decided and exercised.
- Updated `project_state.json` with implemented/verified feature lists.
  Phase 1 remains `in_progress`, not complete -- no CI, no formal security
  review, and no phase completion record yet (roadmap.md's completion bar
  is: implementation + tests + integration + documentation + security
  review + verification, and the security review has not happened).
- Performed the Phase 1 security review. Found a real gap: the core
  service's loopback-only binding (D-0011) was only a config default, not
  enforced -- overriding it would have exposed an unauthenticated API to
  the network. Fixed via `ensure_loopback_only()` in
  `jarvis_core/service/app.py`, called before bind in `service/main.py`.
  Recorded as D-0013. Added 6 new tests (now 26 total, all passing).
- Added CI (`.github/workflows/tests.yml`) -- runs `pytest -v` on every
  push and pull request.
- Wrote `phase_completion_records/P001-completion.md`. Phase 1 -- 
  Foundation is now `verified` per `roadmap.md`'s own completion bar.
  `roadmap.md`, `current_phase.md`, and `project_state.json` updated
  accordingly.
- Flagged an open sequencing question rather than silently deciding it:
  `roadmap.md` lists Phase 2 (Voice) before Phase 3 (Multi-AI Brain), but
  voice has nothing to respond with until a brain exists. Recorded as an
  open question in `current_phase.md`, pending owner choice.
- Owner chose to keep the documented order (Phase 2 -- Voice next).
  Recorded as D-0014.
- Discovered two real sandbox constraints while scoping Phase 2: this
  environment's network policy blocks `huggingface.co` (confirmed via a
  403 from the outbound proxy), and it has zero audio devices. Chose the
  voice stack accordingly (D-0015: openWakeWord, faster-whisper, pyttsx3)
  and designed every model-dependent engine with lazy loading + injectable
  loaders so wiring is testable without network, while TTS (which needs no
  model download) is genuinely exercised for real via `espeak-ng`.
- Implemented `jarvis_core/voice/`: engine interfaces, `Pyttsx3Engine`
  (TTS, real), `FasterWhisperEngine` (STT, lazy-loaded), `OpenWakeWordEngine`
  (wake word, lazy-loaded), `audio_io.py` (real mic/speaker adapter via
  `sounddevice`), `EchoPipeline` + `ListenLoop` (conversation mechanics),
  `factory.py` (assembles the pipeline, gated by the `MICROPHONE`
  permission). Added `VoiceConfig` to the config schema.
- Added 23 new tests (49 total, all passing). Updated CI to install
  `espeak`/`espeak-ng`/`libportaudio2` so it can genuinely run the
  TTS/audio tests, not just skip them.
- Updated `project_state.json`, `current_phase.md`, and `roadmap.md`:
  Phase 2 is `implemented` but explicitly **not** `verified` -- real
  wake-word/STT model accuracy and real microphone capture require the
  owner's actual EliteBook 645 G9 to confirm, which this sandbox cannot
  do (no audio hardware, blocked model-download host).
- **Round 1 real-hardware results from the owner**: audio devices PASS,
  TTS PASS, STT PASS, wake-word detection FAIL ("hey jarvis" not detected
  within 15s). Full pipeline untested (blocked by the wake-word failure).
- Investigated against the real openWakeWord source. Chunk size, sample
  rate, dtype, and threshold logic in `jarvis_core/voice/wakeword.py` all
  checked out correctly. Root cause: `scripts/verify_phase2_voice.py` ran
  wake-word inference directly inside `sounddevice`'s real-time audio
  callback, risking silently dropped input if inference fell behind the
  callback's deadline -- simple blocking calls (`sd.rec()`, used by
  TTS/STT) don't have this problem, which is why only wake-word detection
  failed. Recorded as D-0016.
- Fixed by adding `jarvis_core/voice/audio_io.MicrophoneChunkStream`
  (queue-decoupled capture: a fast callback only enqueues, a normal loop
  does the actual inference) and rewriting the verification script's
  wake-word and full-pipeline steps to use it. Added a diagnostic: the
  script now prints the highest score seen per wake-word model even on
  failure. Added a warning to `ListenLoop`'s docstring so this mistake
  isn't repeated in future real service wiring.
- Added 3 tests for the new capture-callback contract (52 total, all
  passing). Updated `project_state.json` and `current_phase.md` with
  round 1 results and the fix -- Phase 2 remains explicitly unverified,
  pending a round 2 real-hardware retest.
