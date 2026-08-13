# Memory System Specification

Status: proposed

## Memory Layers

- Working Memory
- Session Memory
- Personal Memory
- Project Memory
- Research Memory
- Device Activity Memory
- Task History
- Knowledge Base

## Required Properties

Memory must be:

- searchable
- permission-aware (see `permissions_model.md` — the `MEMORY` capability)
- encrypted where appropriate
- auditable
- configurable
- deletable
- retention-controlled

## Retention

The user must be able to configure retention per memory layer/category.
Initial option set:

```
1 month
2 months
3 months
4 months
5 months
indefinite
disabled
```

Automatic deletion must be a real, verifiable retention mechanism — not
merely a UI option that does nothing. Full mechanism defined in
`data_retention_policy.md`; this document defines what memory categories
that mechanism applies to.

## Relationship to Other Systems

- Research Memory is populated by the Deep Research Engine
  (`research_engine_spec.md`).
- Device Activity Memory is populated by the Device System
  (`device_integration_spec.md`) and feeds the Security System
  (`feature_spec.md`), subject to `privacy_policy.md` monitoring
  boundaries.
- Task History is populated by the Task System (`task_system_spec.md`).
- All memory access is auditable via `observability_spec.md`.
