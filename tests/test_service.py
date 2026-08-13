import pytest
from fastapi.testclient import TestClient

from jarvis_core.permissions.capabilities import Capability
from jarvis_core.plugins.manifest import PluginManifest
from jarvis_core.plugins.registry import PluginRegistry
from jarvis_core.service.app import create_app, ensure_loopback_only


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


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "::1"])
def test_ensure_loopback_only_allows_loopback_hosts(host):
    ensure_loopback_only(host)  # should not raise


@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.1.10", "example.com"])
def test_ensure_loopback_only_rejects_non_loopback_hosts(host):
    with pytest.raises(RuntimeError):
        ensure_loopback_only(host)
