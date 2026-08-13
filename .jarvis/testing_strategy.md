# Testing Strategy

Status: proposed (principles decided; framework selection pending D-0003)

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

## Pending (to be filled in once D-0003 is decided)

- Test framework(s) per language.
- CI pipeline design.
- Coverage thresholds, if any, per module criticality tier.
