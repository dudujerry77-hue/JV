"""Secret storage -- see .jarvis/decisions.md D-0012.

A thin wrapper around the `keyring` library (OS Credential Manager on
Windows) so callers never import `keyring` directly, secrets never have a
second code path into config files or logs, and tests can monkeypatch one
place instead of the underlying OS-specific backend.
"""

import keyring

SERVICE_NAME = "jarvis"


def get_secret(name: str) -> str | None:
    return keyring.get_password(SERVICE_NAME, name)


def set_secret(name: str, value: str) -> None:
    keyring.set_password(SERVICE_NAME, name, value)


def delete_secret(name: str) -> None:
    keyring.delete_password(SERVICE_NAME, name)
