"""TEST: Settings API endpoints for API key storage."""

import keyring
from keyring.backends.fail import Keyring as FailKeyring

import pytest
from fastapi.testclient import TestClient

from jarvis_core.credentials.store import CredentialStore
from jarvis_core.plugins.registry import PluginRegistry
from jarvis_core.service.app import create_app


class MemoryKeyring(keyring.backend.KeyringBackend):
    priority = 1

    def __init__(self) -> None:
        self._data: dict[tuple[str, str], str] = {}

    def get_password(self, service, username):
        return self._data.get((service, username))

    def set_password(self, service, username, password):
        self._data[(service, username)] = password

    def delete_password(self, service, username):
        self._data.pop((service, username), None)


@pytest.fixture
def client(permission_store, monkeypatch):
    backend = MemoryKeyring()
    keyring.set_keyring(backend)
    store = CredentialStore(service_name="jarvis-core-test-api")
    app = create_app(permission_store, PluginRegistry(), credential_store=store)
    yield TestClient(app)
    keyring.set_keyring(FailKeyring())


def test_keys_status_empty(client):
    response = client.get("/settings/keys/status")
    assert response.status_code == 200
    assert response.json() == {"keys": {"groq": False, "google": False}}


def test_save_groq_key(client):
    response = client.post(
        "/settings/keys",
        json={"provider": "groq", "key": "gsk_test_123"},
    )
    assert response.status_code == 200
    assert response.json()["saved"] is True

    status = client.get("/settings/keys/status").json()
    assert status["keys"]["groq"] is True
    assert status["keys"]["google"] is False


def test_save_google_key(client):
    response = client.post(
        "/settings/keys",
        json={"provider": "google", "key": "AIza_test_456"},
    )
    assert response.status_code == 200
    status = client.get("/settings/keys/status").json()
    assert status["keys"]["google"] is True


def test_save_unknown_provider(client):
    response = client.post(
        "/settings/keys",
        json={"provider": "openai", "key": "sk-x"},
    )
    assert response.status_code == 400


def test_delete_key(client):
    client.post("/settings/keys", json={"provider": "groq", "key": "gsk_x"})
    response = client.delete("/settings/keys/groq")
    assert response.status_code == 200
    status = client.get("/settings/keys/status").json()
    assert status["keys"]["groq"] is False


def test_status_includes_keys(client):
    client.post("/settings/keys", json={"provider": "groq", "key": "gsk_y"})
    body = client.get("/status").json()
    assert body["keys"]["groq"] is True
