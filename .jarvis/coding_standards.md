# Coding Standards

Status: decided (process rules and Phase 1 stack), living document for
future language/framework additions

## Process Standards (apply regardless of chosen stack)

These apply from Phase 1 onward, independent of which language/framework is
ultimately chosen:

- No secrets, API keys, or credentials in source code, ever. Use secure
  credential storage (see `security_policy.md`).
- Every module/plugin has a clear, documented boundary (constitution.md
  principle 14).
- Commit messages describe *why*, not just *what*, for anything
  non-trivial.
- No dead code left "just in case" — delete it; git history preserves it.
- No speculative abstractions for hypothetical future requirements
  (constitution.md-aligned: configurable before hard-coded, but not
  over-engineered).
- Public interfaces (module boundaries, plugin APIs, agent contracts) are
  documented at the point of definition.
- Every new capability is evaluated against `plugin_spec.md` — should this
  be Core or a plugin?

## Phase 1 Stack (decided — D-0009 to D-0012)

- **Language**: Python 3.11+.
- **Package layout**: a single `jarvis_core` package, one subpackage per
  major system boundary from `architecture.md` (`config`, `observability`,
  `permissions`, `plugins`, `storage`, `service`, ...). New systems get
  their own subpackage rather than being folded into an existing one, per
  constitution.md principle 14 ("every feature must have an owner/module
  boundary").
- **Dependency management**: `pyproject.toml` (PEP 621), installed
  editable in a local virtualenv (`.venv/`, git-ignored). Runtime deps and
  `dev` extras (test tooling) are kept separate.
- **Web/API framework**: FastAPI + Uvicorn, bound to `127.0.0.1` only
  (D-0011) — never expose Jarvis Core directly to a public interface.
- **Local database**: SQLite via the standard library `sqlite3`, accessed
  only through `jarvis_core.storage.get_connection` (D-0010) — subsystems
  do not open their own database files.
- **Secrets**: the `keyring` library over the OS credential store
  (D-0012). Config files (`JarvisConfig`) never hold secret values —
  enforce this at review time, not just by convention.
- **Config validation**: Pydantic models (`jarvis_core.config.schema`) —
  every config surface is a typed, validated schema, not a loose dict.

## Style / Enforcement (not yet automated)

Formatter/linter enforcement (e.g. via a pre-commit hook or CI check) is
not wired up yet — this is Phase 1 follow-up work, not a Foundation
blocker. Until then: match the style already in `jarvis_core/` (typed
function signatures, module-level docstring explaining *why* a module
exists and which spec it implements, no bare `except:`).

## Minimum Test Coverage Expectation

Every module under `jarvis_core/` must have at least one corresponding
test module under `tests/` before being merged — see `testing_strategy.md`
for what "covered" means per criticality tier. Permission and plugin
loading logic (security-relevant) must cover both the success path and the
failure/denial path, not just the happy path.
