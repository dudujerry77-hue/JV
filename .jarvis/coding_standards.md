# Coding Standards

Status: proposed (process rules are decided; language/framework-specific
style rules are pending `decisions.md` D-0003)

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

## Pending (to be filled in once D-0003 is decided)

- Primary language(s) and version(s).
- Formatter/linter and enforcement (pre-commit, CI).
- Directory/module layout convention.
- Dependency management approach.
- Minimum test coverage expectations by module criticality.

This section must be completed as part of the Phase 1 implementation plan,
not invented ahead of the stack decision.
