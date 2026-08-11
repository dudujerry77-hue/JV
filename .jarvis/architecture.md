# Architecture (Initial)

## Conceptual Topology

```text
                    JARVIS
                      │
                ┌─────┴─────┐
                │ JARVIS CORE│
                └─────┬─────┘
                      │
       ┌──────────────┼──────────────┐
       │              │              │
    AI SYSTEM       MEMORY         AGENTS
       │              │              │
       └──────────────┼──────────────┘
                      │
                TASK SYSTEM
                      │
              PERMISSION SYSTEM
                      │
              PLUGIN SYSTEM
                      │
       ┌──────────────┼──────────────┐
       │              │              │
    LAPTOP          PHONE        INTERNET
```

## Architectural Constraints
- Core coordinates; modules execute specialized capability.
- Provider abstraction required for AI vendors.
- Capability-based permission model required before high-risk automation.
- Long-running work must use queue/worker/checkpoint model.
- Safety controls (pause/stop/revoke) are mandatory system primitives.

## Current State
- Status: `proposed` architecture, `blocked` on foundation implementation.
