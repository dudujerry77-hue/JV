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

Status: `proposed`, not started

Core application, runtime, configuration, database, plugin architecture,
security foundation. Requires technology-stack decisions (`decisions.md`
D-0003) before implementation planning can be finalized.

## Phase 2 — Voice

Status: `proposed`

Wake word, speech recognition, text-to-speech, conversation.

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
