"""Capability catalog -- see .jarvis/permissions_model.md.

Tier assignment below is Phase 1's initial, documented default for the
capabilities the spec didn't already classify by example; refine via the
Feature Request Rule (.jarvis/agent_rules.md) as real usage informs it,
not by silently editing this mapping.
"""

from enum import Enum


class Capability(str, Enum):
    READ_SCREEN = "READ_SCREEN"
    CONTROL_MOUSE = "CONTROL_MOUSE"
    CONTROL_KEYBOARD = "CONTROL_KEYBOARD"
    READ_FILES = "READ_FILES"
    WRITE_FILES = "WRITE_FILES"
    RUN_COMMAND = "RUN_COMMAND"
    CAMERA = "CAMERA"
    MICROPHONE = "MICROPHONE"
    PHONE_NOTIFICATIONS = "PHONE_NOTIFICATIONS"
    PHONE_MESSAGES = "PHONE_MESSAGES"
    NETWORK = "NETWORK"
    AI_PROVIDER = "AI_PROVIDER"
    MEMORY = "MEMORY"
    DEVICE_CONTROL = "DEVICE_CONTROL"
    FINANCIAL_ACTION = "FINANCIAL_ACTION"


class Tier(str, Enum):
    STANDARD = "standard"
    SENSITIVE = "sensitive"
    FINANCIAL = "financial"


_TIER_MAP: dict[Capability, Tier] = {
    Capability.NETWORK: Tier.STANDARD,
    Capability.MEMORY: Tier.STANDARD,
    Capability.AI_PROVIDER: Tier.STANDARD,
    Capability.READ_FILES: Tier.STANDARD,
    Capability.PHONE_NOTIFICATIONS: Tier.STANDARD,
    Capability.READ_SCREEN: Tier.SENSITIVE,
    Capability.CONTROL_MOUSE: Tier.SENSITIVE,
    Capability.CONTROL_KEYBOARD: Tier.SENSITIVE,
    Capability.WRITE_FILES: Tier.SENSITIVE,
    Capability.RUN_COMMAND: Tier.SENSITIVE,
    Capability.CAMERA: Tier.SENSITIVE,
    Capability.MICROPHONE: Tier.SENSITIVE,
    Capability.PHONE_MESSAGES: Tier.SENSITIVE,
    Capability.DEVICE_CONTROL: Tier.SENSITIVE,
    Capability.FINANCIAL_ACTION: Tier.FINANCIAL,
}


def tier_of(capability: Capability) -> Tier:
    return _TIER_MAP[capability]
