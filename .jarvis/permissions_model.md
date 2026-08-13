# Permissions Model

Status: decided (model), proposed (implementation)

## Approach

Jarvis uses **capability-based permissions**. Every action a subsystem,
agent, or plugin wants to take against the real world (files, devices,
network, money) must be expressed as a declared capability, not implied by
code access.

## Initial Capability Catalog

```
READ_SCREEN
CONTROL_MOUSE
CONTROL_KEYBOARD
READ_FILES
WRITE_FILES
RUN_COMMAND
CAMERA
MICROPHONE
PHONE_NOTIFICATIONS
PHONE_MESSAGES
NETWORK
AI_PROVIDER
MEMORY
DEVICE_CONTROL
FINANCIAL_ACTION
```

This list is expected to grow. New capabilities are added via the Feature
Request Rule in `agent_rules.md`, not invented ad hoc inside a feature's
implementation.

## Sensitivity Tiers

- **Standard capabilities** (e.g. `NETWORK`, `MEMORY`) — require an
  explicit grant recorded in configuration, visible in Mission Control
  (`observability_spec.md`).
- **Sensitive capabilities** (e.g. `CAMERA`, `MICROPHONE`, `CONTROL_MOUSE`,
  `CONTROL_KEYBOARD`, `RUN_COMMAND`, `PHONE_MESSAGES`) — require explicit,
  per-use or per-session authorization, not a one-time blanket grant, unless
  the owner has explicitly configured a broader standing grant.
- **`FINANCIAL_ACTION`** — the strictest tier. No autonomous use. Requires
  explicit authorization per action or per tightly-scoped mission, per
  `constitution.md` §"Hard Boundaries" and `autonomy_policy.md`.

## Enforcement

Permission checks are enforced by Jarvis Core / the permission system, not
by the calling agent or plugin's own discipline (see `security_policy.md`
§"Safe plugin loading"). A plugin declaring a permission in its manifest
(`plugin_spec.md`) does not mean it is granted — Core is the authority.

## Auditability

Every grant, denial, and sensitive-capability use must be logged
(`observability_spec.md`) so the owner can always answer "what did Jarvis
do, and under what permission?"
