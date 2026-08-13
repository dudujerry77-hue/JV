# Jarvis Scope

Status: decided (scope boundaries), revisited each phase

## Current Scope (as of governance initialization, 2026-08-13)

The repository currently contains **no application code**. The only work
done so far is the creation of this governance system (`.jarvis/`).

Nothing has been implemented. Nothing has been decided beyond the
governance process itself and the boundaries below. See `current_phase.md`
and `project_state.json` for the live snapshot.

## In Scope, Eventually

Everything described in `vision.md` and cataloged in `feature_spec.md` is
in scope for the project's lifetime. That does not mean it is in scope for
the current phase — see `roadmap.md` for sequencing.

## Explicitly Out of Scope (permanent, not phase-dependent)

- Operating on devices or accounts the owner has not explicitly authorized.
- Monitoring people other than the owner without their knowledge/consent,
  even incidentally (e.g. via camera/microphone security features).
- Autonomous financial transactions or commitments without explicit,
  scoped authorization (see `permissions_model.md`).
- Mass/spammy automated outreach of any kind (see `feature_spec.md` —
  Opportunity Engine, Business/Client Engine).
- Deceptive content manipulation or fabricated claims (see `feature_spec.md`
  — Content Engine).
- Undocumented or silent architectural changes (see `agent_rules.md`).
- Designs that make Jarvis impossible for its owner to disable, uninstall,
  or administratively recover (see `constitution.md` §3).

## Platform Scope

Initial target platforms, per `device_integration_spec.md`:

- Owner's laptop (primary development and runtime target).
- Owner's Android phone.

Future platform expansion (smart speakers, displays, smart-home devices,
Raspberry Pi / mini PCs, other authorized computers) is in scope for later
phases only, per `roadmap.md` Phase 7+ and Phase 12.

## Boundary Between Core and Plugins

Jarvis Core coordinates capabilities; it does not itself implement every
capability. Anything that can reasonably be isolated as a module should be
a plugin rather than a Core addition. See `plugin_spec.md` and
`architecture.md`.
