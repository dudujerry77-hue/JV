# Observability & Mission Control Specification

Status: proposed

## Principle

Jarvis must be observable before it is autonomous (`constitution.md`
principle 3). The owner must always be able to answer:

- "What is Jarvis doing right now?"
- "Why did Jarvis do that?"

## Required Observability Data

- logs
- metrics
- task history
- agent activity
- AI usage
- API usage
- errors
- resource consumption
- security events
- automation history

## Mission Control (dashboard)

A central dashboard, eventually showing:

```
ACTIVE TASKS   AI AGENTS      RESEARCH        JOBS
PROJECTS       DEVICE STATUS  SECURITY EVENTS MEMORY
CONTENT PIPELINE  AI USAGE    SYSTEM HEALTH
```

User controls from Mission Control:

- start / pause / cancel tasks
- inspect reasoning/results where appropriate
- change priority
- inspect logs
- change permissions
- configure AI providers

## Design Note

Avoid overwhelming the user with every internal system at once — advanced
controls should be available without making basic interaction complicated
(`.jarvis` §"User Experience" principle, see `vision.md`).

## Relationship to Other Systems

Every subsystem (`task_system_spec.md`, `agent_system_spec.md`,
`permissions_model.md`, `device_integration_spec.md`, `ai_provider_spec.md`)
emits to this system rather than maintaining its own separate, undiscoverable
logging.
