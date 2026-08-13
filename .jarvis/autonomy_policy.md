# Autonomy Policy

Status: decided (levels + safety principles), proposed (implementation)

## Autonomy Levels

Autonomy is configurable per capability/mission, not a single global
switch:

| Level | Name | Behavior |
|---|---|---|
| 0 | Observe | Can analyze but cannot act. |
| 1 | Suggest | Can recommend actions. |
| 2 | Draft | Can prepare actions for approval. |
| 3 | Execute Approved | Can execute explicitly approved tasks. |
| 4 | Autonomous Limited | Can execute predefined low-risk tasks automatically. |
| 5 | Autonomous Missions | Can manage long-running approved missions within strict, documented boundaries. |

`FINANCIAL_ACTION` (see `permissions_model.md`) is never eligible for
autonomous execution beyond what has been explicitly, narrowly authorized —
regardless of the general autonomy level configured elsewhere.

## Safety Requirements

Jarvis must provide, from Phase 1 forward as each relevant subsystem is
built:

- Emergency stop.
- Task cancellation.
- Permission revocation.
- Activity logs.
- Secure configuration.
- Recovery mode / safe mode.
- Backup/restore.
- Audit trails.

## Non-Negotiable Constraints

- The user must always be able to pause autonomy — globally or per
  mission/capability.
- Jarvis must never be designed to be impossible for its owner to disable,
  uninstall, or administratively recover, even while it runs as a
  background service that protects itself against *accidental* changes
  (see `constitution.md` §"Hard Boundaries").

## Relationship to Other Documents

- `permissions_model.md` defines *what* Jarvis is allowed to touch.
- This document defines *how independently* Jarvis may act once permitted.
- `failure_recovery.md` defines what happens when autonomous action fails.
- `observability_spec.md` defines how the owner can inspect autonomous
  activity after the fact.
