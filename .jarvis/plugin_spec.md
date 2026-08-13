# Plugin System Specification

Status: proposed

## Principle

New capabilities should preferably be implemented as plugins/modules.
Jarvis Core should not need to be rewritten every time a new capability is
added (`constitution.md` principle 1, `architecture.md`).

## Plugin Manifest (required declarations)

Every plugin declares:

- `name`
- `version`
- `description`
- `permissions` — capabilities requested, from `permissions_model.md`'s
  catalog
- `dependencies`
- `tools` — what it exposes for agents/Core to call
- `events` — what it emits/subscribes to
- `configuration` — its own config schema
- `storage` — what it persists and where
- `security requirements` — anything beyond the baseline in
  `security_policy.md`

## Isolation

Plugins must be isolated as much as practical (process isolation,
sandboxing, or equivalent — exact mechanism is a Phase 1+ implementation
decision, see `decisions.md` D-0003). Core enforces the permission grants
declared in the manifest; it does not trust plugin self-restraint
(`security_policy.md` §"Safe plugin loading").

## Lifecycle Expectations

- A crashed plugin must be isolated, not allowed to take down Core
  (`failure_recovery.md`).
- Plugin failures are logged and surfaced via `observability_spec.md`.
- Plugins are versioned; breaking changes to a plugin's own contract are
  the plugin's concern, but changes to the Core-plugin contract itself are
  an architectural decision (`agent_rules.md` §"Change Management").

## Relationship to Core vs. Feature Decisions

When evaluating a new feature request (`agent_rules.md` §"Feature Request
Rule"), the default assumption is **plugin**, not **Core**. Core only grows
when a capability is genuinely cross-cutting (permissions, task
scheduling, observability, plugin loading itself).
