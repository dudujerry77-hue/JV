# Current Phase

Phase: **Phase 1 — Foundation**
Status: `in_progress`
Last updated: 2026-08-13

## What Is Happening Right Now

Phase 0 governance is complete enough to unblock implementation: all
owner-only questions needed for Phase 1 architecture have been answered
(D-0009), and the remaining low-risk implementation choices (database,
Core-to-UI IPC, credential storage) have been recorded as agent-proposed,
documented defaults (D-0010, D-0011, D-0012) per the "small changes may use
a shortened process when documented" allowance in `agent_rules.md`.

Phase 1 objective, per `roadmap.md`: core application, runtime,
configuration, database, plugin architecture, security foundation.

## Decided Foundation Stack

- OS target: Windows (D-0009)
- App shape: headless background service (Jarvis Core) + separate thin UI
  client, talking over a local HTTP API (D-0009, D-0011)
- Language: Python (D-0009)
- Local database: SQLite (D-0010)
- Core-to-UI IPC: local HTTP API via FastAPI/Uvicorn, bound to
  `127.0.0.1` only (D-0011)
- Credential storage: OS keyring (Windows Credential Manager) via
  Python's `keyring` library (D-0012)
- Test framework: pytest (see `testing_strategy.md`)
- Offline posture: cloud-first, offline not required for Phase 1 (D-0009)

## Phase 1 Scope (this pass)

- Package skeleton (`jarvis_core/`) with a clear module boundary per
  major system in `architecture.md`.
- Config system: layered defaults + file + env, no secrets in config
  files (secrets go through D-0012's keyring layer).
- Observability foundation: structured logging to file + console.
- Permission system skeleton: the capability catalog from
  `permissions_model.md`, backed by SQLite, with an enforced (not just
  advisory) check mechanism. No sensitive capability is actually wired to
  a real action yet — this phase builds the gate, not what walks through
  it.
- Plugin loader skeleton: discovers a `plugins/` directory, validates each
  plugin's manifest against `plugin_spec.md`'s required fields, registers
  valid plugins. No first-party plugins ship yet.
- Core service: FastAPI app exposing `/health` and `/status`, wired to
  config, logging, the permission store, and the plugin registry.
- Tests for all of the above (`testing_strategy.md`).

## Explicitly Not in This Pass

AI provider integration (Phase 3), voice (Phase 2), computer automation
(Phase 4), memory beyond the raw SQLite tables needed for permissions/
plugins (Phase 5), and the actual Mission Control UI (Phase 11) — Phase 1
only builds the load-bearing skeleton those phases will attach to.

## Remaining Open Questions (deferred to later phases, not blocking Phase 1)

- Android integration approach — needed for Phase 7, not Phase 1.
- Specific cloud AI provider(s) to wire up first, and a monthly cost
  ceiling — needed for Phase 3.

## Next Action

Implement the Phase 1 scope above, write tests, verify they pass, update
`project_state.json`, and produce a Phase 1 completion record in
`phase_completion_records/` once the full completion bar in `roadmap.md`
is met (implementation + tests + integration + documentation + security
review + verification) — a partial pass does not get marked complete.
