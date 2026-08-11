# Failure Recovery

Recovery design targets:
- worker restart on crash
- retry with backoff for transient provider failures
- task resume from checkpoints
- plugin/process isolation
- safe/recovery mode for severe failures
- graceful shutdown and restart

Constraint:
- No uncontrolled self-modification of security boundaries or core architecture.
