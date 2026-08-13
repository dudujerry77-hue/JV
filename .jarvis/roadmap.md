# Jarvis Roadmap

Status: proposed (sequencing may be reordered by decision; see `decisions.md`)

## Definition of "Phase Complete"

A phase is complete only when **all** of the following are true — code
existing is not sufficient:

```
Implementation + Tests + Integration + Documentation + Security review + Verification
```

Each completed phase gets a record in `phase_completion_records/` following
`phase_completion_records/TEMPLATE.md`.

## Phase 0 — Governance & Architecture Initialization

Status: `in_progress`

Create `.jarvis/` governance system, inspect the repository, record initial
decisions, define the Phase 1 implementation plan. Do not begin Phase 1
implementation until explicitly instructed after this governance is
reviewed by the owner. See `current_phase.md`.

## Phase 1 — Foundation

Status: `verified`

Core application, runtime, configuration, database, plugin architecture,
security foundation. Complete per this document's own completion bar:
implementation, 26 passing tests, integration (real end-to-end smoke
test), documentation, a security review (which found and fixed a real gap
-- unenforced loopback binding), and CI now runs the suite on every push.
See `phase_completion_records/P001-completion.md` for the full record.

## Phase 2 — Voice

Status: `implemented`, not yet `verified`

Wake word, speech recognition, text-to-speech, conversation (as an echo
pipeline until Phase 3 provides a real brain). Code + 49 tests exist and
pass; text-to-speech is genuinely verified in-sandbox, but wake-word/STT
model accuracy and real microphone capture require the owner's actual
hardware to verify (this sandbox has no audio devices and its network
policy blocks the model download host). See `current_phase.md`.

## Phase 3 — Multi-AI Brain

Status: `proposed`

AI providers, routing, model selection, fallback, local models. See
`ai_provider_spec.md`.

## Phase 4 — Computer Control

Status: `proposed`

Applications, browser, files, keyboard/mouse, screen understanding. See
`device_integration_spec.md`.

## Phase 5 — Memory

Status: `proposed`

Personal memory, knowledge base, activity history, retention. See
`memory_spec.md`, `data_retention_policy.md`.

## Phase 6 — Deep Research

Status: `proposed`

Multi-source research, documents, citations, reports, long-running
research. See `research_engine_spec.md`.

## Phase 7 — Device & Security

Status: `proposed`

Phone integration, laptop monitoring, face recognition, security events.
See `device_integration_spec.md`, `security_policy.md`.

## Phase 8 — Opportunity Engine

Status: `proposed`

Jobs, freelance opportunities, leads, businesses, proposals. See
`feature_spec.md`.

## Phase 9 — Content Studio

Status: `proposed`

Faceless content research and production workflow. See `feature_spec.md`.

## Phase 10 — Multi-Agent System

Status: `proposed`

Specialized agents and delegation. See `agent_system_spec.md`.

## Phase 11 — Mission Control

Status: `proposed`

Long-running missions, task queues, workers, recovery, observability. See
`task_system_spec.md`, `observability_spec.md`.

## Phase 12 — Jarvis Platform

Status: `proposed`

Cross-device ecosystem, plugin ecosystem, advanced integrations, optional
commercialization. See `plugin_spec.md`.

## Notes

- Phases are a planning sequence, not a strict waterfall — a later phase
  may begin early work if it does not violate `agent_rules.md` (no
  unrelated-module changes, no undocumented architecture).
- Reordering the roadmap is itself an architectural decision and must be
  recorded in `decisions.md`.
