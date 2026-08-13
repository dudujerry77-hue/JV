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
    assert body["phase"] == "Phase 1 - Foundation"
    assert body["plugins"] == [{"name": "p1", "version": "1.0.0"}]
    assert body["permissions"]["granted"] == 1
    assert body["permissions"]["total"] > 1
