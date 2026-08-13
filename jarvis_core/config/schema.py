"""Config schema for Jarvis Core.

Kept intentionally small for Phase 1 -- Foundation. New sections are added
here as later phases need them (see .jarvis/agent_rules.md Feature Request
Rule: update the spec/schema, don't bolt on ad hoc config reads elsewhere).
"""

from pathlib import Path

from pydantic import BaseModel, Field


class ServiceConfig(BaseModel):
    # Loopback-only per .jarvis/decisions.md D-0011 -- never bind a public
    # interface here.
    host: str = "127.0.0.1"
    port: int = 8756


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file: str = "logs/jarvis.log"


class DatabaseConfig(BaseModel):
    path: str = "jarvis.db"


class PluginsConfig(BaseModel):
    directory: str = "plugins"


class JarvisConfig(BaseModel):
    # Base directory all relative paths above are resolved against. Never
    # holds secrets -- see .jarvis/decisions.md D-0012 (secrets go through
    # the OS keyring, not config files).
    data_dir: str = str(Path.home() / ".jarvis-runtime")

    service: ServiceConfig = Field(default_factory=ServiceConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    plugins: PluginsConfig = Field(default_factory=PluginsConfig)

    def resolved_data_dir(self) -> Path:
        return Path(self.data_dir).expanduser()

    def resolved_log_file(self) -> Path:
        return self.resolved_data_dir() / self.logging.file

    def resolved_db_path(self) -> Path:
        return self.resolved_data_dir() / self.database.path

    def resolved_plugins_dir(self) -> Path:
        return self.resolved_data_dir() / self.plugins.directory
