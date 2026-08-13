# Device Integration & Computer Automation Specification

Status: proposed

## Device System

Initial targets: laptop, Android phone. Future targets (later phases, per
`roadmap.md` Phase 7/12): smart speakers, displays, smart-home devices,
Raspberry Pi / mini PCs, other authorized computers.

Device integrations must use explicit permissions (`permissions_model.md`
— `DEVICE_CONTROL`, `PHONE_NOTIFICATIONS`, `PHONE_MESSAGES`, `CAMERA`,
`MICROPHONE`, etc. as applicable per device).

Jarvis should be able to understand, per authorized device:

- device status
- battery
- connectivity
- applications
- notifications
- selected activity
- available capabilities

## Computer Automation

Approved-task categories Jarvis should eventually perform:

- open/close applications
- launch and navigate websites
- read permitted screen content
- type / interact with permitted UI controls
- create and organize files
- run development tools
- execute approved commands
- inspect logs
- monitor processes

## Automation Safety Requirements

- Permission boundaries (`permissions_model.md`) — `READ_SCREEN`,
  `CONTROL_MOUSE`, `CONTROL_KEYBOARD`, `RUN_COMMAND` are sensitive-tier.
- Confirmation levels tied to `autonomy_policy.md` levels.
- Audit logs for every automated action (`observability_spec.md`).
- Emergency stop, available at all times.
- Timeouts on automation steps.
- Failure recovery (`failure_recovery.md`) — a failed automation step must
  fail gracefully, not corrupt state or hang Jarvis.

## Open Questions

Which OS/platform to target first, and the Android integration approach
(native app vs. Termux vs. companion app talking to the laptop) are open
questions blocking detailed design — see `current_phase.md`.
