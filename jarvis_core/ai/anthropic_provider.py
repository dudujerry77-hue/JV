"""Anthropic provider -- first concrete AIProvider, see .jarvis/decisions.md
D-0015.

The `anthropic` SDK and the API key lookup are both deferred to first use
(not import time, not __init__), so constructing this class -- and
therefore starting Jarvis Core -- never requires a key to be present.
D-0007 still holds: nothing outside this module imports `anthropic`.
"""

from jarvis_core.ai.provider import AIProvider, AIProviderError, AIResponse, AIUsage
from jarvis_core.secrets import SecretStoreError, get_secret

API_KEY_SECRET_NAME = "anthropic_api_key"


class AnthropicProvider(AIProvider):
    name = "anthropic"

    def __init__(self, client=None):
        """`client` is injectable for testing. Production code leaves it
        None; a real `anthropic.Anthropic` client is built lazily on first
        use, with the API key read from the OS keyring (D-0012) -- never
        from a config file or environment variable.
        """
        self._client = client

    def _get_client(self):
        if self._client is not None:
            return self._client

        try:
            import anthropic
        except ImportError as exc:
            raise AIProviderError(
                "the 'anthropic' package is not installed"
            ) from exc

        try:
            api_key = get_secret(API_KEY_SECRET_NAME)
        except SecretStoreError as exc:
            raise AIProviderError(str(exc)) from exc

        if not api_key:
            raise AIProviderError(
                f"no Anthropic API key found in the OS keyring under "
                f"{API_KEY_SECRET_NAME!r} -- see .jarvis/decisions.md D-0012"
            )

        self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def complete(self, prompt: str, *, model: str) -> AIResponse:
        client = self._get_client()

        try:
            message = client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
        except AIProviderError:
            raise
        except Exception as exc:  # SDK-specific exceptions normalized here
            raise AIProviderError(f"Anthropic API call failed: {exc}") from exc

        text = "".join(
            block.text for block in message.content if getattr(block, "type", None) == "text"
        )
        usage = AIUsage(
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )
        return AIResponse(text=text, model=model, usage=usage)
