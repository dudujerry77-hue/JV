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
