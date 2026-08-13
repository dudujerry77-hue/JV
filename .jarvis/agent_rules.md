# Agent Operating Rules

Status: decided

This is the operating manual for every agent (coding, research, testing,
security, UI, AI, or feature agent) that works on Jarvis. If you are an
agent reading this repository, this document tells you how to behave.

## Before Doing Anything

Every agent MUST, in order:

1. Read `.jarvis/constitution.md`.
2. Read `.jarvis/current_phase.md`.
3. Read `.jarvis/project_state.json`.
4. Read `.jarvis/agent_rules.md` (this file).
5. Read whichever spec documents are relevant to the task at hand.
6. Inspect the existing repository before proposing implementation.

## Standing Rules

1. Never assume the repository is empty — check.
2. Never restart the project merely because the current implementation is
   incomplete.
3. Never replace working architecture without documented justification
   (a `decisions.md` entry).
4. Never modify unrelated modules without reason.
5. Record important architectural decisions in `decisions.md` as you make
   them, not after the fact.
6. Update `.jarvis/project_state.json` after any meaningful work.
7. Add or update tests for anything you implement or change (see
   `testing_strategy.md`).
8. Report exactly what was changed.
9. Report what remains incomplete.
10. Report what verification was actually performed.
11. Identify known risks.
12. Leave the repository in a recoverable state (working tree clean,
    nothing half-migrated, no broken build left behind without a note).

Agents must continue from the current project state — do not start over.

## Feature Development Protocol

Every new Jarvis feature follows this sequence:

```
Idea -> Specification -> Research -> Architecture impact analysis ->
Security/privacy analysis -> Decision -> Implementation plan ->
Implementation -> Testing -> Integration -> Verification ->
Documentation -> Project-state update
```

Small changes may use a shortened version of this process **only when the
shortening itself is documented** (e.g. "trivial bugfix, skipped
architecture-impact analysis because none exists").

No major feature jumps directly from idea to implementation.

## Feature Request Rule

When a user says "add X to Jarvis," an agent must **not** immediately
implement it. Instead:

1. Determine which subsystem owns X (see `architecture.md`,
   `feature_spec.md`).
2. Check whether X already exists.
3. Check for overlapping capabilities.
4. Determine dependencies.
5. Analyze security/privacy implications (`security_policy.md`,
   `privacy_policy.md`).
6. Determine whether it belongs in Core or a plugin (`plugin_spec.md`).
7. Update the appropriate specification.
8. Create an implementation plan.
9. Implement.
10. Test.
11. Verify.
12. Update `project_state.json`.

## Change Management (for architecture-level changes)

1. Inspect existing architecture.
2. Identify affected systems.
3. Explain why the change is needed.
4. Create a decision record in `decisions.md`.
5. Mark old decisions `superseded` if necessary.
6. Update affected specifications.
7. Implement migration.
8. Test old and new behavior.
9. Update `project_state.json`.

Never silently rewrite architecture.

## No Unnecessary Rebuilding

If a feature already exists: inspect it, reuse it, improve it, refactor
only when justified. Do not recreate an existing system because you don't
understand it yet — read the code and the relevant spec first.

## No False Completion

Never report "done" when:

- implementation is incomplete,
- tests were not run,
- integration failed,
- required dependencies are missing, or
- behavior has not been verified.

Use the precise status vocabulary from `constitution.md` §4 instead.

## Agent Handoff Protocol

Every agent leaves a handoff report in this format at the end of its work:

```
TASK — What was requested.
UNDERSTANDING — What the agent believes the task means.
FILES CHANGED — Exact files.
IMPLEMENTATION — What was implemented.
TESTS — What tests were executed.
VERIFICATION — What actually passed.
KNOWN ISSUES — Anything incomplete or uncertain.
DECISIONS — Any new architectural decisions (with decisions.md IDs).
NEXT STEP — Recommended next action.
PROJECT STATE — Current phase/status after work.
```

This allows the next agent to continue without losing context.
