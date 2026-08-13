# Testing Strategy

Status: decided (principles + Phase 1 framework)

## Principle

"Testable before production" and "observable before autonomous"
(constitution.md) mean testing is not optional polish — it's a gate on
declaring a phase or feature complete (see `roadmap.md` §"Definition of
Phase Complete").

## Required Test Categories (as subsystems come online)

- Unit tests — individual functions/modules.
- Integration tests — subsystem boundaries (e.g. AI router <-> provider).
- End-to-end tests — user-facing flows.
- Security tests — permission boundaries, credential handling.
- Permission tests — capability-based authorization behaves as declared
  (`permissions_model.md`).
- Plugin tests — isolation and manifest contract compliance
  (`plugin_spec.md`).
- AI integration tests — provider abstraction, fallback behavior
  (`ai_provider_spec.md`).
- Failure recovery tests — checkpoint/resume, worker restart, safe mode
  (`failure_recovery.md`).
- Device integration tests — where applicable, per connected device.

Critical capabilities (anything touching permissions, financial actions,
security monitoring, or data retention) must have automated regression
tests before being marked `verified`.

## What "Verified" Requires

A feature is marked `verified` in `project_state.json` / `decisions.md`
only when its required tests exist, pass, and were actually run — not
merely written. An agent must report which tests were executed and what
passed, per `agent_rules.md` §"Agent Handoff Protocol".

## Phase 1 Framework (decided)

- **Framework**: `pytest`, with `httpx`/FastAPI's `TestClient` for API
  tests. Config is `pyproject.toml`'s `[tool.pytest.ini_options]`.
- **Fixtures**: shared fixtures (temp config, temp SQLite connection,
  seeded permission store) live in `tests/conftest.py` so every test
  module gets an isolated, disposable data directory (`tmp_path`) — tests
  must never touch the owner's real `~/.jarvis-runtime`.
- **What Phase 1 actually covers**: config loading (defaults, file
  override, env override, path resolution), permission store (deny-by-
  default, grant/revoke, full-catalog seeding, tier mapping, the
  `require()` gate's allow/deny paths, audit-log writes), plugin discovery
  (valid manifest, invalid manifest isolation, missing manifest, registry
  behavior), and the core service's `/health` and `/status` endpoints —
  both via the in-process `TestClient` and one real-socket smoke test.
- **CI pipeline**: not yet wired up (no CI config exists in the repo yet).
  Tracked as Phase 1 follow-up, not a Foundation blocker — `pytest` must
  be run manually before each commit until CI exists.
- **Coverage thresholds**: no numeric threshold enforced yet. The concrete
  rule for now is `coding_standards.md`'s "every module has at least one
  test module, security-relevant code covers both allow and deny paths."
