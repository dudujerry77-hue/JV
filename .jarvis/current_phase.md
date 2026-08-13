# Current Phase

Phase 1 status: **`verified`** — see `phase_completion_records/P001-completion.md`
Next phase: **pending owner decision** (see below)
Last updated: 2026-08-13

## Phase 1 — Closed Out

All of `roadmap.md`'s completion bar is now met: implementation, 26
passing tests, a real end-to-end integration smoke test, documentation,
and a security review (which found and fixed a real gap — the core
service's host binding wasn't actually enforced as loopback-only, just
defaulted that way; fixed in `jarvis_core/service/app.py`). CI
(`.github/workflows/tests.yml`) now runs the suite on every push and pull
request.

## Open Sequencing Question Before Starting the Next Phase

`roadmap.md` lists Phase 2 (Voice) before Phase 3 (Multi-AI Brain). But
voice input/output has nothing to talk to until an AI provider exists —
building wake-word/STT/TTS before there's a brain to route to produces
something that listens and speaks but can't actually respond to anything
meaningful. This was flagged to the owner in conversation but not yet
resolved into a decision.

This is a real reordering of the roadmap, not a trivial call — per
`roadmap.md`'s own note ("Reordering the roadmap is itself an
architectural decision and must be recorded in `decisions.md`"), it needs
an explicit decision, not an agent's silent judgment call.

**Options, pending owner choice:**

1. Follow the documented order — build Phase 2 (Voice) next, even though
   it won't have a brain to respond yet (it could still prove out
   wake-word + STT + TTS mechanics in isolation, e.g. echoing back
   transcribed text).
2. Reorder — build Phase 3 (Multi-AI Brain) next instead, so there's
   something to actually talk to, then add voice on top of a working
   brain.

## Also Still Open (deferred, not blocking either option above)

- Specific cloud AI provider(s) to wire up first for Phase 3, and a
  monthly cost ceiling (relates to D-0008).
- Android integration approach — needed for Phase 7.

## Next Action

Owner picks option 1 or 2 above (or another sequencing entirely). Once
chosen, record it in `decisions.md`, update this file and `roadmap.md`'s
phase statuses accordingly, and begin that phase's implementation
following the same process Phase 1 used (implementation -> tests ->
integration -> documentation -> security review -> verification, with
progress reported file-by-file as work happens).
