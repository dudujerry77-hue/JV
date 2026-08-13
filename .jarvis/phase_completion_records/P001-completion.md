# Phase 1 Completion Record

## Phase

Phase 1 — Foundation

## Objectives

Per `roadmap.md`: core application, runtime, configuration, database,
plugin architecture, security foundation.

## Completed Features

- **Config system** (`jarvis_core/config`) — layered defaults -> YAML
  file -> environment overrides, validated via Pydantic. Status:
  `verified`.
- **Observability foundation** (`jarvis_core/observability`) — structured
  logging to console + rotating file. Status: `implemented` (not yet
  independently tested beyond being exercised by other tests; no
  dedicated assertions on log output).
- **Storage layer** (`jarvis_core/storage`) — SQLite via a single
  `get_connection()` entry point, schema for `permission_grants` and
  `audit_log`. Status: `verified` (exercised by permission tests).
- **Permission system** (`jarvis_core/permissions`) — capability catalog
  (15 capabilities per `permissions_model.md`), deny-by-default store,
  tier classification (standard/sensitive/financial), `require()`
  enforcement gate with audit logging. Status: `verified`.
- **Plugin system** (`jarvis_core/plugins`) — manifest schema per
  `plugin_spec.md`, directory-based discovery, per-plugin failure
  isolation, in-memory registry. Status: `verified` for discovery/
  validation/registry. Plugin *execution* (actually running plugin code)
  is explicitly out of scope for Phase 1 — only manifest loading exists.
- **Core service** (`jarvis_core/service`) — FastAPI/Uvicorn app with
  `/health` and `/status`, loopback-only binding enforced in code (not
  just by default config value). Status: `verified`.

## Tests

26 automated tests (`pytest`), all passing:

- `tests/test_config.py` — 4 tests (defaults, file override, env
  override, path resolution).
- `tests/test_permissions.py` — 8 tests (deny-by-default, grant/revoke,
  full-catalog seeding, tier mapping, `require()` allow/deny paths,
  audit-log write).
- `tests/test_plugins.py` — 6 tests (empty dir, missing dir, valid
  manifest, invalid manifest isolation, no-manifest dir skipped, registry
  behavior).
- `tests/test_service.py` — 8 tests (`/health`, `/status`, loopback
  enforcement allow/reject cases).

Run with: `pytest -v` (or via the new CI workflow, below).

## Verification

- All 26 tests run and passed locally (`.venv/bin/pytest -v`, 26 passed).
- A real end-to-end smoke test was also run outside the test suite: booted
  the service on a real socket, hit `/health` and `/status` over real
  HTTP, confirmed a real SQLite database file was created and seeded with
  all 15 capabilities at `granted=0`.
- CI added (`.github/workflows/tests.yml`) — runs `pytest -v` on every
  push and pull request from this point forward, so future changes are
  checked automatically rather than relying on an agent remembering to
  run tests manually.

## Security Review

Performed as part of closing out this phase (`security_policy.md`
requires this before phase completion):

- **SQL**: all queries in `jarvis_core/storage` and `jarvis_core/permissions`
  use parameterized placeholders (`?`) — no string-built SQL, no injection
  surface.
- **YAML parsing**: plugin manifests and config files are loaded with
  `yaml.safe_load`, not `yaml.load` — no arbitrary object deserialization
  risk from a malicious manifest or config file.
- **Secrets**: no secret values exist in config files or source; `keyring`
  (D-0012) is wired as a dependency but not yet exercised since Phase 1
  has no AI provider credentials to store — this will be exercised for
  real in Phase 3.
- **Plugin isolation**: Phase 1 only parses and validates plugin
  manifests — it does not import or execute any plugin code, so there is
  no code-execution surface from a malicious plugin yet. This must be
  re-reviewed when plugin *execution* is implemented in a later phase.
- **Finding, fixed during this review**: the core service's host binding
  had no enforcement — `config.service.host` defaulted to `127.0.0.1`,
  but nothing stopped it from being overridden (via config file or the
  `JARVIS_SERVICE__HOST` env var) to a public interface, which would have
  exposed a completely unauthenticated API to the network. Fixed by
  adding `ensure_loopback_only()` in `jarvis_core/service/app.py`, called
  before the service binds in `jarvis_core/service/main.py::run()`, which
  raises `RuntimeError` and refuses to start rather than silently binding
  wide. Covered by `test_ensure_loopback_only_allows_loopback_hosts` /
  `test_ensure_loopback_only_rejects_non_loopback_hosts`.
- **No authentication exists on the API** — acceptable for Phase 1 only
  because of the loopback-only enforcement above; this must be revisited
  before any future phase exposes the API beyond `127.0.0.1` (e.g. phone
  access in Phase 7).

## Known Limitations

- No first-party plugins exist yet — plugin loading has only been
  exercised against synthetic test fixtures.
- Observability is logging-only; no metrics, no dashboard (that's Phase
  11 — Mission Control).
- No data retention mechanism is implemented yet for `audit_log` (Phase 1
  volume is low; real retention mechanics are Phase 5 — Memory work, per
  `data_retention_policy.md`).
- No AI provider integration (Phase 3), no voice (Phase 2), no
  computer automation (Phase 4).

## Unresolved Issues

None blocking. The API-authentication gap above is a known, accepted-for-now
limitation (mitigated by loopback enforcement), not an unresolved bug.

## Architectural Decisions

D-0009, D-0010, D-0011, D-0012 (stack selection) from the prior pass; no
new architectural decisions were needed to close out this phase — the
loopback-binding fix is an implementation of D-0011, not a new decision.

## Next Phase

Per `roadmap.md`, Phase 2 (Voice) is next in the documented sequence.
However, voice input/output has nothing to talk to until an AI provider
exists (Phase 3). This sequencing question was raised with the owner and
is pending their decision on which phase to actually build next — see
`current_phase.md`.

## Date

2026-08-13

## Commit / Reference Information

Branch: `claude/repo-cleanup-iyam3d`. This record covers the Phase 1 work
across the Foundation-skeleton commit and this completion-gap-closing
commit (security fix + CI). See `changelog.md` for the full list of
individual changes.
