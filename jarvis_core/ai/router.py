"""AI Router -- see .jarvis/ai_provider_spec.md "AI Router (conceptual
flow)" and .jarvis/architecture.md.

Phase 3 first increment: a single concrete provider (AnthropicProvider,
D-0015) is wired up. The router still enforces the permission gate, the
cost ceiling, and audit logging that any future multi-provider fallback
chain will also need -- adding a second provider and real fallback
behavior later is a routing-policy change, not a rearchitecture
(ai_provider_spec.md "Provider Selection Status"). Intent analysis, task
classification, and model/tool selection beyond "one configured model" are
explicitly not part of this increment.
"""

from jarvis_core.ai.cost import CostTracker
from jarvis_core.ai.provider import AIProvider, AIResponse
from jarvis_core.observability.logging import get_logger
from jarvis_core.permissions.capabilities import Capability
from jarvis_core.permissions.checker import require
from jarvis_core.permissions.store import PermissionStore

logger = get_logger("ai.router")


class CostCeilingExceeded(Exception):
    """Raised instead of calling a paid provider once the monthly ceiling
    configured in .jarvis/decisions.md D-0016 would be exceeded."""


class AIRouter:
    def __init__(
        self,
        provider: AIProvider,
        model: str,
        permission_store: PermissionStore,
        cost_tracker: CostTracker,
        input_cost_per_1k_usd: float,
        output_cost_per_1k_usd: float,
    ):
        self._provider = provider
        self._model = model
        self._permission_store = permission_store
        self._cost_tracker = cost_tracker
        self._input_cost_per_1k_usd = input_cost_per_1k_usd
        self._output_cost_per_1k_usd = output_cost_per_1k_usd

    def complete(self, prompt: str) -> AIResponse:
        """Route `prompt` to the configured cloud-tier provider.

        Enforces, in order: the AI_PROVIDER capability gate
        (permissions_model.md) -- raises PermissionDenied and audits the
        denial if not granted; then the monthly cost ceiling (D-0008/
        D-0016) using a conservative pre-call estimate -- raises
        CostCeilingExceeded without calling the provider at all if it
        would be exceeded. Only after both gates pass does the real call
        happen; real usage-based cost is then recorded regardless of how
        accurate the pre-call estimate was.

        The audit entry records provider/model/token counts/cost only --
        never prompt or response text (.jarvis/privacy_policy.md; this
        isn't a memory store, see .jarvis/memory_spec.md for that).
        """
        require(self._permission_store, Capability.AI_PROVIDER)

        estimated_input_tokens = max(1, len(prompt) // 4)
        pre_call_estimate_usd = (estimated_input_tokens / 1000) * self._input_cost_per_1k_usd
        if self._cost_tracker.would_exceed_ceiling(pre_call_estimate_usd):
            logger.warning(
                "AI call blocked: would exceed monthly cost ceiling of $%.2f",
                self._cost_tracker.monthly_ceiling_usd,
            )
            raise CostCeilingExceeded(
                f"monthly AI cost ceiling of ${self._cost_tracker.monthly_ceiling_usd:.2f} "
                "would be exceeded -- see .jarvis/decisions.md D-0016"
            )

        logger.info(
            "routing request to cloud provider %s (data leaves device -- "
            "see .jarvis/privacy_policy.md)",
            self._provider.name,
        )
        response = self._provider.complete(prompt, model=self._model)

        actual_cost_usd = (response.usage.input_tokens / 1000) * self._input_cost_per_1k_usd + (
            response.usage.output_tokens / 1000
        ) * self._output_cost_per_1k_usd
        self._cost_tracker.record_usage(
            provider=self._provider.name,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            estimated_cost_usd=actual_cost_usd,
        )
        self._permission_store.record_audit(
            "ai_call",
            f"provider={self._provider.name} model={response.model} "
            f"input_tokens={response.usage.input_tokens} "
            f"output_tokens={response.usage.output_tokens} "
            f"estimated_cost_usd={actual_cost_usd:.4f}",
        )
        return response
