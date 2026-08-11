# Jarvis Constitution

## Identity
Jarvis is a long-term personal AI operating system focused on modular growth across authorized devices.

## Foundational Principles
1. Modular before monolithic.
2. Secure by design.
3. Observable before autonomous.
4. Recoverable before powerful.
5. Testable before production.
6. Configurable before hard-coded.
7. Extensible before tightly coupled.
8. User-controlled autonomy.
9. Explicit permissions.
10. Persistent project state.
11. Backward compatibility where practical.
12. No unnecessary rewrites.
13. Every major decision must be documented.
14. Every feature must have a module owner/boundary.
15. Long-running tasks should survive interruptions where practical.
16. Agents must never assume undocumented architecture.
17. Existing work must be inspected before changing it.

## Governance Status Vocabulary
- `proposed`: idea exists, not sufficiently investigated.
- `under_investigation`: active technical investigation.
- `decided`: formal project decision made.
- `superseded`: replaced by a newer decision.
- `implemented`: implementation exists.
- `verified`: validation requirements passed.
- `blocked`: cannot progress due to dependency/issue.
- `deprecated`: known but should no longer be used.

## Change Integrity Rules
- Never silently change a decided architecture choice.
- Record a new decision and mark old decision `superseded`.
- All significant work must update `.jarvis/project_state.json`.
