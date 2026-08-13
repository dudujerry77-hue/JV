# Current Phase

Phase: **Phase 0 — Governance & Architecture Initialization**
Status: `in_progress`
Last updated: 2026-08-13 (hardware and AI-execution questions resolved)

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

## Resolved Questions

- **Local model hardware** — RESOLVED (D-0005, D-0006). Primary laptop is
  an HP EliteBook 645 G9, 16GB RAM/512GB SSD, integrated AMD Radeon
  graphics only, no dedicated GPU. Decision: hybrid execution — lightweight
  always-on functions (wake word, speech-to-text, face recognition, memory
  search) run locally for free; the main brain model and computer-use
  automation run via paid cloud API since this hardware cannot run a
  capable model well. Revisit if hardware changes (eGPU / second
  local-inference machine).
- **Provider consolidation** — RESOLVED (D-0007). A single provider/API
  key may cover multiple capabilities for convenience, but this is never
  required — the architecture must support mixing providers per
  capability and must not lock to one vendor.
- **Billing model** — RESOLVED (D-0008). Jarvis must never require payment
  just to run/idle. Cost is incurred only when a paid cloud provider is
  actually invoked; background/unattended tasks must keep cost exposure
  visible and bounded.

## Open Questions Still Blocking Full Technology-Stack Decision (D-0003)

These must still be answered by the owner (an agent must not guess them,
per constitution.md §"Hard Boundaries" and §44 of the original governance
prompt):

- **Primary laptop OS**: Windows, macOS, or Linux (or must Jarvis support
  more than one from day one)?
- **Desktop app approach**: native, Electron/Tauri-style web-tech shell, or
  headless service + separate UI?
- **Primary language preference**: does the owner have a strong preference
  (e.g. Python, TypeScript/Node, Rust, Go) for Jarvis Core?
- **Android integration approach**: native Android app, Termux-based
  scripting, or a lightweight companion app talking to the laptop service?
- **Specific provider selection**: which cloud AI provider(s) should be
  wired up first for the brain/automation tier (OpenAI, Anthropic, Google,
  DeepSeek, other), and is there a monthly cost ceiling to design
  guardrails around (relates to D-0008)?
- **Offline requirements**: must core conversation/automation work without
  internet access, or is "cloud-first with graceful degradation" acceptable
  for Phase 1?

## Next Action

Once the owner answers the remaining questions above (or explicitly
instructs an agent to proceed with reasonable defaults), the next step is
to close out D-0003 in full in `decisions.md`, update this file to Phase 1,
and produce a Phase 1 implementation plan — **not** to start writing
application code preemptively.
