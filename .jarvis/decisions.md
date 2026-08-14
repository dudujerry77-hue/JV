# Decision Log

This is the authoritative record of architectural and process decisions for
Jarvis. Every entry uses the status vocabulary defined in
`constitution.md` §4. Never silently change a `decided` entry — supersede it
with a new entry instead.

## Entry Template

```
### D-XXXX: <title>
Status: proposed | under_investigation | decided | superseded | blocked | deprecated
Date: YYYY-MM-DD
Context: why this decision is needed
Decision: what was decided (or "none yet" if still open)
Alternatives considered: ...
Consequences: ...
Supersedes: D-XXXX (if applicable)
Superseded by: D-XXXX (if applicable)
```

---

### D-0001: Adopt a governance-first, modular-before-monolithic development model
Status: decided
Date: 2026-08-13
Context: Jarvis is a multi-year project that will be touched by many
different future agents/models. Without a durable governance system,
context and rationale get lost between sessions and agents.
Decision: All work on Jarvis follows the governance system in `.jarvis/`.
Every agent reads `constitution.md`, `current_phase.md`,
`project_state.json`, and `agent_rules.md` before making changes. Features
follow the protocol in `feature_spec.md` / `agent_rules.md`. Modular
architecture (plugins over monolith) is the default.
Alternatives considered: Ad-hoc development with only a README; rejected
because it does not survive agent/model turnover on a multi-year project.
Consequences: Slightly slower start; much higher continuity and safety
over the project's lifetime.

### D-0002: Governance documents live in `.jarvis/` as the single source of truth
Status: decided
Date: 2026-08-13
Context: Governance content needs one canonical, discoverable location.
Decision: All governance/spec documents live under `.jarvis/` as listed in
this repository. Application code and documentation for the running system
will live elsewhere once Phase 1 begins, but process/architecture
governance stays in `.jarvis/`.
Alternatives considered: Wiki or external doc tool; rejected because it
would not travel with the repository/commit history.
Consequences: `.jarvis/` must be kept up to date by every agent as part of
"done" for any meaningful change (see `agent_rules.md`).

