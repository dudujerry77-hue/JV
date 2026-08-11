# Agent Rules

Every agent must, before meaningful changes:
1. Read `.jarvis/constitution.md`.
2. Read `.jarvis/current_phase.md`.
3. Read `.jarvis/project_state.json`.
4. Read this file and relevant subsystem specs.
5. Inspect existing repository code before proposing implementation.

Operating constraints:
- Continue from current state; never restart project context.
- Never replace working architecture without documented decision.
- Do not modify unrelated modules without explicit reason.
- Record major decisions in `.jarvis/decisions.md`.
- Update `.jarvis/project_state.json` after meaningful progress.
- Add/update tests when code changes are made.
- Report changed files, verification, risks, and remaining work.
- Leave repository recoverable.

Required handoff format:
- TASK
- UNDERSTANDING
- FILES CHANGED
- IMPLEMENTATION
- TESTS
- VERIFICATION
- KNOWN ISSUES
- DECISIONS
- NEXT STEP
- PROJECT STATE
