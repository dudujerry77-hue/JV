# Current Phase

Phase: **Phase 0 — Governance & Architecture Initialization**
Status: `in_progress`
Last updated: 2026-08-13

## What Is Happening Right Now

The governance system (`.jarvis/`) is being created for the first time.
Before this, the repository contained no files at all (a single `README.md`
was the only tracked file, and it has since been removed). No application
code, no chosen technology stack, and no implemented features exist.

## What Must Happen Before Phase 1 Can Start

Per `constitution.md` and the governance initialization instructions, Phase
1 implementation must **not** begin until:

1. The owner has reviewed and approved this governance system.
2. The open questions below have been answered, so that
   `decisions.md` D-0003 (technology stack) can move from
   `under_investigation` to `decided`.
3. A Phase 1 implementation plan exists and is recorded.

## Open Questions Blocking Technology-Stack Decisions

These must be answered by the owner (an agent must not guess them, per
constitution.md §"Hard Boundaries" and §44 of the original governance
prompt):

- **Primary laptop OS**: Windows, macOS, or Linux (or must Jarvis support
  more than one from day one)?
- **Desktop app approach**: native, Electron/Tauri-style web-tech shell, or
  headless service + separate UI?
- **Local model hardware**: is there a GPU available for local inference,
  and how much VRAM/RAM, or should Phase 1 assume cloud-only AI to start?
- **Primary language preference**: does the owner have a strong preference
  (e.g. Python, TypeScript/Node, Rust, Go) for Jarvis Core?
- **Android integration approach**: native Android app, Termux-based
  scripting, or a lightweight companion app talking to the laptop service?
- **Budget/provider preference**: which AI providers should be wired up
  first (OpenAI, Anthropic, Google, DeepSeek, local models), and is there a
  cost ceiling to design around?
- **Offline requirements**: must core conversation/automation work without
  internet access, or is "cloud-first with graceful degradation" acceptable
  for Phase 1?

## Next Action

Once the owner answers the questions above (or explicitly instructs an
agent to proceed with reasonable defaults), the next step is to record the
technology-stack decision in `decisions.md`, update this file to Phase 1,
and produce a Phase 1 implementation plan — **not** to start writing
application code preemptively.
