# Feature Specification & Catalog

Status: living document — see per-feature status below

This document is the catalog of Jarvis's major planned subsystems/features
and their current governance status. It is also where the Feature
Development Protocol and Feature Request Rule live for quick reference
(full detail in `agent_rules.md`).

## Feature Development Protocol (summary)

```
Idea -> Specification -> Research -> Architecture impact analysis ->
Security/privacy analysis -> Decision -> Implementation plan ->
Implementation -> Testing -> Integration -> Verification ->
Documentation -> Project-state update
```

## Feature Request Rule (summary)

When asked to "add X," an agent determines ownership, checks for existing
or overlapping capability, analyzes dependencies and security/privacy
implications, decides Core-vs-plugin, updates the spec, plans, implements,
tests, verifies, and updates project state. Full steps in `agent_rules.md`.

## Feature Catalog

Every entry below is `proposed` — nothing has been implemented yet (see
`project_state.json`). Detailed specs exist separately for the subsystems
large enough to warrant their own document; smaller/product-level features
are specified here directly and get promoted to their own file if they grow
enough to need one.

| Feature | Status | Detail spec |
|---|---|---|
| AI System (providers, routing, fallback) | proposed | `ai_provider_spec.md` |
| Deep Research Engine | proposed | `research_engine_spec.md` |
| Memory System | proposed | `memory_spec.md` |
| Device System (laptop, phone, future devices) | proposed | `device_integration_spec.md` |
| Computer Automation | proposed | `device_integration_spec.md` |
| Agent System | proposed | `agent_system_spec.md` |
| Task System | proposed | `task_system_spec.md` |
| Plugin System | proposed | `plugin_spec.md` |
| Mission Control dashboard | proposed | `observability_spec.md` |
| Security System (owner/face recognition, device monitoring, alerts) | proposed | this document, below |
| Opportunity Engine | proposed | this document, below |
| Business / Client Engine | proposed | this document, below |
| Content Engine | proposed | this document, below |
| Coding System | proposed | this document, below |

### Security System (product feature)

Owner recognition, face recognition, unknown-user detection, device
monitoring, suspicious activity alerts, camera-based security events,
secure/encrypted event storage, remote notification, device-lock
capabilities where supported. Must never secretly monitor unauthorized
devices/people; must clearly document what is monitored and retention for
the owner's own devices (`privacy_policy.md`, `data_retention_policy.md`).
Governed additionally by `security_policy.md`.

### Opportunity Engine

Discovers, filters, ranks, and explains legitimate opportunities (jobs,
freelance projects, clients, businesses, content, products, contracts);
notifies the user; prepares drafts/proposals; tracks responses; maintains
lead history. Automated outreach requires anti-spam controls, opt-out
handling, rate limits, and user-configurable approval
(`constitution.md` §"Hard Boundaries"). Jarvis must not endlessly message
people.

### Business / Client Engine

Lead discovery, CRM, client profiles, conversation history, proposal/
quotation/contract generation, follow-up scheduling, project tracking,
payment tracking, revenue tracking. Conceptual flow: business discovered ->
online-presence analysis -> lead score -> personalized proposal -> user
approval -> outreach -> response monitoring -> user notification when
interested. `FINANCIAL_ACTION` boundaries from `permissions_model.md`
apply to payment tracking and any commitment-making step.

### Content Engine

Faceless content creation: trend discovery, topic research, script
generation, source verification, narration, visual planning, video
assembly, captions, thumbnail/title/description generation, publishing
assistance, analytics, performance analysis, future-content
recommendations. Must not fabricate claims or manipulate platforms
deceptively (`constitution.md` §"Hard Boundaries").

### Coding System

Understands repositories, inspects architecture, generates and edits code,
runs tests, diagnoses errors, reviews and explains code, creates
documentation, interacts with Git, works with/delegates to coding agents
and external coding systems where permitted. This capability is what an
agent working on Jarvis itself already exercises informally — formalizing
it as a subsystem is future work, not a prerequisite for governance.

## Adding a New Feature to This Catalog

Add a row to the table above with status `proposed`, and either expand it
inline here (if small) or create a new `*_spec.md` file (if large enough to
need its own document, following the Feature Development Protocol).
