# Phase Completion Record Template

Filename convention: `P001-completion.md`, `P002-completion.md`, etc.,
matching the phase number in `roadmap.md`. Do not create a record until the
phase actually meets the completion bar in `roadmap.md` /
`release_strategy.md`:

```
Implementation + Tests + Integration + Documentation + Security review + Verification
```

Copy this template and fill in every section — do not leave a section out
because it's inconvenient; an honest "none" is fine, a missing section is
not.

---

## Phase

Phase number and name (must match `roadmap.md`).

## Objectives

What this phase set out to do, per `roadmap.md`.

## Completed Features

List each feature completed, with its `feature_spec.md` (or relevant spec)
status at the time of this record.

## Tests

What test suites exist for this phase's work, and how to run them.

## Verification

What was actually run, and what passed. Be specific — this is what
justifies moving features from `implemented` to `verified` in
`project_state.json`.

## Known Limitations

What this phase deliberately does not cover.

## Unresolved Issues

What's broken, deferred, or flagged for follow-up, with references to any
new `decisions.md` entries created to track them.

## Architectural Decisions

List any `decisions.md` entries created or superseded during this phase.

## Next Phase

Which phase comes next per `roadmap.md`, and any prerequisites it now has
that it didn't have before this phase.

## Date

Completion date.

## Commit / Reference Information

Relevant commit hashes, branch, or PR reference for this phase's work.
