# Agent System Specification

Status: proposed

## Principle

Jarvis supports specialized agents, but agents must not become uncontrolled
independent systems. Every agent operates within the permission and
autonomy boundaries defined elsewhere (`permissions_model.md`,
`autonomy_policy.md`).

## Initial Conceptual Agent Roster

- CEO / Planner Agent
- Research Agent
- Developer Agent
- Security Agent
- Money Agent
- Business Agent
- Content Agent
- Learning Agent
- Device Agent
- Memory Agent

This roster is conceptual, not a commitment to build all ten at once — each
is introduced per `roadmap.md` Phase 10 and the Feature Request Rule.

## Required Fields Per Agent

Every agent, when actually specified/implemented, must declare:

- identity
- purpose
- permissions (from `permissions_model.md`'s catalog)
- tools
- input contract
- output contract
- limits
- audit trail
- failure behavior

## Delegation

Agents may delegate to other agents or to external coding/AI systems where
permitted, but delegation itself must respect the calling agent's own
permission grant — an agent cannot delegate its way into a capability it
was not given (`security_policy.md` §"Safe plugin loading" applies
analogously here).

## Relationship to Task System

Agents execute work through the Task System (`task_system_spec.md`), which
provides queueing, checkpoints, retries, and observability — agents do not
manage their own ad hoc background execution.
