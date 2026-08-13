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
