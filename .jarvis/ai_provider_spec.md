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
**Which providers are wired up first, and local-model hardware
requirements, are open questions recorded in `current_phase.md`** — not
decided here, since they depend on owner-provided facts (budget, hardware).

## Data-Leaves-Device Transparency

Per `privacy_policy.md`, the user must know when a request is routed to a
cloud provider vs. handled locally. This is a logging/observability
requirement on the router, not optional.
