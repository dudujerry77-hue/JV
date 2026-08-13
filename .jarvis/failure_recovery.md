# Failure Recovery

Status: decided (principles), proposed (implementation)

## Principle

"Recoverable before powerful" (`constitution.md` principle 4). Every
capability added to Jarvis should be evaluated for what happens when it
fails, not only when it succeeds.

## Self-Healing (bounded)

Jarvis may detect and recover from recoverable problems automatically:

| Problem | Response |
|---|---|
| Worker crashed | Restart worker |
| API temporarily unavailable | Retry (with backoff) |
| Task interrupted | Resume from checkpoint |
| Plugin crashed | Isolate plugin |
| Database problem | Enter safe mode |

## Hard Boundary

Jarvis must **not** implement uncontrolled self-modification. It must never
rewrite its own security boundaries or core architecture autonomously —
self-healing means restart/retry/isolate/safe-mode, never self-redesign
(`constitution.md` §"Hard Boundaries").

## Required Mechanics

- Graceful shutdown.
- Crash recovery.
- Process isolation where appropriate (especially plugins,
  `plugin_spec.md`).
- Checkpointing for long-running tasks (`task_system_spec.md`).
- Safe mode: a reduced-capability state Jarvis enters when something is
  wrong that it cannot safely auto-recover from, rather than continuing to
  operate in an unknown-good state.

## Safety Controls (always available)

Emergency stop, task cancellation, permission revocation, activity logs,
secure configuration, recovery mode, backup/restore, audit trails
(`autonomy_policy.md` §"Safety Requirements").

## Relationship to Observability

Every failure and recovery action is logged (`observability_spec.md`) so
the owner can answer "what went wrong, and what did Jarvis do about it?"
