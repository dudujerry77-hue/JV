"""API key storage via the OS keyring — see .jarvis/decisions.md D-0012.

Never write secrets to config files or the SQLite database. Keys are stored
in Windows Credential Manager (or the platform equivalent) through the
`keyring` library.
"""

from __future__ import annotations

import keyring
from keyring.errors import KeyringError

SERVICE_NAME = "jarvis-core"

PROVIDER_GROQ = "groq"
PROVIDER_GOOGLE = "google"

SUPPORTED_PROVIDERS = (PROVIDER_GROQ, PROVIDER_GOOGLE)

_USERNAME = {
    PROVIDER_GROQ: "groq_api_key",
    PROVIDER_GOOGLE: "google_api_key",
}


class CredentialStore:
    """Read/write AI provider API keys through the OS credential store."""

    def __init__(self, service_name: str = SERVICE_NAME) -> None:
        self._service = service_name

    def set_key(self, provider: str, api_key: str) -> None:
        provider = provider.lower().strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider {provider!r}. "
                f"Supported: {', '.join(SUPPORTED_PROVIDERS)}"
            )
        key = (api_key or "").strip()
        if not key:
            raise ValueError("API key must not be empty")
        try:
            keyring.set_password(self._service, _USERNAME[provider], key)
        except KeyringError as exc:
            raise RuntimeError(f"Failed to store key for {provider}: {exc}") from exc

    def get_key(self, provider: str) -> str | None:
        provider = provider.lower().strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider {provider!r}. "
                f"Supported: {', '.join(SUPPORTED_PROVIDERS)}"
            )
        try:
            return keyring.get_password(self._service, _USERNAME[provider])
        except KeyringError as exc:
            raise RuntimeError(f"Failed to read key for {provider}: {exc}") from exc

    def has_key(self, provider: str) -> bool:
        value = self.get_key(provider)
        return bool(value and value.strip())

    def delete_key(self, provider: str) -> None:
        provider = provider.lower().strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider {provider!r}. "
                f"Supported: {', '.join(SUPPORTED_PROVIDERS)}"
            )
        try:
            keyring.delete_password(self._service, _USERNAME[provider])
        except keyring.errors.PasswordDeleteError:
            pass
        except KeyringError as exc:
            raise RuntimeError(f"Failed to delete key for {provider}: {exc}") from exc

    def status(self) -> dict[str, bool]:
        """Return whether each supported provider has a key set (never the key)."""
        return {provider: self.has_key(provider) for provider in SUPPORTED_PROVIDERS}
