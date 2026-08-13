# AI System & Provider Abstraction Specification

Status: proposed

## AI System Responsibilities

- Model providers
- Model routing
- Model selection
- Context management
- Prompt management
- Structured outputs
- Model fallback
- Model comparison
- Local models
- Cloud models
- AI provider health

## Hard Constraint

Jarvis must never be architecturally coupled to a single AI vendor
(`constitution.md` §"Hard Boundaries"). This is enforced through a provider
abstraction:

```
AIProvider
+-- OpenAIProvider
+-- AnthropicProvider
+-- GoogleProvider
+-- DeepSeekProvider
+-- LocalModelProvider
+-- FutureProvider
```

Provider failures must not necessarily crash Jarvis — implement fallback
behavior where appropriate (e.g. route to a healthy provider, or degrade to
Level 0/1 autonomy per `autonomy_policy.md` rather than fail hard).

## AI Router (conceptual flow)

```
User request -> Intent analysis -> Task classification ->
Model/tool selection -> Execution -> Validation -> Response
```

Task categories (initial set, expected to grow via the Feature Request
Rule): conversation, coding, research, document analysis, planning,
vision, summarization, reasoning, automation, content creation.

Routing must support configurable policies — not a hard-coded
if/else chain that assumes one provider or one task taxonomy forever.

## Provider Selection Status

Candidate providers (OpenAI, Anthropic, Google, DeepSeek, other compatible
providers, local/self-hosted models) are noted for future integration.
**Which specific providers are wired up first is still an open question**
recorded in `current_phase.md` — not decided here. The local/cloud
execution split below, however, is decided (D-0006).

## Local/Cloud Execution Split (decided — D-0005, D-0006)

The owner's primary device (HP EliteBook 645 G9) has no dedicated GPU —
integrated AMD Radeon graphics only, 16GB shared RAM. This caps what can
run locally at good quality. The router must therefore treat capability
tier, not just task category, as a routing input:

- **Local tier (free, always-on, runs on-device)**: wake word detection,
  speech-to-text, face/owner recognition, memory/embedding search, and
  baseline text-to-speech. These must work with zero cloud dependency and
  zero per-use cost.
- **Cloud tier (paid, usage-billed)**: the primary reasoning/coding/
  research "brain," and computer-use/UI automation. These are routed to a
  paid provider because current hardware cannot run a capable model for
  them.

This split is a hardware-driven default, not a permanent architectural
lock. If local-inference hardware improves (eGPU, second machine), more
task categories may move from the cloud tier to the local tier — that is a
configuration change to the router's policy, not a rearchitecture, per the
provider-abstraction design above.

## Cost Transparency Requirement (decided — D-0008)

Jarvis must never require payment simply to run or idle — only invoking a
cloud-tier provider incurs cost. This constrains the router's design:

- Idle/background/long-running tasks (`task_system_spec.md`) must default
  to local-tier capability wherever it is sufficient, and must not silently
  poll a paid provider on a tight loop.
- Any use of the cloud tier — especially from unattended/background
  missions — must be visible to the owner via `observability_spec.md` (AI
  usage, API usage), so cost exposure is never a surprise.
- Where a cost ceiling is configured (see the open "monthly cost ceiling"
  question in `current_phase.md`), the router must be able to enforce it —
  e.g. by refusing further cloud-tier calls or falling back to
  local-tier/degraded behavior once the ceiling is hit, consistent with
  `autonomy_policy.md`'s emergency-stop and pause requirements.

## Data-Leaves-Device Transparency

Per `privacy_policy.md`, the user must know when a request is routed to a
cloud provider vs. handled locally. This is a logging/observability
requirement on the router, not optional.
