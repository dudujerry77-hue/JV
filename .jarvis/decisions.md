# Architectural Decisions

## DEC-0001 — Establish governance-first workflow
- Status: `decided`
- Date: 2026-08-11
- Context: Jarvis is intended as a long-term system with many future agents.
- Decision: Create and maintain `.jarvis/` governance as mandatory source of truth.
- Consequences: Future work must update project state and decision records.

## DEC-0002 — Use modular platform architecture
- Status: `decided`
- Date: 2026-08-11
- Decision: Jarvis architecture remains modular with core orchestrating specialized systems.
- Consequences: Features should map to modules/plugins, not monolithic growth.

## DEC-0003 — Capability-based permissions are mandatory
- Status: `decided`
- Date: 2026-08-11
- Decision: Sensitive actions require explicit, capability-scoped authorization.
- Consequences: Automation and financial/device actions need higher control gates.

## DEC-0004 — Repository implementation baseline is empty
- Status: `decided`
- Date: 2026-08-11
- Evidence: Repository currently includes only `README.md`.
- Decision: Foundation implementation has not started.
- Consequences: Phase 1 work begins with stack investigation and initial scaffolding.

## DEC-0005 — Initial technology stack requires investigation
- Status: `under_investigation`
- Date: 2026-08-11
- Decision Scope: desktop framework, language, UI framework, DB, IPC, AI abstraction, voice stack, local models, automation, security, plugin loading, updates, testing.
- Consequences: No stack lock-in until formal decision records are created.
