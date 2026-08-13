# Data Retention Policy

Status: decided (mechanism), proposed (implementation)

## Principle

All stored activity must have explicit retention rules, and the user must
be able to configure retention (see `memory_spec.md` for the option set:
1-5 months, indefinite, or disabled).

## Deletion Workflow

Automatic deletion must be a real mechanism, not a UI toggle with no
effect behind it:

```
Identify expired records -> securely delete -> verify deletion ->
record the deletion event
```

The deletion event itself is logged (`observability_spec.md`), so the
owner can confirm retention is actually being honored.

## Data Minimization

Avoid collecting data Jarvis does not need in the first place. Retention
policy is a backstop, not a substitute for deciding up front what actually
needs to be stored (see `privacy_policy.md`).

## Scope

Applies to every memory layer in `memory_spec.md`, task history
(`task_system_spec.md`), device activity (`device_integration_spec.md`),
security events (`feature_spec.md` — Security System), and research memory
(`research_engine_spec.md`). Each of those subsystems' own spec references
this document rather than redefining retention mechanics locally.
