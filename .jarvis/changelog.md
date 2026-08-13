# Changelog

Human-readable, chronological record of what happened, for humans skimming
project history. For *why* architectural choices were made, see
`decisions.md`. For phase-level outcomes, see `phase_completion_records/`.

## 2026-08-13

- Repository's only file (`README.md`) removed at explicit owner request.
- Governance system initialized under `.jarvis/`: constitution, vision,
  scope, architecture, roadmap, current phase, project state, decision
  log, agent rules, coding standards, testing strategy, security policy,
  permissions model, privacy policy, autonomy policy, feature spec, plugin
  spec, AI provider spec, memory spec, device integration spec, research
  engine spec, agent system spec, task system spec, observability spec,
  data retention policy, failure recovery, release strategy, and this
  changelog.
- Repository inspected: no application code exists; no technology stack
  chosen. Recorded as D-0004.
- Phase set to "Phase 0 — Governance & Architecture Initialization",
  status `in_progress`. Phase 1 implementation explicitly not started,
  pending owner review and the open questions in `current_phase.md`.
- Owner confirmed primary device is an HP EliteBook 645 G9 (integrated AMD
  Radeon graphics, no dedicated GPU, 16GB RAM). Recorded as D-0005.
- Decided a hybrid local/cloud AI execution split driven by that hardware
  constraint: lightweight always-on functions run locally for free; the
  main brain model and computer-use automation run via paid cloud API.
  Recorded as D-0006 and reflected in `ai_provider_spec.md`.
- Confirmed, per owner request, that provider consolidation (one API key
  covering multiple capabilities) is optional convenience, never a
  requirement — reaffirms the existing no-single-vendor-lock-in boundary.
  Recorded as D-0007.
- Decided Jarvis must never require payment just to run/idle; cost is
  incurred only on actual paid-provider use, and background/unattended
  tasks must keep cost exposure visible and bounded. Recorded as D-0008.
- `current_phase.md` updated to separate resolved vs. still-open
  technology-stack questions; `project_state.json` updated accordingly.
