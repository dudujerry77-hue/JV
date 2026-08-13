# Task System Specification

Status: proposed

## Task States

Jarvis must support short and long-running tasks, tracked through these
states: queued, running, paused, completed, failed, cancelled — with
retries, checkpoints, progress, logs, and notifications.

Examples spanning the range:

- "Open VS Code." — short task.
- "Research the best opportunities for starting a web-design business." —
  medium task.
- "Monitor opportunities for the next 30 days and notify me when something
  matches my criteria." — long-running task.

## Heavy-Workload Requirements

Jarvis must be designed to handle heavy workloads without collapsing.
Required architectural elements (introduced incrementally as load
justifies them, not all in Phase 1):

- background workers
- task queues
- concurrency control
- rate limiting
- retries with exponential backoff
- caching
- checkpoints
- persistence
- graceful shutdown
- crash recovery
- process isolation where appropriate
- resource monitoring
- cancellation
- timeouts

A failed task must fail gracefully instead of taking down the entire
Jarvis system (`failure_recovery.md`).

## Self-Healing (bounded)

Jarvis may detect and recover from *recoverable* problems, e.g.:

- worker crashed -> restart worker
- API temporarily unavailable -> retry
- task interrupted -> resume from checkpoint
- plugin crashed -> isolate plugin
- database problem -> enter safe mode

**Hard boundary:** Jarvis must not implement uncontrolled self-modification.
It must never rewrite its own security boundaries or core architecture
autonomously (`constitution.md` §"Hard Boundaries"). Self-healing is
restart/retry/isolate/safe-mode, not self-redesign.

## Relationship to Other Systems

- Long-running research tasks (`research_engine_spec.md`) and missions
  (`autonomy_policy.md` Level 5) run through this system.
- Task activity is surfaced via Mission Control (`observability_spec.md`).
