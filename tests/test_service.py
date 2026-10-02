from fastapi.testclient import TestClient

from jarvis_core.permissions.capabilities import Capability
from jarvis_core.plugins.manifest import PluginManifest
from jarvis_core.plugins.registry import PluginRegistry
from jarvis_core.service.app import create_app


def test_health_endpoint(permission_store):
    app = create_app(permission_store, PluginRegistry())
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_status_endpoint_reports_plugins_and_permissions(permission_store):
    registry = PluginRegistry()
    registry.register(PluginManifest(name="p1", version="1.0.0", description="d"))
    permission_store.grant(Capability.NETWORK)

    app = create_app(permission_store, registry)
    client = TestClient(app)

    response = client.get("/status")
    body = response.json()

    assert response.status_code == 200
    assert body["phase"] == "Phase 3 - Multi-AI Brain"
    assert body["plugins"] == [{"name": "p1", "version": "1.0.0"}]
    assert body["permissions"]["granted"] == 1
    assert body["permissions"]["total"] > 1
    assert body["ai_router_configured"] is False


def test_ai_complete_returns_503_when_no_router_configured(permission_store):
    app = create_app(permission_store, PluginRegistry())
    client = TestClient(app)

    response = client.post("/ai/complete", json={"prompt": "hello"})

    assert response.status_code == 503


def test_ai_complete_returns_403_when_permission_denied(permission_store, fake_ai_router):
    app = create_app(permission_store, PluginRegistry(), fake_ai_router)
    client = TestClient(app)

    response = client.post("/ai/complete", json={"prompt": "hello"})

    assert response.status_code == 403


def test_ai_complete_succeeds_when_granted(permission_store, fake_ai_router):
    permission_store.grant(Capability.AI_PROVIDER)
    app = create_app(permission_store, PluginRegistry(), fake_ai_router)
    client = TestClient(app)

    response = client.post("/ai/complete", json={"prompt": "hello"})
    body = response.json()

    assert response.status_code == 200
    assert body["text"] == "fake response to: hello"
    assert body["model"] == "fake-model"
    assert body["usage"] == {"input_tokens": 2, "output_tokens": 4}
