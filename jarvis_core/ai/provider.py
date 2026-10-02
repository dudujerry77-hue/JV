"""AI provider abstraction -- see .jarvis/ai_provider_spec.md.

Jarvis must never be architecturally coupled to a single AI vendor
(.jarvis/constitution.md "Hard Boundaries", D-0007). Every concrete
provider implements this interface; jarvis_core/ai/router.py is the only
thing allowed to depend on a concrete provider class at wiring time.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AIUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class AIResponse:
    text: str
    model: str
    usage: AIUsage


class AIProviderError(Exception):
    """Raised when a provider call fails (network, auth, API error).

    Concrete providers must translate their own SDK's exceptions into this
    type so the router can handle every provider uniformly.
    """


class AIProvider(ABC):
    name: str

    @abstractmethod
    def complete(self, prompt: str, *, model: str) -> AIResponse:
        """Send `prompt` to the provider and return its response."""
