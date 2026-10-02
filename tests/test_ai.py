import pytest

from jarvis_core.ai.anthropic_provider import API_KEY_SECRET_NAME, AnthropicProvider
from jarvis_core.ai.provider import AIProviderError
from jarvis_core.ai.router import CostCeilingExceeded
from jarvis_core.permissions.capabilities import Capability
from jarvis_core.permissions.checker import PermissionDenied


# ---- CostTracker ------------------------------------------------------


def test_cost_tracker_starts_at_zero_spend(cost_tracker):
    assert cost_tracker.spent_this_month() == 0.0


def test_cost_tracker_accumulates_recorded_usage(cost_tracker):
    cost_tracker.record_usage(
        provider="fake", model="fake-model", input_tokens=1000, output_tokens=500,
        estimated_cost_usd=1.5,
    )
    cost_tracker.record_usage(
        provider="fake", model="fake-model", input_tokens=1000, output_tokens=500,
        estimated_cost_usd=2.5,
    )

    assert cost_tracker.spent_this_month() == 4.0


def test_cost_tracker_would_exceed_ceiling(cost_tracker):
    cost_tracker.record_usage(
        provider="fake", model="fake-model", input_tokens=1, output_tokens=1,
        estimated_cost_usd=19.0,
    )

    assert cost_tracker.would_exceed_ceiling(2.0) is True
    assert cost_tracker.would_exceed_ceiling(1.0) is False


# ---- AIRouter -----------------------------------------------------------


def test_router_denies_without_ai_provider_permission(fake_ai_router):
    with pytest.raises(PermissionDenied):
        fake_ai_router.complete("hello")


def test_router_completes_and_records_usage_and_audit(
    fake_ai_router, fake_provider, permission_store, db_conn, cost_tracker
):
    permission_store.grant(Capability.AI_PROVIDER)

    response = fake_ai_router.complete("hello")

    assert response.text == "fake response to: hello"
    assert fake_provider.calls == ["hello"]
    assert cost_tracker.spent_this_month() > 0

    rows = db_conn.execute(
        "SELECT * FROM audit_log WHERE event_type = 'ai_call'"
    ).fetchall()
    assert len(rows) == 1
    assert "provider=fake" in rows[0]["detail"]
    assert "model=fake-model" in rows[0]["detail"]
    # Prompt/response content must never land in the audit log.
    assert "hello" not in rows[0]["detail"]


def test_router_blocks_call_when_ceiling_would_be_exceeded(
    fake_ai_router, fake_provider, permission_store, cost_tracker
):
    permission_store.grant(Capability.AI_PROVIDER)
    cost_tracker.record_usage(
        provider="fake", model="fake-model", input_tokens=1, output_tokens=1,
        estimated_cost_usd=20.0,
    )

    with pytest.raises(CostCeilingExceeded):
        fake_ai_router.complete("hello")

    # The provider must never be called once the ceiling check fails.
    assert fake_provider.calls == []


# ---- AnthropicProvider ---------------------------------------------------


def test_anthropic_provider_raises_clear_error_without_api_key(monkeypatch):
    monkeypatch.setattr(
        "jarvis_core.ai.anthropic_provider.get_secret", lambda name: None
    )
    provider = AnthropicProvider()

    with pytest.raises(AIProviderError, match=API_KEY_SECRET_NAME):
        provider.complete("hello", model="fake-model")


class _FakeTextBlock:
    type = "text"

    def __init__(self, text):
        self.text = text


class _FakeUsage:
    def __init__(self, input_tokens, output_tokens):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens


class _FakeMessage:
    def __init__(self, text, input_tokens, output_tokens):
        self.content = [_FakeTextBlock(text)]
        self.usage = _FakeUsage(input_tokens, output_tokens)


class _FakeMessages:
    def __init__(self, message):
        self._message = message

    def create(self, **kwargs):
        return self._message


class _FakeAnthropicClient:
    def __init__(self, message):
        self.messages = _FakeMessages(message)


def test_anthropic_provider_returns_response_with_injected_client():
    message = _FakeMessage("hi there", input_tokens=10, output_tokens=20)
    provider = AnthropicProvider(client=_FakeAnthropicClient(message))

    response = provider.complete("hello", model="claude-sonnet-5-5")

    assert response.text == "hi there"
    assert response.model == "claude-sonnet-5-5"
    assert response.usage.input_tokens == 10
    assert response.usage.output_tokens == 20


def test_anthropic_provider_wraps_sdk_errors():
    class _RaisingMessages:
        def create(self, **kwargs):
            raise RuntimeError("boom")

    class _RaisingClient:
        messages = _RaisingMessages()

    provider = AnthropicProvider(client=_RaisingClient())

    with pytest.raises(AIProviderError, match="boom"):
        provider.complete("hello", model="claude-sonnet-5-5")
