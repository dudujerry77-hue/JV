# Privacy Policy

Status: decided (principles), proposed (implementation)

## Local-First Where Practical

Sensitive functionality should prefer local processing where technically
practical:

- local memory
- local device status
- local logs
- local face recognition
- local automation
- local model inference when hardware permits

Cloud AI is used where it provides a meaningful advantage, not by default
for sensitive data. **The user must always be able to know when data
leaves the device** — this is a logging/observability requirement, not
just a design preference (see `observability_spec.md`, `ai_provider_spec.md`).

## Monitoring Boundaries

Jarvis must never secretly monitor unauthorized devices or people. For the
owner's own devices, monitoring scope and retention must be clearly
documented before the relevant feature (e.g. the Security System in
`feature_spec.md`) is implemented — not decided implicitly by the code.

## Data Minimization

Avoid collecting data Jarvis does not need. This applies to every
subsystem, not only the ones that look privacy-sensitive on their face —
e.g. task logs, research history, and device status all accumulate data
and must be scoped deliberately.

## Retention

All stored activity has explicit, user-configurable retention rules. See
`data_retention_policy.md` for the full mechanism. This document defines
the *principle*; that document defines the *mechanism*.

## Relationship to Security

Privacy and security are related but distinct: `security_policy.md` covers
protecting Jarvis and its credentials from compromise; this document covers
what Jarvis collects, why, and for how long, and who it does or does not
watch.
