"""Config schema for Jarvis Core.

Kept intentionally small for Phase 1 -- Foundation. New sections are added
here as later phases need them (see .jarvis/agent_rules.md Feature Request
Rule: update the spec/schema, don't bolt on ad hoc config reads elsewhere).
"""

from pathlib import Path

from pydantic import BaseModel, Field, field_validator

# Loopback-only per .jarvis/decisions.md D-0011 -- never bind a public
# interface. Enforced, not just the default, since a config file or
# JARVIS_SERVICE__HOST env override could otherwise silently widen Core's
# API past localhost (.jarvis/security_policy.md "Network security").
_ALLOWED_SERVICE_HOSTS = {"127.0.0.1", "localhost", "::1"}


class ServiceConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8756

    @field_validator("host")
    @classmethod
    def _host_must_be_loopback(cls, value: str) -> str:
        if value not in _ALLOWED_SERVICE_HOSTS:
            raise ValueError(
                f"service.host must be loopback ({sorted(_ALLOWED_SERVICE_HOSTS)}), "
                f"got {value!r} -- see .jarvis/decisions.md D-0011"
            )
        return value


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file: str = "logs/jarvis.log"


class DatabaseConfig(BaseModel):
    path: str = "jarvis.db"


class PluginsConfig(BaseModel):
    directory: str = "plugins"


class AIConfig(BaseModel):
    # First provider per .jarvis/decisions.md D-0015. Never a secret: the
    # API key itself is never here -- it comes from the OS keyring
    # (D-0012) via jarvis_core/secrets.py.
    provider: str = "anthropic"
    model: str = "claude-sonnet-5-5"

    # D-0008 / D-0016: enforced by jarvis_core/ai/router.py + cost.py, not
    # merely advisory. $20/mo is a conservative Phase-3-first-pass default,
    # not a permanent figure -- override via config file or
    # JARVIS_AI__MONTHLY_COST_CEILING_USD.
    monthly_cost_ceiling_usd: float = 20.0

    # Approximate per-1k-token pricing used only to estimate spend against
    # the ceiling above -- not a claim of exact provider billing. See
    # D-0016: confirm current rates at the provider's own pricing page and
    # adjust these if they differ.
    input_cost_per_1k_usd: float = 0.002
    output_cost_per_1k_usd: float = 0.010


class JarvisConfig(BaseModel):
    # Base directory all relative paths above are resolved against. Never
    # holds secrets -- see .jarvis/decisions.md D-0012 (secrets go through
    # the OS keyring, not config files).
    data_dir: str = str(Path.home() / ".jarvis-runtime")

    service: ServiceConfig = Field(default_factory=ServiceConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    plugins: PluginsConfig = Field(default_factory=PluginsConfig)
    ai: AIConfig = Field(default_factory=AIConfig)

    def resolved_data_dir(self) -> Path:
        return Path(self.data_dir).expanduser()

    def resolved_log_file(self) -> Path:
        return self.resolved_data_dir() / self.logging.file

    def resolved_db_path(self) -> Path:
        return self.resolved_data_dir() / self.database.path

    def resolved_plugins_dir(self) -> Path:
        return self.resolved_data_dir() / self.plugins.directory
