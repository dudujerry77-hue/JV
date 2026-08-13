# Jarvis Vision

Status: proposed (long-term aspirational document; individual subsystems
tracked separately in `feature_spec.md`)

This document describes what Jarvis is meant to become over years of
incremental development. It is intentionally aspirational — nothing here is
a commitment to build immediately. See `roadmap.md` for sequencing and
`feature_spec.md` for the current status of each subsystem.

## Why Jarvis Exists

To give its owner a single, coherent, trustworthy AI system that grows with
them over time — across devices, across tasks, across years — instead of a
collection of disconnected AI tools, subscriptions, and one-off scripts.

## The Long-Term Picture

Jarvis eventually coordinates the following major capability areas. Each is
owned by a subsystem described in more detail in its own spec document.

| Capability area | Primary spec |
|---|---|
| Multi-model AI orchestration | `ai_provider_spec.md` |
| Deep research | `research_engine_spec.md` |
| Long-term memory | `memory_spec.md` |
| Device management & computer automation | `device_integration_spec.md` |
| Security monitoring | `security_policy.md`, `feature_spec.md` |
| Opportunity discovery | `feature_spec.md` |
| Business / client assistance | `feature_spec.md` |
| Content creation | `feature_spec.md` |
| Coding assistance | `feature_spec.md` |
| Multi-agent collaboration | `agent_system_spec.md` |
| Long-running background work | `task_system_spec.md` |
| Cross-device coordination | `device_integration_spec.md` |
| Extensibility | `plugin_spec.md` |

## What Success Looks Like

- Jarvis feels like one unified system, not a pile of disconnected tools
  (see `.jarvis/observability_spec.md` for the Mission Control concept).
- The user can always answer "what is Jarvis doing right now, and why?"
- New capabilities arrive as modules/plugins without core rewrites.
- Autonomy increases only as trust, observability, and recoverability
  justify it (see `autonomy_policy.md`).
- The system remains explainable to a new agent picking up the project for
  the first time, no matter how much has been built.

## What Jarvis Is Not

- Not a chatbot with a large feature list bolted on.
- Not a system that silently monitors people or devices without consent.
- Not a system that acts financially or reputationally on the owner's
  behalf without explicit authorization.
- Not a system whose architecture is locked to one AI vendor.
- Not a system optimized for being built fast at the expense of being
  understood.