### D-0003: Technology stack selection
Status: under_investigation
Date: 2026-08-13
Context: Section 44 of the governance initialization instructions
explicitly prohibits blindly assuming a technology stack (language, UI
framework, local database, IPC architecture, voice technology, local model
strategy, automation strategy, security architecture, plugin architecture,
update mechanism, testing framework). These choices depend on facts only
the owner has: target OS, available hardware (especially GPU/VRAM for local
inference), language preference, budget, and offline requirements.
Decision: None yet. Open questions are recorded in `current_phase.md`.
Alternatives considered: N/A — this entry tracks the open investigation,
not a specific alternative.
Consequences: Phase 1 implementation cannot be planned in detail, and must
not begin, until this decision is made (see `constitution.md` §"Hard
Boundaries" and `current_phase.md`).

### D-0004: Repository state at governance initialization
Status: decided
Date: 2026-08-13
Context: Governance setup requires an honest inspection of what already
exists (see `agent_rules.md` §"Never assume the repository is empty").
Decision: Recorded as fact — at governance initialization, the repository
contained a single `README.md` and no application code. The README was
removed at explicit owner request prior to this governance work. There is
no existing architecture to preserve; Phase 1 Foundation implementation has
not started.
Alternatives considered: N/A — factual record.
Consequences: `feature_spec.md` and `roadmap.md` correctly show zero
implemented features. No migration or backward-compatibility work is
needed for Phase 1.

---

### D-0005: Primary device hardware assessment (laptop)
Status: decided
Date: 2026-08-13
Context: `current_phase.md` flagged local-model hardware as an open
question blocking D-0003. The owner's primary laptop is an HP EliteBook
645 G9, 16GB RAM / 512GB SSD.
Decision: Recorded as fact — this model has **no dedicated/discrete GPU**.
It uses integrated AMD Radeon graphics only, with 16GB of RAM shared
between CPU and graphics. This is a business/productivity laptop, not a
workstation or gaming laptop.
Alternatives considered: N/A — factual hardware record.
Consequences: Local inference capacity on this device is limited to small,
lightweight models. A capable "brain"-tier model cannot run well on this
hardware. This directly drives D-0006.

### D-0006: Hybrid local/cloud AI execution strategy
Status: decided
Date: 2026-08-13
Context: Given D-0005, and the owner's stated wish to run some capability
locally while keeping costs sensible, an execution split is needed between
what runs on-device and what runs via paid cloud API.
Decision: Jarvis splits AI execution by capability tier:
- **Local, free, always-on** (run on the EliteBook 645 G9's CPU/integrated
  graphics): wake word detection, speech-to-text (e.g. Whisper
  small/base), face/owner recognition, memory/embedding search, and
  lower-quality local text-to-speech.
- **Cloud, paid, usage-billed**: the main reasoning/coding/research
  "brain" model, and computer-use/UI-automation, since current hardware
  cannot run capable models for these well.
This split is a default informed by current hardware, not a permanent
architectural lock — it should be revisited if hardware changes (e.g. an
eGPU or a second local-inference machine is added later).
Alternatives considered: All-cloud (rejected — owner wants some local
capability and free always-on functions); all-local (rejected — current
hardware cannot run a capable brain model; would badly degrade quality).
Consequences: `ai_provider_spec.md` updated to document this split.
Ongoing AI cost is driven only by brain/automation usage, not by idle time
or the always-on local functions.

### D-0007: Multi-provider is required, single-provider convenience is optional
Status: decided
Date: 2026-08-13
Context: The owner asked that using one provider/API key to cover
brain + vision + computer-use be **optional**, not a requirement, reaffirming
the existing hard boundary in `constitution.md` against single-vendor
lock-in.
Decision: The AI provider abstraction (`ai_provider_spec.md`) must support
mixing providers per capability (e.g. Anthropic for coding, a different
provider for something else). Using a single provider for convenience is
allowed and may be the practical default, but the architecture must never
require it and must degrade gracefully if any one provider is
unavailable or dropped.
Alternatives considered: Hard-coding a single "primary provider"; rejected,
conflicts with `constitution.md` §"Hard Boundaries".
Consequences: No behavior change to the already-decided provider
abstraction — this entry exists to record the owner's explicit
confirmation of that requirement.

### D-0008: No-cost-to-idle billing principle
Status: decided
Date: 2026-08-13
Context: The owner asked whether payment is required just to run Jarvis,
versus only when actively using paid capabilities.
Decision: Jarvis must never require payment merely to exist or idle.
Cost is only incurred when Jarvis actually invokes a paid cloud provider.
The AI Router and Task System must avoid designs where background/idle
processes (e.g. long-running monitoring missions) repeatedly poll a paid
model when a local model or reduced polling frequency would do — cost
exposure from background tasks must be visible to the owner
(`observability_spec.md`) and bounded/configurable.
Alternatives considered: N/A — this is a cost-transparency requirement,
not a technical alternative choice.
Consequences: `ai_provider_spec.md` and `task_system_spec.md` should
reflect cost-awareness as a design requirement for anything that runs
unattended.

---

### D-0009: Primary OS, app shape, language, and offline posture for Phase 1
Status: decided
Date: 2026-08-13
Context: These were the remaining owner-only questions blocking Phase 1
architecture, listed in `current_phase.md`.
Decision:
- **OS**: Windows (the EliteBook 645 G9's actual OS).
- **App shape**: headless background service + separate thin UI. Jarvis
  Core runs as an always-on Windows background service/process; Mission
  Control and any future chat UI are separate clients that talk to it over
  a local API. This matches the architecture's "Core coordinates, doesn't
  contain everything" principle and keeps the owner's emergency-stop/
  disable path independent of any UI process being open.
- **Language**: Python, for Jarvis Core and first-party plugins, chosen
  for its local-AI ecosystem (Whisper, embeddings, face recognition, local
  model runtimes) which directly matters given the local-tier work
  committed to in D-0006.
- **Offline posture**: cloud-first; offline capability is not a Phase 1
  requirement, consistent with D-0006 (the brain already requires a cloud
  API on current hardware).
Alternatives considered: Electron/Tauri UI-coupled app (rejected --
heavier resource footprint on GPU-less hardware, and couples the always-on
service to a UI process); TypeScript/Rust/Go for Core (rejected -- weaker
local-AI ecosystems for TypeScript/Go, slower iteration for Rust); full
offline requirement (rejected -- would fight D-0005's hardware reality).
Consequences: Unblocks Phase 1 implementation planning. `coding_standards.md`
and `testing_strategy.md` to be filled in with Python-specific tooling.

### D-0010: Local database — SQLite
Status: decided
Date: 2026-08-13
Context: Foundation requires a local database (`roadmap.md` Phase 1). This
was not one of the four questions put to the owner because it is a
low-risk, easily-revisited implementation choice consistent with the
already-decided local-first principle, not a fork in the project's
identity.
Decision: Use SQLite as the local database for Phase 1 (config state,
permission grants, plugin registry, memory/task metadata). Single-file,
zero-server-process, works identically on Windows, trivially backed up.
Alternatives considered: A server-based DB (Postgres, etc.) — rejected as
unnecessary operational overhead for a single-user, single-machine
Foundation phase; can be introduced later behind the same storage
interface if a subsystem outgrows SQLite.
Consequences: Storage access in `memory_spec.md`, `task_system_spec.md`,
and `permissions_model.md` implementations should go through a thin
storage interface so swapping the backend later doesn't require a
rearchitecture.

### D-0011: Core-to-UI communication — local HTTP API
Status: decided
Date: 2026-08-13
Context: D-0009 committed to a headless-service + separate-UI shape, which
requires an IPC mechanism between them.
Decision: Jarvis Core exposes a local HTTP API (FastAPI/Uvicorn), bound
only to `127.0.0.1` (never a public interface) for Phase 1. Any future
remote/phone access goes through an explicit, separately-secured channel,
not this loopback API.
Alternatives considered: Windows named pipes — more "native" but more
complex to build and test against, and harder to reuse for the eventual
web-based Mission Control UI (`observability_spec.md`) than a plain local
HTTP API.
Consequences: `security_policy.md`'s "secure IPC" requirement is satisfied
for Phase 1 by loopback-only binding; this must be revisited before any
feature exposes Core beyond localhost.

### D-0012: Credential storage — OS keyring
Status: decided
Date: 2026-08-13
Context: `security_policy.md` requires encrypted secrets / secure
credential storage, never plaintext API keys in source or config.
Decision: Store AI provider API keys and other secrets using the Windows
Credential Manager via Python's `keyring` library, not in plaintext config
files or source.
Alternatives considered: Plaintext `.env` file — rejected outright, fails
`security_policy.md`; a custom encrypted-file store — rejected as
reinventing what the OS credential store already does safely.
Consequences: Any config field that is a secret must be resolved through
the credential-storage layer, never read directly from a config file.

---

### D-0013: Enforce loopback-only binding in code, not just by config default
Status: decided
Date: 2026-08-13
Context: Closing out Phase 1's required security review (`security_policy.md`)
found that D-0011's "loopback-only" commitment was only a default config
value (`service.host = "127.0.0.1"`), not an enforced constraint. Since the
core service ships with no authentication yet, overriding that default
(via config file or `JARVIS_SERVICE__HOST` env var) would have exposed a
completely unauthenticated control API to the network.
Decision: `jarvis_core/service/app.py::ensure_loopback_only()` is called
before the service binds (`jarvis_core/service/main.py::run()`) and raises
`RuntimeError`, refusing to start, if the configured host is not one of
`127.0.0.1`, `localhost`, `::1`. This must be revisited (not simply
removed) before any future phase adds real authentication and needs to
expose the API beyond localhost (e.g. phone access in Phase 7).
Alternatives considered: Leaving it as a documented-but-unenforced
convention — rejected; conventions don't prevent misconfiguration, and the
consequence here (unauthenticated remote control of Jarvis) is severe
enough to warrant a hard failure instead of a warning.
Consequences: Covered by `tests/test_service.py`'s loopback allow/reject
tests. Recorded in `phase_completion_records/P001-completion.md`.

---

### D-0014: Phase 2 (Voice) confirmed next, documented roadmap order kept
Status: decided
Date: 2026-08-13
Context: `current_phase.md` flagged that `roadmap.md`'s documented order
(Phase 2 Voice before Phase 3 Brain) might not make practical sense, since
voice has nothing to respond with until a brain exists, and asked the
owner to choose.
Decision: Owner chose to keep the documented order — build Phase 2
(Voice) next. Since there is no brain yet, Phase 2 proves out the
wake-word/STT/TTS mechanics via a simple echo pipeline (hears something,
transcribes it, speaks it back) rather than real conversation. Real
conversation is wired in once Phase 3 exists.
Alternatives considered: Reordering to build Phase 3 first — this was the
agent's recommendation, but the owner preferred the documented sequence.
Consequences: `current_phase.md` and `roadmap.md` updated to Phase 2 in
progress. The echo pipeline built in this phase should be easy to point
at a real brain once Phase 3 exists, rather than thrown away.

### D-0015: Voice stack — openWakeWord, faster-whisper, pyttsx3
Status: decided
Date: 2026-08-13
Context: Phase 2 needs concrete wake-word, speech-to-text, and
text-to-speech libraries. Per D-0006, these are local-tier (free,
always-on) capabilities that must run on the owner's GPU-less EliteBook
645 G9.
Decision:
- **Wake word**: `openWakeWord` — open-source, ONNX-based, runs on CPU,
  no cloud dependency.
- **Speech-to-text**: `faster-whisper` (CTranslate2-based Whisper) — CPU-
  efficient compared to the reference Whisper implementation, no cloud
  dependency once its model is downloaded once.
- **Text-to-speech**: `pyttsx3` over the OS-native voice engine (SAPI5 on
  the owner's actual Windows machine; espeak-ng on Linux, used here in
  this development sandbox to verify the wrapper for real). Zero model
  download required, works offline immediately.
Both `openWakeWord` and `faster-whisper` require downloading pretrained
model weights on first use (from GitHub/Hugging Face respectively) — this
could not be verified in the agent's sandbox, whose network policy blocks
`huggingface.co` (confirmed via a 403 from the outbound proxy). Both
engines are built with lazy model loading and tested here against mocked
model layers; **real transcription/wake-word accuracy must be verified on
the owner's actual machine**, which has normal internet access.
Alternatives considered: Cloud STT/TTS (e.g. a paid API) — rejected for
this tier per D-0006, these are meant to be the free/local/always-on
pieces; Piper for TTS — a higher-quality local alternative than pyttsx3,
worth revisiting later, but `pyttsx3` needs zero model download and
matches "get something working first."
Consequences: `pyproject.toml` gains `faster-whisper`, `openwakeword`,
`pyttsx3` as dependencies. `phase_completion_records/P002-completion.md`
(once written) must explicitly note which parts were verified in-sandbox
vs. deferred to the owner's machine — this phase cannot honestly be
marked fully `verified` the way Phase 1 was, until the owner confirms
real-world mic/model behavior.

---

### D-0016: Decouple audio capture from inference (fix real-hardware wake-word failure)
Status: decided
Date: 2026-08-13
Context: First real-hardware run of `scripts/verify_phase2_voice.py` on
the owner's EliteBook 645 G9: audio devices, TTS, and STT all passed, but
wake-word detection failed — "hey jarvis" was not detected within 15
seconds. Investigation against the real `openwakeword` source
(`model.py`) confirmed the chunk size (1280 samples/80ms), sample rate
(16kHz), dtype (int16), and threshold-checking logic in
`jarvis_core/voice/wakeword.py` all matched openWakeWord's documented
contract correctly. The bug was not in detection logic — it was in how
the verification script fed audio into it: `engine.predict()` (a TFLite
model inference call) ran directly inside `sounddevice.InputStream`'s
real-time audio callback. PortAudio callbacks must return in a few
milliseconds; running inference inside one risks it falling behind the
deadline, which can cause PortAudio to silently drop/overrun input frames
— the mic still "works" for simple blocking calls like `sd.rec()` (which
is why device detection, TTS, and STT all passed), but streaming
detection can end up processing mostly-empty or corrupted audio without
any visible error, especially since the script wasn't even checking
`sounddevice`'s `status` flag (which flags exactly this: input overflow).
Decision: Decouple capture from inference. Added
`jarvis_core/voice/audio_io.MicrophoneChunkStream` (queue-based: a fast
callback does nothing but copy each chunk into a `queue.Queue`; a normal
consumer loop in the calling thread pulls chunks off the queue and does
the actual `predict()` call, with no real-time deadline to violate).
Updated `scripts/verify_phase2_voice.py`'s wake-word and full-pipeline
steps to use this pattern, and added a diagnostic: the script now prints
the highest score seen per wake-word model even on failure, so a future
failure can be distinguished as "close but under threshold" (tuning
issue) vs. "no signal at all" (mic/device issue) instead of a bare
pass/fail. Added a warning note to `ListenLoop`'s docstring in
`pipeline.py` so this mistake isn't repeated when real service wiring
(Phase 2/3) drives it from a live audio stream.
Alternatives considered: Lowering the detection threshold — rejected as a
first move; changing a threshold without evidence the model's real scores
were actually close to 0.5 would have been guessing, not diagnosis. The
new diagnostic output will show whether threshold-tuning is still needed
after this fix is retested.
Consequences: 3 new tests for the capture-callback contract (enqueues
without inference, copies rather than aliases the buffer, doesn't raise
on status flags) — all mockable without real hardware, since the property
being tested is "the callback does no slow work," not real audio capture.
52 tests total, all passing. Phase 2 is still not marked `verified` —
this fix needs to be re-run on the owner's actual hardware before that
can happen.
