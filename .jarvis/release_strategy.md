# Release Strategy

Status: proposed

## Phase Completion Requires All Of

```
Implementation + Tests + Integration + Documentation + Security review + Verification
```

Code existing is not sufficient to declare a phase (or a feature) complete
(`constitution.md` principle applied via `roadmap.md`). Each completed
phase gets a record in `phase_completion_records/` following
`phase_completion_records/TEMPLATE.md`, including objectives, completed
features, tests, verification, known limitations, unresolved issues,
architectural decisions, next phase, date, and commit/reference
information.

## Versioning

Proposed default: semantic versioning (`MAJOR.MINOR.PATCH`) for both the
governance system (`project_state.json.governance_version`) and, once
Phase 1 begins, for Jarvis itself. This is a `proposed` default, not yet a
`decided` D-XXXX entry — confirm as part of the Phase 1 implementation
plan.

## Secure Updates

Per `security_policy.md`, any update mechanism must be verifiable and must
not be a vector for silent capability escalation (e.g. a routine update
should not be able to silently grant itself new permissions). The concrete
update mechanism is a Phase 1+ technology decision (`decisions.md`
D-0003).

## Relationship to Governance

Releases are not just code drops — a release that changes decided
architecture requires the Change Management process
(`agent_rules.md`) to have already happened, not to happen retroactively
in the release notes.
