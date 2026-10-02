## Phase

Phase 1 — Foundation (`roadmap.md`).

## Objectives

Per `roadmap.md` / `current_phase.md`: core application, runtime,
configuration, database, plugin architecture, security foundation. Build
the load-bearing skeleton later phases (voice, AI brain, computer control,
memory, etc.) attach to — not any of those capabilities themselves.

## Completed Features

- **Config system** (`jarvis_core/config`) — layered defaults → YAML file →
  env overrides, validated via Pydantic. No secrets in config files
  (D-0012 reserves that for the OS keyring). `verified`.
- **Observability** (`jarvis_core/observability`) — structured logging to
  console + rotating file, single idempotent setup entry point. `verified`.
- **Permission system** (`jarvis_core/permissions`) — deny-by-default
  SQLite-backed capability store, tier classification
  (`permissions_model.md`), `require()` enforcement gate with **mandatory**
  audit logging (see D-0014 — this was fixed during this phase's security
  review, not merely designed this way from the start). `verified`.
- **Plugin loader** (`jarvis_core/plugins`) — manifest schema matching
  `plugin_spec.md`'s required fields, directory-based discovery with
  per-plugin failure isolation, in-memory registry. No first-party plugins
  ship yet (expected — out of Phase 1 scope). `verified`.
- **Core service** (`jarvis_core/service`) — FastAPI/Uvicorn app, bound to
  loopback only and now *enforced* as loopback-only at the config layer
  (D-0011, hardened by D-0014), exposing `/health` and `/status`.
  `verified`.
- **CI pipeline** (`.github/workflows/ci.yml`) — runs `pytest -v` on every
  push/PR to `main` (D-0013). `verified`.
- **Security review** — performed against `security_policy.md` and
  `permissions_model.md`; two findings, both fixed (D-0014). `verified`.

## Tests

`pytest`, config in `pyproject.toml`. Run with:

```
pip install -e ".[dev]"
pytest -v
```

24 tests across 4 modules:
- `tests/test_config.py` — 7 tests (defaults, file override, env override,
  path resolution, plus 3 new tests added this review for the loopback-host
  enforcement: rejects `0.0.0.0` via direct construction, via YAML file, and
  via env override).
- `tests/test_permissions.py` — 9 tests (deny-by-default, grant/revoke,
  full-catalog seeding, tier mapping, `require()` allow/deny paths, and now
  two audit-log tests: the original granted-check audit test plus a new
  denied-check audit test added to prove audits are written on both paths,
  not just the happy path).
- `tests/test_plugins.py` — 6 tests (empty dir, missing dir, valid
  manifest, invalid manifest isolation, no-manifest dir skipped, registry
  register/get/list).
- `tests/test_service.py` — 2 tests (in-process `/health` and `/status` via
  `TestClient`).

## Verification

Actually run, this session: `pip install -e ".[dev]"` followed by
`python -m pytest -q` — **24 passed, 1 warning** (an unrelated
`StarletteDeprecationWarning` about `httpx`/`starlette.testclient`, not a
failure). Also manually re-confirmed the previously-recorded real-socket
smoke test still applies (no changes to `service/main.py`'s startup path).

CI (`.github/workflows/ci.yml`) has not yet executed on GitHub itself as of
this record (it ships in the same change that introduces it) — it will run
on this phase's first push/PR and on every one thereafter.

## Known Limitations

- No first-party plugins exist, so plugin isolation is only exercised
  against synthetic test fixtures, not a real plugin — expected per
  `roadmap.md`, first real plugin is a Phase 1 follow-up / Phase-adjacent
  decision, not a Phase 1 blocker.
- `keyring`/credential storage (D-0012) has no exercised code path yet —
  nothing in Phase 1 handles a secret. This is a limitation, not a defect:
  there is no AI provider or other secret-holding integration yet for it
  to protect.
- No lint/type-check step in CI — scoped out of D-0013 deliberately: the
  only gap `known_risks` flagged was tests not running automatically,
  which is now fixed. Adding lint/type gates is a reasonable future
  improvement, not a Phase 1 requirement.
- No numeric coverage threshold enforced (unchanged from
  `testing_strategy.md`'s original Phase 1 framework decision).

## Unresolved Issues

None blocking. See D-0014 for the two issues found during security review
— both are fixed, not deferred; no new open issues were created as a
result.

## Architectural Decisions

- D-0013: CI pipeline — GitHub Actions running pytest.
- D-0014: Phase 1 security review findings and fixes (mandatory audit
  logging; enforced loopback-only service host).

No prior decision was superseded.

## Next Phase

Per `roadmap.md`, Phase 2 (Voice) and Phase 3 (Multi-AI Brain) are both
`proposed`. Per `project_state.json`'s `next_actions` and this session's
direction from the owner, the chosen next step is **Phase 3 (Multi-AI
Brain)** — wiring a real AI provider — rather than Phase 2, so Jarvis has
an actual capability to exercise the Foundation layer against (permission
checks, config, logging) before building the voice interface on top of it.
This is an explicit reordering relative to `roadmap.md`'s listed sequence;
per that document's own "Notes" section this is allowed ("a later phase may
begin early work if it does not violate `agent_rules.md`") and is recorded
here as the decision record for that reordering.

Prerequisites Phase 3 now has that it didn't before this record: a CI gate
that will catch regressions in the config/permission/service layers Phase 3
builds on, and a hardened (not just documented) loopback/audit guarantee to
build the AI provider's credential handling against.

## Date

2026-10-02

## Commit / Reference Information

Branch: `claude/phase1-closeout`. See the commit on this branch titled
"Close out Phase 1: CI, security review fixes, completion record" for the
exact diff (`.github/workflows/ci.yml`,
`jarvis_core/permissions/checker.py`, `jarvis_core/permissions/store.py`,
`jarvis_core/config/schema.py`, `tests/test_permissions.py`,
`tests/test_config.py`, `.jarvis/decisions.md`,
`.jarvis/testing_strategy.md`, `.jarvis/current_phase.md`,
`.jarvis/project_state.json`, this file).
