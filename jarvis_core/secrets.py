"""Secret storage -- see .jarvis/decisions.md D-0012.

A thin wrapper around the `keyring` library (OS Credential Manager on
Windows) so callers never import `keyring` directly, secrets never have a
second code path into config files or logs, and tests can monkeypatch one
place instead of the underlying OS-specific backend.
"""

import keyring
from keyring.errors import KeyringError

SERVICE_NAME = "jarvis"


class SecretStoreError(Exception):
    """The OS keyring backend itself is unavailable or failed (no backend
    installed, vault locked, etc.) -- distinct from a secret simply not
    being set, which is a normal `None` return from get_secret()."""


def get_secret(name: str) -> str | None:
    try:
        return keyring.get_password(SERVICE_NAME, name)
    except KeyringError as exc:
        raise SecretStoreError(f"OS keyring backend unavailable: {exc}") from exc


def set_secret(name: str, value: str) -> None:
    try:
        keyring.set_password(SERVICE_NAME, name, value)
    except KeyringError as exc:
        raise SecretStoreError(f"OS keyring backend unavailable: {exc}") from exc


def delete_secret(name: str) -> None:
    try:
        keyring.delete_password(SERVICE_NAME, name)
    except KeyringError as exc:
        raise SecretStoreError(f"OS keyring backend unavailable: {exc}") from exc
