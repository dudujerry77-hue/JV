import pytest

from jarvis_core.ai.cost import CostTracker
from jarvis_core.ai.provider import AIProvider, AIResponse, AIUsage
from jarvis_core.ai.router import AIRouter
from jarvis_core.config.schema import JarvisConfig
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.storage.db import get_connection


@pytest.fixture
def config(tmp_path) -> JarvisConfig:
    return JarvisConfig(data_dir=str(tmp_path))


@pytest.fixture
def db_conn(config):
    conn = get_connection(config.resolved_db_path())
    yield conn
    conn.close()


@pytest.fixture
def permission_store(db_conn) -> PermissionStore:
    return PermissionStore(db_conn)


class FakeProvider(AIProvider):
    """A canned AIProvider for tests -- never touches the network."""

    name = "fake"

    def __init__(self):
        self.calls: list[str] = []

    def complete(self, prompt: str, *, model: str) -> AIResponse:
        self.calls.append(prompt)
        return AIResponse(
            text=f"fake response to: {prompt}",
            model="fake-model",
            usage=AIUsage(input_tokens=2, output_tokens=4),
        )


@pytest.fixture
def fake_provider() -> FakeProvider:
    return FakeProvider()


@pytest.fixture
def cost_tracker(db_conn) -> CostTracker:
    return CostTracker(db_conn, monthly_ceiling_usd=20.0)


@pytest.fixture
def fake_ai_router(fake_provider, permission_store, cost_tracker) -> AIRouter:
    return AIRouter(
        provider=fake_provider,
        model="fake-model",
        permission_store=permission_store,
        cost_tracker=cost_tracker,
        input_cost_per_1k_usd=0.002,
        output_cost_per_1k_usd=0.010,
    )
