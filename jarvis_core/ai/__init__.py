"""AI System -- see .jarvis/ai_provider_spec.md and .jarvis/architecture.md.

Provider abstraction, routing, cost tracking. Jarvis must never be
architecturally coupled to a single AI vendor (.jarvis/constitution.md
"Hard Boundaries", D-0007) -- jarvis_core.ai.router.AIRouter is the only
thing callers outside this package should depend on.
"""
