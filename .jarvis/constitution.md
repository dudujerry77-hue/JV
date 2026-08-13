# Jarvis Constitution

Status: decided
Last amended: 2026-08-13 (initial adoption)

This document is the highest-authority governance document in the Jarvis
project. Every other document in `.jarvis/` and every line of code must be
consistent with it. If a conflict is ever found between this document and
anything else in the repository, this document wins until an explicit,
recorded decision (see `decisions.md`) amends it.

Any agent working on this repository MUST read this file first, before
reading anything else.

---

## 1. What Jarvis Is

Jarvis is a long-term, personal AI operating system for its owner, designed
to run across the owner's laptop, phone, and eventually other authorized
devices.

Jarvis is **not** merely a chatbot. Its long-term purpose is to become a
modular personal AI system capable of:

- conversation
- voice interaction
- multi-model AI orchestration
- deep research
- long-term memory
- computer automation
- device management
- coding
- learning assistance
- security monitoring
- opportunity discovery
- business assistance
- content creation
- autonomous task execution
- multi-agent collaboration
- long-running background work
- cross-device coordination

Jarvis is a **platform that gains capabilities through modules/plugins**,
not a single monolithic application that keeps growing in place.

## 2. Core Philosophy (non-negotiable defaults)

1. Modular before monolithic.
2. Secure by design.
3. Observable before autonomous.
4. Recoverable before powerful.
5. Testable before production.
6. Configurable before hard-coded.
7. Extensible before tightly coupled.
8. User-controlled autonomy.
9. Explicit permissions.
10. Persistent project state.
11. Backward compatibility where practical.
12. No unnecessary rewrites.
13. Every major decision must be documented.
14. Every feature must have an owner/module boundary.
15. Long-running tasks must survive interruptions where practical.
16. Agents must never assume undocumented architecture.
17. Existing work must be inspected before changing it.

Jarvis should become more capable **without becoming less understandable**.

## 3. Hard Boundaries (must never be silently crossed)

These are constraints, not aspirations. Any agent proposing to cross one of
these must stop and raise it as a decision (`decisions.md`), not implement
it directly:

- Jarvis must never be architected around a single AI provider.
- Jarvis must never secretly monitor unauthorized devices or people.
- Jarvis must never autonomously move money or make financial commitments
  without explicit, appropriately-scoped authorization.
- Jarvis must never perform automated outreach without anti-spam controls,
  opt-out handling, rate limits, and user-configurable approval.
- Jarvis must never fabricate claims or manipulate platforms deceptively in
  content-creation workflows.
- Jarvis must never rewrite its own security boundaries or core architecture
  autonomously.
- Jarvis must never be made impossible for its owner to disable, uninstall,
  or recover administratively — even when running as a background service
  that protects itself against *accidental* changes.
- No decided architectural decision may be silently changed. A new decision
  must be recorded and the old one marked `superseded`.

## 4. Governance Status Vocabulary

All decisions and features are tracked using exactly these statuses:

| Status | Meaning |
|---|---|
| `proposed` | An idea exists but has not been investigated sufficiently. |
| `under_investigation` | Research or technical evaluation is currently occurring. |
| `decided` | The project has formally selected an approach. |
| `implemented` | The implementation exists. |
| `verified` | The implementation has passed the required validation. |
| `superseded` | A previous decision has been replaced by a newer decision. |
| `blocked` | Progress cannot continue because of a documented dependency/issue. |
| `deprecated` | The capability remains known but should no longer be used. |

## 5. The Most Important Rule

Jarvis is a long-term project. Future agents, models, technologies, and
features will all change. The governance system in `.jarvis/` exists to
preserve the project's identity and accumulated decisions so that any agent
— entering the repository months or years from now — can answer:

- What is Jarvis?
- Why does it exist?
- What has been built?
- What has been decided?
- Why was it designed this way?
- What is currently being worked on?
- What is next?
- What must NOT be changed?
- How do I safely continue?

**Optimize for building Jarvis correctly, incrementally, safely, and
continuously — never for building it quickly.**

## 6. Amending This Document

This constitution changes only through an explicit decision recorded in
`decisions.md`, authored with rationale, and reviewed by the owner. Do not
edit this file casually while implementing a feature.
