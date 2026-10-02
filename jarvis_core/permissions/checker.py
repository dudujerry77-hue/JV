"""Enforcement + audit trail for capability checks.

Every check is logged -- granted or denied -- so the owner can always
answer "what did Jarvis try to do, and under what permission?" per
.jarvis/observability_spec.md and .jarvis/permissions_model.md
"Auditability".
"""

from jarvis_core.observability.logging import get_logger
from jarvis_core.permissions.capabilities import Capability
from jarvis_core.permissions.store import PermissionStore

logger = get_logger("permissions")


class PermissionDenied(Exception):
    def __init__(self, capability: Capability):
        self.capability = capability
        super().__init__(f"Capability not granted: {capability.value}")


def require(store: PermissionStore, capability: Capability) -> None:
    """Raise PermissionDenied if `capability` is not granted.

    The check is always recorded in the durable audit log via the store's
    own connection -- auditing is not an opt-in the caller can forget (see
    .jarvis/permissions_model.md "Auditability").
    """
    granted = store.is_granted(capability)
    store.record_audit("permission_check", f"capability={capability.value} granted={granted}")

    if granted:
        logger.debug("permission check passed: %s", capability.value)
    else:
        logger.warning("permission check denied: %s", capability.value)
        raise PermissionDenied(capability)
