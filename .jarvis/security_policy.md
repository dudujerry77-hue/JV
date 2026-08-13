# Security Policy

Status: decided (principles), proposed (implementation)

This document covers securing **Jarvis itself** (the system, its code, its
credentials, its runtime). For the *product feature* called "Security
System" (owner/face recognition, device monitoring, alerts), see
`feature_spec.md` — that feature must itself comply with this policy plus
`privacy_policy.md`.

## Required Practices

- Least privilege everywhere — components get only the permissions they
  need (see `permissions_model.md`).
- Encrypted secrets and secure credential storage — never plaintext API
  keys, never secrets committed to source control.
- Explicit permission boundaries between subsystems.
- Authentication and authorization on any interface that can act on the
  owner's behalf.
- Audit logging for sensitive actions (see `observability_spec.md`).
- Secure IPC between Jarvis Core, agents, and devices.
- Sandboxing where appropriate, especially for plugin execution
  (`plugin_spec.md`).
- Safe plugin loading — plugins declare required permissions; Core enforces
  them, does not trust plugin self-restraint.
- Input validation and output validation at every trust boundary.
- Network security for any Jarvis component that talks over a network.
- Secure update mechanism (see `release_strategy.md`) — updates must be
  verifiable and must not be a vector for silent capability escalation.

## Relationship to Autonomy

Security review is a required gate for phase completion
(`roadmap.md`) and for any feature touching permissions, devices, or
financial actions (`agent_rules.md` §"Feature Development Protocol").

## Incident Handling

Security-relevant failures (credential leak, permission bypass, plugin
misbehavior) trigger `failure_recovery.md` safe-mode behavior, not silent
recovery. They must be logged and surfaced via `observability_spec.md`.
