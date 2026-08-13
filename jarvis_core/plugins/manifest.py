"""Plugin manifest schema -- see .jarvis/plugin_spec.md "Plugin Manifest".

Every field listed in plugin_spec.md is represented here. Core validates
against this schema and is the enforcement authority for `permissions`;
a plugin declaring a permission does not mean it has been granted it
(see .jarvis/security_policy.md "Safe plugin loading").
"""

from pydantic import BaseModel, Field


class PluginManifest(BaseModel):
    name: str
    version: str
    description: str
    permissions: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    configuration: dict = Field(default_factory=dict)
    storage: dict = Field(default_factory=dict)
    security_requirements: str = ""
