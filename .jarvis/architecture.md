# Jarvis Architecture

Status: proposed (conceptual architecture only; no implementation exists yet)
Architecture version: 0.1 (draft)

This document describes the conceptual shape of Jarvis. It is intentionally
implementation-agnostic until technology-stack decisions are made (see
`decisions.md` D-0003). Do not treat anything here as a locked technical
design — it is a structural contract that future decisions must fit inside.

## Guiding Principle

**Jarvis Core coordinates capabilities; it does not contain all of them.**
New capabilities should arrive as plugins/modules (`plugin_spec.md`) rather
than growing Core indefinitely.

## Conceptual Diagram

```
                    JARVIS
                      |
                +-----+-----+
                | JARVIS CORE|
                +-----+-----+
                      |
       +--------------+--------------+
       |              |              |
    AI SYSTEM       MEMORY         AGENTS
       |              |              |
       +--------------+--------------+
                      |
                TASK SYSTEM
                      |
              PERMISSION SYSTEM
                      |
              PLUGIN SYSTEM
                      |
       +--------------+--------------+
       |              |              |
    LAPTOP          PHONE        INTERNET
```

## Major Systems (each owns a boundary; each has its own spec)

| System | Responsibility | Spec |
|---|---|---|
| AI System | Providers, routing, model selection, context/prompt management, fallback | `ai_provider_spec.md` |
| Memory System | Working/session/personal/project/research memory, retention | `memory_spec.md` |
| Agent System | Specialized agents, delegation, contracts | `agent_system_spec.md` |
| Task System | Queue, workers, checkpoints, retries, long-running tasks | `task_system_spec.md` |
| Permission System | Capability-based authorization | `permissions_model.md` |
| Plugin System | Capability extension without Core rewrites | `plugin_spec.md` |
| Device System | Laptop/phone/future-device coordination | `device_integration_spec.md` |
| Research Engine | Multi-source deep research | `research_engine_spec.md` |
| Observability / Mission Control | Logs, metrics, dashboard | `observability_spec.md` |
| Security System (product feature) | Owner recognition, device monitoring, alerts | `feature_spec.md` |

## AI Router (conceptual flow)

```
User request
     |
Intent analysis
     |
Task classification
     |
Model/tool selection
     |
Execution
     |
Validation
     |
Response
```

Task categories: conversation, coding, research, document analysis,
planning, vision, summarization, reasoning, automation, content creation.
Routing policy must be configurable, not hard-coded to one provider or
model. See `ai_provider_spec.md`.

## Architectural Invariants (do not violate without a recorded decision)

- No single AI vendor may be architecturally required.
- Sensitive capabilities are gated by the permission system
  (`permissions_model.md`), not by convention.
- Long-running tasks must be able to survive interruption via checkpoints
  (`task_system_spec.md`).
- Plugins must be isolated as much as practical; Core must not need a
  rewrite for every new capability.
- Self-healing (`failure_recovery.md`) may restart/retry/isolate failed
  components, but must never rewrite security boundaries or core
  architecture autonomously.

## Change Management

Before changing anything in this document: inspect current architecture,
identify affected systems, explain why the change is needed, create a
decision record, mark superseded decisions, update affected specs, migrate,
test old and new behavior, update `project_state.json`. See
`agent_rules.md` §"Change Management".
