import pytest
from keyring.errors import KeyringError

from jarvis_core.secrets import SecretStoreError, get_secret, set_secret


def test_get_secret_wraps_keyring_backend_failure(monkeypatch):
    def _raise(*args, **kwargs):
        raise KeyringError("no backend")

    monkeypatch.setattr("jarvis_core.secrets.keyring.get_password", _raise)

    with pytest.raises(SecretStoreError, match="no backend"):
        get_secret("some_key")


def test_set_secret_wraps_keyring_backend_failure(monkeypatch):
    def _raise(*args, **kwargs):
        raise KeyringError("vault locked")

    monkeypatch.setattr("jarvis_core.secrets.keyring.set_password", _raise)

    with pytest.raises(SecretStoreError, match="vault locked"):
        set_secret("some_key", "value")
