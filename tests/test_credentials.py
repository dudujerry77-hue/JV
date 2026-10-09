"""TEST: CredentialStore unit tests (in-memory keyring backend)."""

import keyring
from keyring.backends.fail import Keyring as FailKeyring

import pytest

from jarvis_core.credentials.store import (
    PROVIDER_GOOGLE,
    PROVIDER_GROQ,
    CredentialStore,
)


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
def store(monkeypatch):
    backend = MemoryKeyring()
    keyring.set_keyring(backend)
    yield CredentialStore(service_name="jarvis-core-test")
    keyring.set_keyring(FailKeyring())


def test_set_and_has_key(store):
    assert store.has_key(PROVIDER_GROQ) is False
    store.set_key(PROVIDER_GROQ, "gsk_test_key")
    assert store.has_key(PROVIDER_GROQ) is True
    assert store.get_key(PROVIDER_GROQ) == "gsk_test_key"


def test_status_reports_both_providers(store):
    store.set_key(PROVIDER_GOOGLE, "AIza_test")
    status = store.status()
    assert status[PROVIDER_GROQ] is False
    assert status[PROVIDER_GOOGLE] is True


def test_empty_key_rejected(store):
    with pytest.raises(ValueError):
        store.set_key(PROVIDER_GROQ, "   ")


def test_unknown_provider_rejected(store):
    with pytest.raises(ValueError):
        store.set_key("openai", "sk-test")


def test_delete_key(store):
    store.set_key(PROVIDER_GROQ, "gsk_x")
    store.delete_key(PROVIDER_GROQ)
    assert store.has_key(PROVIDER_GROQ) is False
